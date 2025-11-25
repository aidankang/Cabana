# 🏢 Brochure Processor - Quick Start Guide

## 🎯 What This Does

The Brochure Processor converts your static brochure images into crawlable, SEO-friendly web content by:

- **Extracting text** using OCR (Replicate API)
- **Detecting graphics** using YOLO11n (Replicate API)  
- **Extracting individual graphics** using Pillow
- **Analyzing content** using OpenAI GPT-4
- **Generating HTML pages** using OpenAI GPT-4
- **Creating structured JSON data** for easy integration

## 🚀 Quick Setup (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r config/brochure_requirements.txt
```

### 2. Get API Keys
- **Replicate:** https://replicate.com/account/api-tokens
- **OpenAI:** https://platform.openai.com/api-keys

### 3. Set Environment Variables
```bash
# Copy template
cp config/.env.template ../.env

# Edit .env file and add your keys:
REPLICATE_API_TOKEN=your_replicate_token_here  
OPENAI_API_KEY=your_openai_key_here
```

### 4. Test Setup
```bash
python scripts/test_brochure_processor.py
```

### 5. Run Processor
```bash
python scripts/run_brochure_processor.py
```

## 📊 Cost Estimate

**Per Image:** ~$0.03-0.06  
**160 Images:** ~$5-10 total

## 📁 Files Created

| File | Purpose |
|------|---------|
| `scripts/brochure_processor.py` | Main processing script |
| `scripts/run_brochure_processor.py` | Interactive menu interface |
| `scripts/test_brochure_processor.py` | Validation and testing |
| `scripts/batch_processor.py` | Advanced batch processing |
| `config/brochure_requirements.txt` | Python dependencies |
| `config/.env.template` | Environment configuration template |
| `docs/BROCHURE_PROCESSOR_README.md` | Complete documentation |

## 🎮 Usage Options

### Option 1: Interactive (Recommended)
```bash
python run_brochure_processor.py
# Follow the menu prompts
```

### Option 2: Command Line
```bash
python scripts/brochure_processor.py \
  --folder_path "../input/Coastal Cabana EC - Archi Briefing for Jasmine_files" \
  --output_dir "../output" \
  --limit 5
```

### Option 3: Advanced Batch Processing
```bash
python scripts/batch_processor.py \
  --folder_path "../input/images" \
  --output_dir "../output" \
  --resume \
  --batch_size 3
```

## 📤 Output Structure

```
output/
├── brochure_data.json          # Complete structured data
├── graphics/                   # Extracted graphics
│   ├── img_0_graphic_0_person.png
│   └── ...
└── html_pages/                 # Generated HTML pages  
    ├── coastal-cabana-overview.html
    └── ...
```

## 🔧 Troubleshooting

### Common Issues

**"Module not found"**
```bash
pip install -r config/brochure_requirements.txt
```

**"API key not set"**
```bash
# Check .env file exists and has correct format
cat .env
```

**"Folder not found"** 
```bash
# Verify path exists
ls "input/Coastal Cabana EC - Archi Briefing for Jasmine_files"
```

### Get Help
```bash
python scripts/test_brochure_processor.py  # Run diagnostics
python scripts/run_brochure_processor.py   # Interactive setup help
```

## 🎯 What's Included

### Structured JSON Output
```json
{
  "pages": [
    {
      "original_filename": "img_0.jpg",
      "proposed_page_name": "coastal-cabana-overview", 
      "page_text_content": "Welcome to Coastal Cabana...",
      "graphic_coordinates": [{"x1": 100, "y1": 200, "x2": 300, "y2": 400}],
      "graphic_paths": ["graphics/img_0_graphic_0.png"],
      "page_description": "Overview of the development",
      "page_structure_plan": "Header with hero, main content...",
      "page_html": "<!DOCTYPE html>..."
    }
  ]
}
```

### Generated HTML Features
- ✅ Semantic HTML5 structure
- ✅ SEO meta tags  
- ✅ Mobile responsive
- ✅ Accessibility features
- ✅ Structured data markup

## 🚀 Next Steps

1. **Test with small batch:** Start with `--limit 2` 
2. **Check output quality:** Review generated HTML and extracted text
3. **Run full processing:** Remove limit for all 160 images
4. **Integrate with Django:** Use generated JSON and HTML in your website

## 📚 Advanced Features

- **Resume processing:** Continue interrupted batch jobs
- **Filter processing:** Process specific image patterns
- **Progress tracking:** Monitor batch processing status  
- **Error handling:** Automatic retries and graceful failures
- **Cost tracking:** Built-in API cost calculation

---

**Ready to get started?** Run `python scripts/test_brochure_processor.py` to validate your setup!