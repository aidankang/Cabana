# GPT Package

A reusable OpenAI API wrapper for Django projects.

## Quick Start

```python
from gpt import gpt_request

# Simple request
params = {
    'model': 'gpt-4o-mini',
    'messages': [{'role': 'user', 'content': 'Hello!'}],
}
outputs, cost = await gpt_request(__name__, params)
```

## Documentation

- **[Full Documentation](docs/README.md)** - Complete usage guide
- **[Testing Guide](tests/README.md)** - How to run and write tests

## Package Structure

```
gpt/
├── __init__.py           # Package exports
├── gpt_requests.py       # Main API wrapper
├── render_template.py    # Template rendering utilities
├── price_lut.json        # Model pricing data
├── docs/                 # Documentation
│   ├── README.md         # Complete usage guide
│   ├── TESTING.md        # Detailed testing guide
│   └── SETUP.md          # Setup summary
└── tests/                # All tests
    ├── conftest.py       # Pytest fixtures
    ├── test_unit.py      # Unit tests (fast, mocked)
    └── test_integration.py  # Integration tests (real API)
```

## Testing

```bash
# Run unit tests (fast, no API calls)
pytest gpt/tests/test_unit.py

# Run integration tests (real API)
pytest gpt/tests/test_integration.py

# Run all tests
pytest gpt/tests/
```

## Installation

Set your API key in `.env`:

```
OPENAI_API_KEY=your_key_here
```
