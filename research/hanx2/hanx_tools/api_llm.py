#!/usr/bin/env python3
"""
LLM API Module

This module provides a unified interface for interacting with various LLM providers.
"""

import os
import sys
import json
import logging
import time
from typing import Dict, List, Optional, Union, Any, Generator
from pathlib import Path
import argparse
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from hanx_tools
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import token tracker
try:
    from hanx.hanx_tools.tool_token_tracker import TokenTracker, get_token_tracker
except ImportError:
    try:
        from tool_token_tracker import TokenTracker, get_token_tracker
    except ImportError:
        print("Error: Could not import TokenTracker. Using dummy implementation.")
        
        class TokenTracker:
            def __init__(self, **kwargs):
                pass
                
            def track_usage(self, **kwargs):
                pass
        
        def get_token_tracker():
            return TokenTracker()

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger("api_llm")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Global variables
token_tracker = get_token_tracker()

def load_environment():
    """Load environment variables from .env files in order of precedence"""
    # Check if we should skip loading from .env files
    if os.environ.get("SKIP_ENV_FILES") == "1":
        print("SKIP_ENV_FILES is set, skipping loading from .env files", file=sys.stderr)
        return
        
    # Order of precedence:
    # 1. System environment variables (already loaded)
    # 2. .env.local (user-specific overrides)
    # 3. .env (project defaults)
    # 4. .env.example (example configuration)
    
    env_files = ['.env.local', '.env', '.env.example']
    env_loaded = False
    
    print("Current working directory:", Path('.').absolute(), file=sys.stderr)
    print("Looking for environment files:", env_files, file=sys.stderr)
    
    for env_file in env_files:
        env_path = Path('.') / env_file
        print(f"Checking {env_path.absolute()}", file=sys.stderr)
        if env_path.exists():
            print(f"Found {env_file}, loading variables...", file=sys.stderr)
            load_dotenv(dotenv_path=env_path)
            env_loaded = True
            print(f"Loaded environment variables from {env_file}", file=sys.stderr)
            # Print loaded keys (but not values for security)
            with open(env_path) as f:
                keys = [line.split('=')[0].strip() for line in f if '=' in line and not line.startswith('#')]
            print(f"Keys loaded from {env_file}: {keys}", file=sys.stderr)
    
    if not env_loaded:
        print("Warning: No .env files found. Using system environment variables only.", file=sys.stderr)
        print("Available system environment variables:", list(os.environ.keys()), file=sys.stderr)

# Load environment variables at module import
load_environment()

def encode_image_file(image_path: str) -> tuple[str, str]:
    """
    Encode an image file to base64 and determine its MIME type.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        tuple: (base64_encoded_string, mime_type)
    """
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = 'image/png'  # Default to PNG if type cannot be determined
        
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
    return encoded_string, mime_type

