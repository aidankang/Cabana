"""
OpenAI API Request Wrapper

Provides asynchronous OpenAI API calls with:
- Automatic retry logic with exponential backoff
- Cost tracking and calculation
- Support for structured outputs via Pydantic models
- Concurrent request processing
- Error handling and logging
"""

import httpx
from openai import AsyncOpenAI, LengthFinishReasonError
from pydantic import BaseModel 
import re
import json
import asyncio
import os
import logging
import traceback
import platform
from dotenv import load_dotenv

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

# Load environment variables
load_dotenv()

# Set event loop policy for Windows
if platform.system == "Windows":    
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load price lookup table
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'price_lut.json')) as f: 
    price_lut = json.load(f)

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = AsyncOpenAI(api_key=OPENAI_API_KEY,
                     http_client=httpx.AsyncClient(
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        ))

def clean_output(output):
    if not isinstance(output, str):
        return output
    output = output.replace("\n\n", "\n")
    # remove \n from the start and end of the string if they exist
    output = re.sub(r'^\n|\n$', '', output)
    # replace '"' at the start and end of the string if they exist
    output = re.sub(r'^"|"$', '', output)
    return output


def print_error(retry_state):
    print("Error: ", traceback.format_exception(None, retry_state.outcome.exception(), retry_state.outcome.exception().__traceback__))


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3), after=print_error, reraise=True)
async def api_call_chat(messages, model="gpt-3.5-turbo-1106", temperature=0, max_tokens=1000, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None, logit_bias=None, index=0, tools=None, tool_choice=None, response_format:BaseModel=None):
    # print(f"requesting {prompt} from {model}")
    # Make the request to the OpenAI API
    # print(f"requesting {messages} from {model}", "messages type: ", type(messages))    
    try: 
        if response_format:
            response = await client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop,
                logit_bias=logit_bias,
                response_format=response_format
            )
        else:   
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop,
                logit_bias=logit_bias,
                tools=tools,
                tool_choice=tool_choice
            )
        
        choices = response.choices
    except Exception as e:
        from pydantic import ValidationError
        from json_repair import repair_json
        
        # Check if this is a ValidationError due to incomplete JSON from stop parameter
        if isinstance(e, ValidationError) and response_format and "Invalid JSON: EOF while parsing" in str(e):
            # The response was cut off by the stop parameter, leaving incomplete JSON
            # Try to repair using json-repair package
            try:
                # Access the raw response content
                raw_content = e.errors()[0]['input'] if e.errors() else None
                
                if raw_content:
                    logging.warning(f"Incomplete JSON detected, attempting to repair. Original: {raw_content[:200]}...")
                    
                    # Use json-repair to fix the incomplete JSON
                    repaired_json_str = repair_json(raw_content)
                    
                    logging.info(f"Repaired JSON: {repaired_json_str}")
                    
                    # Parse the repaired JSON and instantiate the Pydantic model
                    output = response_format.model_validate_json(repaired_json_str)
                    logging.info("Successfully parsed repaired JSON")
                    
                    # Return early with repaired data (cost set to 0 since we don't have usage info)
                    return output, 0, index
                    
            except Exception as repair_error:
                logging.error(f"Failed to repair JSON: {repair_error}")
                # Fall through to original error handling
        
        # Check if this is a LengthFinishReasonError - we can still access partial content
        if isinstance(e, LengthFinishReasonError):
            logging.warning(
                f"LENGTH LIMIT REACHED - Partial response available:\n"
                f"Finish Reason: length\n"
                f"Usage: {e.completion.usage if hasattr(e, 'completion') else 'N/A'}\n"
                f"Partial Content: {e.completion.choices[0].message.content if hasattr(e, 'completion') and e.completion.choices else 'N/A'}"
            )
            # Log the full partial response for inspection
            if hasattr(e, 'completion') and e.completion.choices:
                logging.info(f"Full partial response object: {e.completion}")
                logging.info(f"Partial content:\n{e.completion.choices[0].message.content}")
        
        logging.error(
            f"ERROR:\n"
            f"Type: {type(e)}\n"
            f"Message: {e}\n"
            f"Stack Trace: {traceback.format_exc()}"
        )
        raise
    
    choices[0].message.content = clean_output(choices[0].message.content)

    if tools:
        output = choices[0]
    elif response_format:
        output = choices[0].message.parsed
    else:
        output = choices[0].message.content
    # output = clean_output(output)

    model = response.model
    prompt_tokens= response.usage.prompt_tokens
    completion_tokens= response.usage.completion_tokens

    def cost_lookup(model, prompt_tokens, completion_tokens):
        # get the pricing
        pricing = price_lut[model]
        # get the cost
        prompt_cost = pricing['prompt_price'] * prompt_tokens/1000
        completion_cost = pricing['completion_price'] * completion_tokens/1000
        return prompt_cost + completion_cost

    cost = cost_lookup(model, prompt_tokens, completion_tokens)

    return output, cost, index

