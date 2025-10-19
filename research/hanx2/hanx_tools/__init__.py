"""
Hanx Tools Package

This package provides a collection of tools for the Hanx system, including:
- Agents for planning and execution
- Tools for file operations, web scraping, and more
- APIs for interacting with external services
"""

import os
import sys
from pathlib import Path

# Define the modules that should be exposed
__all__ = [
    # Agents
    'agent_planner',
    'agent_executor',
    'agent_computer_use',
    'agent_knowledge_base',
    'agent_plan_exec_llm',
    'agent_rag_librarian',
    'agent_youtube_researcher',
    'base_agent',
    
    # APIs
    'api_llm',
    'api_perplexity',
    'api_trello',
    'api_jira',
    'api_confluence',
    'api_bitbucket',
    
    # Tools
    'tool_file_utils',
    'tool_path_utils',
    'tool_system_info',
    'tool_web_scraper',
    'tool_search_engine',
    'tool_youtube',
    'tool_mysql',
    'tool_oracle_db',
    'tool_rag_utils',
    'tool_rag_ingest',
    'tool_document_processors',
    'tool_file_processors',
    'tool_screenshot_utils',
    'tool_token_tracker',
    'tool_llm_wrapper',
    'tool_fix_imports',
    
    # OpenManus
    'openmanus',
]

# Add the parent directory to the path so we can import from hanx
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the modules for convenience
for module_name in __all__:
    try:
        if module_name != 'openmanus':  # Skip openmanus as it's a package
            module_path = Path(__file__).parent / f"{module_name}.py"
            if module_path.exists():
                # Use relative imports
                exec(f"from . import {module_name}")
    except Exception as e:
        print(f"Error importing {module_name}: {e}")
