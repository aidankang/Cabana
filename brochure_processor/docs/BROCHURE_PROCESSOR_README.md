# Brochure Processor Documentation

## Overview

The Brochure Processor is a comprehensive script that converts static brochure images into crawlable, SEO-friendly web content. It processes each page image through a complete pipeline to extract text, identify graphics, and generate structured HTML pages.

## Features

### 🔍 Text Extraction
- Uses Replicate's OCR API (`abiruyt/text-extract-ocr`) to extract all text from brochure images
- Handles various image formats (JPG, PNG, TIFF, etc.)

### 🎯 Graphics Detection
- Uses YOLO11n model (`ultralytics/yolo11n`) to detect and locate graphics/objects in images
- Returns bounding box coordinates with confidence scores
- Detects various object classes (person, car, building elements, etc.)

### ✂️ Graphics Extraction
- Uses Pillow to crop individual graphics based on detected coordinates
- Saves graphics as separate PNG files for web use
- Maintains aspect ratios and image quality

### 🧠 AI-Powered Analysis
- Uses OpenAI GPT-4 to analyze page content and structure
- Generates SEO-friendly page names and descriptions
- Creates detailed HTML structure plans

### 🌐 HTML Generation
- Generates complete, semantic HTML5 pages
- Includes proper meta tags for SEO
- Mobile-responsive design
- Structured data markup
- Accessibility features

## Architecture

```
brochure_processor.py
├── BrochureProcessor (main class)
├── Pydantic Models
│   ├── GraphicData
│   ├── PageData  
│   ├── PageAnalysis
│   └── HTMLGeneration
└── Processing Pipeline
    ├── 1. OCR Text Extraction
    ├── 2. Graphics Detection
    ├── 3. Graphics Extraction
    ├── 4. Content Analysis
    ├── 5. HTML Generation
    └── 6. Data Structuring
```

## Installation

### 1. Install Dependencies

```bash
pip install -r brochure_requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file from the template:

```bash
cp .env.template .env
```

Edit `.env` and add your API keys:

```env
REPLICATE_API_TOKEN=your_replicate_token_here
OPENAI_API_KEY=your_openai_key_here
```

**Get API Keys:**
- **Replicate:** https://replicate.com/account/api-tokens
- **OpenAI:** https://platform.openai.com/api-keys

## Usage

### Quick Start (Interactive)

```bash
python run_brochure_processor.py
```

This launches an interactive menu with options for:
1. Test run (2 images)
2. Full processing (all images)
3. Environment setup help

### Command Line Usage

```bash
# Basic usage
python brochure_processor.py --folder_path "path/to/images" --output_dir "output"

# With custom settings
python brochure_processor.py \
    --folder_path "input/Coastal Cabana EC - Archi Briefing for Jasmine_files" \
    --output_dir "output/brochure_processing" \
    --batch_size 3 \
    --limit 5
```

### Programmatic Usage

```python
import asyncio
from brochure_processor import BrochureProcessor

async def main():
    processor = BrochureProcessor(
        folder_path="input/images", 
        output_dir="output"
    )
    await processor.process_all_images(batch_size=3, limit=10)

asyncio.run(main())
```

## Parameters

### Command Line Arguments

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `--folder_path` | Yes | Path to folder containing brochure images | - |
| `--output_dir` | Yes | Output directory for results | - |
| `--batch_size` | No | Number of images to process concurrently | 3 |
| `--limit` | No | Limit number of images (for testing) | None |

### API Configuration

**Replicate Settings:**
- `conf`: Detection confidence threshold (0.25)
- `iou`: IoU threshold for object detection (0.45)

**OpenAI Settings:**
- Model: `gpt-4o-mini` (cost-effective, high quality)
- Temperature: 0.2-0.3 (consistent results)
- Max tokens: 1000-4000 (depending on task)

## Output Structure

```
output_directory/
├── brochure_data.json          # Complete structured data
├── graphics/                   # Extracted graphics
│   ├── img_0_graphic_0_person.png
│   ├── img_0_graphic_1_car.png
│   └── ...
└── html_pages/                 # Generated HTML pages
    ├── coastal-cabana-overview.html
    ├── floor-plans.html
    └── ...