# @cache_async()
async def gpt_request(func_name, params_list):
    """
    Asynchronous GPT request handler with automatic cost tracking and concurrent processing.
    
    This function handles OpenAI GPT requests with built-in retry logic, cost calculation,
    and support for both single and multiple concurrent requests. It automatically handles
    structured outputs via Pydantic models and provides comprehensive error handling.
    
    Args:
        func_name (str): Identifier for the calling function (used for logging and debugging).
                        Typically use __name__ from the calling module.
        params_list (dict or list): Single parameter dictionary or list of parameter dictionaries.
                                   Each params dict should contain:
                                   - model (str): OpenAI model name (e.g., 'gpt-4o-mini', 'gpt-4-turbo-preview')
                                   - messages (list): List of message dictionaries with 'role' and 'content'
                                   - temperature (float, optional): Sampling temperature (default: 0)
                                   - max_tokens (int, optional): Maximum tokens to generate (default: 1000)
                                   - response_format (BaseModel, optional): Pydantic model for structured output
                                   - top_p, frequency_penalty, presence_penalty, etc. (optional)
    
    Returns:
        tuple: (outputs, total_cost)
            - outputs (list): List of GPT responses. For structured outputs, contains Pydantic model instances.
                             For regular text, contains strings. Order matches input params_list order.
            - total_cost (float): Total cost in USD for all requests combined.
    
    Raises:
        Exception: Propagates any API errors after retry attempts are exhausted.
    
    Usage Examples:
        
        # 1. Basic single request
        params = {
            'model': 'gpt-4o-mini',
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant'},
                {'role': 'user', 'content': 'Hello!'}
            ],
            'temperature': 0,
            'max_tokens': 256
        }
        outputs, cost = await gpt_request(__name__, params)
        response_text = outputs[0]
        
        # 2. Structured output with Pydantic model
        from pydantic import BaseModel, Field
        
        class ExtractedData(BaseModel):
            items: list = Field(description="List of extracted items")
        
        params = {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'user', 'content': 'Extract items from: apple, banana, orange'}],
            'response_format': ExtractedData
        }
        outputs, cost = await gpt_request(__name__, params)
        structured_result = outputs[0]  # ExtractedData instance
        
        # 3. Multiple concurrent requests
        params_list = [
            {
                'model': 'gpt-4o-mini',
                'messages': [{'role': 'user', 'content': 'Analyze text 1'}],
                'temperature': 0
            },
            {
                'model': 'gpt-4o-mini', 
                'messages': [{'role': 'user', 'content': 'Analyze text 2'}],
                'temperature': 0
            }
        ]
        outputs, total_cost = await gpt_request(__name__, params_list)
        *results = outputs  # Unpack the results directly
    """
    print("gpt_request running")
    if not isinstance(params_list, list):
        params_list = [params_list]
        
    outputs = [""] * len(params_list)
    
    tasks = []
    for i, params in enumerate(params_list):
        tasks.append(api_call_chat(**params, index=i))
    # if 'messages' in params.keys():
    #     prompt_type = 'messages'
    # else:
    #     prompt_type = 'prompt'
    
    # prompts = params[prompt_type]

    # # if isinstance(prompts, list) and not len(prompts) == 1:
    # outputs = [""] * len(prompts)
    # else:
    #     prompts = [prompts]
    #     outputs = [""]

    # tasks = []
    # for i in range(len(outputs)):
    #     if outputs[i] == "":
    #         params[prompt_type] = prompts[i]
    #         if 'messages' in params.keys():
    #             tasks.append(api_call_chat(**params, index=i))
    
    api_outputs = await asyncio.gather(*tasks, return_exceptions=True)
    total_cost = 0
    for api_output in api_outputs:
        # cache.set(f'gpt_{func_name}_{str(params[i])}', await output)
        if not isinstance(api_output, Exception):
            output, cost, index = api_output
            outputs[index] = output
            total_cost += cost
    
    return outputs, total_cost

