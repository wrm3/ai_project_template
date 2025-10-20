#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
import sys
import time
from token_tracker import TokenUsage, APIResponse, get_token_tracker
from llm_api import query_llm, create_llm_client

STATUS_FILE = 'hanx_plan.md'

def load_environment():
    """Load environment variables from .env files"""
    env_files = ['.env.local', '.env', '.env.example']
    env_loaded = False
    
    for env_file in env_files:
        env_path = Path('.') / env_file
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            env_loaded = True
            break
    
    if not env_loaded:
        print("Warning: No .env files found. Using system environment variables only.", file=sys.stderr)

def read_plan_status():
    """Read the content of the plan status file, only including content after Multi-Agent Scratchpad"""
    status_file = STATUS_FILE
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find the Multi-Agent Scratchpad section
            scratchpad_marker = "# Multi-Agent Scratchpad"
            if scratchpad_marker in content:
                return content[content.index(scratchpad_marker):]
            else:
                print(f"Warning: '{scratchpad_marker}' section not found in {status_file}", file=sys.stderr)
                return ""
    except Exception as e:
        print(f"Error reading {status_file}: {e}", file=sys.stderr)
        return ""

def read_file_content(file_path):
    """Read content from a specified file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return None

def query_llm_with_plan(plan_content, user_prompt=None, file_content=None, provider="openai", model=None):
    """Query the LLM with combined prompts"""
    # Combine prompts
    system_prompt = """"""
    
    combined_prompt = f"""You are working on a multi-agent context. The executor is the one who actually does the work. And you are the planner. Now the executor is asking you for help. Please analyze the provided project plan and status, then address the executor's specific query or request.

You need to think like a founder. Prioritize agility and don't over-engineer. Think deep. Try to foresee challenges and derisk earlier. If opportunity sizing or probing experiments can reduce risk with low cost, instruct the executor to do them.
    
Project Plan and Status:
======
{plan_content}
======
"""

    if file_content:
        combined_prompt += f"\nFile Content:\n======\n{file_content}\n======\n"

    if user_prompt:
        combined_prompt += f"\nUser Query:\n{user_prompt}\n"

    combined_prompt += f"""\nYour response should be focusing on revising the Multi-Agent Scratchpad section in the {STATUS_FILE} file. There is no need to regenerate the entire document. You can use the following format to prompt how to revise the document:

<<<<<<<SEARCH
<text in the original document>
=======
<Proprosed changes>
>>>>>>>

We will do the actual changes in the {STATUS_FILE} file.
"""

    # Use the imported query_llm function
    response = query_llm(combined_prompt, model=model, provider=provider)
    return response

def main():
    parser = argparse.ArgumentParser(description='Query LLM with project plan context')
    parser.add_argument('--prompt', type=str, help='Additional prompt to send to the LLM', required=False)
    parser.add_argument('--prompt-file', type=str, help='Path to a file containing the prompt to send to the LLM', required=False)
    parser.add_argument('--file', type=str, help='Path to a file whose content should be included in the prompt', required=False)
    parser.add_argument('--provider', choices=['openai','anthropic','gemini','local','deepseek','azure'], default='openai', help='The API provider to use')
    parser.add_argument('--model', type=str, help='The model to use (default depends on provider)')
    args = parser.parse_args()

    # Load environment variables
    load_environment()

    # Read plan status
    plan_content = read_plan_status()

    # Read file content if specified
    file_content = None
    if args.file:
        file_content = read_file_content(args.file)
        if file_content is None:
            sys.exit(1)
    
    # Get the prompt from either the command line or a file
    user_prompt = None
    if args.prompt:
        user_prompt = args.prompt
    elif args.prompt_file:
        prompt_content = read_file_content(args.prompt_file)
        if prompt_content is None:
            sys.exit(1)
        user_prompt = prompt_content
    
    if not user_prompt:
        print("Error: Either --prompt or --prompt-file must be provided")
        sys.exit(1)

    # Query LLM and output response
    response = query_llm_with_plan(plan_content, user_prompt, file_content, provider=args.provider, model=args.model)
    if response:
        print(f'Following is the instruction on how to revise the Multi-Agent Scratchpad section in {STATUS_FILE}:')
        print('========================================================')
        print(response)
        print('========================================================')
        print(f'Now please do the actual changes in the {STATUS_FILE} file. And then switch to the executor role, and read the content of the file to decide what to do next.')
    else:
        print("Failed to get response from LLM")
        sys.exit(1)

if __name__ == "__main__":
    main() 