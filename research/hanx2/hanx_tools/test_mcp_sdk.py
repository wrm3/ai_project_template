#!/usr/bin/env python3
"""
Test MCP SDK Server
This script tests the MCP SDK server implementation.
"""

import os
import sys
import json
import argparse
import requests
import time
from typing import Dict, Any, List, Optional

# Add parent directory to path to ensure imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def test_server_info(base_url: str) -> bool:
    """Test the server info endpoint"""
    print("\n=== Testing Server Info ===")
    try:
        response = requests.get(f"{base_url}")
        if response.status_code != 200:
            print(f"Error: Server returned status code {response.status_code}")
            return False
        
        data = response.json()
        print(f"Server info: {json.dumps(data, indent=2)}")
        
        # Check if the response has the expected format
        if "jsonrpc" not in data:
            print("Error: Response missing 'jsonrpc' field")
            return False
        
        if "id" not in data:
            print("Error: Response missing 'id' field")
            return False
        
        if "result" not in data:
            print("Error: Response missing 'result' field")
            return False
        
        result = data["result"]
        if "name" not in result:
            print("Error: Response missing 'name' field")
            return False
        
        if "version" not in result:
            print("Error: Response missing 'version' field")
            return False
        
        print("Server info test passed!")
        return True
    except Exception as e:
        print(f"Error testing server info: {e}")
        return False

def test_list_tools(base_url: str) -> bool:
    """Test the list tools endpoint"""
    print("\n=== Testing List Tools ===")
    try:
        response = requests.get(f"{base_url}/tools")
        if response.status_code != 200:
            print(f"Error: Server returned status code {response.status_code}")
            return False
        
        data = response.json()
        print(f"Tools: {json.dumps(data, indent=2)}")
        
        # Check if the response has the expected format
        if "jsonrpc" not in data:
            print("Error: Response missing 'jsonrpc' field")
            return False
        
        if "id" not in data:
            print("Error: Response missing 'id' field")
            return False
        
        if "result" not in data:
            print("Error: Response missing 'result' field")
            return False
        
        if "tools" not in data["result"]:
            print("Error: Response missing 'tools' field")
            return False
        
        tools = data["result"]["tools"]
        if not isinstance(tools, list):
            print("Error: 'tools' field is not a list")
            return False
        
        print(f"Found {len(tools)} tools")
        for tool in tools:
            print(f"- {tool['name']}: {tool['description']}")
        
        print("List tools test passed!")
        return True
    except Exception as e:
        print(f"Error testing list tools: {e}")
        return False

def test_list_resources(base_url: str) -> bool:
    """Test the list resources endpoint"""
    print("\n=== Testing List Resources ===")
    try:
        response = requests.get(f"{base_url}/resources")
        if response.status_code != 200:
            print(f"Error: Server returned status code {response.status_code}")
            return False
        
        data = response.json()
        print(f"Resources: {json.dumps(data, indent=2)}")
        
        # Check if the response has the expected format
        if "jsonrpc" not in data:
            print("Error: Response missing 'jsonrpc' field")
            return False
        
        if "id" not in data:
            print("Error: Response missing 'id' field")
            return False
        
        if "result" not in data:
            print("Error: Response missing 'result' field")
            return False
        
        if "resources" not in data["result"]:
            print("Error: Response missing 'resources' field")
            return False
        
        resources = data["result"]["resources"]
        if not isinstance(resources, list):
            print("Error: 'resources' field is not a list")
            return False
        
        print(f"Found {len(resources)} resources")
        for resource in resources:
            print(f"- {resource['name']}: {resource['description']}")
        
        print("List resources test passed!")
        return True
    except Exception as e:
        print(f"Error testing list resources: {e}")
        return False

def test_call_tool(base_url: str, tool_name: str, parameters: Dict[str, Any]) -> bool:
    """Test calling a tool"""
    print(f"\n=== Testing Call Tool: {tool_name} ===")
    try:
        response = requests.post(
            f"{base_url}/tools/{tool_name}",
            json=parameters
        )
        if response.status_code != 200:
            print(f"Error: Server returned status code {response.status_code}")
            return False
        
        data = response.json()
        print(f"Tool result: {json.dumps(data, indent=2)}")
        
        # Check if the response has the expected format
        if "jsonrpc" not in data:
            print("Error: Response missing 'jsonrpc' field")
            return False
        
        if "id" not in data:
            print("Error: Response missing 'id' field")
            return False
        
        if "result" not in data:
            print("Error: Response missing 'result' field")
            return False
        
        print(f"Tool {tool_name} call test passed!")
        return True
    except Exception as e:
        print(f"Error testing call tool: {e}")
        return False

def test_get_resource(base_url: str, resource_name: str) -> bool:
    """Test getting a resource"""
    print(f"\n=== Testing Get Resource: {resource_name} ===")
    try:
        response = requests.get(f"{base_url}/resources/{resource_name}")
        if response.status_code != 200:
            print(f"Error: Server returned status code {response.status_code}")
            return False
        
        data = response.json()
        print(f"Resource content: {json.dumps(data, indent=2)}")
        
        # Check if the response has the expected format
        if "jsonrpc" not in data:
            print("Error: Response missing 'jsonrpc' field")
            return False
        
        if "id" not in data:
            print("Error: Response missing 'id' field")
            return False
        
        if "result" not in data:
            print("Error: Response missing 'result' field")
            return False
        
        print(f"Get resource {resource_name} test passed!")
        return True
    except Exception as e:
        print(f"Error testing get resource: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Test MCP SDK Server")
    parser.add_argument("--url", type=str, default="http://localhost:8080", help="Base URL of the MCP server")
    args = parser.parse_args()
    
    base_url = args.url
    
    print(f"Testing MCP server at {base_url}")
    
    # Test server info
    if not test_server_info(base_url):
        print("Server info test failed!")
        return
    
    # Test list tools
    if not test_list_tools(base_url):
        print("List tools test failed!")
        return
    
    # Test list resources
    if not test_list_resources(base_url):
        print("List resources test failed!")
        return
    
    # Test call tool: system_info
    if not test_call_tool(base_url, "system_info", {}):
        print("Call tool test failed!")
        return
    
    # Test call tool: web_search
    if not test_call_tool(base_url, "web_search", {"query": "MCP protocol"}):
        print("Call tool test failed!")
        return
    
    # Test get resource: plan://current
    if not test_get_resource(base_url, "plan://current"):
        print("Get resource test failed!")
        return
    
    print("\n=== All tests passed! ===")

if __name__ == "__main__":
    main() 