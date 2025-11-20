# GPT Utilities Package

A reusable OpenAI API wrapper for Django projects, providing asynchronous requests with automatic retry logic, cost tracking, and structured outputs.

## Features

- ✅ **Async/Await Support** - Efficient concurrent API requests
- ✅ **Automatic Retries** - Exponential backoff with tenacity
- ✅ **Cost Tracking** - Automatic token usage and cost calculation
- ✅ **Structured Outputs** - Pydantic model support for type-safe responses
- ✅ **Template Rendering** - Jinja2 integration for dynamic prompts
- ✅ **Error Handling** - Comprehensive logging and error recovery

## Installation

This package is already part of your Django project. Ensure dependencies are installed:

```bash
pip install openai httpx tenacity jinja2 pydantic python-dotenv json-repair
```

## Configuration

Set your OpenAI API key in `.env`:

```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Basic GPT Request

```python
from gpt import gpt_request

# In an async function or view
async def my_view(request):
    params = {
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant'},
            {'role': 'user', 'content': 'What is Django?'}
        ],
        'temperature': 0,
        'max_tokens': 256
    }
    
    outputs, cost = await gpt_request(__name__, params)
    response_text = outputs[0]
    print(f"Cost: ${cost:.4f}")
    
    return JsonResponse({'response': response_text, 'cost': cost})
```

### Structured Output with Pydantic

```python
from gpt import gpt_request
from pydantic import BaseModel, Field

class LocationData(BaseModel):
    city: str = Field(description="City name")
    country: str = Field(description="Country name")
    latitude: float
    longitude: float

async def extract_location(text):
    params = {
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'user', 'content': f'Extract location data from: {text}'}
        ],
        'response_format': LocationData  # Returns typed Pydantic model
    }
    
    outputs, cost = await gpt_request(__name__, params)
    location = outputs[0]  # LocationData instance
    
    # Access typed fields
    print(f"{location.city}, {location.country}")
    print(f"Coordinates: {location.latitude}, {location.longitude}")
```

### Concurrent Requests

Process multiple requests in parallel:

```python
from gpt import gpt_request

async def batch_analysis(texts):
    params_list = [
        {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'user', 'content': f'Summarize: {text}'}],
            'temperature': 0,
            'max_tokens': 100
        }
        for text in texts
    ]
    
    outputs, total_cost = await gpt_request(__name__, params_list)
    # outputs[i] corresponds to texts[i]
    
    return outputs, total_cost
```

### Template Rendering

Use Jinja2 templates for complex prompts:

```python
from gpt import render_template

# Create template file: prompts/location_prompt.txt
# "Extract location from: {{ text }}"

prompt = render_template('location_prompt.txt', text='Visit Paris, France')
```

## API Reference

### `gpt_request(func_name, params_list)`

**Parameters:**
- `func_name` (str): Identifier for logging (use `__name__`)
- `params_list` (dict | list): Single params dict or list of dicts
  - `model` (str): OpenAI model name
  - `messages` (list): Chat messages
  - `temperature` (float): Sampling temperature (default: 0)
  - `max_tokens` (int): Max tokens to generate (default: 1000)
  - `response_format` (BaseModel, optional): Pydantic model for structured output
  - `top_p`, `frequency_penalty`, `presence_penalty`: Optional parameters

**Returns:**
- `tuple`: `(outputs, total_cost)`
  - `outputs` (list): List of responses (same order as input)
  - `total_cost` (float): Total cost in USD

### `render_template(template_name, **kwargs)`

**Parameters:**
- `template_name` (str): Template filename in `prompts/` directory
- `**kwargs`: Variables to pass to template

**Returns:**
- `str`: Rendered template content

## File Structure

```
gpt/
├── __init__.py           # Package exports
├── gpt_requests.py       # Main API wrapper
├── render_template.py    # Template rendering
├── price_lut.json        # Model pricing data
└── README.md            # This file
```

## Usage in Django Apps

Import and use in any Django app:

```python
# In location_map/views.py
from gpt import gpt_request
from asgiref.sync import async_to_sync

# For sync views, wrap with async_to_sync
def my_sync_view(request):
    result = async_to_sync(gpt_request)(__name__, params)
    return JsonResponse({'result': result})

# For async views, use directly
async def my_async_view(request):
    outputs, cost = await gpt_request(__name__, params)
    return JsonResponse({'outputs': outputs, 'cost': cost})
```

## Cost Tracking

The package automatically calculates costs based on token usage:

```python
outputs, cost = await gpt_request(__name__, params)
print(f"Request cost: ${cost:.6f}")
```

Pricing is maintained in `price_lut.json`.

## Error Handling

Automatic retry with exponential backoff (3 attempts):

```python
from tenacity import RetryError

try:
    outputs, cost = await gpt_request(__name__, params)
except RetryError as e:
    # All retry attempts failed
    print(f"API request failed after retries: {e}")
```

## Testing

The package includes comprehensive pytest-based tests:

```bash
# Run all tests
pytest gpt/

# Run unit tests only (fast, no API calls to slow tests)
pytest gpt/ -m "not integration"

# Run with coverage
pytest --cov=gpt gpt/
```

See [TESTING.md](TESTING.md) for detailed testing guide.

### Test Structure

- `test_gpt_unit.py` - Fast unit tests for all core functionality
- `test_gpt_integration.py` - Integration tests with real API calls
- `conftest.py` - Shared pytest fixtures and configuration
- `pytest.ini` (in project root) - Pytest configuration

## Notes

- Supports Windows with automatic event loop policy
- Handles incomplete JSON responses with `json-repair`
- Logs partial responses when hitting length limits
- Thread-safe with connection pooling (100 max connections)
