#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server
This script implements a Model Context Protocol server that exposes the Hanx multi-agent system
through the standardized MCP interface.
"""

import os
import sys
import logging
import argparse
import asyncio
import json
import importlib
import pkgutil
import socket
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

# Import colorama for colored console output
try:
    from colorama import init, Fore, Back, Style
    # Initialize colorama
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    # Create dummy color constants if colorama is not available
    class DummyColors:
        def __getattr__(self, name):
            return ""
    Fore = DummyColors()
    Back = DummyColors()
    Style = DummyColors()

# Add parent directory to path to ensure imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Custom logger with colored output
class ColoredLogger:
    def __init__(self, logger):
        self.logger = logger
    
    def info(self, msg, *args, **kwargs):
        if HAS_COLORAMA:
            print(f"{Fore.GREEN}[INFO] {msg}{Style.RESET_ALL}")
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        if HAS_COLORAMA:
            print(f"{Fore.RED}[WARNING] {msg}{Style.RESET_ALL}")
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        if HAS_COLORAMA:
            print(f"{Fore.RED}[ERROR] {msg}{Style.RESET_ALL}")
        self.logger.error(msg, *args, **kwargs)
    
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)
    
    def critical(self, msg, *args, **kwargs):
        if HAS_COLORAMA:
            print(f"{Fore.RED}{Back.WHITE}[CRITICAL] {msg}{Style.RESET_ALL}")
        self.logger.critical(msg, *args, **kwargs)
    
    def success(self, msg, *args, **kwargs):
        if HAS_COLORAMA:
            print(f"{Fore.GREEN}{Style.BRIGHT}[SUCCESS] {msg}{Style.RESET_ALL}")
        self.logger.info(f"SUCCESS: {msg}", *args, **kwargs)

# Import hanx modules with proper error handling
try:
    from hanx_agents import *
    if HAS_COLORAMA:
        print(f"{Fore.GREEN}✓ Successfully imported hanx_agents{Style.RESET_ALL}")
    logging.info("Successfully imported hanx_agents")
except ImportError as e:
    if HAS_COLORAMA:
        print(f"{Fore.RED}✗ Could not import hanx_agents: {e}{Style.RESET_ALL}")
    logging.warning(f"Could not import hanx_agents: {e}")

# Import hanx_apis modules individually with error handling
api_modules = {
    "api_llm": None,
    "api_perplexity": None,
    "api_trello": None,
    "api_jira": None,
    "api_bitbucket": None,
    "api_confluence": None
}

for module_name in api_modules.keys():
    try:
        module = importlib.import_module(f"hanx_apis.{module_name}")
        api_modules[module_name] = module
        logging.info(f"Successfully imported {module_name}")
    except ImportError as e:
        logging.warning(f"Could not import {module_name}: {e}")

# Check if we imported any API modules
if any(api_modules.values()):
    if HAS_COLORAMA:
        print(f"{Fore.GREEN}✓ Successfully imported hanx_apis modules{Style.RESET_ALL}")
    logging.info("Successfully imported hanx_apis modules")
else:
    if HAS_COLORAMA:
        print(f"{Fore.RED}✗ Could not import any hanx_apis modules{Style.RESET_ALL}")
    logging.warning("Could not import any hanx_apis modules")

# Import hanx_tools modules individually instead of using wildcard import
try:
    import hanx_tools
    # Import specific modules we need
    try:
        from hanx_tools.tool_search_engine import search_web
    except ImportError:
        pass
    try:
        from hanx_tools.tool_web_scraper import scrape_url
    except ImportError:
        pass
    try:
        from hanx_tools.tool_system_info import get_system_info
    except ImportError:
        pass
    try:
        from hanx_tools.tool_file_utils import list_files
    except ImportError:
        pass
    try:
        from hanx_tools.tool_mysql import query as mysql_query
    except ImportError:
        pass
    
    if HAS_COLORAMA:
        print(f"{Fore.GREEN}✓ Successfully imported hanx_tools{Style.RESET_ALL}")
    logging.info("Successfully imported hanx_tools")
except ImportError as e:
    if HAS_COLORAMA:
        print(f"{Fore.RED}✗ Could not import hanx_tools: {e}{Style.RESET_ALL}")
    logging.warning(f"Could not import hanx_tools: {e}")

# Import OpenManus integration
try:
    import hanx_tools.openmanus.integration as openmanus_integration
    if HAS_COLORAMA:
        print(f"{Fore.GREEN}✓ Successfully imported OpenManus integration{Style.RESET_ALL}")
    logging.info("Successfully imported OpenManus integration")
except ImportError as e:
    if HAS_COLORAMA:
        print(f"{Fore.RED}✗ Could not import OpenManus integration: {e}{Style.RESET_ALL}")
    logging.warning(f"Could not import OpenManus integration: {e}")
    openmanus_integration = None

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/mcp_server.log")
    ]
)
logger = logging.getLogger("mcp_server")

# Initialize colorama if available
if HAS_COLORAMA:
    init(autoreset=True)

def load_env_files():
    """Load environment variables from .env files."""
    # Print current working directory
    cwd = os.getcwd()
    logger.info(f"Current working directory: {cwd}")
    
    # List of environment files to check
    env_files = ['.env.local', '.env']
    logger.info(f"Looking for environment files: {env_files}")
    
    # Check each file
    found_env_file = False
    for env_file in env_files:
        env_path = os.path.join(cwd, env_file)
        logger.info(f"Checking {env_path}")
        if os.path.exists(env_path):
            found_env_file = True
            logger.info(f"Found {env_file}, loading variables...")
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
            logger.info(f"Loaded environment variables from {env_file}")
            # Print the keys that were loaded (not the values for security)
            keys = [key for key in os.environ.keys() if key in [line.split('=', 1)[0].strip() for line in open(env_path, 'r').readlines() if '=' in line and not line.startswith('#')]]
            logger.info(f"Keys loaded from {env_file}: {keys}")
    
    # Only check .env.example if no other .env files were found
    if not found_env_file:
        env_example_path = os.path.join(cwd, '.env.example')
        if os.path.exists(env_example_path):
            logger.info("No primary .env files found, checking .env.example as fallback")
            logger.info("Found .env.example, loading variables...")
            with open(env_example_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            # Only set if the environment variable is not already set
                            if key not in os.environ:
                                # Remove quotes if present
                                if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                                    value = value[1:-1]
                                os.environ[key] = value
                        except ValueError:
                            # Skip lines that don't have a key=value format
                            pass
            logger.info("Loaded environment variables from .env.example")
            # Print the keys that were loaded (not the values for security)
            keys = [key for key in os.environ.keys() if key in [line.split('=', 1)[0].strip() for line in open(env_example_path, 'r').readlines() if '=' in line and not line.startswith('#')]]
            logger.info(f"Keys loaded from .env.example: {keys}")
            found_env_file = True
    
    if not found_env_file:
        logger.warning("No .env files found. Using system environment variables only.")
        # Print available environment variables (excluding sensitive ones)
        safe_env_vars = [k for k in os.environ.keys() if not k.lower().endswith('key') and not k.lower().endswith('token') and not k.lower().endswith('password')]
        logger.info(f"Available system environment variables: {sorted(safe_env_vars)}")

# Load environment variables from .env files
if os.environ.get("SKIP_ENV_FILES") == "1":
    logger.warning("SKIP_ENV_FILES is set, skipping .env files")
else:
    load_env_files()

# Define our own simplified MCP types since the package isn't available
class ResourceType:
    TEXT = "text"
    BINARY = "binary"
    IMAGE = "image"

class Resource:
    def __init__(self, id: str, name: str, description: str, type: str):
        self.id = id
        self.name = name
        self.description = description
        self.type = type

class ResourceContent:
    def __init__(self, text: str = None, binary: bytes = None, metadata: Dict[str, str] = None):
        self.text = text
        self.binary = binary
        self.metadata = metadata or {}

class ToolCall:
    def __init__(self, name: str, parameters: Dict[str, Any]):
        self.name = name
        self.parameters = parameters

class ToolResult:
    def __init__(self, content: str = None, error: str = None):
        self.content = content
        self.error = error

class Prompt:
    def __init__(self, name: str, text: str):
        self.name = name
        self.text = text

class PromptResponse:
    def __init__(self, text: str):
        self.text = text

class ServerConfig:
    def __init__(self, name: str, display_name: str, description: str, version: str, contact_email: str = None):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.version = version
        self.contact_email = contact_email
        self.jsonrpc = "2.0"  # Add the jsonrpc version field

# Import Hanx agents
try:
    from hanx_agents.agent_planner import main as planner_main
    from hanx_agents.agent_executor import main as executor_main
    from hanx_agents.agent_rag_librarian import main as rag_main
    from hanx_agents.agent_youtube_researcher import main as youtube_main
    HAS_AGENTS = True
except ImportError:
    logger.warning("Hanx agents not found. Some functionality may be limited.")
    HAS_AGENTS = False

class SimpleServer:
    """A simplified MCP server implementation."""
    
    def __init__(self, config: ServerConfig):
        self.config = config
        self.resource_handlers = {}
        self.tool_handlers = {}
        self.prompt_handlers = {}
    
    def register_resource_handler(self, resource_type: str, resource_name: str, description: str, 
                                 list_handler, get_handler):
        """Register a resource handler."""
        self.resource_handlers[resource_name] = {
            "type": resource_type,
            "description": description,
            "list_handler": list_handler,
            "get_handler": get_handler
        }
    
    def register_tool_handler(self, name: str, description: str, parameter_schema: Dict[str, Any], handler):
        """Register a tool handler."""
        self.tool_handlers[name] = {
            "description": description,
            "parameter_schema": parameter_schema,
            "handler": handler
        }
    
    def register_prompt_handler(self, name: str, description: str, handler):
        """Register a prompt handler."""
        self.prompt_handlers[name] = {
            "description": description,
            "handler": handler
        }
    
    async def start(self, host: str, port: int):
        """Start the server."""
        from aiohttp import web
        
        app = web.Application()
        
        # Define routes
        app.router.add_get("/", self.handle_root)
        app.router.add_get("/events", self.handle_sse)  # Add SSE endpoint
        app.router.add_get("/resources", self.handle_list_resources)
        app.router.add_get("/resources/{resource_name}/{resource_id}", self.handle_get_resource)
        app.router.add_get("/tools", self.handle_list_tools)
        app.router.add_post("/tools/{tool_name}", self.handle_call_tool)
        app.router.add_post("/prompts/{prompt_name}", self.handle_send_prompt)
        
        # Start the server
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        logger.info(f"Server started on {host}:{port}")
        
        # Keep the server running
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour
    
    async def stop(self):
        """Stop the server."""
        # In a real implementation, we would stop the web server here
        pass
    
    async def handle_root(self, request):
        """Handle root endpoint."""
        from aiohttp import web
        
        # Check if the client accepts text/event-stream
        accept_header = request.headers.get('Accept', '')
        if 'text/event-stream' in accept_header:
            return await self.handle_sse(request)
        
        # Return properly formatted server info following JSON-RPC 2.0 format
        server_info = {
            "jsonrpc": "2.0",
            "id": 1,  # Add an id field
            "result": {
                "name": self.config.name,
                "display_name": self.config.display_name,
                "description": self.config.description,
                "version": self.config.version,
                "tools": [],
                "resources": []
            }
        }
        
        # Add tools if available
        if hasattr(self, 'tool_handlers'):
            server_info["result"]["tools"] = list(self.tool_handlers.keys())
        
        # Add resources if available
        if hasattr(self, 'resource_handlers'):
            server_info["result"]["resources"] = list(self.resource_handlers.keys())
        
        return web.json_response(server_info)
    
    async def handle_sse(self, request):
        """Handle Server-Sent Events (SSE) endpoint."""
        from aiohttp import web
        
        response = web.StreamResponse()
        response.headers['Content-Type'] = 'text/event-stream'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Connection'] = 'keep-alive'
        response.headers['Access-Control-Allow-Origin'] = '*'
        await response.prepare(request)
        
        # Send initial server info with proper schema following JSON-RPC 2.0 format
        server_info = {
            "jsonrpc": "2.0",
            "id": 1,  # Add an id field
            "result": {
                "name": self.config.name,
                "display_name": self.config.display_name,
                "description": self.config.description,
                "version": self.config.version,
                "tools": [],  # Initialize as empty arrays to avoid null values
                "resources": []
            }
        }
        
        # Add tools if available
        if hasattr(self, 'tool_handlers'):
            server_info["result"]["tools"] = list(self.tool_handlers.keys())
        
        # Add resources if available
        if hasattr(self, 'resource_handlers'):
            server_info["result"]["resources"] = list(self.resource_handlers.keys())
        
        # Format as SSE event
        event_data = f"event: message\ndata: {json.dumps(server_info)}\n\n"
        await response.write(event_data.encode('utf-8'))
        
        # Keep the connection alive with periodic heartbeats
        try:
            while True:
                # Send a heartbeat every 30 seconds
                await asyncio.sleep(30)
                await response.write(b"event: heartbeat\ndata: {}\n\n")
        except asyncio.CancelledError:
            # Client disconnected
            pass
        
        return response
    
    async def handle_list_resources(self, request):
        """Handle list resources endpoint."""
        from aiohttp import web
        
        resources = []
        for resource_name, handler_info in self.resource_handlers.items():
            try:
                handler_resources = await handler_info["list_handler"]()
                resources.extend(handler_resources)
            except Exception as e:
                logger.error(f"Error listing resources for {resource_name}: {e}")
        
        resource_list = [{
            "id": resource.id,
            "name": resource.name,
            "description": resource.description,
            "type": resource.type
        } for resource in resources]
        
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "resources": resource_list
            }
        }
        
        return web.json_response(response)
    
    async def handle_get_resource(self, request):
        """Handle get resource endpoint."""
        from aiohttp import web
        
        resource_name = request.match_info["resource_name"]
        resource_id = request.match_info["resource_id"]
        
        if resource_name not in self.resource_handlers:
            return web.json_response({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": f"Resource {resource_name} not found"
                }
            }, status=404)
        
        try:
            handler_info = self.resource_handlers[resource_name]
            content = await handler_info["get_handler"](resource_id)
            
            if content is None:
                return web.json_response({
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32602,
                        "message": f"Resource {resource_id} not found"
                    }
                }, status=404)
            
            response = {
                "jsonrpc": "2.0",
                "result": {
                    "metadata": content.metadata
                }
            }
            
            if content.text is not None:
                response["result"]["text"] = content.text
            
            if content.binary is not None:
                # In a real implementation, we would handle binary data properly
                response["result"]["binary"] = "binary data"
            
            return web.json_response(response)
        except Exception as e:
            logger.error(f"Error getting resource {resource_name}/{resource_id}: {e}")
            return web.json_response({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }, status=500)
    
    async def handle_list_tools(self, request):
        """Handle list tools endpoint."""
        from aiohttp import web
        
        tools = []
        for tool_name, handler_info in self.tool_handlers.items():
            # Ensure parameter_schema is properly formatted
            parameter_schema = handler_info.get("parameter_schema", {})
            if not parameter_schema:
                parameter_schema = {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            
            tools.append({
                "name": tool_name,
                "description": handler_info.get("description", ""),
                "parameter_schema": parameter_schema
            })
        
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": tools
            }
        }
        
        return web.json_response(response)
    
    async def handle_call_tool(self, request):
        """Handle call tool endpoint."""
        from aiohttp import web
        
        tool_name = request.match_info["tool_name"]
        
        if tool_name not in self.tool_handlers:
            return web.json_response({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": f"Tool {tool_name} not found"
                }
            }, status=404)
        
        try:
            # Parse request body
            body = await request.json()
            
            # Create tool call
            tool_call = ToolCall(tool_name, body)
            
            # Call handler
            handler_info = self.tool_handlers[tool_name]
            result = await handler_info["handler"](tool_call)
            
            if result.error:
                return web.json_response({
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": result.error
                    }
                }, status=400)
            
            return web.json_response({
                "jsonrpc": "2.0",
                "result": {
                    "content": result.content
                }
            })
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return web.json_response({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }, status=500)
    
    async def handle_send_prompt(self, request):
        """Handle send prompt endpoint."""
        from aiohttp import web
        
        prompt_name = request.match_info["prompt_name"]
        
        if prompt_name not in self.prompt_handlers:
            return web.json_response({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": f"Prompt {prompt_name} not found"
                }
            }, status=404)
        
        try:
            # Parse request body
            body = await request.json()
            
            if "text" not in body:
                return web.json_response({
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32602,
                        "message": "Missing 'text' field in request body"
                    }
                }, status=400)
            
            # Create prompt
            prompt = Prompt(prompt_name, body["text"])
            
            # Call handler
            handler_info = self.prompt_handlers[prompt_name]
            response = await handler_info["handler"](prompt)
            
            return web.json_response({
                "jsonrpc": "2.0",
                "result": {
                    "text": response.text
                }
            })
        except Exception as e:
            logger.error(f"Error sending prompt {prompt_name}: {e}")
            return web.json_response({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }, status=500)

class HanxMCPServer:
    """Hanx MCP Server implementation."""
    
    def __init__(self, config: Optional[ServerConfig] = None):
        """Initialize the Hanx MCP Server."""
        if config is None:
            config = ServerConfig(
                name="hanx-mcp-server",
                display_name="Hanx Multi-Agent System",
                description="A Model Context Protocol server for the Hanx multi-agent system",
                version="1.0.0",
                contact_email="support@example.com",
            )
        
        self.server = SimpleServer(config)
        self.setup_resources()
        self.setup_tools()
        self.setup_prompts()
    
    def setup_resources(self):
        """Set up MCP resources."""
        # Register the plan resource
        self.server.register_resource_handler(
            resource_type=ResourceType.TEXT,
            resource_name="plan",
            description="The current plan in the Hanx multi-agent system",
            list_handler=self.list_plans,
            get_handler=self.get_plan,
        )
        
        # Register the learned lessons resource
        self.server.register_resource_handler(
            resource_type=ResourceType.TEXT,
            resource_name="lessons",
            description="Lessons learned by the Hanx multi-agent system",
            list_handler=self.list_lessons,
            get_handler=self.get_lesson,
        )
    
    async def list_plans(self) -> List[Resource]:
        """List available plans."""
        try:
            plan_path = Path("hanx_plan.md")
            if plan_path.exists():
                return [
                    Resource(
                        id="current_plan",
                        name="Current Plan",
                        description="The current plan in the Hanx multi-agent system",
                        type=ResourceType.TEXT,
                    )
                ]
            return []
        except Exception as e:
            logger.error(f"Error listing plans: {e}")
            return []
    
    async def get_plan(self, resource_id: str) -> Optional[ResourceContent]:
        """Get a specific plan."""
        try:
            if resource_id == "current_plan":
                plan_path = Path("hanx_plan.md")
                if plan_path.exists():
                    content = plan_path.read_text(encoding="utf-8")
                    return ResourceContent(
                        text=content,
                        metadata={
                            "last_modified": str(plan_path.stat().st_mtime),
                            "size": str(plan_path.stat().st_size),
                        }
                    )
            return None
        except Exception as e:
            logger.error(f"Error getting plan {resource_id}: {e}")
            return None
    
    async def list_lessons(self) -> List[Resource]:
        """List available lessons."""
        try:
            lessons_path = Path("hanx_learned.md")
            if lessons_path.exists():
                return [
                    Resource(
                        id="all_lessons",
                        name="All Lessons",
                        description="All lessons learned by the Hanx multi-agent system",
                        type=ResourceType.TEXT,
                    )
                ]
            return []
        except Exception as e:
            logger.error(f"Error listing lessons: {e}")
            return []
    
    async def get_lesson(self, resource_id: str) -> Optional[ResourceContent]:
        """Get a specific lesson."""
        try:
            if resource_id == "all_lessons":
                lessons_path = Path("hanx_learned.md")
                if lessons_path.exists():
                    content = lessons_path.read_text(encoding="utf-8")
                    return ResourceContent(
                        text=content,
                        metadata={
                            "last_modified": str(lessons_path.stat().st_mtime),
                            "size": str(lessons_path.stat().st_size),
                        }
                    )
            return None
        except Exception as e:
            logger.error(f"Error getting lesson {resource_id}: {e}")
            return None
    
    def setup_tools(self):
        """Set up MCP tools."""
        # Register all tools from hanx_tools directory
        self.register_hanx_tools()
        
        # Register OpenManus tools
        try:
            if openmanus_integration is not None:
                logger.info("Registering OpenManus tools with MCP server")
                openmanus_integration.register_with_mcp_server(self)
                logger.info("Successfully registered OpenManus tools")
            else:
                logger.warning("OpenManus integration not available, skipping registration")
        except Exception as e:
            logger.error(f"Error registering OpenManus tools: {e}")
        
        # Register the planner tool
        self.server.register_tool_handler(
            name="planner",
            description="Run the Planner agent to analyze and plan tasks",
            parameter_schema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt for the Planner agent"
                    },
                    "file": {
                        "type": "string",
                        "description": "Optional file to include in the analysis"
                    }
                },
                "required": ["prompt"]
            },
            handler=self.run_planner
        )
        
        # Register the executor tool
        self.server.register_tool_handler(
            name="executor",
            description="Run the Executor agent to execute tasks",
            parameter_schema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task description"
                    },
                    "section": {
                        "type": "string",
                        "description": "The section to update"
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to update"
                    }
                },
                "required": ["task", "section", "content"]
            },
            handler=self.run_executor
        )
        
        # Register the RAG tool
        self.server.register_tool_handler(
            name="rag",
            description="Run the RAG Librarian agent to search and retrieve information",
            parameter_schema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt for the RAG agent"
                    }
                },
                "required": ["prompt"]
            },
            handler=self.run_rag
        )
        
        # Register the YouTube tool
        self.server.register_tool_handler(
            name="youtube",
            description="Run the YouTube Researcher agent to analyze YouTube videos",
            parameter_schema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt for the YouTube agent"
                    },
                    "url": {
                        "type": "string",
                        "description": "The YouTube video URL"
                    }
                },
                "required": ["prompt"]
            },
            handler=self.run_youtube
        )
        
        # Register the Trello API tool
        self.server.register_tool_handler(
            name="trello_api",
            description="Use the Trello API to manage boards, lists, and cards",
            parameter_schema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The Trello action to perform (get_boards, create_board, create_card, get_cards)"
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for board or card creation"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description for board or card creation"
                    },
                    "list_id": {
                        "type": "string",
                        "description": "List ID for card operations"
                    }
                },
                "required": ["action"]
            },
            handler=self.run_trello_api
        )
        
        # Register the Jira API tool
        self.server.register_tool_handler(
            name="jira_api",
            description="Use the Jira API to manage issues and projects",
            parameter_schema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The Jira action to perform (create_issue, get_issue, search_issues)"
                    },
                    "project": {
                        "type": "string",
                        "description": "Project key for issue creation"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Summary for issue creation"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description for issue creation"
                    },
                    "issue_type": {
                        "type": "string",
                        "description": "Issue type for issue creation (default: Task)"
                    },
                    "issue_key": {
                        "type": "string",
                        "description": "Issue key for getting issue details"
                    },
                    "jql": {
                        "type": "string",
                        "description": "JQL query for searching issues"
                    }
                },
                "required": ["action"]
            },
            handler=self.run_jira_api
        )
        
        # Register the Bitbucket API tool
        self.server.register_tool_handler(
            name="bitbucket_api",
            description="Use the Bitbucket API to manage repositories and pull requests",
            parameter_schema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The Bitbucket action to perform (create_repo, get_repo, create_pull_request)"
                    },
                    "project_key": {
                        "type": "string",
                        "description": "Project key for repository operations"
                    },
                    "repo_name": {
                        "type": "string",
                        "description": "Repository name for creation"
                    },
                    "repo_slug": {
                        "type": "string",
                        "description": "Repository slug for operations"
                    },
                    "is_private": {
                        "type": "boolean",
                        "description": "Whether the repository is private (default: true)"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for pull request creation"
                    },
                    "source_branch": {
                        "type": "string",
                        "description": "Source branch for pull request"
                    },
                    "target_branch": {
                        "type": "string",
                        "description": "Target branch for pull request (default: main)"
                    }
                },
                "required": ["action"]
            },
            handler=self.run_bitbucket_api
        )
        
        # Register the Confluence API tool
        self.server.register_tool_handler(
            name="confluence_api",
            description="Use the Confluence API to manage pages and content",
            parameter_schema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The Confluence action to perform (create_page, get_page, search_content)"
                    },
                    "space": {
                        "type": "string",
                        "description": "Space key for page operations"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for page creation"
                    },
                    "body": {
                        "type": "string",
                        "description": "Body content for page creation"
                    },
                    "parent_id": {
                        "type": "string",
                        "description": "Parent page ID for page creation"
                    },
                    "page_id": {
                        "type": "string",
                        "description": "Page ID for getting page details"
                    },
                    "query": {
                        "type": "string",
                        "description": "Query for searching content"
                    }
                },
                "required": ["action"]
            },
            handler=self.run_confluence_api
        )
    
    def register_hanx_tools(self):
        """Register Hanx tools with the MCP server."""
        logger.info("Registering tools from hanx_tools and hanx_apis directories")
        
        # Register MySQL query tool
        try:
            from hanx_tools.tool_mysql import query as mysql_query
            self.server.register_tool_handler(
                name="mysql_query",
                description="Execute a MySQL query",
                parameter_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "SQL query to execute"},
                        "params": {"type": "array", "description": "Parameters for the query", "items": {"type": "string"}}
                    },
                    "required": ["query"]
                },
                handler=self.run_mysql_query
            )
            logger.info("Registered tool: mysql_query")
        except ImportError as e:
            logger.error(f"Could not register mysql_query tool: {e}")
        
        # Register list_files tool
        try:
            from hanx_tools.tool_file_utils import list_files
            self.server.register_tool_handler(
                name="list_files",
                description="List files in a directory",
                parameter_schema={
                    "type": "object",
                    "properties": {
                        "directory": {"type": "string", "description": "Directory to list files from"},
                        "pattern": {"type": "string", "description": "File pattern to match (glob)"}
                    },
                    "required": ["directory"]
                },
                handler=self.run_list_files
            )
            logger.info("Registered tool: list_files")
        except ImportError as e:
            logger.error(f"Could not register list_files tool: {e}")
        
        # Register take_screenshot tool
        try:
            from hanx_tools.tool_screenshot_utils import take_screenshot
            self.server.register_tool_handler(
                name="take_screenshot",
                description="Take a screenshot of a webpage",
                parameter_schema={
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to take screenshot of"},
                        "output": {"type": "string", "description": "Output file path"},
                        "width": {"type": "integer", "description": "Screenshot width"},
                        "height": {"type": "integer", "description": "Screenshot height"}
                    },
                    "required": ["url"]
                },
                handler=self.run_take_screenshot
            )
            logger.info("Registered tool: take_screenshot")
        except ImportError as e:
            logger.error(f"Could not register take_screenshot tool: {e}")
        
        # Register web_search tool
        try:
            from hanx_tools.tool_search_engine import search_web
            self.server.register_tool_handler(
                name="web_search",
                description="Search the web",
                parameter_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "num_results": {"type": "integer", "description": "Number of results to return"}
                    },
                    "required": ["query"]
                },
                handler=self.run_web_search
            )
            logger.info("Registered tool: web_search")
        except ImportError as e:
            logger.error(f"Could not register web_search tool: {e}")
        
        # Register system_info tool
        try:
            from hanx_tools.tool_system_info import get_system_info
            self.server.register_tool_handler(
                name="system_info",
                description="Get system information",
                parameter_schema={
                    "type": "object",
                    "properties": {
                        "include_env": {"type": "boolean", "description": "Include environment variables"},
                        "include_python": {"type": "boolean", "description": "Include Python information"}
                    }
                },
                handler=self.run_system_info
            )
            logger.info("Registered tool: system_info")
        except ImportError as e:
            logger.error(f"Could not register system_info tool: {e}")
        
        # Register web_scrape tool
        try:
            from hanx_tools.tool_web_scraper import scrape_url
            self.server.register_tool_handler(
                name="web_scrape",
                description="Scrape a webpage",
                parameter_schema={
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to scrape"},
                        "selector": {"type": "string", "description": "CSS selector to extract"}
                    },
                    "required": ["url"]
                },
                handler=self.run_web_scrape
            )
            logger.info("Registered tool: web_scrape")
        except ImportError as e:
            logger.error(f"Could not register web_scrape tool: {e}")
        
        # Register llm_query tool
        try:
            from hanx_apis.api_llm import query_llm
            self.server.register_tool_handler(
                name="llm_query",
                description="Query an LLM",
                parameter_schema={
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Prompt to send to the LLM"},
                        "provider": {"type": "string", "description": "LLM provider (openai, anthropic, etc.)"},
                        "model": {"type": "string", "description": "Model to use"}
                    },
                    "required": ["prompt"]
                },
                handler=self.run_llm_query
            )
            logger.info("Registered tool: llm_query")
        except ImportError as e:
            logger.error(f"Could not register llm_query tool: {e}")
        
        # Register perplexity_query tool
        try:
            from hanx_apis.api_perplexity import PerplexityAPI
            self.server.register_tool_handler(
                name="perplexity_query",
                description="Query Perplexity API",
                parameter_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Query to send to Perplexity"},
                        "model": {"type": "string", "description": "Model to use"}
                    },
                    "required": ["query"]
                },
                handler=self.run_perplexity_query
            )
            logger.info("Registered tool: perplexity_query")
        except ImportError as e:
            logger.error(f"Could not register perplexity_query tool: {e}")
        
        # Register OpenManus integration if available
        if openmanus_integration:
            try:
                openmanus_integration.register_with_mcp_server(self)
                logger.success("Registered OpenManus tools")
            except Exception as e:
                logger.error(f"OpenManus integration not available, skipping registration: {e}")
        else:
            logger.error("OpenManus integration not available, skipping registration")
    
    async def run_planner(self, tool_call: ToolCall) -> ToolResult:
        """Run the Planner agent."""
        try:
            if not HAS_AGENTS:
                return ToolResult(
                    error="Hanx agents not available"
                )
            
            params = tool_call.parameters
            prompt = params.get("prompt")
            file = params.get("file")
            
            kwargs = {"prompt": prompt}
            if file:
                kwargs["file"] = file
            
            # Run the planner in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: planner_main(**kwargs)
            )
            
            return ToolResult(
                content=json.dumps({
                    "status": "success",
                    "result": result
                })
            )
        except Exception as e:
            logger.error(f"Error running planner: {e}")
            return ToolResult(
                error=str(e)
            )
    
    async def run_executor(self, tool_call: ToolCall) -> ToolResult:
        """Run the Executor agent."""
        try:
            if not HAS_AGENTS:
                return ToolResult(
                    error="Hanx agents not available"
                )
            
            params = tool_call.parameters
            task = params.get("task")
            section = params.get("section")
            content = params.get("content")
            
            # Run the executor in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: executor_main(task=task, update_section=section, content=content)
            )
            
            return ToolResult(
                content=json.dumps({
                    "status": "success",
                    "result": result
                })
            )
        except Exception as e:
            logger.error(f"Error running executor: {e}")
            return ToolResult(
                error=str(e)
            )
    
    async def run_rag(self, tool_call: ToolCall) -> ToolResult:
        """Run the RAG Librarian agent."""
        try:
            if not HAS_AGENTS:
                return ToolResult(
                    error="Hanx agents not available"
                )
            
            params = tool_call.parameters
            prompt = params.get("prompt")
            
            # Run the RAG agent in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: rag_main(prompt=prompt)
            )
            
            return ToolResult(
                content=json.dumps({
                    "status": "success",
                    "result": result
                })
            )
        except Exception as e:
            logger.error(f"Error running RAG agent: {e}")
            return ToolResult(
                error=str(e)
            )
    
    async def run_youtube(self, tool_call: ToolCall) -> ToolResult:
        """Run the YouTube Researcher agent."""
        try:
            if not HAS_AGENTS:
                return ToolResult(
                    error="Hanx agents not available"
                )
            
            params = tool_call.parameters
            prompt = params.get("prompt")
            url = params.get("url", "")
            
            # Run the YouTube agent in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: youtube_main(prompt=prompt, url=url)
            )
            
            return ToolResult(
                content=json.dumps({
                    "status": "success",
                    "result": result
                })
            )
        except Exception as e:
            logger.error(f"Error running YouTube agent: {e}")
            return ToolResult(
                error=str(e)
            )
    
    def setup_prompts(self):
        """Set up MCP prompts."""
        # Register the general prompt handler
        self.server.register_prompt_handler(
            name="hanx",
            description="Interact with the Hanx multi-agent system",
            handler=self.handle_prompt
        )
    
    async def handle_prompt(self, prompt: Prompt) -> PromptResponse:
        """Handle a general prompt to the Hanx system."""
        try:
            # Determine which agent to use based on the prompt
            text = prompt.text.lower()
            
            if "plan" in text or "analyze" in text:
                # Use the planner
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, 
                    lambda: planner_main(prompt=prompt.text)
                )
                return PromptResponse(
                    text=f"Planner response: {result}"
                )
            elif "execute" in text or "implement" in text:
                # Use the executor
                # For simplicity, we'll just acknowledge the request
                return PromptResponse(
                    text="To execute a task, please use the executor tool with specific task, section, and content parameters."
                )
            elif "search" in text or "find" in text or "retrieve" in text:
                # Use the RAG agent
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, 
                    lambda: rag_main(prompt=prompt.text)
                )
                return PromptResponse(
                    text=f"RAG response: {result}"
                )
            elif "youtube" in text or "video" in text:
                # Use the YouTube agent
                return PromptResponse(
                    text="To analyze a YouTube video, please use the youtube tool with specific prompt and URL parameters."
                )
            else:
                # Default to a helpful response
                return PromptResponse(
                    text=f"I received your prompt: '{prompt.text}'. To interact with the Hanx multi-agent system, you can use specific tools like 'planner', 'executor', 'rag', or 'youtube', or you can phrase your prompt to indicate which agent you want to use."
                )
        except Exception as e:
            logger.error(f"Error handling prompt: {e}")
            return PromptResponse(
                text=f"Error handling prompt: {str(e)}"
            )
    
    async def start(self, host: str = "0.0.0.0", port: int = 8080):
        """Start the MCP server."""
        await self.server.start(host=host, port=port)
        
        # Get local IP address for easier access
        local_ip = "unknown"
        try:
            # Get the local IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Doesn't need to be reachable
            s.connect(('10.255.255.255', 1))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "127.0.0.1"
        
        # Print server information with colors if available
        if HAS_COLORAMA:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{Style.BRIGHT} HANX MCP SERVER RUNNING{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{Style.BRIGHT}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{Style.BRIGHT} Server Name:    {self.server.config.name}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{Style.BRIGHT} Version:        {self.server.config.version}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{Style.BRIGHT} Listening on:   {host}:{port}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{Style.BRIGHT} Local Access:   http://localhost:{port}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{Style.BRIGHT} Network Access: http://{local_ip}:{port}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{Style.BRIGHT}{'='*60}{Style.RESET_ALL}\n")
        else:
            logger.info(f"MCP server started on {host}:{port}")
            logger.info(f"Local access URL: http://localhost:{port}")
            logger.info(f"Network access URL: http://{local_ip}:{port}")
    
    async def stop(self):
        """Stop the MCP server."""
        await self.server.stop()
        logger.info("MCP server stopped")

    async def run_process_document(self, tool_call: ToolCall) -> ToolResult:
        """Run the process_document tool."""
        try:
            # Try both absolute and relative imports
            try:
                from hanx_tools.tool_document_processors import process_document
            except ImportError:
                try:
                    from tool_document_processors import process_document
                except ImportError:
                    from .tool_document_processors import process_document
            
            params = tool_call.parameters
            file_path = params.get("file_path")
            
            if not file_path:
                return ToolResult(error="Missing file_path parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            content, metadata = await loop.run_in_executor(
                None, 
                lambda: process_document(file_path)
            )
            
            return ToolResult(
                content=json.dumps({
                    "content": content,
                    "metadata": metadata
                })
            )
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return ToolResult(error=str(e))

    async def run_process_word(self, tool_call: ToolCall) -> ToolResult:
        """Run the process_word tool."""
        try:
            # Try both absolute and relative imports
            try:
                from hanx_tools.tool_file_processors import WordProcessor
            except ImportError:
                try:
                    from tool_file_processors import WordProcessor
                except ImportError:
                    from .tool_file_processors import WordProcessor
            
            params = tool_call.parameters
            file_path = params.get("file_path")
            action = params.get("action")
            content = params.get("content", "")
            
            if not file_path or not action:
                return ToolResult(error="Missing required parameters")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            
            if action == "read":
                result = await loop.run_in_executor(
                    None, 
                    lambda: WordProcessor.read_docx(file_path)
                )
                return ToolResult(content=result)
            elif action == "create":
                await loop.run_in_executor(
                    None, 
                    lambda: WordProcessor.create_docx(file_path, content)
                )
                return ToolResult(content=f"Created Word document at {file_path}")
            elif action == "add":
                await loop.run_in_executor(
                    None, 
                    lambda: WordProcessor.add_to_docx(file_path, content)
                )
                return ToolResult(content=f"Added content to Word document at {file_path}")
            else:
                return ToolResult(error=f"Invalid action: {action}")
        except Exception as e:
            logger.error(f"Error processing Word document: {e}")
            return ToolResult(error=str(e))

    async def run_mysql_query(self, tool_call: ToolCall) -> ToolResult:
        """Run the mysql_query tool."""
        try:
            # Try both absolute and relative imports
            try:
                from hanx_tools.tool_mysql import query
            except ImportError:
                try:
                    from tool_mysql import query
                except ImportError:
                    from .tool_mysql import query
            
            params = tool_call.parameters
            sql = params.get("query")
            db_type = params.get("db_type", "main")
            
            if not sql:
                return ToolResult(error="Missing query parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: query(sql, db_type=db_type)
            )
            
            return ToolResult(
                content=json.dumps(result)
            )
        except Exception as e:
            logger.error(f"Error executing MySQL query: {e}")
            return ToolResult(error=str(e))

    async def run_oracle_query(self, tool_call: ToolCall) -> ToolResult:
        """Run the oracle_query tool."""
        try:
            # Try both absolute and relative imports
            try:
                from hanx_tools.tool_oracle_db import OracleDB
            except ImportError:
                try:
                    from tool_oracle_db import OracleDB
                except ImportError:
                    from .tool_oracle_db import OracleDB
            
            params = tool_call.parameters
            sql = params.get("query")
            source_db = params.get("source_db", True)
            
            if not sql:
                return ToolResult(error="Missing query parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            
            async def execute_query():
                with OracleDB(source_db=source_db) as db:
                    return db.execute_query(sql)
            
            result = await loop.run_in_executor(
                None, 
                lambda: asyncio.run(execute_query())
            )
            
            return ToolResult(
                content=json.dumps(result)
            )
        except Exception as e:
            logger.error(f"Error executing Oracle query: {e}")
            return ToolResult(error=str(e))

    async def run_list_files(self, tool_call: ToolCall) -> ToolResult:
        """Run the list_files tool."""
        try:
            # Try both absolute and relative imports
            try:
                from hanx_tools.tool_file_utils import list_files
            except ImportError:
                try:
                    from tool_file_utils import list_files
                except ImportError:
                    from .tool_file_utils import list_files
            
            params = tool_call.parameters
            directory = params.get("directory")
            pattern = params.get("pattern", "*.*")
            
            if not directory:
                return ToolResult(error="Missing directory parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: list_files(directory, pattern)
            )
            
            return ToolResult(
                content=json.dumps(result)
            )
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return ToolResult(error=str(e))

    async def run_take_screenshot(self, tool_call: ToolCall) -> ToolResult:
        """Run the take_screenshot tool."""
        try:
            # Try both absolute and relative imports
            try:
                from hanx_tools.tool_screenshot_utils import take_screenshot
            except ImportError:
                try:
                    from tool_screenshot_utils import take_screenshot
                except ImportError:
                    from .tool_screenshot_utils import take_screenshot
            
            params = tool_call.parameters
            url = params.get("url")
            output_path = params.get("output")
            width = params.get("width", 1280)
            height = params.get("height", 720)
            
            if not url:
                return ToolResult(error="Missing url parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: take_screenshot(url, output_path, width, height)
            )
            
            return ToolResult(
                content=json.dumps({
                    "screenshot_path": result
                })
            )
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return ToolResult(error=str(e))

    async def run_web_search(self, tool_call: ToolCall) -> ToolResult:
        """Run the web_search tool."""
        try:
            # Try both absolute and relative imports
            try:
                from hanx_tools.tool_search_engine import search_web
            except ImportError:
                try:
                    from tool_search_engine import search_web
                except ImportError:
                    from .tool_search_engine import search_web
            
            params = tool_call.parameters
            query = params.get("query")
            max_results = params.get("num_results", 10)
            
            if not query:
                return ToolResult(error="Missing query parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: search_web(query, max_results)
            )
            
            return ToolResult(
                content=json.dumps(result)
            )
        except Exception as e:
            logger.error(f"Error searching web: {e}")
            return ToolResult(error=str(e))

    async def run_system_info(self, tool_call: ToolCall) -> ToolResult:
        """Run the system_info tool."""
        try:
            # Try both absolute and relative imports
            try:
                from hanx_tools.tool_system_info import get_system_info
            except ImportError:
                try:
                    from tool_system_info import get_system_info
                except ImportError:
                    from .tool_system_info import get_system_info
            
            params = tool_call.parameters
            include_env = params.get("include_env", True)
            include_python = params.get("include_python", True)
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            
            result = await loop.run_in_executor(
                None, 
                lambda: get_system_info(include_env=include_env, include_python=include_python)
            )
            
            return ToolResult(
                content=json.dumps(result)
            )
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return ToolResult(error=str(e))

    async def run_web_scrape(self, tool_call: ToolCall) -> ToolResult:
        """Run the web_scrape tool."""
        try:
            import asyncio
            # Try both absolute and relative imports
            try:
                from hanx_tools.tool_web_scraper import scrape_url
            except ImportError:
                try:
                    from tool_web_scraper import scrape_url
                except ImportError:
                    from .tool_web_scraper import scrape_url
            
            params = tool_call.parameters
            url = params.get("url")
            selector = params.get("selector")
            
            if not url:
                return ToolResult(error="Missing url parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: scrape_url(url, selector)
            )
            
            return ToolResult(
                content=json.dumps({
                    "results": result
                })
            )
        except Exception as e:
            logger.error(f"Error scraping web: {e}")
            return ToolResult(error=str(e))

    async def run_llm_query(self, tool_call: ToolCall) -> ToolResult:
        """Run the llm_query tool."""
        try:
            # Use the already imported module
            if 'api_llm' in sys.modules:
                query_llm = sys.modules['api_llm'].query_llm
            else:
                # Try different import paths
                try:
                    from api_llm import query_llm
                except ImportError:
                    # Add hanx_apis to path and try again
                    sys.path.append(os.path.join(os.getcwd(), 'hanx_apis'))
                    from api_llm import query_llm
            
            params = tool_call.parameters
            prompt = params.get("prompt")
            provider = params.get("provider", "openai")
            model = params.get("model")
            
            if not prompt:
                return ToolResult(error="Missing prompt parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: query_llm(prompt, provider=provider, model=model)
            )
            
            return ToolResult(
                content=result
            )
        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            return ToolResult(error=str(e))

    async def run_perplexity_query(self, tool_call: ToolCall) -> ToolResult:
        """Run the perplexity_query tool."""
        try:
            # Use the already imported module
            if 'api_perplexity' in sys.modules:
                PerplexityAPI = sys.modules['api_perplexity'].PerplexityAPI
            else:
                # Try different import paths
                try:
                    from api_perplexity import PerplexityAPI
                except ImportError:
                    # Add hanx_apis to path and try again
                    sys.path.append(os.path.join(os.getcwd(), 'hanx_apis'))
                    from api_perplexity import PerplexityAPI
            
            params = tool_call.parameters
            question = params.get("query")
            model = params.get("model")
            
            if not question:
                return ToolResult(error="Missing query parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            
            async def execute_query():
                api = PerplexityAPI()
                return api.research_query(question, model=model)
            
            result = await loop.run_in_executor(
                None, 
                lambda: asyncio.run(execute_query())
            )
            
            return ToolResult(
                content=json.dumps(result)
            )
        except Exception as e:
            logger.error(f"Error querying Perplexity: {e}")
            return ToolResult(error=str(e))

    async def run_trello_api(self, tool_call: ToolCall) -> ToolResult:
        """Run the Trello API tool."""
        try:
            # Use the already imported module
            if 'api_trello' in sys.modules:
                TrelloAPI = sys.modules['api_trello'].TrelloAPI
            else:
                # Try different import paths
                try:
                    from api_trello import TrelloAPI
                except ImportError:
                    # Add hanx_apis to path and try again
                    sys.path.append(os.path.join(os.getcwd(), 'hanx_apis'))
                    from api_trello import TrelloAPI
            
            params = tool_call.parameters
            action = params.get("action")
            
            if not action:
                return ToolResult(error="Missing action parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            
            async def execute_trello_action():
                # Initialize the Trello API client
                api_key = os.getenv('TRELLO_API_KEY')
                token = os.getenv('TRELLO_TOKEN')
                
                if not api_key or not token:
                    return {"error": "Trello API credentials not found in environment variables"}
                
                trello = TrelloAPI(api_key=api_key, token=token)
                
                if action == "get_boards":
                    return {"boards": trello.get_boards()}
                elif action == "create_board":
                    name = params.get("name")
                    description = params.get("description")
                    if not name:
                        return {"error": "Missing name parameter for create_board action"}
                    return {"board": trello.create_board(name, description)}
                elif action == "create_card":
                    list_id = params.get("list_id")
                    name = params.get("name")
                    description = params.get("description")
                    if not list_id or not name:
                        return {"error": "Missing list_id or name parameter for create_card action"}
                    return {"card": trello.create_card(list_id, name, description)}
                elif action == "get_cards":
                    list_id = params.get("list_id")
                    if not list_id:
                        return {"error": "Missing list_id parameter for get_cards action"}
                    return {"cards": trello.get_cards(list_id)}
                else:
                    return {"error": f"Unknown Trello action: {action}"}
            
            result = await loop.run_in_executor(
                None, 
                lambda: asyncio.run(execute_trello_action())
            )
            
            return ToolResult(
                content=json.dumps(result)
            )
        except Exception as e:
            logger.error(f"Error using Trello API: {e}")
            return ToolResult(error=str(e))

    async def run_jira_api(self, tool_call: ToolCall) -> ToolResult:
        """Run the Jira API tool."""
        try:
            # Use the already imported module
            if 'api_jira' in sys.modules:
                JiraAPI = sys.modules['api_jira'].JiraAPI
            else:
                # Try different import paths
                try:
                    from api_jira import JiraAPI
                except ImportError:
                    # Add hanx_apis to path and try again
                    sys.path.append(os.path.join(os.getcwd(), 'hanx_apis'))
                    from api_jira import JiraAPI
            
            params = tool_call.parameters
            action = params.get("action")
            
            if not action:
                return ToolResult(error="Missing action parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            
            async def execute_jira_action():
                # Initialize the Jira API client
                url = os.getenv('JIRA_URL')
                username = os.getenv('JIRA_USERNAME')
                api_token = os.getenv('JIRA_API_TOKEN')
                
                if not url or not username or not api_token:
                    return {"error": "Jira API credentials not found in environment variables"}
                
                jira = JiraAPI(url=url, username=username, api_token=api_token)
                
                if action == "create_issue":
                    project = params.get("project")
                    summary = params.get("summary")
                    description = params.get("description")
                    issue_type = params.get("issue_type", "Task")
                    if not project or not summary or not description:
                        return {"error": "Missing required parameters for create_issue action"}
                    return {"issue": jira.create_issue(project, summary, description, issue_type)}
                elif action == "get_issue":
                    issue_key = params.get("issue_key")
                    if not issue_key:
                        return {"error": "Missing issue_key parameter for get_issue action"}
                    return {"issue": jira.get_issue(issue_key)}
                elif action == "search_issues":
                    jql = params.get("jql")
                    if not jql:
                        return {"error": "Missing jql parameter for search_issues action"}
                    return {"issues": jira.search_issues(jql)}
                else:
                    return {"error": f"Unknown Jira action: {action}"}
            
            result = await loop.run_in_executor(
                None, 
                lambda: asyncio.run(execute_jira_action())
            )
            
            return ToolResult(
                content=json.dumps(result)
            )
        except Exception as e:
            logger.error(f"Error using Jira API: {e}")
            return ToolResult(error=str(e))

    async def run_bitbucket_api(self, tool_call: ToolCall) -> ToolResult:
        """Run the Bitbucket API tool."""
        try:
            # Use the already imported module
            if 'api_bitbucket' in sys.modules:
                BitbucketAPI = sys.modules['api_bitbucket'].BitbucketAPI
            else:
                # Try different import paths
                try:
                    from hanx_apis.api_bitbucket import BitbucketAPI
                except ImportError:
                    # Add hanx_apis to path and try again
                    sys.path.append(os.path.join(os.getcwd(), 'hanx_apis'))
                    from api_bitbucket import BitbucketAPI
            
            params = tool_call.parameters
            action = params.get("action")
            
            if not action:
                return ToolResult(error="Missing action parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            
            async def execute_bitbucket_action():
                # Initialize the Bitbucket API client
                url = os.getenv('BITBUCKET_URL')
                username = os.getenv('BITBUCKET_USERNAME')
                api_token = os.getenv('BITBUCKET_API_TOKEN')
                
                if not url or not username or not api_token:
                    return {"error": "Bitbucket API credentials not found in environment variables"}
                
                bitbucket = BitbucketAPI(url=url, username=username, api_token=api_token)
                
                if action == "create_repo":
                    project_key = params.get("project_key")
                    repo_name = params.get("repo_name")
                    is_private = params.get("is_private", True)
                    if not project_key or not repo_name:
                        return {"error": "Missing required parameters for create_repo action"}
                    return {"repo": bitbucket.create_repo(project_key, repo_name, is_private)}
                elif action == "get_repo":
                    project_key = params.get("project_key")
                    repo_slug = params.get("repo_slug")
                    if not project_key or not repo_slug:
                        return {"error": "Missing required parameters for get_repo action"}
                    return {"repo": bitbucket.get_repo(project_key, repo_slug)}
                elif action == "create_pull_request":
                    project_key = params.get("project_key")
                    repo_slug = params.get("repo_slug")
                    title = params.get("title")
                    source_branch = params.get("source_branch")
                    target_branch = params.get("target_branch", "main")
                    if not project_key or not repo_slug or not title or not source_branch:
                        return {"error": "Missing required parameters for create_pull_request action"}
                    return {"pull_request": bitbucket.create_pull_request(project_key, repo_slug, title, source_branch, target_branch)}
                else:
                    return {"error": f"Unknown Bitbucket action: {action}"}
            
            result = await loop.run_in_executor(
                None, 
                lambda: asyncio.run(execute_bitbucket_action())
            )
            
            return ToolResult(
                content=json.dumps(result)
            )
        except Exception as e:
            logger.error(f"Error using Bitbucket API: {e}")
            return ToolResult(error=str(e))

    async def run_confluence_api(self, tool_call: ToolCall) -> ToolResult:
        """Run the Confluence API tool."""
        try:
            # Use the already imported module
            if 'api_confluence' in sys.modules:
                ConfluenceAPI = sys.modules['api_confluence'].ConfluenceAPI
            else:
                # Try different import paths
                try:
                    from hanx_apis.api_confluence import ConfluenceAPI
                except ImportError:
                    # Add hanx_apis to path and try again
                    sys.path.append(os.path.join(os.getcwd(), 'hanx_apis'))
                    from api_confluence import ConfluenceAPI
            
            params = tool_call.parameters
            action = params.get("action")
            
            if not action:
                return ToolResult(error="Missing action parameter")
            
            # Run in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            
            async def execute_confluence_action():
                # Initialize the Confluence API client
                url = os.getenv('JIRA_URL')  # Usually same as Jira URL
                username = os.getenv('JIRA_USERNAME')
                api_token = os.getenv('JIRA_API_TOKEN')
                
                if not url or not username or not api_token:
                    return {"error": "Confluence API credentials not found in environment variables"}
                
                confluence = ConfluenceAPI(url=url, username=username, api_token=api_token)
                
                if action == "create_page":
                    space = params.get("space")
                    title = params.get("title")
                    body = params.get("body")
                    parent_id = params.get("parent_id")
                    if not space or not title or not body:
                        return {"error": "Missing required parameters for create_page action"}
                    return {"page": confluence.create_page(space, title, body, parent_id)}
                elif action == "get_page":
                    page_id = params.get("page_id")
                    if not page_id:
                        return {"error": "Missing page_id parameter for get_page action"}
                    return {"page": confluence.get_page(page_id)}
                elif action == "search_content":
                    query = params.get("query")
                    space = params.get("space")
                    if not query:
                        return {"error": "Missing query parameter for search_content action"}
                    return {"results": confluence.search_content(query, space)}
                else:
                    return {"error": f"Unknown Confluence action: {action}"}
            
            result = await loop.run_in_executor(
                None, 
                lambda: asyncio.run(execute_confluence_action())
            )
            
            return ToolResult(
                content=json.dumps(result)
            )
        except Exception as e:
            logger.error(f"Error using Confluence API: {e}")
            return ToolResult(error=str(e))

def add_hanx_to_python_path():
    """Add hanx_tools and hanx_apis to Python path"""
    # Get the current directory (should be hanx_tools)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the parent directory (should be the project root)
    parent_dir = os.path.dirname(current_dir)
    
    # Add parent directory to path if not already there
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    # Ensure hanx_tools is in the path
    hanx_tools_dir = os.path.join(parent_dir, "hanx_tools")
    if os.path.exists(hanx_tools_dir) and hanx_tools_dir not in sys.path:
        sys.path.insert(0, hanx_tools_dir)
    
    # Ensure hanx_apis is in the path
    hanx_apis_dir = os.path.join(parent_dir, "hanx_apis")
    if os.path.exists(hanx_apis_dir) and hanx_apis_dir not in sys.path:
        sys.path.insert(0, hanx_apis_dir)
    
    # Ensure hanx_agents is in the path
    hanx_agents_dir = os.path.join(parent_dir, "hanx_agents")
    if os.path.exists(hanx_agents_dir) and hanx_agents_dir not in sys.path:
        sys.path.insert(0, hanx_agents_dir)
    
    # Log the Python path for debugging
    logger.info(f"Python path: {sys.path}")
    
    # Try to import the modules to verify they're accessible
    try:
        import hanx_apis
        logger.info("Successfully imported hanx_apis")
    except ImportError as e:
        logger.warning(f"Failed to import hanx_apis: {e}")
    
    try:
        import hanx_tools
        logger.info("Successfully imported hanx_tools")
    except ImportError as e:
        logger.warning(f"Failed to import hanx_tools: {e}")
    
    try:
        import hanx_agents
        logger.info("Successfully imported hanx_agents")
    except ImportError as e:
        logger.warning(f"Failed to import hanx_agents: {e}")

def main():
    """Main function."""
    # Configure logging first
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/mcp_server.log")
        ]
    )
    global logger
    logger = logging.getLogger("mcp_server")
    # Wrap the logger with our colored logger
    logger = ColoredLogger(logger)
    
    # Add hanx_tools and hanx_apis to Python path before any imports
    logger.info("Setting up Python path...")
    add_hanx_to_python_path()
    
    # Get host and port from environment variables or use defaults
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    try:
        port = int(os.environ.get("MCP_PORT", "8080"))
    except ValueError:
        logger.warning(f"Invalid MCP_PORT value: {os.environ.get('MCP_PORT')}. Using default 8080.")
        port = 8080
    
    logger.info(f"MCP Server will run on {host}:{port}")
    
    # Check if aiohttp is installed
    try:
        import aiohttp
        logger.success("aiohttp is installed")
    except ImportError:
        logger.error("aiohttp not installed. Please run 'pip install aiohttp'.")
        sys.exit(1)
    
    # Create the server
    server = HanxMCPServer()
    
    # Run the server
    try:
        asyncio.run(server.start(host=host, port=port))
    except KeyboardInterrupt:
        logger.info("Server interrupted. Shutting down...")
        asyncio.run(server.stop())
    except Exception as e:
        logger.error(f"Error running server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 