```

### JSON Data Structure

```json
{
  "metadata": {
    "total_pages": 160,
    "source_folder": "input/images",
    "output_directory": "output",
    "processing_timestamp": "1234567890"
  },
  "pages": [
    {
      "original_filename": "img_1763380200_558438_0.jpg",
      "proposed_page_name": "coastal-cabana-overview",
      "page_text_content": "Welcome to Coastal Cabana...",
      "graphic_coordinates": [
        {"x1": 100, "y1": 200, "x2": 300, "y2": 400}
      ],
      "graphic_paths": ["output/graphics/img_0_graphic_0_person.png"],
      "page_description": "Overview of Coastal Cabana development",
      "page_structure_plan": "Header with hero image, main content sections...",
      "page_html": "<!DOCTYPE html>..."
    }
  ]
}
```

## Cost Estimation

### Per Image Processing Costs

**Replicate APIs:**
- OCR: ~$0.00075 per image
- YOLO11n: ~$0.00010 per image

**OpenAI APIs:**
- Page Analysis: ~$0.01-0.02 per image  
- HTML Generation: ~$0.02-0.04 per image

**Total per image:** ~$0.03-0.06

**For 160 images:** ~$4.80-9.60

### Optimization Tips

1. **Use batch processing** (default: 3 concurrent)
2. **Test with --limit** first
3. **Monitor API usage** in dashboards
4. **Use smaller models** for non-critical tasks

## Error Handling

### Common Issues

**1. API Rate Limits**
- Solution: Reduce `batch_size` parameter
- Built-in delays between batches

**2. Invalid Bounding Boxes**
- Solution: Automatic validation and skipping
- Logged for review

**3. OCR Failures**
- Solution: Graceful fallback with empty text
- Processing continues

**4. Network Issues**
- Solution: Automatic retry with exponential backoff
- Up to 3 retry attempts

### Logging

Comprehensive logging to both file and console:

```
2024-01-20 10:30:15 - INFO - Processing img_0.jpg
2024-01-20 10:30:18 - INFO - Extracted 1250 characters of text
2024-01-20 10:30:22 - INFO - Detected 3 graphics
2024-01-20 10:30:25 - INFO - Successfully extracted 3 graphics
```

Log files saved to: `brochure_processor.log`

## Performance

### Processing Times

- **Single image:** 30-60 seconds
- **Batch of 3:** 45-90 seconds  
- **160 images:** 2-4 hours (with rate limiting)

### System Requirements

- **Memory:** 2GB+ RAM
- **Storage:** 1GB+ for graphics and HTML files
- **Network:** Stable internet for API calls

## Advanced Usage

### Custom Processing Pipeline

```python
# Process single image with custom steps
processor = BrochureProcessor(folder_path, output_dir)

# Step-by-step processing
image_path = Path("image.jpg")
text = await processor.extract_text_ocr(image_path)
graphics = await processor.detect_graphics(image_path) 
graphic_paths = processor.extract_graphic_images(image_path, graphics)
analysis = await processor.analyze_page_content(image_path.name, text, len(graphics))
html = await processor.generate_html({...})
```

### Batch Processing Utilities

```python
# Process with custom filters
image_files = processor.get_image_files()
filtered_files = [f for f in image_files if "overview" in f.name]
results = await processor.process_batch(filtered_files)
```

## Integration with Django

The generated HTML and extracted data can be easily integrated into the existing Django project:

### 1. Import Structured Data

```python
# In your Django management command
import json
from coastal_cabana.models import BrochurePage

with open('brochure_data.json') as f:
    data = json.load(f)

for page_data in data['pages']:
    BrochurePage.objects.create(
        name=page_data['proposed_page_name'],
        content=page_data['page_text_content'],
        html_content=page_data['page_html'],
        description=page_data['page_description']
    )
```

### 2. Serve Generated HTML

```python
# In views.py
def brochure_page(request, page_name):
    html_path = f"output/html_pages/{page_name}.html"
    with open(html_path) as f:
        return HttpResponse(f.read())
```

### 3. Use Extracted Graphics

```python
# Copy graphics to Django static files
import shutil
import os

graphics_source = "output/graphics/"
graphics_dest = "static/images/brochure/"

for graphic_file in os.listdir(graphics_source):
    shutil.copy2(
        os.path.join(graphics_source, graphic_file),
        os.path.join(graphics_dest, graphic_file)
    )
```

## Troubleshooting

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components

```python
# Test OCR only
text = await processor.extract_text_ocr(image_path)
print(f"Extracted: {text[:200]}...")

# Test graphics detection only  
graphics = await processor.detect_graphics(image_path)
print(f"Found {len(graphics)} graphics")
```

### Validate API Keys

```python
import replicate
import openai

# Test Replicate
try:
    replicate.run("hello-world")
    print("✅ Replicate API working")
except:
    print("❌ Replicate API failed")

# Test OpenAI
try:
    from openai import OpenAI
    client = OpenAI()
    client.models.list()
    print("✅ OpenAI API working")
except:
    print("❌ OpenAI API failed")
```

## Contributing

### Code Structure

- **Main script:** `brochure_processor.py`
- **Pydantic models:** Define data structures
- **Async processing:** Handles concurrent API calls
- **Error handling:** Comprehensive exception management

### Adding New Features

1. **New AI Models:** Update API calls in respective methods
2. **Additional Formats:** Extend `get_image_files()` method
3. **Custom Prompts:** Modify OpenAI prompt templates
4. **Post-processing:** Add methods to `BrochureProcessor` class

## License

This project uses the existing project license. Check the main project repository for license details.

## Support

For issues and questions:

1. Check the logs: `brochure_processor.log`
2. Verify API keys and quotas
3. Test with --limit=1 for debugging
4. Review error messages and stack traces

## Changelog

### v1.0.0 (Initial Release)
- Complete brochure processing pipeline
- OCR text extraction with Replicate
- Graphics detection with YOLO11n
- AI-powered content analysis
- HTML generation with OpenAI
- Structured JSON output
- Batch processing support
- Comprehensive error handling