#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Test Script
This script tests the connection to an MCP server and verifies its functionality.
"""

import os
import sys
import logging
import argparse
import asyncio
from pathlib import Path

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/mcp_test.log")
    ]
)
logger = logging.getLogger("mcp_test")

def add_hanx_to_python_path():
    """Add hanx directories to Python path"""
    # Get the current directory (should be hanx_mcp)
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
    
    # Ensure hanx_mcp is in the path
    hanx_mcp_dir = os.path.join(parent_dir, "hanx_mcp")
    if os.path.exists(hanx_mcp_dir) and hanx_mcp_dir not in sys.path:
        sys.path.insert(0, hanx_mcp_dir)
    
    # Log the Python path for debugging
    logger.info(f"Python path: {sys.path}")

# Add hanx directories to Python path
add_hanx_to_python_path()

# Try to import the MCP package
try:
    import mcp
    from mcp.client import Client
    HAS_MCP = True
except ImportError:
    logger.warning("Model Context Protocol SDK not installed. Please run 'pip install mcp[cli]'.")
    HAS_MCP = False

async def test_server(url: str):
    """Test the MCP server."""
    if not HAS_MCP:
        logger.error("MCP SDK not installed. Cannot test server.")
        return False
    
    try:
        # Create a client config
        from mcp.client import ClientConfig
        config = ClientConfig(
            name="hanx-mcp-test",
            display_name="Hanx MCP Test",
            description="A test client for the Hanx MCP server",
            version="1.0.0",
        )
        
        # Create a client
        client = Client(config)
        
        # Connect to the server
        logger.info(f"Connecting to MCP server at {url}...")
        server_info = await client.connect(url)
        logger.info(f"Connected to MCP server: {server_info.display_name} (v{server_info.version})")
        
        # List resources
        logger.info("Listing resources...")
        resources = await client.list_resources(url)
        if resources:
            logger.info(f"Found {len(resources)} resources:")
            for resource in resources:
                logger.info(f"  {resource.type} - {resource.name}: {resource.description}")
        else:
            logger.info("No resources found")
        
        # List tools
        logger.info("Listing tools...")
        tools = await client.list_tools(url)
        if tools:
            logger.info(f"Found {len(tools)} tools:")
            for tool in tools:
                logger.info(f"  {tool.name}: {tool.description}")
        else:
            logger.info("No tools found")
        
        # Disconnect from the server
        await client.disconnect(url)
        logger.info(f"Disconnected from MCP server at {url}")
        
        return True
    except Exception as e:
        logger.error(f"Error testing MCP server at {url}: {e}")
        return False

async def test_server_fallback(url: str):
    """Test the MCP server using a fallback implementation."""
    try:
        import aiohttp
        
        logger.info(f"Connecting to MCP server at {url} (fallback mode)...")
        
        async with aiohttp.ClientSession() as session:
            # Test server root
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Error connecting to server at {url}: {response.status}")
                    return False
                
                data = await response.json()
                logger.info(f"Connected to MCP server: {data.get('display_name')} (v{data.get('version')})")
            
            # Test resources
            logger.info("Listing resources...")
            async with session.get(f"{url}/resources") as response:
                if response.status != 200:
                    logger.error(f"Error listing resources from {url}: {response.status}")
                else:
                    data = await response.json()
                    if data:
                        logger.info(f"Found {len(data)} resources:")
                        for item in data:
                            logger.info(f"  {item.get('type')} - {item.get('name')}: {item.get('description')}")
                    else:
                        logger.info("No resources found")
            
            # Test tools
            logger.info("Listing tools...")
            async with session.get(f"{url}/tools") as response:
                if response.status != 200:
                    logger.error(f"Error listing tools from {url}: {response.status}")
                else:
                    data = await response.json()
                    if data:
                        logger.info(f"Found {len(data)} tools:")
                        for item in data:
                            logger.info(f"  {item.get('name')}: {item.get('description')}")
                    else:
                        logger.info("No tools found")
        
        logger.info(f"Completed testing MCP server at {url} (fallback mode)")
        return True
    except Exception as e:
        logger.error(f"Error testing MCP server at {url} (fallback mode): {e}")
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Hanx MCP Test")
    parser.add_argument("--url", type=str, default="http://localhost:8080", help="MCP server URL")
    args = parser.parse_args()
    
    # Run the test
    try:
        if HAS_MCP:
            success = asyncio.run(test_server(args.url))
        else:
            # Check if aiohttp is installed
            try:
                import aiohttp
                success = asyncio.run(test_server_fallback(args.url))
            except ImportError:
                logger.error("Neither MCP SDK nor aiohttp is installed. Cannot test server.")
                logger.error("Please run 'pip install mcp[cli]' or 'pip install aiohttp'.")
                sys.exit(1)
        
        if success:
            logger.info("MCP server test completed successfully")
            sys.exit(0)
        else:
            logger.error("MCP server test failed")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Test interrupted. Shutting down...")
    except Exception as e:
        logger.error(f"Error running test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 