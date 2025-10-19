#!/usr/bin/env python3
"""
Base Agent Module

This module provides the base functionality for all agents in the multi-agent system.
It includes common utilities for environment loading, file operations, and logging.
"""

import argparse
import os
import json
import logging
from pathlib import Path
import sys
import time
from typing import Optional, Dict, Any, List, Union
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from hanx_tools and hanx_apis
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try to import from hanx.hanx_tools first, then fall back to relative imports
try:
    from hanx.hanx_tools.tool_token_tracker import TokenUsage, APIResponse, get_token_tracker
    from hanx.hanx_tools.api_llm import query_llm, create_llm_client, stream_llm_response
    from hanx.hanx_tools.tool_file_utils import read_file, write_file
except ImportError:
    try:
        from tool_token_tracker import TokenUsage, APIResponse, get_token_tracker
        from api_llm import query_llm, create_llm_client, stream_llm_response
        from tool_file_utils import read_file, write_file
    except ImportError:
        print("Error: Could not import required modules. Using dummy implementations.")
        
        class TokenUsage:
            def __init__(self, **kwargs):
                pass
        
        class APIResponse:
            def __init__(self, **kwargs):
                pass
        
        def get_token_tracker():
            return None
        
        def query_llm(*args, **kwargs):
            return "Error: LLM API not available"
        
        def create_llm_client(*args, **kwargs):
            return None
        
        def stream_llm_response(*args, **kwargs):
            yield "Error: LLM API not available"
        
        def read_file(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading file: {e}")
                return ""
        
        def write_file(file_path, content):
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            except Exception as e:
                print(f"Error writing file: {e}")
                return False

# Constants
STATUS_FILE = '.cursorrules'
PLAN_FILE = 'hanx_plan.md'

# Load environment variables
load_dotenv()

class BaseAgent:
    """Base class for all agents in the Hanx system."""
    
    def __init__(self, name="BaseAgent", log_level=logging.INFO):
        """Initialize the agent with a name and logging configuration."""
        self.name = name
        self.setup_logging(log_level)
        self.logger.info(f"Initializing {self.name}")
        
        # Get the project root directory
        self.project_root = self._get_project_root()
        self.logger.debug(f"Project root: {self.project_root}")
        
    def _get_project_root(self):
        """Get the project root directory."""
        # Start with the current file's directory
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        
        # Go up until we find the hanx directory
        while current_dir.name != "hanx" and current_dir.parent != current_dir:
            current_dir = current_dir.parent
            
        # If we found the hanx directory, return its parent
        if current_dir.name == "hanx":
            return current_dir.parent
        
        # If we didn't find it, return the current working directory
        return Path(os.getcwd())
    
    def setup_logging(self, log_level=logging.INFO):
        """Set up logging for the agent."""
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(log_level)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(console_handler)
    
    def run(self, *args, **kwargs):
        """Run the agent. This method should be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement the run method")
    
    def query_llm(self, prompt, model=None, provider=None, temperature=0.7, max_tokens=None):
        """Query an LLM with the given prompt."""
        self.logger.debug(f"Querying LLM with prompt: {prompt[:100]}...")
        return query_llm(prompt, model=model, provider=provider, temperature=temperature, max_tokens=max_tokens)
    
    def stream_llm_response(self, prompt, model=None, provider=None, temperature=0.7, max_tokens=None):
        """Stream a response from an LLM with the given prompt."""
        self.logger.debug(f"Streaming LLM response with prompt: {prompt[:100]}...")
        return stream_llm_response(prompt, model=model, provider=provider, temperature=temperature, max_tokens=max_tokens)
    
    def read_file(self, file_path):
        """Read a file and return its contents."""
        self.logger.debug(f"Reading file: {file_path}")
        return read_file(file_path)
    
    def write_file(self, file_path, content):
        """Write content to a file."""
        self.logger.debug(f"Writing to file: {file_path}")
        return write_file(file_path, content)
    
    def update_plan(self, section, content):
        """Update a section in the plan file."""
        plan_file = os.path.join(self.project_root, "hanx_plan.md")
        self.logger.debug(f"Updating plan section '{section}' in {plan_file}")
        
        try:
            plan_content = self.read_file(plan_file)
            
            # Find the section
            section_marker = f"## {section}"
            section_start = plan_content.find(section_marker)
            
            if section_start == -1:
                self.logger.error(f"Section '{section}' not found in plan file")
                return False
            
            # Find the next section
            next_section_start = plan_content.find("##", section_start + len(section_marker))
            
            if next_section_start == -1:
                # This is the last section, append to the end
                updated_content = plan_content[:section_start + len(section_marker)] + "\n\n" + content
            else:
                # Insert before the next section
                updated_content = plan_content[:section_start + len(section_marker)] + "\n\n" + content + "\n\n" + plan_content[next_section_start:]
            
            # Write the updated content
            self.write_file(plan_file, updated_content)
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating plan: {e}")
            return False
    
    def get_plan_section(self, section):
        """Get a section from the plan file."""
        plan_file = os.path.join(self.project_root, "hanx_plan.md")
        self.logger.debug(f"Getting plan section '{section}' from {plan_file}")
        
        try:
            plan_content = self.read_file(plan_file)
            
            # Find the section
            section_marker = f"## {section}"
            section_start = plan_content.find(section_marker)
            
            if section_start == -1:
                self.logger.error(f"Section '{section}' not found in plan file")
                return None
            
            # Find the next section
            next_section_start = plan_content.find("##", section_start + len(section_marker))
            
            if next_section_start == -1:
                # This is the last section
                return plan_content[section_start + len(section_marker):].strip()
            else:
                # Return content up to the next section
                return plan_content[section_start + len(section_marker):next_section_start].strip()
            
        except Exception as e:
            self.logger.error(f"Error getting plan section: {e}")
            return None
    
    def load_environment(self) -> None:
        """Load environment variables from .env files"""
        from dotenv import load_dotenv
        
        # Look for environment files in the current directory
        env_files = ['.env.local', '.env', '.env.example']
        env_file_found = False
        
        print(f"[{self.name}] Looking for environment files:", env_files)
        for env_file in env_files:
            env_path = os.path.join(os.getcwd(), env_file)
            print(f"[{self.name}] Checking {env_path}")
            if os.path.exists(env_path):
                print(f"[{self.name}] Found {env_file}, loading variables...")
                load_dotenv(env_path)
                env_file_found = True
                print(f"[{self.name}] Loaded environment variables from {env_file}")
                # Print the keys that were loaded (not the values for security)
                keys = [k for k in os.environ.keys() if k.isupper()]
                print(f"[{self.name}] Keys loaded from {env_file}: {keys}")
        
        if not env_file_found:
            print(f"[{self.name}] Warning: No environment file found. Using default environment variables.")
    
    def read_plan_status(self) -> str:
        """Read the current plan status from the plan file"""
        try:
            plan_path = os.path.join(os.getcwd(), PLAN_FILE)
            if os.path.exists(plan_path):
                return self.read_file(plan_path)
            else:
                print(f"[{self.name}] Warning: Plan file {PLAN_FILE} not found.")
                return ""
        except Exception as e:
            print(f"[{self.name}] Error reading plan file: {e}")
            return ""
    
    def log(self, message: str) -> None:
        """Log a message with the agent's name"""
        print(f"[{self.name}] {message}") 