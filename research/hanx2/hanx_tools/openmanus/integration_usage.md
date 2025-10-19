# OpenManus Integration Module

The `integration.py` module provides a unified interface for registering OpenManus tools with both the `.cursorrules` interface and the MCP server. It serves as the central connection point between the Hanx project and the OpenManus capabilities.

## Basic Usage

### Registering OpenManus Tools with .cursorrules

```python
# In your .cursorrules file or any Python module that needs access to OpenManus tools
from hanx_tools.openmanus.integration import register_with_cursorrules

# Register all OpenManus tools with the current globals dictionary
register_with_cursorrules(globals())

# Now you can use the OpenManus tools directly
result = planning_enhancer("generate_plan", goal="Analyze a dataset and create visualizations")
browser_result = browser_use("navigate", url="https://example.com")
```

### Registering OpenManus Tools with MCP Server

```python
# In your MCP server initialization code
from hanx_tools.openmanus.integration import register_with_mcp_server

# Register all OpenManus tools with the MCP server
register_with_mcp_server(mcp_server)
```

### Accessing Individual Tools

```python
from hanx_tools.openmanus.integration import get_tool, list_tools, get_tool_collection

# List all available tools
available_tools = list_tools()
print(f"Available OpenManus tools: {available_tools}")

# Get a specific tool
planning_tool = get_tool("planning_enhancer")
if planning_tool:
    # Use the tool directly
    result = planning_tool.run(action="generate_plan", goal="Analyze data")

# Get the shared tool collection
tool_collection = get_tool_collection()
```

## Available Tools

The OpenManus integration provides access to the following tools:

| Tool Name | Description | Module |
|-----------|-------------|--------|
| `browser_use` | Web browsing and interaction capabilities | `browser_use.py` |
| `flow_manager` | Workflow management for complex tasks | `flow_management.py` |
| `planning_enhancer` | Enhanced planning capabilities | `planning.py` |
| `python_execute` | Secure Python execution environment | `python_execute.py` |
| `tool_collection` | Tool orchestration and management | `tool_collection.py` |

## Integration Class

The `OpenManusIntegration` class is the core of the integration module. It:

1. Initializes and manages all OpenManus tools
2. Provides methods for registering tools with different interfaces
3. Maintains a shared tool collection for coordinated tool usage

```python
from hanx_tools.openmanus.integration import OpenManusIntegration

# Create an integration instance
integration = OpenManusIntegration()

# Register tools with a custom interface
integration.register_with_cursorrules(my_globals_dict)
integration.register_with_mcp_server(my_server)

# Access tools directly
planning_tool = integration.get_tool("planning_enhancer")
```

## Singleton Pattern

The integration module uses a singleton pattern to ensure that only one instance of `OpenManusIntegration` exists. This is important for maintaining a consistent state across different parts of the application.

```python
from hanx_tools.openmanus.integration import get_integration

# Get the singleton instance
integration = get_integration()
```

## Best Practices

1. **Single Registration Point**: Register OpenManus tools at a single point in your application, typically during initialization.

2. **Error Handling**: The integration module handles import errors gracefully, but you should still check for tool availability before using them:

   ```python
   from hanx_tools.openmanus.integration import get_tool
   
   planning_tool = get_tool("planning_enhancer")
   if planning_tool:
       # Tool is available
       result = planning_tool.run(action="generate_plan", goal="Analyze data")
   else:
       # Tool is not available
       print("Planning enhancer not available")
   ```

3. **Tool Collection**: Use the shared tool collection for coordinated tool usage:

   ```python
   from hanx_tools.openmanus.integration import get_tool_collection
   
   tool_collection = get_tool_collection()
   
   # Register a custom tool with the collection
   tool_collection.register_tool(my_custom_tool)
   
   # Use the collection to run tools
   result = tool_collection.run_tool("my_custom_tool", action="do_something")
   ```

4. **MCP Server Integration**: When integrating with the MCP server, ensure that the server is properly initialized before registering tools.

## Example: Complete Integration Workflow

```python
# Step 1: Import the necessary modules
from hanx_tools.openmanus.integration import register_with_cursorrules, get_tool

# Step 2: Register OpenManus tools with the current globals dictionary
register_with_cursorrules(globals())

# Step 3: Use the tools directly
# Generate a plan
plan_result = planning_enhancer("generate_plan", 
    goal="Scrape data from a website and analyze it",
    available_tools=[
        {"name": "browser_use", "description": "Web browsing capabilities"}
    ]
)

if plan_result["success"]:
    plan = plan_result["plan"]
    
    # Execute the plan
    execution_result = planning_enhancer("execute_plan", plan=plan)
    
    if execution_result["success"]:
        print("Plan executed successfully!")
        print(f"Results: {execution_result['results']}")
    else:
        print(f"Error executing plan: {execution_result['error']}")
else:
    print(f"Error generating plan: {plan_result['error']}")
```

## Troubleshooting

- **Import Errors**: If you encounter import errors, ensure that all required dependencies are installed.
- **Tool Not Found**: If a tool is not found, check that it was properly registered and that the import was successful.
- **MCP Server Integration**: If tools are not appearing in the MCP server, check that the server was properly initialized before registering tools.
- **Multiple Registrations**: Avoid registering tools multiple times, as this can lead to unexpected behavior. 