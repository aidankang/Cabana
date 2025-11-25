#!/usr/bin/env python3
"""
Setup script for Brochure Processor

This script helps set up the brochure processor environment.
"""

import os
import sys
import subprocess
from pathlib import Path


def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    
    requirements_file = Path(__file__).parent / "config" / "brochure_requirements.txt"
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False


def setup_environment():
    """Set up environment file"""
    print("\n🔧 Setting up environment...")
    
    env_template = Path(__file__).parent / "config" / ".env.template"
    env_file = Path(__file__).parent.parent / ".env"
    
    if env_file.exists():
        print(f"✅ Environment file already exists: {env_file}")
        return True
    
    try:
        # Copy template to project root
        with open(env_template, 'r') as template:
            content = template.read()
        
        with open(env_file, 'w') as env:
            env.write(content)
        
        print(f"✅ Created environment file: {env_file}")
        print("⚠️  Remember to edit .env and add your API keys!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create environment file: {e}")
        return False


def run_tests():
    """Run validation tests"""
    print("\n🧪 Running validation tests...")
    
    test_script = Path(__file__).parent / "scripts" / "test_brochure_processor.py"
    
    try:
        result = subprocess.run([sys.executable, str(test_script)], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed. Check the output above.")
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False


def main():
    """Main setup process"""
    print("🏢 Brochure Processor Setup")
    print("=" * 50)
    
    steps = [
        ("Install Requirements", install_requirements),
        ("Setup Environment", setup_environment),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        success = step_func()
        
        if not success:
            print(f"\n❌ Setup failed at: {step_name}")
            print("\n🔧 Manual steps needed:")
            print("  1. Fix the error above")
            print("  2. Run this setup script again")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("  1. Edit .env file and add your API keys:")
    print("     - REPLICATE_API_TOKEN (from https://replicate.com/account/api-tokens)")  
    print("     - OPENAI_API_KEY (from https://platform.openai.com/api-keys)")
    print("  2. Run tests: python scripts/test_brochure_processor.py")
    print("  3. Start processing: python scripts/run_brochure_processor.py")
    print("\n🚀 Ready to convert your brochure images!")


if __name__ == "__main__":
    main()