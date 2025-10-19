# OpenManus Tool Collection Module

The `tool_collection.py` module provides tool orchestration and management capabilities for the Hanx project. It enables the registration, discovery, and execution of tools in a unified way, supporting both the `.cursorrules` interface and the MCP server architecture.

## Basic Usage

### Using the tool_collection Function (via .cursorrules)

```python
# List all available tools
result = tool_collection("list_tools")
if result["success"]:
    print(f"Available tools: {result['result']}")

# Get schemas for all tools
schemas_result = tool_collection("get_tool_schemas")
if schemas_result["success"]:
    for tool_name, schema in schemas_result["result"].items():
        print(f"Tool: {tool_name}")
        print(f"  Description: {schema.get('description', 'No description')}")
        print(f"  Parameters: {schema.get('parameters', {})}")

# Run a specific tool
tool_result = tool_collection("run_tool", 
    tool_name="browser_use",
    action="navigate",
    url="https://example.com"
)
if tool_result["success"]:
    print(f"Tool execution result: {tool_result['result']}")
else:
    print(f"Error executing tool: {tool_result['error']}")

# Run a chain of tools
chain_result = tool_collection("run_tool_chain", 
    chain=[
        {
            "tool_name": "browser_use",
            "parameters": {
                "action": "navigate",
                "url": "https://example.com"
            }
        },
        {
            "tool_name": "browser_use",
            "parameters": {
                "action": "extract_text",
                "selector": "h1"
            }
        }
    ]
)
if chain_result["success"]:
    for i, step_result in enumerate(chain_result["result"]):
        print(f"Step {i+1} result: {step_result}")
```

### Using the ToolCollection Class Directly

```python
from hanx_tools.openmanus.tool_collection import ToolCollection, Tool
from hanx_tools.openmanus.browser_use import BrowserUseTool
from hanx_tools.openmanus.python_execute import PythonExecute

# Create a tool collection
collection = ToolCollection()

# Register tools with the collection
collection.register_tool(BrowserUseTool())
collection.register_tool(PythonExecute())

# List all registered tools
tools = collection.list_tools()
print(f"Registered tools: {tools}")

# Get a specific tool
browser_tool = collection.get_tool("browser_use")
if browser_tool:
    # Use the tool directly
    result = browser_tool.run(action="navigate", url="https://example.com")
    print(f"Browser tool result: {result.to_dict()}")

# Run a tool through the collection
result = collection.run_tool("python_execute", code="result = 2 + 2")
print(f"Python execute result: {result.to_dict()}")

# Run a chain of tools
chain = [
    {
        "tool_name": "browser_use",
        "parameters": {
            "action": "navigate",
            "url": "https://example.com"
        }
    },
    {
        "tool_name": "browser_use",
        "parameters": {
            "action": "extract_text",
            "selector": "h1"
        }
    }
]
results = collection.run_tool_chain(chain)
for i, result in enumerate(results):
    print(f"Step {i+1} result: {result.to_dict()}")
```

### Creating a Custom Tool

```python
from hanx_tools.openmanus.tool_collection import Tool, ToolCollection

class CalculatorTool(Tool):
    """A simple calculator tool."""
    
    name = "calculator"
    description = "A tool for performing basic calculations"
    
    def _run(self, operation: str, a: float, b: float) -> float:
        """
        Perform a basic calculation.
        
        Args:
            operation: The operation to perform (add, subtract, multiply, divide)
            a: The first number
            b: The second number
            
        Returns:
            float: The result of the calculation
        """
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("Cannot divide by zero")
            return a / b
        else:
            raise ValueError(f"Unknown operation: {operation}")

# Create a tool collection
collection = ToolCollection()

# Register the custom tool
collection.register_tool(CalculatorTool())

# Use the custom tool
result = collection.run_tool("calculator", operation="add", a=5, b=3)
print(f"5 + 3 = {result.result}")
```

## Core Components

### ToolResult

The `ToolResult` class represents the result of a tool execution:

```python
class ToolResult(BaseModel):
    """Result of a tool execution."""
    success: bool = True
    result: Any = None
    error: Optional[str] = None
```

### Tool

