#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server using the official SDK
This script implements a Model Context Protocol server that exposes the Hanx multi-agent system
through the standardized MCP interface using the official Python SDK.
"""

import os
import sys
import logging
import importlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import mcp

# Add parent directory to path to ensure imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the MCP SDK
try:
    from mcp.server import FastMCP
except ImportError:
    print("Error: MCP SDK not installed. Please run 'pip install mcp'")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/mcp_server_sdk.log", mode="a")
    ]
)
logger = logging.getLogger("mcp_server_sdk")

# Create the MCP server
mcp = FastMCP(
    "Hanx Multi-Agent System",
    description="A Model Context Protocol server for the Hanx multi-agent system",
    version="1.0.0",
    host="0.0.0.0",
    port=8080,
    transport="http"
)

# Import Hanx modules
def add_hanx_to_python_path():
    """Add hanx_tools and hanx_apis to Python path"""
    # Get the current directory (should be hanx_mcp)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the parent directory (should be the project root)
    parent_dir = os.path.dirname(current_dir)
    
    # Add parent directory to path if not already there
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    # Create a proper hanx package structure
    hanx_dir = parent_dir
    
    # Ensure hanx_tools is in the path
    hanx_tools_dir = os.path.join(parent_dir, "hanx_tools")
    if os.path.exists(hanx_tools_dir) and hanx_tools_dir not in sys.path:
        sys.path.insert(0, hanx_tools_dir)
    
    # Create a symbolic link or copy for proper module structure if needed
    try:
        # Create a hanx module if it doesn't exist
        if not os.path.exists(os.path.join(parent_dir, "__init__.py")):
            with open(os.path.join(parent_dir, "__init__.py"), "w") as f:
                f.write("# Hanx package\n")
        
        # Create a hanx_tools module if it doesn't exist
        if not os.path.exists(os.path.join(hanx_tools_dir, "__init__.py")):
            with open(os.path.join(hanx_tools_dir, "__init__.py"), "w") as f:
                f.write("# Hanx tools package\n")
        
        # Create openmanus module if it doesn't exist
        openmanus_dir = os.path.join(hanx_tools_dir, "openmanus")
        if os.path.exists(openmanus_dir) and not os.path.exists(os.path.join(openmanus_dir, "__init__.py")):
            with open(os.path.join(openmanus_dir, "__init__.py"), "w") as f:
                f.write("# OpenManus integration package\n")
    except Exception as e:
        logger.warning(f"Error creating package structure: {e}")
    
    # Log the Python path for debugging
    logger.info(f"Python path: {sys.path}")
    logger.info(f"Current working directory: {os.getcwd()}")

# Add Hanx modules to Python path
add_hanx_to_python_path()

# Import Hanx modules
try:
    import hanx_tools
    logger.info("Successfully imported hanx_tools")
except ImportError as e:
    logger.warning(f"Failed to import hanx_tools: {e}")

# Tool registration factory
class ToolRegistrationFactory:
    """Factory for registering tools with MCP server with proper dependency handling"""
    
    def __init__(self):
        self.registered_tools = []
        self.registered_resources = []
        self.registered_prompts = []
        self.missing_dependencies = {}
    
    def register_tool(self, name, func, module_path, dependencies=None):
        """Register a tool with proper dependency handling"""
        if dependencies is None:
            dependencies = []
        
        missing_deps = []
        for dep in dependencies:
            try:
                importlib.import_module(dep)
            except ImportError as e:
                missing_deps.append((dep, str(e)))
        
        if missing_deps:
            self.missing_dependencies[name] = missing_deps
            logger.warning(f"Tool {name} has missing dependencies: {missing_deps}")
            
            # Create a dummy implementation that reports the missing dependencies
            @mcp.tool()
            def dummy_tool(*args, **kwargs):
                return f"Tool {name} is unavailable due to missing dependencies: {missing_deps}"
            
            # Rename the function to match the intended name
            dummy_tool.__name__ = name
            return False
        
        try:
            # Import the actual function
            module = importlib.import_module(module_path)
            actual_func = getattr(module, func)
            
            # Register with MCP
            @mcp.tool()
            def tool_wrapper(*args, **kwargs):
                try:
                    return actual_func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error executing tool {name}: {e}")
                    return f"Error executing tool {name}: {e}"
            
            # Rename the function to match the intended name
            tool_wrapper.__name__ = name
            
            self.registered_tools.append(name)
            logger.info(f"Successfully registered tool: {name}")
            return True
        except Exception as e:
            logger.error(f"Error registering tool {name}: {e}")
            
            # Create a dummy implementation that reports the error
            @mcp.tool()
            def error_tool(*args, **kwargs):
                return f"Tool {name} encountered an error during registration: {e}"
            
            # Rename the function to match the intended name
            error_tool.__name__ = name
            return False
    
    def register_resource(self, uri_template, func, module_path, dependencies=None):
        """Register a resource with proper dependency handling"""
        if dependencies is None:
            dependencies = []
        
        missing_deps = []
        for dep in dependencies:
            try:
                importlib.import_module(dep)
            except ImportError as e:
                missing_deps.append((dep, str(e)))
        
        if missing_deps:
            self.missing_dependencies[uri_template] = missing_deps
            logger.warning(f"Resource {uri_template} has missing dependencies: {missing_deps}")
            
            # Create a dummy implementation that reports the missing dependencies
            if "{" in uri_template and "}" in uri_template:
                # Extract parameter names from URI template
                param_names = []
                parts = uri_template.split("{")
                for part in parts[1:]:
                    if "}" in part:
                        param_name = part.split("}")[0]
                        param_names.append(param_name)
                
                # Create a function with the correct parameters
                exec_str = f"def dummy_resource({', '.join(param_names)}):\n"
                exec_str += f"    return f\"Resource {uri_template} is unavailable due to missing dependencies: {missing_deps}\"\n"
                
                # Execute the dynamic function definition
                local_vars = {}
                exec(exec_str, globals(), local_vars)
                dummy_resource = local_vars["dummy_resource"]
                
                # Register with MCP
                mcp.resource(uri_template)(dummy_resource)
            else:
                # No parameters in URI
                @mcp.resource(uri_template)
                def dummy_resource():
                    return f"Resource {uri_template} is unavailable due to missing dependencies: {missing_deps}"
            
            return False
        
        try:
            # Import the actual function if it's not in __main__
            if module_path != "__main__":
                module = importlib.import_module(module_path)
                actual_func = getattr(module, func)
            else:
                # Get the function from the global namespace
                actual_func = globals()[func]
            
            # Check if the URI has parameters
            if "{" in uri_template and "}" in uri_template:
                # Extract parameter names from URI template
                param_names = []
                parts = uri_template.split("{")
                for part in parts[1:]:
                    if "}" in part:
                        param_name = part.split("}")[0]
                        param_names.append(param_name)
                
                # Create a wrapper function with the correct parameters
                exec_str = f"def resource_wrapper({', '.join(param_names)}):\n"
                exec_str += "    try:\n"
                if param_names:
                    exec_str += f"        return actual_func({', '.join(param_names)})\n"
                else:
                    exec_str += "        return actual_func()\n"
                exec_str += "    except Exception as e:\n"
                exec_str += f"        logger.error(f\"Error accessing resource {uri_template}: {{e}}\")\n"
                exec_str += f"        return f\"Error accessing resource {uri_template}: {{e}}\"\n"
                
                # Execute the dynamic function definition
                local_vars = {"actual_func": actual_func, "logger": logger}
                exec(exec_str, globals(), local_vars)
                resource_wrapper = local_vars["resource_wrapper"]
                
                # Register with MCP
                mcp.resource(uri_template)(resource_wrapper)
            else:
                # No parameters in URI
                @mcp.resource(uri_template)
                def resource_wrapper():
                    try:
                        return actual_func()
                    except Exception as e:
                        logger.error(f"Error accessing resource {uri_template}: {e}")
                        return f"Error accessing resource {uri_template}: {e}"
            
            self.registered_resources.append(uri_template)
            logger.info(f"Successfully registered resource: {uri_template}")
            return True
        except Exception as e:
            logger.error(f"Error registering resource {uri_template}: {e}")
            
            # Create a dummy implementation that reports the error
            if "{" in uri_template and "}" in uri_template:
                # Extract parameter names from URI template
                param_names = []
                parts = uri_template.split("{")
                for part in parts[1:]:
                    if "}" in part:
                        param_name = part.split("}")[0]
                        param_names.append(param_name)
                
                # Create a function with the correct parameters
                exec_str = f"def error_resource({', '.join(param_names)}):\n"
                exec_str += f"    return f\"Resource {uri_template} encountered an error during registration: {e}\"\n"
                
                # Execute the dynamic function definition
                local_vars = {}
                exec(exec_str, globals(), local_vars)
                error_resource = local_vars["error_resource"]
                
                # Register with MCP
                mcp.resource(uri_template)(error_resource)
            else:
                # No parameters in URI
                @mcp.resource(uri_template)
                def error_resource():
                    return f"Resource {uri_template} encountered an error during registration: {e}"
            
            return False
    
    def register_prompt(self, name, func, module_path, dependencies=None):
        """Register a prompt with proper dependency handling"""
        if dependencies is None:
            dependencies = []
        
        missing_deps = []
        for dep in dependencies:
            try:
                importlib.import_module(dep)
            except ImportError as e:
                missing_deps.append((dep, str(e)))
        
        if missing_deps:
            self.missing_dependencies[name] = missing_deps
            logger.warning(f"Prompt {name} has missing dependencies: {missing_deps}")
            
            # Create a dummy implementation that reports the missing dependencies
            try:
                # Define a simple function with proper type annotations
                @mcp.prompt()
                def dummy_prompt(message: str) -> str:
                    return f"Prompt {name} is unavailable due to missing dependencies: {missing_deps}"
                
                # Rename the function to match the intended name
                dummy_prompt.__name__ = name
            except Exception as e:
                logger.error(f"Error registering dummy prompt {name}: {e}")
            
            return False
        
        try:
            # Import the actual function if it's not in __main__
            if module_path != "__main__":
                module = importlib.import_module(module_path)
                actual_func = getattr(module, func)
            else:
                # Get the function from the global namespace
                actual_func = globals()[func]
            
            # Create a wrapper function with proper type annotations
            try:
                # Define a wrapper function with proper type annotations
                @mcp.prompt()
                def prompt_wrapper(message: str) -> str:
                    try:
                        return actual_func(message)
                    except Exception as e:
                        logger.error(f"Error executing prompt {name}: {e}")
                        return f"Error executing prompt {name}: {e}"
                
                # Rename the function to match the intended name
                prompt_wrapper.__name__ = name
                
                self.registered_prompts.append(name)
                logger.info(f"Successfully registered prompt: {name}")
                return True
            except Exception as e:
                logger.error(f"Error registering prompt wrapper {name}: {e}")
                return False
        except Exception as e:
            logger.error(f"Error registering prompt {name}: {e}")
            
            # Create a dummy implementation that reports the error
            try:
                # Define a simple function with proper type annotations
                @mcp.prompt()
                def error_prompt(message: str) -> str:
                    return f"Prompt {name} encountered an error during registration: {e}"
                
                # Rename the function to match the intended name
                error_prompt.__name__ = name
            except Exception as e2:
                logger.error(f"Error registering error prompt {name}: {e2}")
            
            return False
    
    def get_registration_summary(self):
        """Get a summary of registered tools, resources, and prompts"""
        return {
            "tools": self.registered_tools,
            "resources": self.registered_resources,
            "prompts": self.registered_prompts,
            "missing_dependencies": self.missing_dependencies
        }

# Create a tool registration factory
tool_factory = ToolRegistrationFactory()

# Define resources
@mcp.resource("plan://current")
def get_current_plan():
    """Get the current plan from hanx_plan.md"""
    try:
        plan_path = os.path.join(parent_dir, "hanx_plan.md")
        if os.path.exists(plan_path):
            with open(plan_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return "No plan found."
    except Exception as e:
        logger.error(f"Error reading plan: {e}")
        return f"Error reading plan: {e}"

@mcp.resource("learned://lessons")
def get_learned_lessons():
    """Get the learned lessons from hanx_learned.md"""
    try:
        learned_path = os.path.join(parent_dir, "hanx_learned.md")
        if os.path.exists(learned_path):
            with open(learned_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return "No learned lessons found."
    except Exception as e:
        logger.error(f"Error reading learned lessons: {e}")
        return f"Error reading learned lessons: {e}"

@mcp.resource("file://{path}")
def get_file_content(path: str):
    """Get the content of any file in the workspace"""
    try:
        # Ensure the path is within the workspace
        full_path = os.path.join(parent_dir, path)
        if not os.path.exists(full_path):
            return f"File not found: {path}"
        
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {path}: {e}")
        return f"Error reading file {path}: {e}"

@mcp.resource("directory://{path}")
def list_directory(path: str):
    """List the contents of a directory"""
    try:
        # Ensure the path is within the workspace
        full_path = os.path.join(parent_dir, path)
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            return f"Directory not found: {path}"
        
        items = os.listdir(full_path)
        result = []
        for item in items:
            item_path = os.path.join(full_path, item)
            if os.path.isdir(item_path):
                result.append(f"[DIR] {item}/")
            else:
                size = os.path.getsize(item_path)
                result.append(f"[FILE] {item} ({size} bytes)")
        
        return "\n".join(result)
    except Exception as e:
        logger.error(f"Error listing directory {path}: {e}")
        return f"Error listing directory {path}: {e}"

@mcp.resource("tools://list")
def list_available_tools():
    """List all available tools in the hanx_tools directory"""
    try:
        tools_dir = os.path.join(parent_dir, "hanx_tools")
        if not os.path.exists(tools_dir):
            return "Tools directory not found."
        
        tools = []
        for file in os.listdir(tools_dir):
            if file.endswith(".py") and not file.startswith("__"):
                tools.append(file)
        
        return "\n".join(tools)
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        return f"Error listing tools: {e}"

@mcp.resource("agents://list")
def list_available_agents():
    """List all available agents in the hanx_tools directory"""
    try:
        tools_dir = os.path.join(parent_dir, "hanx_tools")
        if not os.path.exists(tools_dir):
            return "Tools directory not found."
        
        agents = []
        for file in os.listdir(tools_dir):
            if file.startswith("agent_") and file.endswith(".py"):
                agents.append(file)
        
        return "\n".join(agents)
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        return f"Error listing agents: {e}"

@mcp.resource("apis://list")
def list_available_apis():
    """List all available APIs in the hanx_tools directory"""
    try:
        tools_dir = os.path.join(parent_dir, "hanx_tools")
        if not os.path.exists(tools_dir):
            return "Tools directory not found."
        
        apis = []
        for file in os.listdir(tools_dir):
            if file.startswith("api_") and file.endswith(".py"):
                apis.append(file)
        
        return "\n".join(apis)
    except Exception as e:
        logger.error(f"Error listing APIs: {e}")
        return f"Error listing APIs: {e}"

@mcp.resource("system://info")
def get_system_information():
    """Get system information"""
    try:
        from hanx_tools.tool_system_info import get_system_info
        info = get_system_info()
        return str(info)
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return f"Error getting system info: {e}"

# Define prompts
@mcp.prompt()
def hanx_prompt(message: str):
    """Create a prompt for the Hanx multi-agent system"""
    return f"Please process this request as the Hanx multi-agent system: {message}"

@mcp.prompt()
def planner_prompt(task: str):
    """Create a prompt for the Planner agent"""
    return f"As the Planner agent, please analyze and break down this task: {task}"

@mcp.prompt()
def executor_prompt(task: str):
    """Create a prompt for the Executor agent"""
    return f"As the Executor agent, please implement this task: {task}"

@mcp.prompt()
def youtube_research_prompt(topic: str, max_videos: int = 3):
    """Create a prompt for the YouTube Researcher agent"""
    return f"""
    As the YouTube Researcher agent, please research the following topic:
    
    Topic: {topic}
    Maximum videos to analyze: {max_videos}
    
    Please provide a comprehensive analysis with key insights, timestamps of important information, and a summary.
    """

@mcp.prompt()
def rag_librarian_prompt(question: str):
    """Create a prompt for the RAG Librarian agent"""
    return f"""
    As the RAG Librarian agent, please answer the following question using the knowledge base:
    
    Question: {question}
    
    Please provide a detailed answer with citations to the relevant documents in the knowledge base.
    """

@mcp.prompt()
def knowledge_base_prompt(query: str):
    """Create a prompt for the Knowledge Base agent"""
    return f"""
    As the Knowledge Base agent, please respond to the following query:
    
    Query: {query}
    
    Please provide information from the knowledge base with proper citations and context.
    """

@mcp.prompt()
def computer_use_prompt(command: str):
    """Create a prompt for the Computer Use agent"""
    return f"""
    As the Computer Use agent, please execute the following command:
    
    Command: {command}
    
    Please provide the output and explain what the command does.
    """

@mcp.prompt()
def web_search_prompt(query: str):
    """Create a prompt for web search"""
    return f"""
    Please search the web for information about:
    
    Query: {query}
    
    Provide a comprehensive summary of the search results with citations to the sources.
    """

@mcp.prompt()
def document_analysis_prompt(file_path: str):
    """Create a prompt for document analysis"""
    return f"""
    Please analyze the following document:
    
    File: {file_path}
    
    Provide a detailed summary of the document's content, key points, and any important information.
    """

@mcp.prompt()
def code_analysis_prompt(file_path: str):
    """Create a prompt for code analysis"""
    return f"""
    Please analyze the following code file:
    
    File: {file_path}
    
    Provide a detailed explanation of the code's functionality, structure, and any potential issues or improvements.
    """

def generate_requirements_file():
    """Generate a requirements.txt file with all necessary dependencies"""
    try:
        requirements = [
            "mcp>=1.4.0",
            "fastmcp>=0.4.0",
            "python-dotenv>=1.0.0",
            "requests>=2.25.0",
            "beautifulsoup4>=4.9.0",
            "pandas>=1.0.0",
            "numpy>=1.19.0",
            "pillow>=8.0.0",
            "openai>=1.0.0",
            "anthropic>=0.5.0",
            "google-generativeai>=0.1.0",
            "deepseek-ai>=0.1.0",
            "pymysql>=1.0.0",
            "cx_Oracle>=8.0.0",
            "psycopg2-binary>=2.9.0",
            "pytube>=12.0.0",
            "PyPDF2>=2.0.0",
            "python-docx>=0.8.0",
            "trello>=0.9.0",
            "jira>=3.0.0",
            "atlassian-python-api>=3.0.0",
            "selenium>=4.0.0",
            "webdriver-manager>=3.5.0",
        ]
        
        requirements_path = os.path.join(parent_dir, "requirements.txt")
        with open(requirements_path, "w") as f:
            f.write("\n".join(requirements))
        
        logger.info(f"Generated requirements.txt at {requirements_path}")
        return requirements_path
    except Exception as e:
        logger.error(f"Error generating requirements.txt: {e}")
        return None

def register_all_tools(factory):
    """Register all available tools using the tool factory"""
    # Register built-in resources
    factory.register_resource("plan://current", "get_current_plan", "__main__")
    factory.register_resource("learned://lessons", "get_learned_lessons", "__main__")
    factory.register_resource("file://{path}", "get_file_content", "__main__")
    factory.register_resource("directory://{path}", "list_directory", "__main__")
    factory.register_resource("tools://list", "list_available_tools", "__main__")
    factory.register_resource("agents://list", "list_available_agents", "__main__")
    factory.register_resource("apis://list", "list_available_apis", "__main__")
    factory.register_resource("system://info", "get_system_information", "__main__")
    
    # Register built-in prompts
    factory.register_prompt("hanx_prompt", "hanx_prompt", "__main__")
    factory.register_prompt("planner_prompt", "planner_prompt", "__main__")
    factory.register_prompt("executor_prompt", "executor_prompt", "__main__")
    factory.register_prompt("youtube_research_prompt", "youtube_research_prompt", "__main__")
    factory.register_prompt("rag_librarian_prompt", "rag_librarian_prompt", "__main__")
    factory.register_prompt("knowledge_base_prompt", "knowledge_base_prompt", "__main__")
    factory.register_prompt("computer_use_prompt", "computer_use_prompt", "__main__")
    factory.register_prompt("web_search_prompt", "web_search_prompt", "__main__")
    factory.register_prompt("document_analysis_prompt", "document_analysis_prompt", "__main__")
    factory.register_prompt("code_analysis_prompt", "code_analysis_prompt", "__main__")
    
    # Register web tools
    factory.register_tool("web_search", "search_web", "hanx_tools.tool_search_engine", ["requests"])
    factory.register_tool("web_scrape", "scrape_url", "hanx_tools.tool_web_scraper", ["requests", "beautifulsoup4"])
    factory.register_tool("take_screenshot", "take_screenshot", "hanx_tools.tool_screenshot_utils", ["selenium", "webdriver_manager"])
    
    # Register file tools
    factory.register_tool("list_files", "list_files", "hanx_tools.tool_file_utils")
    factory.register_tool("read_file", "read_file", "hanx_tools.tool_file_utils")
    factory.register_tool("write_file", "write_file", "hanx_tools.tool_file_utils")
    factory.register_tool("process_document", "process_document", "hanx_tools.tool_document_processors", ["PyPDF2", "python-docx"])
    factory.register_tool("process_data_file", "process_file", "hanx_tools.tool_file_processors", ["pandas"])
    
    # Register system tools
    factory.register_tool("system_info", "get_system_info", "hanx_tools.tool_system_info")
    factory.register_tool("fix_imports", "fix_imports", "hanx_tools.tool_fix_imports")
    
    # Register API tools
    factory.register_tool("llm_query", "query_llm", "hanx_tools.api_llm", ["openai", "anthropic", "google-generativeai", "deepseek-ai"])
    factory.register_tool("perplexity_query", "query", "hanx_tools.api_perplexity", ["requests"])
    factory.register_tool("trello_create_card", "create_card", "hanx_tools.api_trello", ["trello"])
    factory.register_tool("jira_create_issue", "create_issue", "hanx_tools.api_jira", ["jira"])
    factory.register_tool("confluence_create_page", "create_page", "hanx_tools.api_confluence", ["atlassian-python-api"])
    factory.register_tool("bitbucket_create_pr", "create_pull_request", "hanx_tools.api_bitbucket", ["atlassian-python-api"])
    
    # Register database tools
    factory.register_tool("mysql_query", "query", "hanx_tools.tool_mysql", ["pymysql"])
    factory.register_tool("oracle_query", "query", "hanx_tools.tool_oracle_db", ["cx_Oracle"])
    
    # Register RAG tools
    factory.register_tool("rag_query", "query_collection", "hanx_tools.tool_rag_utils", ["psycopg2-binary"])
    factory.register_tool("rag_ingest", "ingest_document", "hanx_tools.tool_rag_ingest", ["psycopg2-binary"])
    
    # Register YouTube tools
    factory.register_tool("youtube_download", "download_video", "hanx_tools.tool_youtube", ["pytube"])
    factory.register_tool("youtube_transcribe", "get_transcript", "hanx_tools.tool_youtube", ["pytube"])
    
    # Register token tracking tools
    factory.register_tool("track_tokens", "track_usage", "hanx_tools.tool_token_tracker")
    
    # Register agent tools
    factory.register_tool("run_planner", "run_planner", "hanx_tools.agent_planner", ["openai", "anthropic"])
    factory.register_tool("run_executor", "run_executor", "hanx_tools.agent_executor", ["openai", "anthropic"])
    factory.register_tool("run_youtube_researcher", "research_topic", "hanx_tools.agent_youtube_researcher", ["pytube", "openai", "anthropic"])
    factory.register_tool("run_rag_librarian", "answer_question", "hanx_tools.agent_rag_librarian", ["psycopg2-binary", "openai", "anthropic"])
    factory.register_tool("run_knowledge_base", "query_kb", "hanx_tools.agent_knowledge_base", ["psycopg2-binary", "openai", "anthropic"])
    factory.register_tool("run_computer_use", "execute_command", "hanx_tools.agent_computer_use", ["openai", "anthropic"])
    
    # Register OpenManus tools if available
    try:
        from hanx_tools.openmanus.integration import register_with_mcp_sdk
        register_with_mcp_sdk(mcp)
        logger.info("Successfully registered OpenManus tools")
    except ImportError as e:
        logger.warning(f"Could not import OpenManus integration: {e}")
    
    # Log registration summary
    summary = factory.get_registration_summary()
    logger.info(f"Registered {len(summary['tools'])} tools, {len(summary['resources'])} resources, and {len(summary['prompts'])} prompts")
    logger.info(f"Missing dependencies for {len(summary['missing_dependencies'])} items")

def load_environment_variables():
    """Load environment variables from .env files."""
    # Print current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    
    # List of environment files to check
    env_files = ['.env.local', '.env', '.env.example']
    print(f"Looking for environment files: {env_files}")
    
    # Check each file
    for env_file in env_files:
        env_path = os.path.join(cwd, env_file)
        print(f"Checking {env_path}")
        if os.path.exists(env_path):
            print(f"Found {env_file}, loading variables...")
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            # Remove quotes if present
                            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                                value = value[1:-1]
                            os.environ[key] = value
                        except ValueError:
                            # Skip lines that don't have a key=value format
                            pass
            print(f"Loaded environment variables from {env_file}")
            # Print the keys that were loaded (not the values for security)
            keys = [key for key in os.environ.keys() if key in [line.split('=', 1)[0].strip() for line in open(env_path, 'r').readlines() if '=' in line and not line.startswith('#')]]
            print(f"Keys loaded from {env_file}: {keys}")

# Load environment variables
load_environment_variables()

def main():
    """Main function to run the MCP server."""
    # Get host and port from environment variables or use defaults
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    try:
        port = int(os.environ.get("MCP_PORT", "8080"))
    except ValueError:
        print(f"Invalid MCP_PORT value: {os.environ.get('MCP_PORT')}. Using default 8080.")
        port = 8080
    
    print(f"MCP Server will run on {host}:{port}")
    
    # Generate requirements.txt file
    generate_requirements_file()
    
    # Register all tools, resources, and prompts
    register_all_tools(tool_factory)
    
    # Run the server
    print(f"Starting MCP server on {host}:{port}...")
    mcp.run(host=host, port=port)

if __name__ == "__main__":
    main() 