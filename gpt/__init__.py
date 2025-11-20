"""
GPT Utilities Package

This package provides a wrapper around the OpenAI API for use across Django apps.
It handles asynchronous requests, automatic retries, cost tracking, and structured outputs.

Main Functions:
    - gpt_request: Asynchronous GPT request handler with automatic cost tracking
    - render_template: Jinja2 template rendering for prompts

Usage:
    from gpt import gpt_request, render_template
    
    # Make a GPT request
    params = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': 'Hello!'}]
    }
    outputs, cost = await gpt_request(__name__, params)
    
    # Render a prompt template
    prompt = render_template('my_prompt.txt', variable='value')
"""

# Import main functions for easy access
from .gpt_requests import gpt_request
from .render_template import render_template

# Define what gets imported with "from gpt import *"
__all__ = ['gpt_request', 'render_template']
