"""
Pytest configuration and fixtures for GPT package tests.
"""

import pytest
import os
from unittest.mock import Mock, AsyncMock


@pytest.fixture(scope="session")
def ensure_api_key():
    """Ensure OpenAI API key is available for integration tests."""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set in environment")
    return api_key


@pytest.fixture
def sample_messages():
    """Provide sample messages for testing."""
    return [
        {'role': 'system', 'content': 'You are a helpful assistant. Be concise.'},
        {'role': 'user', 'content': 'Say "Hello from pytest!" and nothing else.'}
    ]


@pytest.fixture
def gpt_params(sample_messages):
    """Provide standard GPT request parameters for integration tests."""
    return {
        'model': 'gpt-4o-mini',
        'messages': sample_messages,
        'temperature': 0,
        'max_tokens': 50
    }


@pytest.fixture
def mock_openai_response():
    """Provide a mock OpenAI API response for unit tests."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Mocked response"
    mock_response.choices[0].message.parsed = None
    mock_response.model = "gpt-4o-mini"
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20
    return mock_response


@pytest.fixture
def mock_openai_client(mocker, mock_openai_response):
    """Mock the OpenAI client for unit tests."""
    # Create async mock
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    
    # Patch the client in gpt_requests module
    mocker.patch('gpt.gpt_requests.client', mock_client)
    
    return mock_client
