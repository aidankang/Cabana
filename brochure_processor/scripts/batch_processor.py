#!/usr/bin/env python3
"""
Batch Processing Utilities for Brochure Processor

This module provides advanced utilities for batch processing,
progress tracking, and resume functionality.
"""

import json
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Optional, Set
from datetime import datetime
import argparse

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from brochure_processor.scripts.brochure_processor import BrochureProcessor, PageData


class BatchProgressTracker:
    """Track and manage batch processing progress"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.progress_file = self.output_dir / ".processing_progress.json"
        self.completed_files: Set[str] = set()
        self.failed_files: Set[str] = set()
        self.total_files = 0
        self.start_time = None
        
    def load_progress(self):
        """Load existing progress from file"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                self.completed_files = set(data.get('completed_files', []))
                self.failed_files = set(data.get('failed_files', []))
                self.total_files = data.get('total_files', 0)
                print(f"📋 Loaded progress: {len(self.completed_files)}/{self.total_files} completed")
    
    def save_progress(self):
        """Save current progress to file"""
        data = {
            'completed_files': list(self.completed_files),
            'failed_files': list(self.failed_files),
            'total_files': self.total_files,
            'last_updated': datetime.now().isoformat()
        }
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.progress_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def mark_completed(self, filename: str):
        """Mark a file as completed"""
        self.completed_files.add(filename)
        self.failed_files.discard(filename)  # Remove from failed if it was there
        self.save_progress()
    
    def mark_failed(self, filename: str):
        """Mark a file as failed"""
        self.failed_files.add(filename)
        self.save_progress()
    
    def is_completed(self, filename: str) -> bool:
        """Check if a file has been completed"""
        return filename in self.completed_files
    
    def get_remaining_files(self, all_files: List[Path]) -> List[Path]:
        """Get list of files that still need processing"""
        return [f for f in all_files if f.name not in self.completed_files]
    
    def print_status(self):
        """Print current processing status"""
        completed = len(self.completed_files)
        failed = len(self.failed_files)
        remaining = self.total_files - completed - failed
        
        print(f"📊 Processing Status:")
        print(f"  ✅ Completed: {completed}")
        print(f"  ❌ Failed: {failed}")
        print(f"  ⏳ Remaining: {remaining}")
        print(f"  📈 Progress: {completed/self.total_files*100:.1f}%")
        
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            if completed > 0:
                avg_time = elapsed.total_seconds() / completed
                eta_seconds = avg_time * remaining
                eta = datetime.now() + timedelta(seconds=eta_seconds)
                print(f"  ⏱️  ETA: {eta.strftime('%H:%M:%S')}")


class ResumableBatchProcessor(BrochureProcessor):
    """Extended processor with resume capability"""
    
    def __init__(self, folder_path: str, output_dir: str):
        super().__init__(folder_path, output_dir)
        self.progress = BatchProgressTracker(self.output_dir)
        
    async def process_with_resume(self, batch_size: int = 3, limit: Optional[int] = None):
        """Process images with resume capability"""
        
        # Load existing progress
        self.progress.load_progress()
        
        # Get all image files
        all_files = self.get_image_files()
        if limit:
            all_files = all_files[:limit]
        
        self.progress.total_files = len(all_files)
        
        # Get remaining files to process
        remaining_files = self.progress.get_remaining_files(all_files)
        
        if not remaining_files:
            print("✅ All files already processed!")
            return
        
        print(f"📋 Resuming processing: {len(remaining_files)} files remaining")
        self.progress.start_time = datetime.now()
        
        # Process in batches
        for i in range(0, len(remaining_files), batch_size):
            batch = remaining_files[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(remaining_files) + batch_size - 1) // batch_size
            
            print(f"\n🔄 Processing batch {batch_num}/{total_batches}")
            self.progress.print_status()
            
            # Process batch with individual error handling
            for image_path in batch:
                try:
                    print(f"  📄 Processing {image_path.name}...")
                    result = await self.process_single_image(image_path)
                    
                    # Save individual result immediately
                    await self.save_individual_result(result)
                    
                    self.progress.mark_completed(image_path.name)
                    print(f"  ✅ Completed {image_path.name}")
                    
                except Exception as e:
                    print(f"  ❌ Failed {image_path.name}: {e}")
                    self.progress.mark_failed(image_path.name)
                    continue
            
            # Delay between batches
            if i + batch_size < len(remaining_files):
                print("  ⏳ Waiting between batches...")
                await asyncio.sleep(2)
        
        # Final consolidation
        await self.consolidate_results()
        print("\n🎉 Batch processing completed!")
    
    async def save_individual_result(self, page_data: PageData):
        """Save individual page result immediately"""
        individual_dir = self.output_dir / "individual_results"
        individual_dir.mkdir(exist_ok=True)
        
        filename = f"{page_data.proposed_page_name}.json"
        file_path = individual_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(page_data.model_dump(), f, indent=2, ensure_ascii=False)
    
    async def consolidate_results(self):
        """Consolidate all individual results into final JSON"""
        individual_dir = self.output_dir / "individual_results"
        
        if not individual_dir.exists():
            return
        
        all_pages = []
        
        for json_file in individual_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    page_data = json.load(f)
                    all_pages.append(page_data)
            except Exception as e:
                print(f"Warning: Could not load {json_file}: {e}")
        
        # Sort by original filename
        all_pages.sort(key=lambda x: x.get('original_filename', ''))
        
        # Create consolidated JSON
        output_json = {
            'metadata': {
                'total_pages': len(all_pages),
                'source_folder': str(self.folder_path),
                'output_directory': str(self.output_dir),
                'processing_timestamp': datetime.now().isoformat(),
                'completed_files': len(self.progress.completed_files),
                'failed_files': len(self.progress.failed_files)
            },
            'pages': all_pages
        }
        
        json_path = self.output_dir / 'brochure_data.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_json, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Consolidated {len(all_pages)} pages into {json_path}")


