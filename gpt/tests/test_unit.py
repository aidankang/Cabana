"""
Unit tests for GPT package (no API calls - uses mocks).

These tests are fast and free - they test internal logic without calling OpenAI.
Run with: pytest gpt/tests/test_unit.py
"""

import pytest
from unittest.mock import Mock, AsyncMock
from pydantic import BaseModel, Field


@pytest.mark.unit
def test_package_imports():
    """Test that package imports work correctly."""
    from gpt import gpt_request, render_template
    
    assert callable(gpt_request)
    assert callable(render_template)


@pytest.mark.unit
def test_clean_output():
    """Test the clean_output function."""
    from gpt.gpt_requests import clean_output
    
    # Test removing double newlines
    assert clean_output("hello\n\nworld") == "hello\nworld"
    
    # Test removing leading/trailing newlines
    assert clean_output("\nhello\n") == "hello"
    
    # Test removing leading/trailing quotes
    assert clean_output('"hello"') == "hello"
    
    # Test non-string input
    assert clean_output(123) == 123


@pytest.mark.unit
def test_cost_calculation():
    """Test cost calculation logic without API call."""
    from gpt.gpt_requests import price_lut
    
    # Test that price_lut is loaded
    assert isinstance(price_lut, dict)
    assert len(price_lut) > 0
    
    # Test cost calculation for a known model
    model = "gpt-4o-mini"
    if model in price_lut:
        pricing = price_lut[model]
        assert 'prompt_price' in pricing
        assert 'completion_price' in pricing
        
        # Calculate cost for 100 prompt tokens, 50 completion tokens
        prompt_cost = pricing['prompt_price'] * 100 / 1000
        completion_cost = pricing['completion_price'] * 50 / 1000
        total_cost = prompt_cost + completion_cost
        
        assert total_cost > 0
        assert isinstance(total_cost, float)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_gpt_request_with_mock(mock_openai_client, mock_openai_response):
    """Test gpt_request with mocked OpenAI client (no real API call)."""
    from gpt import gpt_request
    
    params = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': 'Test'}],
        'temperature': 0,
        'max_tokens': 50
    }
    
    outputs, cost = await gpt_request(__name__, params)
    
    # Verify mock was called (at least once, retries may happen)
    assert mock_openai_client.chat.completions.create.called
    
    # Verify output
    assert len(outputs) == 1
    assert outputs[0] == "Mocked response"
    assert cost > 0


@pytest.mark.unit
@pytest.mark.asyncio
async def test_concurrent_requests_with_mock(mock_openai_client):
    """Test concurrent requests with mocked API."""
    from gpt import gpt_request
    
    params_list = [
        {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'user', 'content': 'Test 1'}],
            'temperature': 0,
            'max_tokens': 10
        },
        {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'user', 'content': 'Test 2'}],
            'temperature': 0,
            'max_tokens': 10
        }
    ]
    
    outputs, total_cost = await gpt_request(__name__, params_list)
    
    # Verify requests were made (at least 2, retries may happen)
    assert mock_openai_client.chat.completions.create.call_count >= 2
    
    # Verify outputs
    assert len(outputs) == 2
    assert all(isinstance(output, str) for output in outputs)
    assert total_cost > 0


@pytest.mark.unit
def test_template_rendering():
    """Test Jinja2 template rendering (no API involved)."""
    from gpt import render_template
    import os
    
    # Create test template
    template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'prompts')
    os.makedirs(template_dir, exist_ok=True)
    
    test_template_path = os.path.join(template_dir, 'test_unit.txt')
    with open(test_template_path, 'w') as f:
        f.write('Hello {{ name }}!')
    
    try:
        result = render_template('test_unit.txt', name='World')
        assert result == 'Hello World!'
    finally:
        if os.path.exists(test_template_path):
            os.remove(test_template_path)


@pytest.mark.unit
def test_template_rendering_with_dict():
    """Test template rendering with complex data structures."""
    from gpt import render_template
    import os
    
    template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'prompts')
    os.makedirs(template_dir, exist_ok=True)
    
    test_template_path = os.path.join(template_dir, 'test_unit_dict.txt')
    with open(test_template_path, 'w') as f:
        f.write('{{ user.name }} is {{ user.age }} years old.')
    
    try:
        result = render_template('test_unit_dict.txt', user={'name': 'Alice', 'age': 30})
        assert result == 'Alice is 30 years old.'
    finally:
        if os.path.exists(test_template_path):
            os.remove(test_template_path)


@pytest.mark.unit
def test_template_rendering_with_list():
    """Test template rendering with list iteration."""
    from gpt import render_template
    import os
    
    template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'prompts')
    os.makedirs(template_dir, exist_ok=True)
    
    test_template_path = os.path.join(template_dir, 'test_unit_list.txt')
    with open(test_template_path, 'w') as f:
        f.write('{% for item in items %}{{ item }}, {% endfor %}')
    
    try:
        result = render_template('test_unit_list.txt', items=['a', 'b', 'c'])
        assert result == 'a, b, c, '
    finally:
        if os.path.exists(test_template_path):
            os.remove(test_template_path)


@pytest.mark.unit
def test_replace_in_value():
    """Test the replace_in_value helper function."""
    from gpt.render_template import replace_in_value
    
    # Test string
    assert replace_in_value('hello "world"') == 'hello world'
    
    # Test dict
    result = replace_in_value({'key': 'value "test"'})
    assert result == {'key': 'value test'}
    
    # Test list
    result = replace_in_value(['a "b"', 'c "d"'])
    assert result == ['a b', 'c d']
    
    # Test nested
    result = replace_in_value({'list': ['a "b"'], 'str': 'x "y"'})
    assert result == {'list': ['a b'], 'str': 'x y'}
    
    # Test non-string
    assert replace_in_value(123) == 123
    assert replace_in_value(None) is None