def create_llm_client(provider="openai"):
    if provider == "openai":
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return OpenAI(
            api_key=api_key
        )
    elif provider == "azure":
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        if not api_key:
            raise ValueError("AZURE_OPENAI_API_KEY not found in environment variables")
        return AzureOpenAI(
            api_key=api_key,
            api_version="2024-08-01-preview",
            azure_endpoint="https://msopenai.openai.azure.com"
        )
    elif provider == "deepseek":
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
        return OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
        )
    elif provider == "anthropic":
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        return Anthropic(
            api_key=api_key
        )
    elif provider == "gemini":
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        return genai
    elif provider == "local":
        return OpenAI(
            base_url="http://192.168.180.137:8006/v1",
            api_key="not-needed"
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def query_llm(prompt: str, client=None, model=None, provider="openai", image_path: Optional[str] = None) -> Optional[str]:
    """
    Query an LLM with a prompt and optional image attachment.
    
    Args:
        prompt (str): The text prompt to send
        client: The LLM client instance
        model (str, optional): The model to use. Special handling for OpenAI's o1 model:
            - Uses different response format
            - Has reasoning_effort parameter
            - Is the only model that provides reasoning_tokens in its response
        provider (str): The API provider to use
        image_path (str, optional): Path to an image file to attach
        
    Returns:
        Optional[str]: The LLM's response or None if there was an error
        
    Note:
        Token tracking behavior varies by provider:
        - OpenAI-style APIs (OpenAI, Azure, DeepSeek, Local): Full token tracking
        - Anthropic: Has its own token tracking system (input/output tokens)
        - Gemini: No token tracking
    """
    if client is None:
        client = create_llm_client(provider)
    
    try:
        # Set default model
        if model is None:
            if provider == "openai":
                model = "gpt-4o"
            elif provider == "azure":
                model = os.getenv('AZURE_OPENAI_MODEL_DEPLOYMENT', 'gpt-4o-ms')  # Get from env with fallback
            elif provider == "deepseek":
                model = "deepseek-chat"
            elif provider == "anthropic":
                model = "claude-3-5-sonnet-20241022"
            elif provider == "gemini":
                model = "gemini-pro"
            elif provider == "local":
                model = "Qwen/Qwen2.5-32B-Instruct-AWQ"
        
        start_time = time.time()
        
        if provider in ["openai", "local", "deepseek", "azure"]:
            messages = [{"role": "user", "content": []}]
            
            # Add text content
            messages[0]["content"].append({
                "type": "text",
                "text": prompt
            })
            
            # Add image content if provided
            if image_path:
                if provider == "openai":
                    encoded_image, mime_type = encode_image_file(image_path)
                    messages[0]["content"] = [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{encoded_image}"}}
                    ]
            
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": 0.7,
            }
            
            # Add o1-specific parameters
            if model == "o1":
                kwargs["response_format"] = {"type": "text"}
                kwargs["reasoning_effort"] = "low"
                del kwargs["temperature"]
            
            response = client.chat.completions.create(**kwargs)
            thinking_time = time.time() - start_time
            
            # Track token usage
            token_usage = TokenTracker(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                reasoning_tokens=response.usage.reasoning_tokens if model.lower().startswith("o") else None  # Only checks if model starts with "o", e.g., o1, o1-preview, o1-mini, o3, etc. Can update this logic to specific models in the future.
            )
            
            # Calculate cost
            cost = get_token_tracker().calculate_openai_cost(
                token_usage.prompt_tokens,
                token_usage.completion_tokens,
                model
            )
            
            # Track the request
            api_response = APIResponse(
                content=response.choices[0].message.content,
                token_usage=token_usage,
                cost=cost,
                thinking_time=thinking_time,
                provider=provider,
                model=model
            )
            get_token_tracker().track_request(api_response)
            
            return response.choices[0].message.content
            
        elif provider == "anthropic":
            messages = [{"role": "user", "content": []}]
            
            # Add text content
            messages[0]["content"].append({
                "type": "text",
                "text": prompt
            })
            
            # Add image content if provided
            if image_path:
                encoded_image, mime_type = encode_image_file(image_path)
                messages[0]["content"].append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": mime_type,
                        "data": encoded_image
                    }
                })
            
            response = client.messages.create(
                model=model,
                max_tokens=1000,
                messages=messages
            )
            thinking_time = time.time() - start_time
            
            # Track token usage
            token_usage = TokenTracker(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens
            )
            
            # Calculate cost
            cost = get_token_tracker().calculate_claude_cost(
                token_usage.prompt_tokens,
                token_usage.completion_tokens,
                model
            )
            
            # Track the request
            api_response = APIResponse(
                content=response.content[0].text,
                token_usage=token_usage,
                cost=cost,
                thinking_time=thinking_time,
                provider=provider,
                model=model
            )
            get_token_tracker().track_request(api_response)
            
            return response.content[0].text
            
        elif provider == "gemini":
            model = client.GenerativeModel(model)
            response = model.generate_content(prompt)
            return response.text
            
    except Exception as e:
        print(f"Error querying LLM: {e}", file=sys.stderr)
        return None

