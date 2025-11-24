#!/usr/bin/env python3
"""
Test and Validation Script for Brochure Processor

This script performs basic validation to ensure the brochure processor
can run with the current environment setup.
"""

import os
import sys
import asyncio
from pathlib import Path
import traceback

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))


def test_imports():
    """Test that all required modules can be imported"""
    print("🔄 Testing imports...")
    
    try:
        import replicate
        print("  ✅ replicate")
    except ImportError as e:
        print(f"  ❌ replicate: {e}")
        return False
    
    try:
        from PIL import Image
        print("  ✅ PIL (Pillow)")
    except ImportError as e:
        print(f"  ❌ PIL: {e}")
        return False
    
    try:
        from pydantic import BaseModel
        print("  ✅ pydantic")
    except ImportError as e:
        print(f"  ❌ pydantic: {e}")
        return False
    
    try:
        import httpx
        print("  ✅ httpx")
    except ImportError as e:
        print(f"  ❌ httpx: {e}")
        return False
    
    try:
        from openai import AsyncOpenAI
        print("  ✅ openai")
    except ImportError as e:
        print(f"  ❌ openai: {e}")
        return False
    
    try:
        from gpt.gpt_requests import gpt_request
        print("  ✅ gpt module")
    except ImportError as e:
        print(f"  ❌ gpt module: {e}")
        return False
    
    return True


def test_environment():
    """Test environment configuration"""
    print("\n🔄 Testing environment...")
    
    required_vars = ['REPLICATE_API_TOKEN', 'OPENAI_API_KEY']
    all_set = True
    
    for var in required_vars:
        if os.environ.get(var):
            print(f"  ✅ {var} is set")
        else:
            print(f"  ❌ {var} is not set")
            all_set = False
    
    return all_set


def test_input_folder():
    """Test that input folder exists and contains images"""
    print("\n🔄 Testing input folder...")
    
    input_folder = Path("input/Coastal Cabana EC - Archi Briefing for Jasmine_files")
    
    if not input_folder.exists():
        print(f"  ❌ Input folder not found: {input_folder}")
        return False
    
    print(f"  ✅ Input folder exists: {input_folder}")
    
    # Count image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    image_files = []
    
    for file_path in input_folder.iterdir():
        if file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    print(f"  ✅ Found {len(image_files)} image files")
    
    if len(image_files) > 0:
        print(f"  📋 Sample files:")
        for i, img in enumerate(sorted(image_files)[:5]):
            print(f"     {i+1}. {img.name}")
        if len(image_files) > 5:
            print(f"     ... and {len(image_files) - 5} more")
    
    return len(image_files) > 0


async def test_api_connections():
    """Test API connections (lightweight)"""
    print("\n🔄 Testing API connections...")
    
    # Test Replicate connection (without making actual API calls)
    try:
        import replicate
        # Just test that we can import and the client initializes
        replicate_client = replicate.Client()
        print("  ✅ Replicate client initialized")
    except Exception as e:
        print(f"  ❌ Replicate client failed: {e}")
        return False
    
    # Test OpenAI connection
    try:
        from openai import AsyncOpenAI
        import httpx
        
        client = AsyncOpenAI(
            api_key=os.environ.get('OPENAI_API_KEY', 'test'),
            http_client=httpx.AsyncClient(
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
            )
        )
        print("  ✅ OpenAI client initialized")
        await client.close()
    except Exception as e:
        print(f"  ❌ OpenAI client failed: {e}")
        return False
    
    return True


def test_brochure_processor_import():
    """Test that the main brochure processor can be imported"""
    print("\n🔄 Testing brochure processor import...")
    
    try:
        from brochure_processor.scripts.brochure_processor import BrochureProcessor
        print("  ✅ BrochureProcessor imported successfully")
        
        # Test basic initialization (without API calls)
        processor = BrochureProcessor(
            folder_path="test", 
            output_dir="test_output"
        )
        print("  ✅ BrochureProcessor initializes without errors")
        
        return True
        
    except Exception as e:
        print(f"  ❌ BrochureProcessor import failed: {e}")
        print(f"  📋 Error details: {traceback.format_exc()}")
        return False


async def run_validation():
    """Run all validation tests"""
    print("🏢 Brochure Processor - Validation Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Environment Test", test_environment), 
        ("Input Folder Test", test_input_folder),
        ("API Connection Test", test_api_connections),
        ("Processor Import Test", test_brochure_processor_import),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! The brochure processor is ready to use.")
        print("\n📋 Next steps:")
        print("  1. Run: python run_brochure_processor.py")
        print("  2. Choose option 1 for a test run")
        print("  3. Check the output folder for results")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before proceeding.")
        print("\n🔧 Common fixes:")
        print("  - Install missing packages: pip install -r brochure_requirements.txt")
        print("  - Set environment variables (see .env.template)")
        print("  - Ensure input folder exists and contains images")
    
    return passed == len(results)


def print_system_info():
    """Print system information for debugging"""
    print("\n📋 System Information:")
    print(f"  Python version: {sys.version}")
    print(f"  Current directory: {os.getcwd()}")
    print(f"  Script location: {Path(__file__).parent}")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("  ✅ .env file found")
    else:
        print("  ⚠️  .env file not found (you can create one from .env.template)")


if __name__ == "__main__":
    print_system_info()
    result = asyncio.run(run_validation())
    sys.exit(0 if result else 1)