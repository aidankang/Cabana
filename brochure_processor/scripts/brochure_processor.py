"""
Brochure Image Processing Script

This script processes a folder of brochure images to create crawlable web content by:
1. Extracting text using OCR (Replicate API)
2. Detecting graphics coordinates using YOLO11n (Replicate API)  
3. Extracting individual graphics using Pillow
4. Getting page descriptions and structure plans using OpenAI
5. Generating HTML pages using OpenAI
6. Saving all data in structured JSON format

Usage:
    python brochure_processor.py --folder_path "path/to/images" --output_dir "output"
"""

import os
import json
import asyncio
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import traceback

# Third-party imports
import replicate
from PIL import Image
from pydantic import BaseModel, Field
import httpx

# Local imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from gpt.gpt_requests import gpt_request


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('brochure_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GraphicData(BaseModel):
    """Data structure for detected graphics"""
    coordinates: Dict[str, float] = Field(description="Bounding box coordinates (x1, y1, x2, y2)")
    confidence: float = Field(description="Detection confidence score")
    class_name: str = Field(description="Detected object class name")
    graphic_path: Optional[str] = Field(description="Path to extracted graphic image")


class PageData(BaseModel):
    """Structured data for a single brochure page"""
    original_filename: str = Field(description="Original image filename")
    proposed_page_name: str = Field(description="SEO-friendly page name")
    page_text_content: str = Field(description="Extracted text content")
    graphic_coordinates: List[Dict[str, float]] = Field(description="Array of graphic bounding boxes")
    graphic_paths: List[str] = Field(description="Array of paths to extracted graphics")
    page_description: str = Field(description="Description of the page content")
    page_structure_plan: str = Field(description="Plan for HTML structure")
    page_html: str = Field(description="Generated HTML content")


class PageAnalysis(BaseModel):
    """OpenAI response for page analysis"""
    proposed_page_name: str = Field(description="SEO-friendly page name (no spaces, lowercase, hyphens)")
    page_description: str = Field(description="Brief description of what this page is about")
    page_structure_plan: str = Field(description="Detailed plan for HTML structure and layout")


class HTMLGeneration(BaseModel):
    """OpenAI response for HTML generation"""
    html_content: str = Field(description="Complete HTML page content with proper semantic structure")


class BrochureProcessor:
    """Main processor class for brochure images"""
    
    def __init__(self, folder_path: str, output_dir: str):
        self.folder_path = Path(folder_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.graphics_dir = self.output_dir / "graphics"
        self.graphics_dir.mkdir(exist_ok=True)
        self.html_dir = self.output_dir / "html_pages"
        self.html_dir.mkdir(exist_ok=True)
        
        # Results storage
        self.processed_pages: List[PageData] = []
        
        # Ensure Replicate token is set
        if not os.environ.get('REPLICATE_API_TOKEN'):
            raise ValueError("REPLICATE_API_TOKEN environment variable must be set")
    
    def get_image_files(self) -> List[Path]:
        """Get all image files from the folder, sorted by name"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        image_files = []
        
        for file_path in self.folder_path.iterdir():
            if file_path.suffix.lower() in image_extensions:
                image_files.append(file_path)
        
        # Sort by filename to maintain order
        image_files.sort(key=lambda x: x.name)
        logger.info(f"Found {len(image_files)} image files")
        return image_files
    
    async def extract_text_ocr(self, image_path: Path) -> str:
        """Extract text from image using Replicate OCR API"""
        try:
            logger.info(f"Extracting text from {image_path.name}")
            
            # Upload image and get OCR result
            with open(image_path, 'rb') as image_file:
                output = replicate.run(
                    "abiruyt/text-extract-ocr",
                    input={"image": image_file}
                )
            
            # The output should be the extracted text
            extracted_text = output if isinstance(output, str) else str(output)
            logger.info(f"Extracted {len(extracted_text)} characters of text")
            return extracted_text
            
        except Exception as e:
            logger.error(f"Error extracting text from {image_path.name}: {e}")
            return ""
    
    async def detect_graphics(self, image_path: Path) -> List[GraphicData]:
        """Detect graphics in image using YOLO11n"""
        try:
            logger.info(f"Detecting graphics in {image_path.name}")
            
            with open(image_path, 'rb') as image_file:
                output = replicate.run(
                    "ultralytics/yolo11n:5b5cd6ec47664a3194d03ae0bf514ed0a887003e2d466dd938a66faab9fe7875",
                    input={
                        "image": image_file,
                        "conf": 0.25,  # Confidence threshold
                        "iou": 0.45,   # IoU threshold
                        "return_json": True
                    }
                )
            
            graphics_data = []
            
            # Parse YOLO output
            if isinstance(output, dict) and 'json_str' in output:
                detections = json.loads(output['json_str'])
            elif isinstance(output, list):
                detections = output
            else:
                logger.warning(f"Unexpected YOLO output format: {type(output)}")
                return graphics_data
            
            for detection in detections:
                if isinstance(detection, dict) and 'box' in detection:
                    box = detection['box']
                    graphic = GraphicData(
                        coordinates={
                            'x1': box['x1'],
                            'y1': box['y1'], 
                            'x2': box['x2'],
                            'y2': box['y2']
                        },
                        confidence=detection.get('confidence', 0.0),
                        class_name=detection.get('name', 'unknown')
                    )
                    graphics_data.append(graphic)
            
            logger.info(f"Detected {len(graphics_data)} graphics")
            return graphics_data
            
        except Exception as e:
            logger.error(f"Error detecting graphics in {image_path.name}: {e}")
            return []
    
    def extract_graphic_images(self, image_path: Path, graphics_data: List[GraphicData]) -> List[str]:
        """Extract individual graphics using Pillow"""
        try:
            logger.info(f"Extracting {len(graphics_data)} graphics from {image_path.name}")
            
            # Open the original image
            image = Image.open(image_path)
            image_width, image_height = image.size
            
            graphic_paths = []
            base_name = image_path.stem
            
            for i, graphic in enumerate(graphics_data):
                try:
                    # Get coordinates
                    coords = graphic.coordinates
                    x1, y1 = max(0, int(coords['x1'])), max(0, int(coords['y1']))
                    x2, y2 = min(image_width, int(coords['x2'])), min(image_height, int(coords['y2']))
                    
                    # Ensure valid bounding box
                    if x2 <= x1 or y2 <= y1:
                        logger.warning(f"Invalid bounding box for graphic {i}: ({x1}, {y1}, {x2}, {y2})")
                        continue
                    
                    # Crop the image
                    cropped = image.crop((x1, y1, x2, y2))
                    
                    # Save the graphic
                    graphic_filename = f"{base_name}_graphic_{i}_{graphic.class_name}.png"
                    graphic_path = self.graphics_dir / graphic_filename
                    cropped.save(graphic_path)
                    
                    # Store the path
                    graphic_paths.append(str(graphic_path))
                    graphic.graphic_path = str(graphic_path)
                    
                    logger.debug(f"Saved graphic {i} to {graphic_filename}")
                    
                except Exception as e:
                    logger.error(f"Error extracting graphic {i} from {image_path.name}: {e}")
                    continue
            
            logger.info(f"Successfully extracted {len(graphic_paths)} graphics")
            return graphic_paths
            
        except Exception as e:
            logger.error(f"Error processing graphics for {image_path.name}: {e}")
            return []
    
    async def analyze_page_content(self, filename: str, text_content: str, num_graphics: int) -> PageAnalysis:
        """Get page analysis using OpenAI"""
        try:
            logger.info(f"Analyzing page content for {filename}")
            
            system_prompt = """You are an expert web content strategist specializing in real estate brochures. 
            You help convert brochure pages into SEO-friendly web pages with proper structure and naming conventions."""
            
            user_prompt = f"""
            I have a brochure page with the following details:
            
            Filename: {filename}
            Extracted Text: {text_content[:2000]}{'...' if len(text_content) > 2000 else ''}
            Number of Graphics: {num_graphics}
            
            Please provide:
            1. A proposed SEO-friendly page name (lowercase, hyphens, no spaces, descriptive)
            2. A brief description of what this page is about (1-2 sentences)
            3. A detailed plan for how to structure this as an HTML page (consider headings, sections, image placement, etc.)
            
            Focus on making this content crawlable and SEO-friendly for a real estate/condominium website.
            """
            
            params = {
                'model': 'gpt-4o-mini',
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 1000,
                'response_format': PageAnalysis
            }
            
            outputs, cost = await gpt_request(__name__, params)
            logger.info(f"Page analysis completed. Cost: ${cost:.4f}")
            
            return outputs[0]
            
        except Exception as e:
            logger.error(f"Error analyzing page content for {filename}: {e}")
            # Return default values
            return PageAnalysis(
                proposed_page_name=filename.lower().replace(' ', '-').replace('.jpg', '').replace('.png', ''),
                page_description="Real estate brochure page content",
                page_structure_plan="Standard page with header, main content area, and images"
            )
    
    async def generate_html(self, page_data: Dict) -> str:
        """Generate HTML content using OpenAI"""
        try:
            logger.info(f"Generating HTML for {page_data['proposed_page_name']}")
            
            system_prompt = """You are an expert web developer specializing in creating SEO-optimized HTML pages. 
            Create semantic, accessible HTML that will rank well in search engines."""
            
            user_prompt = f"""
            Create a complete HTML page with the following content:
            
            Page Name: {page_data['proposed_page_name']}
            Description: {page_data['page_description']}
            Structure Plan: {page_data['page_structure_plan']}
            Text Content: {page_data['page_text_content'][:3000]}{'...' if len(page_data['page_text_content']) > 3000 else ''}
            Number of Graphics: {len(page_data['graphic_paths'])}
            
            Requirements:
            1. Use proper HTML5 semantic elements (header, main, section, article, etc.)
            2. Include meta tags for SEO (title, description, keywords)
            3. Make it mobile-responsive with proper viewport meta tag
            4. Add structured data markup where appropriate
            5. Use descriptive alt text placeholders for images
            6. Include proper heading hierarchy (h1, h2, h3)
            7. Add CSS classes for styling hooks
            8. Make the content crawlable and SEO-friendly
            
            Generate ONLY the HTML content (complete page from <!DOCTYPE html> to </html>).
            """
            
            params = {
                'model': 'gpt-4o-mini', 
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                'temperature': 0.2,
                'max_tokens': 4000,
                'response_format': HTMLGeneration
            }
            
            outputs, cost = await gpt_request(__name__, params)
            logger.info(f"HTML generation completed. Cost: ${cost:.4f}")
            
            return outputs[0].html_content
            
        except Exception as e:
            logger.error(f"Error generating HTML: {e}")
            # Return basic HTML template
            return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_data.get('proposed_page_name', 'Brochure Page')}</title>
    <meta name="description" content="{page_data.get('page_description', 'Real estate brochure page')}">
</head>
<body>
    <header>
        <h1>{page_data.get('proposed_page_name', 'Brochure Page').replace('-', ' ').title()}</h1>
    </header>
    <main>
        <section>
            <p>{page_data.get('page_text_content', 'Content not available')}</p>
        </section>
    </main>
</body>
</html>"""
    
    async def process_single_image(self, image_path: Path) -> PageData:
        """Process a single brochure image through the complete pipeline"""
        logger.info(f"Processing {image_path.name}")
        
        try:
            # Step 1: Extract text using OCR
            text_content = await self.extract_text_ocr(image_path)
            
            # Step 2: Detect graphics 
            graphics_data = await self.detect_graphics(image_path)
            
            # Step 3: Extract graphics using Pillow
            graphic_paths = self.extract_graphic_images(image_path, graphics_data)
            
            # Step 4: Get page analysis from OpenAI
            analysis = await self.analyze_page_content(
                image_path.name, 
                text_content, 
                len(graphics_data)
            )
            
            # Step 5: Prepare data for HTML generation
            page_data_dict = {
                'proposed_page_name': analysis.proposed_page_name,
                'page_description': analysis.page_description, 
                'page_structure_plan': analysis.page_structure_plan,
                'page_text_content': text_content,
                'graphic_paths': graphic_paths
            }
            
            # Step 6: Generate HTML
            html_content = await self.generate_html(page_data_dict)
            
            # Step 7: Save HTML file
            html_filename = f"{analysis.proposed_page_name}.html"
            html_path = self.html_dir / html_filename
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Step 8: Create structured data
            page_data = PageData(
                original_filename=image_path.name,
                proposed_page_name=analysis.proposed_page_name,
                page_text_content=text_content,
                graphic_coordinates=[g.coordinates for g in graphics_data],
                graphic_paths=graphic_paths,
                page_description=analysis.page_description,
                page_structure_plan=analysis.page_structure_plan,
                page_html=html_content
            )
            
            logger.info(f"Successfully processed {image_path.name}")
            return page_data
            
        except Exception as e:
            logger.error(f"Error processing {image_path.name}: {e}")
            logger.error(traceback.format_exc())
            raise
    
    async def process_batch(self, image_files: List[Path], batch_size: int = 3) -> List[PageData]:
        """Process images in batches to manage API rate limits"""
        all_results = []
        
        for i in range(0, len(image_files), batch_size):
            batch = image_files[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(image_files) + batch_size - 1)//batch_size}")
            
            # Process batch concurrently
            batch_tasks = [self.process_single_image(img) for img in batch]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            # Handle results and exceptions
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Batch processing error: {result}")
                else:
                    all_results.append(result)
            
            # Add delay between batches to respect rate limits
            if i + batch_size < len(image_files):
                logger.info("Waiting between batches...")
                await asyncio.sleep(2)
        
        return all_results
    
    async def process_all_images(self, batch_size: int = 3, limit: Optional[int] = None):
        """Process all images in the folder"""
        logger.info(f"Starting brochure processing for folder: {self.folder_path}")
        
        # Get image files
        image_files = self.get_image_files()
        
        if limit:
            image_files = image_files[:limit]
            logger.info(f"Processing limited to first {limit} images")
        
        if not image_files:
            logger.warning("No image files found!")
            return
        
        # Process images
        self.processed_pages = await self.process_batch(image_files, batch_size)
        
        # Save consolidated JSON
        output_json = {
            'metadata': {
                'total_pages': len(self.processed_pages),
                'source_folder': str(self.folder_path),
                'output_directory': str(self.output_dir),
                'processing_timestamp': str(asyncio.get_event_loop().time())
            },
            'pages': [page.model_dump() for page in self.processed_pages]
        }
        
        json_path = self.output_dir / 'brochure_data.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_json, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Processing complete! Results saved to {json_path}")
        logger.info(f"Generated {len(self.processed_pages)} pages")
        logger.info(f"HTML files saved to: {self.html_dir}")
        logger.info(f"Graphics saved to: {self.graphics_dir}")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Process brochure images into crawlable web content')
    parser.add_argument('--folder_path', required=True, help='Path to folder containing brochure images')
    parser.add_argument('--output_dir', required=True, help='Output directory for results')
    parser.add_argument('--batch_size', type=int, default=3, help='Number of images to process concurrently')
    parser.add_argument('--limit', type=int, help='Limit number of images to process (for testing)')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.folder_path):
        logger.error(f"Folder path does not exist: {args.folder_path}")
        return
    
    # Create processor and run
    processor = BrochureProcessor(args.folder_path, args.output_dir)
    await processor.process_all_images(batch_size=args.batch_size, limit=args.limit)


if __name__ == "__main__":
    asyncio.run(main())