The `Tool` base class provides a common interface for all tools:

```python
class Tool(BaseModel):
    """Base class for all tools."""
    
    name: str
    description: str
    
    def run(self, **kwargs) -> ToolResult:
        """Run the tool with the specified parameters."""
        # ...
    
    def _run(self, **kwargs) -> Any:
        """Internal method to run the tool (must be implemented by subclasses)."""
        raise NotImplementedError("Tool._run() must be implemented by subclasses")
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the schema for the tool."""
        # ...
```

### ToolCollection

The `ToolCollection` class provides a registry for tools and methods for discovering, registering, and executing tools:

```python
class ToolCollection:
    """A collection of tools for orchestration and management."""
    
    def __init__(self, *tools: Tool):
        """Initialize the ToolCollection with optional tools."""
        # ...
    
    def register_tool(self, tool: Tool) -> None:
        """Register a tool with the collection."""
        # ...
    
    def unregister_tool(self, tool_name: str) -> None:
        """Unregister a tool from the collection."""
        # ...
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Get a tool from the collection."""
        # ...
    
    def list_tools(self) -> List[str]:
        """List all tools in the collection."""
        # ...
    
    def get_tool_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Get schemas for all tools in the collection."""
        # ...
    
    def run_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """Run a tool with the specified parameters."""
        # ...
    
    def run_tool_chain(self, chain: List[Dict[str, Any]]) -> List[ToolResult]:
        """Run a chain of tools."""
        # ...
```

## Actions

The tool_collection function supports the following actions:

| Action | Description | Parameters | Return Value |
|--------|-------------|------------|--------------|
| `list_tools` | List all available tools | None | `{"success": true, "result": ["tool1", "tool2", ...]}` |
| `get_tool_schemas` | Get schemas for all tools | None | `{"success": true, "result": {"tool1": {...}, "tool2": {...}, ...}}` |
| `run_tool` | Run a specific tool | `tool_name` (required): The name of the tool to run<br>Additional parameters for the tool | `{"success": true, "result": <tool result>}` |
| `run_tool_chain` | Run a chain of tools | `chain` (required): List of tool configurations | `{"success": true, "result": [<result1>, <result2>, ...]}` |

## Tool Chain Structure

A tool chain is a list of tool configurations, where each configuration is a dictionary with the following structure:

```python
{
    "tool_name": "name_of_tool",  # Required: The name of the tool to run
    "parameters": {               # Optional: Parameters for the tool
        "param1": "value1",
        "param2": "value2"
    }
}
```

## Integration with MCP Server

The ToolCollectionTool class can be integrated with the MCP server through the OpenManus integration module:

```python
from hanx_tools.openmanus.integration import register_with_mcp_server

# Register all OpenManus tools (including ToolCollectionTool) with the MCP server
register_with_mcp_server(mcp_server)
```

## Best Practices

1. **Tool Registration**: Register all tools at the beginning of your application:

   ```python
   from hanx_tools.openmanus.tool_collection import ToolCollection
   from hanx_tools.openmanus.browser_use import BrowserUseTool
   from hanx_tools.openmanus.python_execute import PythonExecute
   
   # Create a shared tool collection
   collection = ToolCollection()
   
   # Register tools
   collection.register_tool(BrowserUseTool())
   collection.register_tool(PythonExecute())
   ```

2. **Error Handling**: Always check for success in tool results:

   ```python
   result = collection.run_tool("browser_use", action="navigate", url="https://example.com")
   if result.success:
       print(f"Successfully navigated to {result.result.get('url')}")
   else:
       print(f"Error: {result.error}")
   ```

3. **Tool Chains**: Use tool chains for complex operations:

   ```python
   # Define a chain of tools
   chain = [
       {
           "tool_name": "browser_use",
           "parameters": {
               "action": "navigate",
               "url": "https://example.com"
           }
       },
       {
           "tool_name": "browser_use",
           "parameters": {
               "action": "extract_text",
               "selector": "h1"
           }
       },
       {
           "tool_name": "python_execute",
           "parameters": {
               "code": """
               # Process the extracted text
               text = context.get('results', [{}])[-1].get('result', {}).get('text', '')
               result = f"Processed: {text.upper()}"
               """
           }
       }
   ]
   
   # Run the chain
   results = collection.run_tool_chain(chain)
   ```

