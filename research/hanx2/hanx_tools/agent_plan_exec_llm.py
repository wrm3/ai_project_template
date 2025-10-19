#!/usr/bin/env python3
"""
Plan Executor LLM Agent

This agent is used by the Planner in the multi-agent system to generate plans and revisions
to the hanx_plan.md file. It uses a high-intelligence model (OpenAI o1 by default) to analyze
the current plan status and generate recommendations for next steps.

Usage:
    python hanx_agents/agent_plan_exec_llm.py --prompt "Your planning prompt here"
    python hanx_agents/agent_plan_exec_llm.py --prompt "Your planning prompt here" --file path/to/file.txt
    python hanx_agents/agent_plan_exec_llm.py --prompt "Your planning prompt here" --provider anthropic

The agent will read the current plan status from the .cursorrules file, analyze it along with
any additional context provided, and generate recommendations for updating the plan.
"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
import sys
import time
import logging

# Add the parent directory to the path so we can import from hanx_tools and hanx_apis
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import token tracker with fallback
try:
    from hanx.hanx_tools.tool_token_tracker import TokenUsage, APIResponse, get_token_tracker
except ImportError:
    try:
        from tool_token_tracker import TokenUsage, APIResponse, get_token_tracker
    except ImportError:
        print("Error: Could not import token tracker. Using dummy implementation.")
        
        class TokenUsage:
            def __init__(self, prompt_tokens=0, completion_tokens=0, total_tokens=0, reasoning_tokens=None):
                self.prompt_tokens = prompt_tokens
                self.completion_tokens = completion_tokens
                self.total_tokens = total_tokens
                self.reasoning_tokens = reasoning_tokens
                
        class APIResponse:
            def __init__(self, content="", token_usage=None, cost=0.0, thinking_time=0.0, provider="", model=""):
                self.content = content
                self.token_usage = token_usage or TokenUsage()
                self.cost = cost
                self.thinking_time = thinking_time
                self.provider = provider
                self.model = model
                
        def get_token_tracker():
            return None

# Import LLM API with fallback
try:
    from hanx.hanx_apis.api_llm import query_llm, create_llm_client
except ImportError:
    try:
        from hanx_tools.api_llm import query_llm, create_llm_client
    except ImportError:
        try:
            from api_llm import query_llm, create_llm_client
        except ImportError:
            def query_llm(prompt, provider="openai", model=None, temperature=0.7, max_tokens=None):
                print(f"Error: Could not import LLM API. Using dummy implementation.")
                return "Dummy LLM response"
                
            def create_llm_client(provider="openai"):
                return None

# Constants
STATUS_FILE = '.cursorrules'
PLAN_FILE = 'hanx_plan.md'

def load_environment():
    """Load environment variables from .env files"""
    # Look for environment files in the current directory
    env_files = ['.env.local', '.env', '.env.example']
    env_file_found = False
    
    print("Looking for environment files:", env_files)
    for env_file in env_files:
        env_path = os.path.join(os.getcwd(), env_file)
        print(f"Checking {env_path}")
        if os.path.exists(env_path):
            print(f"Found {env_file}, loading variables...")
            load_dotenv(env_path)
            env_file_found = True
            print(f"Loaded environment variables from {env_file}")
            # Print the keys that were loaded (not the values for security)
            keys = [k for k in os.environ.keys() if k.isupper()]
            print(f"Keys loaded from {env_file}: {keys}")
    
    if not env_file_found:
        print("Warning: No environment file found. Using default environment variables.")

def read_plan_status():
    """Read the current plan status from the plan file"""
    try:
        plan_path = os.path.join(os.getcwd(), PLAN_FILE)
        if os.path.exists(plan_path):
            with open(plan_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            print(f"Warning: Plan file {PLAN_FILE} not found.")
            return ""
    except Exception as e:
        print(f"Error reading plan file: {e}")
        return ""

def read_file_content(file_path):
    """Read content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def query_llm_with_plan(plan_content, user_prompt=None, file_content=None, provider="openai", model=None):
    """Query the LLM with the plan content and user prompt"""
    # Prepare the prompt
    prompt = f"""You are an AI planning assistant. Your task is to analyze the current plan and provide recommendations for next steps.

Current Plan:
{plan_content}

"""
    
    if file_content:
        prompt += f"""
Additional Context (file content):
{file_content}

"""
    
    if user_prompt:
        prompt += f"""
User Request:
{user_prompt}

"""
    
    prompt += """
Please provide a detailed analysis and recommendations for updating the plan. Focus on:
1. What has been accomplished so far
2. What are the next logical steps
3. Any potential issues or challenges to address
4. Specific tasks that should be added to the plan

Your response should be clear, actionable, and help move the project forward.
"""
    
    # Query the LLM
    try:
        response = query_llm(prompt, provider=provider, model=model)
        return response
    except Exception as e:
        print(f"Error querying LLM: {e}")
        return f"Error: {str(e)}"

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Plan Executor LLM Agent")
    parser.add_argument("--prompt", help="User prompt for the LLM")
    parser.add_argument("--file", help="Path to a file to include in the context")
    parser.add_argument("--provider", default="openai", choices=["openai", "anthropic", "gemini", "deepseek", "local"], 
                        help="LLM provider to use")
    parser.add_argument("--model", help="Specific model to use (provider-dependent)")
    
    args = parser.parse_args()
    
    # Load environment variables
    load_environment()
    
    # Read the current plan status
    plan_content = read_plan_status()
    
    # Read file content if provided
    file_content = None
    if args.file:
        file_content = read_file_content(args.file)
    
    # Query the LLM
    response = query_llm_with_plan(
        plan_content=plan_content,
        user_prompt=args.prompt,
        file_content=file_content,
        provider=args.provider,
        model=args.model
    )
    
    # Print the response
    print("\n=== LLM Response ===\n")
    print(response)
    print("\n===================\n")

if __name__ == "__main__":
    main() 