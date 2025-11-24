# 🏢 Brochure Processor

A comprehensive toolkit for converting static brochure images into crawlable, SEO-friendly web content.

## 📁 Directory Structure

```
brochure_processor/
├── __init__.py                 # Package initialization
├── README.md                   # This file
├── scripts/                    # Main processing scripts
│   ├── __init__.py
│   ├── brochure_processor.py   # Core processing engine
│   ├── batch_processor.py      # Advanced batch processing
│   ├── run_brochure_processor.py # Interactive menu interface
│   └── test_brochure_processor.py # Validation and testing
├── config/                     # Configuration files
│   ├── .env.template          # Environment variables template
│   └── brochure_requirements.txt # Python dependencies
└── docs/                       # Documentation
    ├── BROCHURE_PROCESSOR_README.md # Complete documentation
    └── QUICK_START.md          # 5-minute setup guide
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd brochure_processor
pip install -r config/brochure_requirements.txt
```

### 2. Configure Environment
```bash
# Copy and edit configuration
cp config/.env.template ../.env
# Edit .env with your API keys
```

### 3. Test Setup
```bash
python scripts/test_brochure_processor.py
```

### 4. Run Processing
```bash
python scripts/run_brochure_processor.py
```

## 📋 What It Does

Converts brochure images into web content by:

- 🔍 **Extracting text** using OCR (Replicate API)
- 🎯 **Detecting graphics** using YOLO11n (Replicate API)  
- ✂️ **Extracting individual graphics** using Pillow
- 🧠 **Analyzing content** using OpenAI GPT-4
- 🌐 **Generating HTML pages** using OpenAI GPT-4
- 📊 **Creating structured JSON data** for integration

## 💰 Cost Estimate

- **Per image:** ~$0.03-0.06
- **160 images:** ~$5-10 total

## 📤 Output

```
output/
├── brochure_data.json          # Complete structured data
├── graphics/                   # Extracted graphics
└── html_pages/                 # Generated HTML pages
```

## 📚 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- **[Complete Documentation](docs/BROCHURE_PROCESSOR_README.md)** - Full feature reference

## 🎮 Usage Options

### Interactive (Recommended)
```bash
python scripts/run_brochure_processor.py
```

### Command Line
```bash
python scripts/brochure_processor.py \
  --folder_path "../input/Coastal Cabana EC - Archi Briefing for Jasmine_files" \
  --output_dir "../output" \
  --limit 5
```

### Advanced Batch Processing
```bash
python scripts/batch_processor.py \
  --folder_path "../input/images" \
  --output_dir "../output" \
  --resume \
  --batch_size 3
```

## 🔧 API Requirements

- **Replicate API Token** - https://replicate.com/account/api-tokens
- **OpenAI API Key** - https://platform.openai.com/api-keys

## 🎯 Features

- ✅ Async processing for efficiency
- ✅ Batch processing with rate limiting  
- ✅ Resume capability for interrupted jobs
- ✅ Error handling with automatic retries
- ✅ Progress tracking and logging
- ✅ SEO-optimized HTML generation
- ✅ Mobile-responsive output
- ✅ Structured data for search engines

---

**Ready to start?** Check out the [Quick Start Guide](docs/QUICK_START.md)!