4. **Custom Tools**: Create custom tools for specific tasks:

   ```python
   class DataProcessorTool(Tool):
       """A tool for processing data."""
       
       name = "data_processor"
       description = "A tool for processing data"
       
       def _run(self, data: List[Dict[str, Any]], operation: str) -> Dict[str, Any]:
           """Process the data."""
           if operation == "filter":
               # Filter the data
               return {"filtered": [item for item in data if item.get("value", 0) > 0]}
           elif operation == "transform":
               # Transform the data
               return {"transformed": [{**item, "value_squared": item.get("value", 0) ** 2} for item in data]}
           else:
               raise ValueError(f"Unknown operation: {operation}")
   
   # Register the custom tool
   collection.register_tool(DataProcessorTool())
   ```

5. **Tool Discovery**: Use tool discovery to find available tools:

   ```python
   # List all available tools
   tools = collection.list_tools()
   print(f"Available tools: {tools}")
   
   # Get schemas for all tools
   schemas = collection.get_tool_schemas()
   for tool_name, schema in schemas.items():
       print(f"Tool: {tool_name}")
       print(f"  Description: {schema.get('description', 'No description')}")
       print(f"  Parameters: {schema.get('parameters', {})}")
   ```

## Example: Data Processing Pipeline

```python
def process_data_from_website(url, data_selector):
    # Create a tool collection
    collection = ToolCollection()
    
    # Register tools
    collection.register_tool(BrowserUseTool())
    collection.register_tool(PythonExecute())
    
    # Define the data processing chain
    chain = [
        # Step 1: Navigate to the website
        {
            "tool_name": "browser_use",
            "parameters": {
                "action": "navigate",
                "url": url
            }
        },
        # Step 2: Extract the data
        {
            "tool_name": "browser_use",
            "parameters": {
                "action": "extract_text",
                "selector": data_selector
            }
        },
        # Step 3: Process the data
        {
            "tool_name": "python_execute",
            "parameters": {
                "code": """
                import json
                
                # Get the extracted text
                text = context.get('results', [{}])[-1].get('result', {}).get('text', '')
                
                # Parse the text as JSON
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    # If not JSON, create a simple data structure
                    data = {"text": text}
                
                # Process the data
                if isinstance(data, list):
                    # Calculate statistics for list data
                    result = {
                        "count": len(data),
                        "types": {type(item).__name__ for item in data}
                    }
                elif isinstance(data, dict):
                    # Extract keys for dict data
                    result = {
                        "keys": list(data.keys()),
                        "value_types": {k: type(v).__name__ for k, v in data.items()}
                    }
                else:
                    # Simple analysis for other data
                    result = {
                        "type": type(data).__name__,
                        "length": len(str(data))
                    }
                """
            }
        },
        # Step 4: Close the browser
        {
            "tool_name": "browser_use",
            "parameters": {
                "action": "close"
            }
        }
    ]
    
    # Run the chain
    results = collection.run_tool_chain(chain)
    
    # Check if all steps succeeded
    if all(result.success for result in results):
        # Return the processed data (from step 3)
        return {
            "success": True,
            "data": results[2].result
        }
    else:
        # Find the first error
        for i, result in enumerate(results):
            if not result.success:
                return {
                    "success": False,
                    "error": f"Step {i+1} failed: {result.error}"
                }

# Example usage
result = process_data_from_website(
    "https://example.com/api/data",
    "#data-container"
)

if result["success"]:
    print(f"Processed data: {result['data']}")
else:
    print(f"Error: {result['error']}")
```

## Troubleshooting

- **Tool Not Found**: If a tool is not found, ensure it's registered with the collection.
- **Parameter Errors**: If a tool fails with parameter errors, check the tool's schema for required parameters.
- **Tool Chain Errors**: If a tool chain fails, check the results of each step to identify the failing step.
- **Custom Tool Errors**: If a custom tool fails, ensure the `_run` method is properly implemented and handles all edge cases. 