def stream_llm_response(prompt: str, client=None, model=None, provider="openai", image_path: Optional[str] = None) -> Generator[str, None, None]:
    """
    Stream a response from an LLM with a prompt and optional image attachment.
    
    Args:
        prompt (str): The text prompt to send
        client: The LLM client instance
        model (str, optional): The model to use
        provider (str): The API provider to use
        image_path (str, optional): Path to an image file to attach
        
    Yields:
        str: Chunks of the LLM's response as they become available
        
    Note:
        This function streams the response from the LLM, which is useful for
        long-running queries where you want to display partial results as they
        become available.
    """
    try:
        start_time = time.time()
        
        if client is None:
            client = create_llm_client(provider)
            
        if model is None:
            if provider == "openai":
                model = "gpt-4o"
            elif provider == "deepseek":
                model = "deepseek-chat"
            elif provider == "anthropic":
                model = "claude-3-5-sonnet-20241022"
            elif provider == "gemini":
                model = "gemini-2.0-flash-exp"
            elif provider == "azure":
                model = os.getenv('AZURE_OPENAI_MODEL_DEPLOYMENT', 'gpt-4o-ms')
                
        if provider in ["openai", "azure", "deepseek", "local"]:
            messages = [{"role": "user", "content": prompt}]
            
            # Handle image attachment
            if image_path:
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    
                mime_type = mimetypes.guess_type(image_path)[0]
                if not mime_type:
                    mime_type = "image/jpeg"  # Default to JPEG if we can't determine
                    
                messages = [{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:{mime_type};base64,{encoded_image}"
                    }}
                ]}]
            
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
                    
            # Track token usage (approximate since we don't have exact counts in streaming mode)
            # This is a rough estimate based on the length of the prompt and response
            prompt_tokens = len(prompt) // 4  # Rough estimate: 4 chars per token
            completion_tokens = len(full_response) // 4
            total_tokens = prompt_tokens + completion_tokens
            
            thinking_time = time.time() - start_time
            
            # Track token usage
            token_usage = TokenTracker(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens
            )
            
            # Calculate cost (approximate)
            cost = get_token_tracker().calculate_openai_cost(
                token_usage.prompt_tokens,
                token_usage.completion_tokens,
                model
            )
            
            # Track the request
            api_response = APIResponse(
                content=full_response,
                token_usage=token_usage,
                cost=cost,
                thinking_time=thinking_time,
                provider=provider,
                model=model
            )
            get_token_tracker().track_request(api_response)
            
        elif provider == "anthropic":
            with client.messages.stream(
                model=model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            ) as stream:
                full_response = ""
                for text in stream.text_stream:
                    full_response += text
                    yield text
                    
                # Get usage from the final response
                response = stream.get_final_message()
                thinking_time = time.time() - start_time
                
                # Track token usage
                token_usage = TokenTracker(
                    prompt_tokens=response.usage.input_tokens,
                    completion_tokens=response.usage.output_tokens,
                    total_tokens=response.usage.input_tokens + response.usage.output_tokens
                )
                
                # Calculate cost
                cost = get_token_tracker().calculate_claude_cost(
                    token_usage.prompt_tokens,
                    token_usage.completion_tokens,
                    model
                )
                
                # Track the request
                api_response = APIResponse(
                    content=full_response,
                    token_usage=token_usage,
                    cost=cost,
                    thinking_time=thinking_time,
                    provider=provider,
                    model=model
                )
                get_token_tracker().track_request(api_response)
                
        elif provider == "gemini":
            model_instance = client.GenerativeModel(model)
            response = model_instance.generate_content(prompt, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    yield chunk.text
                    
            # No token tracking for Gemini
            
    except Exception as e:
        print(f"Error streaming LLM response: {e}", file=sys.stderr)
        yield f"Error: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='Query an LLM with a prompt')
    parser.add_argument('--prompt', type=str, help='The prompt to send to the LLM', required=True)
    parser.add_argument('--provider', choices=['openai','anthropic','gemini','local','deepseek','azure'], default='openai', help='The API provider to use')
    parser.add_argument('--model', type=str, help='The model to use (default depends on provider)')
    parser.add_argument('--image', type=str, help='Path to an image file to attach to the prompt')
    args = parser.parse_args()

    if not args.model:
        if args.provider == 'openai':
            args.model = "gpt-4o" 
        elif args.provider == "deepseek":
            args.model = "deepseek-chat"
        elif args.provider == 'anthropic':
            args.model = "claude-3-5-sonnet-20241022"
        elif args.provider == 'gemini':
            args.model = "gemini-2.0-flash-exp"
        elif args.provider == 'azure':
            args.model = os.getenv('AZURE_OPENAI_MODEL_DEPLOYMENT', 'gpt-4o-ms')  # Get from env with fallback

    client = create_llm_client(args.provider)
    response = query_llm(args.prompt, client, model=args.model, provider=args.provider, image_path=args.image)
    if response:
        print(response)
    else:
        print("Failed to get response from LLM")

if __name__ == "__main__":
    main()