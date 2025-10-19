# Hanx MCP Server

This directory contains the Model Context Protocol (MCP) server implementation for the Hanx multi-agent system.

## Overview

The MCP server exposes the Hanx multi-agent system through the standardized Model Context Protocol interface, allowing it to be used with compatible clients like Cursor IDE and Claude Desktop.

## Implementation Options

There are two implementations available:

1. **Custom Implementation** (`mcp_server.py`): A from-scratch implementation of the MCP protocol.
2. **SDK Implementation** (`mcp_server_sdk.py`): An implementation using the official MCP Python SDK.

The SDK implementation is recommended for new projects as it provides a cleaner, more maintainable, and more reliable implementation.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Installing the MCP SDK

Run the installation script:

```bash
python install_mcp_sdk.py
```

Or install manually:

```bash
pip install mcp python-dotenv aiohttp pydantic loguru tabulate
```

## Running the Server

### Using the SDK Implementation (Recommended)

```bash
python run_mcp_sdk.py
```

### Using the Custom Implementation

```bash
python run_mcp.py
```

## Configuration

The server can be configured using environment variables, which can be loaded from:

1. `.cursor/mcp.json` (highest priority)
2. `.env.local`
3. `.env`
4. `.env.example` (lowest priority)

## Features

The MCP server exposes the following features:

### Resources

- `plan://current`: The current plan from `hanx_plan.md`
- `learned://lessons`: The learned lessons from `hanx_learned.md`

### Tools

- `web_search`: Search the web for information
- `web_scrape`: Scrape content from a web page
- `system_info`: Get system information
- `list_files`: List files in a directory
- `take_screenshot`: Take a screenshot of a webpage
- `llm_query`: Query an LLM with a prompt
- `perplexity_query`: Query Perplexity API
- `mysql_query`: Execute a MySQL query

### OpenManus Tools

- `browser_use_tool`: Use browser automation to interact with web pages
- `flow_manager_tool`: Manage complex workflows
- `planning_enhancer_tool`: Enhance planning capabilities using LLMs
- `python_execute_tool`: Execute Python code in a secure environment
- `tool_collection_tool`: Run a tool from the OpenManus tool collection

### Prompts

- `hanx_prompt`: Create a prompt for the Hanx system
- `planner_prompt`: Create a prompt for the Planner agent
- `executor_prompt`: Create a prompt for the Executor agent

## Development

### Adding New Tools

To add a new tool to the SDK implementation, add a new function with the `@mcp.tool()` decorator:

```python
@mcp.tool()
def my_new_tool(param1: str, param2: int = 0):
    """Tool description"""
    # Tool implementation
    return result
```

### Adding New Resources

To add a new resource to the SDK implementation, add a new function with the `@mcp.resource()` decorator:

```python
@mcp.resource("resource://path")
def my_new_resource():
    """Resource description"""
    # Resource implementation
    return content
```

### Adding New Prompts

To add a new prompt to the SDK implementation, add a new function with the `@mcp.prompt()` decorator:

```python
@mcp.prompt()
def my_new_prompt(param1: str):
    """Prompt description"""
    # Prompt implementation
    return prompt_text
```

## Troubleshooting

### Common Issues

- **Connection Refused**: Make sure the server is running and listening on the correct port (default: 8080).
- **Tool Not Found**: Make sure the tool is properly registered with the server.
- **Resource Not Found**: Make sure the resource is properly registered with the server.
- **Environment Variables Not Loaded**: Check that the environment variables are properly set in one of the supported configuration files.

### Logs

Logs are stored in the `logs` directory:

- `logs/mcp_server.log`: Logs for the custom implementation
- `logs/mcp_server_sdk.log`: Logs for the SDK implementation
- `logs/run_mcp_sdk.log`: Logs for the SDK runner script 