#!/usr/bin/env python3
"""
Executor Agent

This agent is responsible for executing specific tasks in the multi-agent system.
It handles implementation details, runs tests, and reports progress back to the Planner.
The Executor updates the plan file with progress reports and assistance requests.

Usage:
    python hanx_agents/agent_executor.py --task "Task description" --update-section "Current Status / Progress Tracking"
    python hanx_agents/agent_executor.py --task "Task description" --update-section "Executor's Feedback or Assistance Requests"
"""

import argparse
import os
import sys
import re
from typing import Optional, Dict, Any, List
import logging
from pathlib import Path

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
                
            def update_plan(self, section, content):
                print(f"Updating plan section '{section}' with content: {content[:50]}...")
                return True

class Executor(BaseAgent):
    """Executor agent for the Hanx system."""
    
    def __init__(self, log_level=logging.INFO):
        """Initialize the Executor agent."""
        super().__init__(name="Executor", log_level=log_level)
        self.logger.info("Executor agent initialized")
    
    def run(self, task=None, update_section=None, content=None):
        """Run the Executor agent to update a section in the plan file."""
        self.logger.info("Running Executor agent")
        
        if not task:
            self.logger.error("No task provided")
            return "Error: No task provided"
        
        if not update_section:
            self.logger.error("No update section provided")
            return "Error: No update section provided"
        
        if not content:
            self.logger.error("No content provided")
            return "Error: No content provided"
        
        # Get the current content of the section
        current_content = self.get_plan_section(update_section)
        if current_content is None:
            self.logger.error(f"Section '{update_section}' not found in plan file")
            return f"Error: Section '{update_section}' not found in plan file"
        
        # Prepare the updated content
        timestamp = self.get_timestamp()
        updated_content = f"{current_content}\n\n### {timestamp}: {task}\n{content}"
        
        # Update the section in the plan file
        success = self.update_plan(update_section, updated_content)
        if not success:
            self.logger.error("Failed to update plan file")
            return "Error: Failed to update plan file"
        
        self.logger.info(f"Successfully updated section '{update_section}' in plan file")
        return f"Successfully updated section '{update_section}' in plan file"
    
    def get_timestamp(self):
        """Get the current timestamp in a readable format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """Main function to run the Executor agent from the command line."""
    parser = argparse.ArgumentParser(description="Run the Executor agent")
    parser.add_argument("--task", type=str, required=True, help="The task being executed")
    parser.add_argument("--update-section", type=str, required=True, help="The section in the plan file to update")
    parser.add_argument("--content", type=str, required=True, help="The content to add to the section")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    args = parser.parse_args()
    
    # Set up logging
    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    
    # Create and run the Executor agent
    executor = Executor(log_level=log_level)
    result = executor.run(task=args.task, update_section=args.update_section, content=args.content)
    
    # Print the result
    print(result)

if __name__ == "__main__":
    main() 