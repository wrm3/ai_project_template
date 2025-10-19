#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Client
This script implements a Model Context Protocol client that connects to MCP servers
and provides a unified interface for interacting with them.
"""

import os
import sys
import logging
import argparse
import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import requests

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/mcp_client.log")
    ]
)
logger = logging.getLogger("mcp_client")

# Define our own simplified MCP types since the package might not be available
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

class ServerInfo:
    def __init__(self, name: str, display_name: str, description: str, version: str):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.version = version

class ClientConfig:
    def __init__(self, name: str, display_name: str, description: str, version: str):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.version = version

# Try to import the MCP package
try:
    import mcp
    from mcp.client import Client
    HAS_MCP = True
    logger.info("Model Context Protocol SDK is installed")
except ImportError:
    logger.warning("Model Context Protocol SDK not installed. Please run 'pip install mcp[cli]'.")
    HAS_MCP = False

class SimpleClient:
    """A simplified MCP client implementation."""
    
    def __init__(self, config: ClientConfig):
        self.config = config
        self.servers = {}
    
    async def connect(self, url: str) -> Optional[ServerInfo]:
        """Connect to an MCP server."""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        logger.error(f"Error connecting to server at {url}: {response.status}")
                        return None
                    
                    data = await response.json()
                    server_info = ServerInfo(
                        name=data.get("name", "unknown"),
                        display_name=data.get("display_name", "Unknown Server"),
                        description=data.get("description", ""),
                        version=data.get("version", "0.0.0"),
                    )
                    
                    self.servers[url] = server_info
                    return server_info
        except Exception as e:
            logger.error(f"Error connecting to server at {url}: {e}")
            return None
    
    async def disconnect(self, url: str) -> bool:
        """Disconnect from an MCP server."""
        if url in self.servers:
            del self.servers[url]
            return True
        return False
    
    async def list_resources(self, url: str, resource_type: Optional[str] = None) -> List[Resource]:
        """List resources from a server."""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/resources") as response:
                    if response.status != 200:
                        logger.error(f"Error listing resources from {url}: {response.status}")
                        return []
                    
                    data = await response.json()
                    resources = []
                    
                    for item in data:
                        if resource_type is None or item.get("type") == resource_type:
                            resources.append(Resource(
                                id=item.get("id", ""),
                                name=item.get("name", ""),
                                description=item.get("description", ""),
                                type=item.get("type", ""),
                            ))
                    
                    return resources
        except Exception as e:
            logger.error(f"Error listing resources from {url}: {e}")
            return []
    
    async def get_resource(self, url: str, resource_type: str, resource_name: str, resource_id: str) -> Optional[ResourceContent]:
        """Get a resource from a server."""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/resources/{resource_name}/{resource_id}") as response:
                    if response.status != 200:
                        logger.error(f"Error getting resource {resource_id} from {url}: {response.status}")
                        return None
                    
                    data = await response.json()
                    
                    return ResourceContent(
                        text=data.get("text"),
                        binary=None,  # Binary data not supported in this simple implementation
                        metadata=data.get("metadata", {}),
                    )
        except Exception as e:
            logger.error(f"Error getting resource {resource_id} from {url}: {e}")
            return None
    
    async def list_tools(self, url: str) -> List[Dict[str, Any]]:
        """List tools from a server."""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/tools") as response:
                    if response.status != 200:
                        logger.error(f"Error listing tools from {url}: {response.status}")
                        return []
                    
                    return await response.json()
        except Exception as e:
            logger.error(f"Error listing tools from {url}: {e}")
            return []
    
    async def call_tool(self, url: str, tool_name: str, parameters: Dict[str, Any]) -> Optional[ToolResult]:
        """Call a tool on a server."""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{url}/tools/{tool_name}", json=parameters) as response:
                    data = await response.json()
                    
                    if response.status != 200:
                        return ToolResult(error=data.get("error", "Unknown error"))
                    
                    return ToolResult(content=data.get("content"))
        except Exception as e:
            logger.error(f"Error calling tool {tool_name} on {url}: {e}")
            return ToolResult(error=str(e))
    
    async def send_prompt(self, url: str, prompt_name: str, text: str) -> Optional[PromptResponse]:
        """Send a prompt to a server."""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{url}/prompts/{prompt_name}", json={"text": text}) as response:
                    data = await response.json()
                    
                    if response.status != 200:
                        logger.error(f"Error sending prompt to {url}: {data.get('error', 'Unknown error')}")
                        return None
                    
                    return PromptResponse(text=data.get("text", ""))
        except Exception as e:
            logger.error(f"Error sending prompt to {url}: {e}")
            return None

class HanxMCPClient:
    """Hanx MCP Client implementation."""
    
    def __init__(self, config: Optional[ClientConfig] = None):
        """Initialize the Hanx MCP Client."""
        if config is None:
            config = ClientConfig(
                name="hanx-mcp-client",
                display_name="Hanx MCP Client",
                description="A Model Context Protocol client for the Hanx multi-agent system",
                version="1.0.0",
            )
        
        if HAS_MCP:
            self.client = Client(config)
            self.use_mcp_sdk = True
        else:
            self.client = SimpleClient(config)
            self.use_mcp_sdk = False
        
        self.servers: Dict[str, ServerInfo] = {}
    
    async def connect(self, url: str) -> bool:
        """Connect to an MCP server."""
        try:
            if self.use_mcp_sdk:
                server_info = await self.client.connect(url)
            else:
                server_info = await self.client.connect(url)
            
            if server_info:
                self.servers[url] = server_info
                logger.info(f"Connected to MCP server at {url}: {server_info.display_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error connecting to MCP server at {url}: {e}")
            return False
    
    async def disconnect(self, url: str) -> bool:
        """Disconnect from an MCP server."""
        try:
            if self.use_mcp_sdk:
                await self.client.disconnect(url)
            else:
                await self.client.disconnect(url)
            
            if url in self.servers:
                del self.servers[url]
            
            logger.info(f"Disconnected from MCP server at {url}")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from MCP server at {url}: {e}")
            return False
    
    async def list_servers(self) -> List[ServerInfo]:
        """List connected servers."""
        return list(self.servers.values())
    
    async def list_resources(self, url: str, resource_type: Optional[str] = None) -> List[Resource]:
        """List resources from a server."""
        try:
            if self.use_mcp_sdk:
                resources = await self.client.list_resources(url, resource_type)
            else:
                resources = await self.client.list_resources(url, resource_type)
            
            return resources
        except Exception as e:
            logger.error(f"Error listing resources from {url}: {e}")
            return []
    
    async def get_resource(self, url: str, resource_type: str, resource_name: str, resource_id: str) -> Optional[ResourceContent]:
        """Get a resource from a server."""
        try:
            if self.use_mcp_sdk:
                content = await self.client.get_resource(url, resource_type, resource_name, resource_id)
            else:
                content = await self.client.get_resource(url, resource_type, resource_name, resource_id)
            
            return content
        except Exception as e:
            logger.error(f"Error getting resource {resource_id} from {url}: {e}")
            return None
    
    async def list_tools(self, url: str) -> List[Dict[str, Any]]:
        """List tools from a server."""
        try:
            if self.use_mcp_sdk:
                tools = await self.client.list_tools(url)
            else:
                tools = await self.client.list_tools(url)
            
            return tools
        except Exception as e:
            logger.error(f"Error listing tools from {url}: {e}")
            return []
    
    async def call_tool(self, url: str, tool_name: str, parameters: Dict[str, Any]) -> Optional[ToolResult]:
        """Call a tool on a server."""
        try:
            if self.use_mcp_sdk:
                result = await self.client.call_tool(url, tool_name, parameters)
            else:
                result = await self.client.call_tool(url, tool_name, parameters)
            
            return result
        except Exception as e:
            logger.error(f"Error calling tool {tool_name} on {url}: {e}")
            return None
    
    async def send_prompt(self, url: str, prompt_name: str, text: str) -> Optional[PromptResponse]:
        """Send a prompt to a server."""
        try:
            if self.use_mcp_sdk:
                response = await self.client.send_prompt(url, prompt_name, text)
            else:
                response = await self.client.send_prompt(url, prompt_name, text)
            
            return response
        except Exception as e:
            logger.error(f"Error sending prompt to {url}: {e}")
            return None

def handle_command(command, server_url):
    """Handle a command from the user."""
    try:
        parts = command.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        
        if cmd == "exit":
            return True
        
        if cmd == "help":
            print("Available commands:")
            print("  resources - List available resources")
            print("  resource <type> <name> <id> - Get a specific resource")
            print("  tools - List available tools")
            print("  tool <name> <parameters_json> - Call a tool")
            print("  prompt <name> <text> - Send a prompt")
            print("  exit - Exit the session")
            return
        
        if cmd == "resources":
            resources = list_resources(server_url)
            print("Available resources:")
            for resource in resources:
                print(f"  {resource['type']} - {resource['name']}: {resource['description']}")
            return
        
        if cmd == "resource":
            if len(parts) < 4:
                print("Usage: resource <type> <name> <id>")
                return
            
            resource_type = parts[1]
            resource_name = parts[2]
            resource_id = parts[3]
            
            content = get_resource(server_url, resource_name, resource_id)
            if "error" in content:
                print(f"Error: {content['error']}")
                return
            
            if "text" in content:
                print(content["text"])
            else:
                print(content)
            return
        
        if cmd == "tools":
            tools = list_tools(server_url)
            print("Available tools:")
            for tool in tools:
                print(f"  {tool['name']}: {tool['description']}")
            return
        
        if cmd == "tool":
            if len(parts) < 3:
                print("Usage: tool <name> <parameters_json>")
                return
            
            tool_name = parts[1]
            try:
                parameters = json.loads(" ".join(parts[2:]))
            except json.JSONDecodeError:
                print("Error: Invalid JSON parameters")
                return
            
            result = call_tool(server_url, tool_name, parameters)
            if "error" in result:
                print(f"Error: {result['error']}")
                return
            
            if "content" in result:
                try:
                    # Try to parse as JSON for pretty printing
                    content = json.loads(result["content"])
                    print(json.dumps(content, indent=2))
                except (json.JSONDecodeError, TypeError):
                    # If not valid JSON, print as is
                    print(result["content"])
            else:
                print(result)
            return
        
        if cmd == "prompt":
            if len(parts) < 3:
                print("Usage: prompt <name> <text>")
                return
            
            prompt_name = parts[1]
            text = " ".join(parts[2:])
            
            response = send_prompt(server_url, prompt_name, text)
            if "error" in response:
                print(f"Error: {response['error']}")
                return
            
            if "text" in response:
                print(response["text"])
            else:
                print(response)
            return
        
        print(f"Unknown command: {command}")
    except Exception as e:
        print(f"Error executing command: {str(e)}")
        logger.error(f"Error executing command: {str(e)}", exc_info=True)

def list_resources(server_url):
    """List available resources."""
    try:
        response = requests.get(f"{server_url}/resources")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error listing resources: {str(e)}")
        return []

def get_resource(server_url, resource_name, resource_id):
    """Get a specific resource."""
    try:
        response = requests.get(f"{server_url}/resources/{resource_name}/{resource_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error getting resource: {str(e)}")
        return {"error": str(e)}

def list_tools(server_url):
    """List available tools."""
    try:
        response = requests.get(f"{server_url}/tools")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error listing tools: {str(e)}")
        return []

def call_tool(server_url, tool_name, parameters):
    """Call a tool."""
    try:
        response = requests.post(f"{server_url}/tools/{tool_name}", json=parameters)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error calling tool: {str(e)}")
        return {"error": str(e)}

def send_prompt(server_url, prompt_name, text):
    """Send a prompt."""
    try:
        response = requests.post(f"{server_url}/prompts/{prompt_name}", json={"text": text})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error sending prompt: {str(e)}")
        return {"error": str(e)}

def interactive_mode(server_url):
    """Run the client in interactive mode."""
    print(f"Connected to MCP server at {server_url}")
    print("Type 'help' for available commands, 'exit' to quit")
    
    try:
        while True:
            try:
                command = input("> ")
                if handle_command(command, server_url):
                    break
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Error: {str(e)}")
                logger.error(f"Error in interactive mode: {str(e)}", exc_info=True)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        logger.error(f"Fatal error in interactive mode: {str(e)}", exc_info=True)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Hanx MCP Client")
    parser.add_argument("--server", type=str, default="http://localhost:8080", help="MCP server URL")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--resource-type", type=str, help="Resource type")
    parser.add_argument("--resource-name", type=str, help="Resource name")
    parser.add_argument("--resource-id", type=str, help="Resource ID")
    parser.add_argument("--tool", type=str, help="Tool name")
    parser.add_argument("--parameters", type=str, help="Tool parameters (JSON)")
    parser.add_argument("--prompt", type=str, help="Prompt name")
    parser.add_argument("--text", type=str, help="Prompt text")
    args = parser.parse_args()
    
    # Create the client
    client = HanxMCPClient()
    
    # Run the client
    if args.interactive:
        interactive_mode(args.server)
        return
    
    # Handle resource request
    if args.resource_type and args.resource_name and args.resource_id:
        resource = get_resource(args.server, args.resource_name, args.resource_id)
        if "error" in resource:
            print(f"Error: {resource['error']}")
        elif "text" in resource:
            print(resource["text"])
        else:
            print(resource)
        return
    
    # Handle tool request
    if args.tool and args.parameters:
        try:
            parameters = json.loads(args.parameters)
        except json.JSONDecodeError:
            print("Error: Invalid JSON parameters")
            return
        
        result = call_tool(args.server, args.tool, parameters)
        if "error" in result:
            print(f"Error: {result['error']}")
        elif "content" in result:
            try:
                # Try to parse as JSON for pretty printing
                content = json.loads(result["content"])
                print(json.dumps(content, indent=2))
            except (json.JSONDecodeError, TypeError):
                # If not valid JSON, print as is
                print(result["content"])
        else:
            print(result)
        return
    
    # Handle prompt request
    if args.prompt and args.text:
        response = send_prompt(args.server, args.prompt, args.text)
        if "error" in response:
            print(f"Error: {response['error']}")
        elif "text" in response:
            print(response["text"])
        else:
            print(response)
        return
    
    # If no specific action is requested, list resources and tools
    print("Available resources:")
    resources = list_resources(args.server)
    for resource in resources:
        print(f"  {resource['type']} - {resource['name']}: {resource['description']}")
    
    print("\nAvailable tools:")
    tools = list_tools(args.server)
    for tool in tools:
        print(f"  {tool['name']}: {tool['description']}")

if __name__ == "__main__":
    main() 