class FilteredProcessor:
    """Process only specific images based on filters"""
    
    def __init__(self, processor: BrochureProcessor):
        self.processor = processor
    
    def filter_by_pattern(self, files: List[Path], pattern: str) -> List[Path]:
        """Filter files by name pattern"""
        return [f for f in files if pattern.lower() in f.name.lower()]
    
    def filter_by_range(self, files: List[Path], start: int, end: int) -> List[Path]:
        """Filter files by index range"""
        return files[start:end]
    
    def filter_by_keywords(self, files: List[Path], keywords: List[str]) -> List[Path]:
        """Filter files by multiple keywords"""
        filtered = []
        for f in files:
            if any(keyword.lower() in f.name.lower() for keyword in keywords):
                filtered.append(f)
        return filtered


async def main():
    """Command line interface for batch processing"""
    parser = argparse.ArgumentParser(description='Advanced Batch Processing for Brochure Processor')
    parser.add_argument('--folder_path', required=True, help='Path to folder containing images')
    parser.add_argument('--output_dir', required=True, help='Output directory')
    parser.add_argument('--batch_size', type=int, default=3, help='Batch size for processing')
    parser.add_argument('--resume', action='store_true', help='Resume from previous processing')
    parser.add_argument('--limit', type=int, help='Limit number of images to process')
    parser.add_argument('--filter_pattern', help='Filter images by name pattern')
    parser.add_argument('--start_index', type=int, help='Start processing from this index')
    parser.add_argument('--end_index', type=int, help='End processing at this index')
    parser.add_argument('--status', action='store_true', help='Show processing status only')
    
    args = parser.parse_args()
    
    # Initialize processor
    if args.resume:
        processor = ResumableBatchProcessor(args.folder_path, args.output_dir)
    else:
        processor = BrochureProcessor(args.folder_path, args.output_dir)
    
    # Show status only
    if args.status:
        if hasattr(processor, 'progress'):
            processor.progress.load_progress()
            processor.progress.print_status()
        else:
            print("❌ Status only available with --resume flag")
        return
    
    # Apply filters if specified
    files = processor.get_image_files()
    
    if args.filter_pattern:
        filter_proc = FilteredProcessor(processor)
        files = filter_proc.filter_by_pattern(files, args.filter_pattern)
        print(f"📋 Filtered to {len(files)} files matching '{args.filter_pattern}'")
    
    if args.start_index is not None or args.end_index is not None:
        start = args.start_index or 0
        end = args.end_index or len(files)
        filter_proc = FilteredProcessor(processor)
        files = filter_proc.filter_by_range(files, start, end)
        print(f"📋 Processing files {start} to {end} ({len(files)} files)")
    
    if args.limit:
        files = files[:args.limit]
        print(f"📋 Limited to {args.limit} files")
    
    # Process files
    if args.resume and hasattr(processor, 'process_with_resume'):
        await processor.process_with_resume(batch_size=args.batch_size)
    else:
        # Standard processing with selected files
        processor.processed_pages = await processor.process_batch(files, args.batch_size)
        
        # Save results
        output_json = {
            'metadata': {
                'total_pages': len(processor.processed_pages),
                'source_folder': str(processor.folder_path),
                'output_directory': str(processor.output_dir),
                'processing_timestamp': datetime.now().isoformat()
            },
            'pages': [page.model_dump() for page in processor.processed_pages]
        }
        
        json_path = processor.output_dir / 'brochure_data.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_json, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Processing complete! Results saved to {json_path}")


if __name__ == "__main__":
    # Import datetime at module level for ETA calculation
    from datetime import datetime, timedelta
    
    asyncio.run(main())