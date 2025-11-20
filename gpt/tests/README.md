"""
GPT Package Tests

This directory contains all tests for the GPT utility package.

## Structure

```
tests/
├── conftest.py           # Pytest fixtures and configuration
├── test_unit.py          # Unit tests (fast, no API calls, uses mocks)
└── test_integration.py   # Integration tests (real API calls, costs money)
```

## Test Types

### Unit Tests (`test_unit.py`)

**What:** Tests internal logic without calling external APIs  
**How:** Uses mocks to simulate OpenAI responses  
**Speed:** Fast (~1 second)  
**Cost:** Free  
**When:** Run frequently during development

```bash
pytest gpt/tests/test_unit.py -v
```

### Integration Tests (`test_integration.py`)

**What:** Tests end-to-end functionality with real OpenAI API  
**How:** Makes actual API calls  
**Speed:** Slower (~15-20 seconds)  
**Cost:** ~$0.0001 per test run  
**When:** Run before committing or deploying

```bash
pytest gpt/tests/test_integration.py -v
```

## Quick Commands

```bash
# Run all tests
pytest gpt/tests/

# Run only unit tests (fast, free)
pytest gpt/tests/test_unit.py

# Run only integration tests
pytest gpt/tests/test_integration.py

# Skip integration tests by marker
pytest gpt/tests/ -m "not integration"

# Verbose output
pytest gpt/tests/ -v

# With coverage
pytest --cov=gpt gpt/tests/
```

## Test Coverage

### Unit Tests (11 tests)

- ✅ Package imports
- ✅ Output cleaning logic
- ✅ Cost calculation
- ✅ Mocked API requests (single)
- ✅ Mocked concurrent requests
- ✅ Template rendering (basic)
- ✅ Template rendering (dict)
- ✅ Template rendering (list)
- ✅ Value replacement helper

### Integration Tests (6 tests)

- ✅ Simple API request
- ✅ Structured output (Pydantic)
- ✅ Concurrent API requests
- ✅ Real-world extraction scenario
- ✅ Cost tracking
- ✅ Temperature parameter

## Fixtures

See `conftest.py` for available fixtures:

- `ensure_api_key` - Ensures API key exists (integration tests)
- `sample_messages` - Standard test messages
- `gpt_params` - Complete request parameters
- `mock_openai_response` - Mocked API response (unit tests)
- `mock_openai_client` - Mocked OpenAI client (unit tests)

## Best Practices

1. **During Development:** Run unit tests frequently

   ```bash
   pytest gpt/tests/test_unit.py
   ```

2. **Before Commit:** Run all tests

   ```bash
   pytest gpt/tests/
   ```

3. **In CI/CD:** Skip integration tests to avoid API costs

   ```bash
   pytest gpt/tests/ -m "not integration"
   ```

4. **Adding New Tests:**
   - Unit test → `test_unit.py` (use mocks)
   - Integration test → `test_integration.py` (mark with `@pytest.mark.integration`)
