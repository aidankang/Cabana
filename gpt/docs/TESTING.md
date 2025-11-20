# GPT Package Testing Guide

## Quick Start

```bash
# Run all tests
pytest gpt/

# Run with verbose output
pytest gpt/ -v

# Run specific test file
pytest gpt/test_gpt_unit.py

# Run specific test
pytest gpt/test_gpt_unit.py::test_imports
```

## Test Organization

### Unit Tests (`test_gpt_unit.py`)
- Fast, comprehensive tests
- Cover all basic functionality
- Run these frequently during development
- No special markers needed

### Integration Tests (`test_gpt_integration.py`)
- Make real API calls
- Marked as `@pytest.mark.integration` and `@pytest.mark.slow`
- Use for end-to-end validation

### Legacy Test Script (`test_gpt.py`)
- Original standalone test script
- Still works but not recommended for new tests
- Use pytest tests instead

## Running Tests Selectively

```bash
# Skip slow/integration tests (fast development cycle)
pytest gpt/ -m "not integration"
pytest gpt/ -m "not slow"

# Run only integration tests
pytest gpt/ -m integration

# Run only unit tests
pytest gpt/ -m unit
```

## Test Coverage

```bash
# Install coverage tool
pip install pytest-cov

# Run with coverage report
pytest --cov=gpt gpt/

# Generate HTML coverage report
pytest --cov=gpt --cov-report=html gpt/
# View in browser: htmlcov/index.html
```

## Writing New Tests

### Basic Test Structure

```python
import pytest

@pytest.mark.unit
@pytest.mark.asyncio  # For async tests
async def test_my_feature():
    from gpt import gpt_request
    
    # Arrange
    params = {...}
    
    # Act
    outputs, cost = await gpt_request(__name__, params)
    
    # Assert
    assert len(outputs) > 0
    assert cost > 0
```

### Using Fixtures

```python
@pytest.mark.unit
@pytest.mark.asyncio
async def test_with_fixture(ensure_api_key, gpt_params):
    """Fixtures provide reusable test data."""
    from gpt import gpt_request
    
    outputs, cost = await gpt_request(__name__, gpt_params)
    assert outputs[0] is not None
```

### Marking Tests

```python
@pytest.mark.unit           # Unit test
@pytest.mark.integration    # Integration test
@pytest.mark.slow          # Slow test (can be skipped)
@pytest.mark.asyncio       # Async test (required for async functions)
```

## Available Fixtures (see `conftest.py`)

- `ensure_api_key` - Ensures API key is set, skips test if not
- `sample_messages` - Standard message format for testing
- `gpt_params` - Complete parameter dict for basic requests

## Common Test Patterns

### Test Structured Output

```python
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    field: str

@pytest.mark.unit
@pytest.mark.asyncio
async def test_structured():
    from gpt import gpt_request
    
    params = {
        'model': 'gpt-4o-mini',
        'messages': [...],
        'response_format': MyModel
    }
    
    outputs, cost = await gpt_request(__name__, params)
    assert isinstance(outputs[0], MyModel)
```

### Test Concurrent Requests

```python
@pytest.mark.unit
@pytest.mark.asyncio
async def test_concurrent():
    from gpt import gpt_request
    
    params_list = [
        {'model': 'gpt-4o-mini', 'messages': [...]},
        {'model': 'gpt-4o-mini', 'messages': [...]}
    ]
    
    outputs, cost = await gpt_request(__name__, params_list)
    assert len(outputs) == 2
```

### Test Template Rendering

```python
@pytest.mark.unit
def test_template():
    from gpt import render_template
    
    # Create template file first
    result = render_template('my_template.txt', var='value')
    assert result == 'expected output'
```

## Continuous Integration

For CI/CD pipelines, skip integration tests to avoid API costs:

```bash
# In your CI script
pytest gpt/ -m "not integration" --tb=short
```

## Troubleshooting

### "No module named 'gpt'"
- Ensure you're running pytest from project root
- Check that `gpt/__init__.py` exists

### "OPENAI_API_KEY not set"
- Create `.env` file with `OPENAI_API_KEY=your_key`
- Or set environment variable

### Async tests not running
- Install `pytest-asyncio`: `pip install pytest-asyncio`
- Mark tests with `@pytest.mark.asyncio`
- Check `pytest.ini` has `asyncio_mode = auto`

## Best Practices

1. **Mark tests appropriately** - Use `@pytest.mark.unit` or `@pytest.mark.integration`
2. **Keep unit tests fast** - Mock API calls for pure unit tests if needed
3. **Use descriptive names** - `test_concurrent_requests_with_pydantic_models`
4. **One assertion focus** - Each test should verify one behavior
5. **Use fixtures** - Reuse common setup via `conftest.py`
6. **Clean up resources** - Remove test files in `finally` blocks
