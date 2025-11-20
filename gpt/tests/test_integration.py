"""
Integration tests for GPT package (makes real API calls).

These tests verify end-to-end functionality with the actual OpenAI API.
They cost money and require OPENAI_API_KEY to be set.

Run with: pytest gpt/tests/test_integration.py
Skip with: pytest -m "not integration"
"""

import pytest
from pydantic import BaseModel, Field


@pytest.mark.integration
@pytest.mark.asyncio
async def test_simple_api_request(ensure_api_key, gpt_params):
    """Test a simple GPT request with real API."""
    from gpt import gpt_request
    
    outputs, cost = await gpt_request(__name__, gpt_params)
    
    assert len(outputs) == 1
    assert isinstance(outputs[0], str)
    assert len(outputs[0]) > 0
    assert cost > 0
    assert "Hello from pytest!" in outputs[0]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_structured_output_api(ensure_api_key):
    """Test structured output with Pydantic model and real API."""
    from gpt import gpt_request
    
    class CityInfo(BaseModel):
        city: str = Field(description="City name")
        country: str = Field(description="Country name")
        population_millions: float = Field(description="Population in millions")
    
    params = {
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'user', 'content': 'Provide information about Tokyo, Japan'}
        ],
        'response_format': CityInfo,
        'temperature': 0,
        'max_tokens': 100
    }
    
    outputs, cost = await gpt_request(__name__, params)
    
    assert len(outputs) == 1
    assert isinstance(outputs[0], CityInfo)
    assert outputs[0].city == "Tokyo"
    assert outputs[0].country == "Japan"
    assert outputs[0].population_millions > 0
    assert cost > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_concurrent_api_requests(ensure_api_key):
    """Test multiple concurrent requests with real API."""
    from gpt import gpt_request
    
    params_list = [
        {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'user', 'content': 'What is 3+3? Answer with just the number.'}],
            'temperature': 0,
            'max_tokens': 10
        },
        {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'user', 'content': 'What is 7+7? Answer with just the number.'}],
            'temperature': 0,
            'max_tokens': 10
        }
    ]
    
    outputs, total_cost = await gpt_request(__name__, params_list)
    
    assert len(outputs) == 2
    assert all(isinstance(output, str) for output in outputs)
    assert total_cost > 0
    # Check that we got numeric answers
    assert any(char.isdigit() for char in outputs[0])
    assert any(char.isdigit() for char in outputs[1])


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_world_scenario(ensure_api_key):
    """Test a realistic use case - extracting information from text."""
    from gpt import gpt_request
    
    class ExtractedInfo(BaseModel):
        person_name: str = Field(description="Name of the person")
        location: str = Field(description="Location mentioned")
        activity: str = Field(description="Activity being done")
    
    params = {
        'model': 'gpt-4o-mini',
        'messages': [
            {
                'role': 'user', 
                'content': 'Extract information from: "John visited Paris and went sightseeing."'
            }
        ],
        'response_format': ExtractedInfo,
        'temperature': 0,
        'max_tokens': 100
    }
    
    outputs, cost = await gpt_request(__name__, params)
    result = outputs[0]
    
    assert isinstance(result, ExtractedInfo)
    assert result.person_name == "John"
    assert result.location == "Paris"
    assert "sightseeing" in result.activity.lower()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cost_tracking(ensure_api_key, gpt_params):
    """Verify that cost tracking works correctly."""
    from gpt import gpt_request
    
    outputs, cost = await gpt_request(__name__, gpt_params)
    
    assert isinstance(cost, (int, float))
    assert cost > 0
    # Typical cost for a small request should be less than $0.01
    assert cost < 0.01


@pytest.mark.integration
@pytest.mark.asyncio
async def test_temperature_variation(ensure_api_key):
    """Test that temperature parameter affects responses."""
    from gpt import gpt_request
    
    # Low temperature (more deterministic)
    params_low = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': 'Say "consistent" and nothing else.'}],
        'temperature': 0,
        'max_tokens': 10
    }
    
    # Make same request twice
    outputs1, _ = await gpt_request(__name__, params_low)
    outputs2, _ = await gpt_request(__name__, params_low)
    
    # With temperature=0, responses should be identical
    assert outputs1[0] == outputs2[0]
