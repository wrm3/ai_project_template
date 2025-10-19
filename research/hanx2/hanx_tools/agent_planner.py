#!/usr/bin/env python3
"""
Planner Agent

This agent is responsible for high-level planning in the multi-agent system.
It analyzes the current plan status, breaks down tasks, defines success criteria,
and evaluates progress. It uses a high-intelligence model (OpenAI o1 by default)
for planning tasks.

Usage:
    python hanx_agents/agent_planner.py --prompt "Your planning prompt here"
    python hanx_agents/agent_planner.py --prompt "Your planning prompt here" --file path/to/file.txt
    python hanx_agents/agent_planner.py --prompt "Your planning prompt here" --provider anthropic
"""

import argparse
import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Add the parent directory to the path so we can import from hanx_tools
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import base agent
try:
    from hanx.hanx_tools.base_agent import BaseAgent
except ImportError:
    try:
        from base_agent import BaseAgent
    except ImportError:
        print("Error: Could not import BaseAgent. Using dummy implementation.")
        
        class BaseAgent:
            def __init__(self, name="BaseAgent", log_level=logging.INFO):
                self.name = name
                self.logger = logging.getLogger(name)
                
            def read_file(self, file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    print(f"Error reading file: {e}")
                    return ""
                
            def query_llm(self, prompt, provider="openai", model=None, temperature=0.7, max_tokens=None):
                return f"Error: LLM API not available. Prompt: {prompt[:50]}..."

class Planner(BaseAgent):
    """Planner agent for the Hanx system."""
    
    def __init__(self, log_level=logging.INFO):
        """Initialize the Planner agent."""
        super().__init__(name="Planner", log_level=log_level)
        self.logger.info("Planner agent initialized")
    
    def run(self, prompt=None, file=None):
        """Run the Planner agent with the given prompt and optional file."""
        self.logger.info("Running Planner agent")
        
        if not prompt:
            self.logger.error("No prompt provided")
            return "Error: No prompt provided"
        
        # If a file is provided, read its contents and include in the prompt
        file_content = ""
        if file:
            self.logger.info(f"Reading file: {file}")
            file_content = self.read_file(file)
            if not file_content:
                self.logger.error(f"Failed to read file: {file}")
                return f"Error: Failed to read file: {file}"
        
        # Construct the full prompt
        full_prompt = f"""
You are the Planner agent in a multi-agent system. Your task is to analyze the following prompt and provide a detailed plan:

{prompt}

{f'Here is the content of the file you should consider in your analysis: \n\n{file_content}' if file_content else ''}

Please provide a detailed plan that includes:
1. Key challenges and analysis
2. Verifiable success criteria
3. High-level task breakdown
4. Next steps and action items

Your response should be formatted in Markdown and be ready to be inserted into the hanx_plan.md file.
"""
        
        # Query the LLM with the prompt
        self.logger.info("Querying LLM with planning prompt")
        response = self.query_llm(full_prompt, provider="openai", model="gpt-4o")
        
        self.logger.info("Planning complete")
        return response

def main():
    """Main function to run the Planner agent from the command line."""
    parser = argparse.ArgumentParser(description="Run the Planner agent")
    parser.add_argument("--prompt", type=str, help="The prompt to analyze")
    parser.add_argument("--file", type=str, help="Optional file to include in the analysis")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    args = parser.parse_args()
    
    # Set up logging
    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    
    # Create and run the Planner agent
    planner = Planner(log_level=log_level)
    result = planner.run(prompt=args.prompt, file=args.file)
    
    # Print the result
    print(result)

if __name__ == "__main__":
    main() 