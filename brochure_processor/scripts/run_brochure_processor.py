#!/usr/bin/env python3
"""
Example usage script for the Brochure Processor

This script demonstrates how to use the brochure processor to convert
a folder of brochure images into crawlable web content.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from brochure_processor.scripts.brochure_processor import BrochureProcessor


async def run_example():
    """Example usage of the brochure processor"""
    
    # Configuration
    input_folder = r"c:\Projects\Cabana\input\Coastal Cabana EC - Archi Briefing for Jasmine_files"
    output_directory = r"c:\Projects\Cabana\output\brochure_processing"
    
    print("=== Brochure Processor Example ===")
    print(f"Input folder: {input_folder}")
    print(f"Output directory: {output_directory}")
    print()
    
    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"❌ Error: Input folder does not exist: {input_folder}")
        return
    
    # Check environment variables
    required_env_vars = ['REPLICATE_API_TOKEN', 'OPENAI_API_KEY']
    missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these environment variables before running.")
        return
    
    print("✅ Environment variables configured")
    print("✅ Input folder found")
    print()
    
    try:
        # Initialize processor
        processor = BrochureProcessor(input_folder, output_directory)
        
        # Run with limited images for testing (remove limit for full processing)
        print("🔄 Starting processing (limited to 2 images for testing)...")
        await processor.process_all_images(batch_size=2, limit=2)
        
        print("\n✅ Processing completed successfully!")
        print(f"📁 Check results in: {output_directory}")
        print(f"📄 Main data file: {output_directory}/brochure_data.json")
        print(f"🎨 Graphics folder: {output_directory}/graphics/")
        print(f"🌐 HTML pages folder: {output_directory}/html_pages/")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        import traceback
        print(traceback.format_exc())


async def run_full_processing():
    """Process all images without limit"""
    
    input_folder = r"c:\Projects\Cabana\input\Coastal Cabana EC - Archi Briefing for Jasmine_files"
    output_directory = r"c:\Projects\Cabana\output\brochure_processing_full"
    
    print("=== Full Brochure Processing ===")
    print("⚠️  This will process ALL 160 images and may take several hours!")
    print("⚠️  This will use significant API credits!")
    print()
    
    confirm = input("Are you sure you want to continue? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Processing cancelled.")
        return
    
    try:
        processor = BrochureProcessor(input_folder, output_directory)
        await processor.process_all_images(batch_size=3)  # Process 3 at a time
        
        print("\n🎉 Full processing completed!")
        
    except Exception as e:
        print(f"❌ Error during full processing: {e}")


def setup_environment():
    """Help user set up environment variables"""
    print("=== Environment Setup ===")
    print()
    print("You need to set the following environment variables:")
    print()
    print("1. REPLICATE_API_TOKEN")
    print("   - Get your token from: https://replicate.com/account/api-tokens")
    print("   - Set with: export REPLICATE_API_TOKEN=your_token_here")
    print()
    print("2. OPENAI_API_KEY") 
    print("   - Get your key from: https://platform.openai.com/api-keys")
    print("   - Set with: export OPENAI_API_KEY=your_key_here")
    print()
    print("For Windows PowerShell:")
    print("   $env:REPLICATE_API_TOKEN='your_token_here'")
    print("   $env:OPENAI_API_KEY='your_key_here'")
    print()
    print("You can also create a .env file in the project root with:")
    print("   REPLICATE_API_TOKEN=your_token_here")
    print("   OPENAI_API_KEY=your_key_here")


async def main():
    """Main menu"""
    print("🏢 Brochure Processor - Coastal Cabana EC")
    print("=" * 50)
    print()
    print("Choose an option:")
    print("1. Run example (2 images for testing)")
    print("2. Run full processing (all 160 images)")
    print("3. Show environment setup instructions")
    print("4. Exit")
    print()
    
    while True:
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == '1':
            await run_example()
            break
        elif choice == '2':
            await run_full_processing()
            break
        elif choice == '3':
            setup_environment()
            break
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    asyncio.run(main())