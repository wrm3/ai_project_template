# OpenManus Flow Management Module

The `flow_management.py` module provides workflow management capabilities for the Hanx project, enabling the execution of complex, multi-step tasks with different execution patterns. It supports sequential, parallel, conditional, planning, and retry flows.

## Basic Usage

### Using the flow_manager Function (via .cursorrules)

```python
# Define a sequential flow with multiple steps
result = flow_manager("execute_flow", 
    flow_type="sequential",
    steps=[
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
            "tool_name": "browser_use",
            "parameters": {
                "action": "close"
            }
        }
    ]
)

if result["success"]:
    print("Flow executed successfully!")
    for i, step_result in enumerate(result["results"]):
        print(f"Step {i+1} result: {step_result}")
else:
    print(f"Error executing flow: {result['error']}")
```

### Using the FlowManager Class Directly

```python
from hanx_tools.openmanus.flow_management import FlowManager, FlowType, FlowStep
from hanx_tools.openmanus.tool_collection import ToolCollection
import asyncio

async def run_flow():
    # Create a tool collection
    tool_collection = ToolCollection()
    
    # Register tools with the collection
    # ... (register your tools)
    
    # Create a flow manager
    flow_manager = FlowManager(tool_collection)
    
    # Define steps
    steps = [
        FlowStep(
            tool_name="browser_use",
            parameters={
                "action": "navigate",
                "url": "https://example.com"
            }
        ),
        FlowStep(
            tool_name="browser_use",
            parameters={
                "action": "extract_text",
                "selector": "h1"
            }
        )
    ]
    
    # Execute a sequential flow
    result = await flow_manager.execute_flow(
        flow_type=FlowType.SEQUENTIAL,
        steps=steps,
        context={"session_id": "12345"}
    )
    
    if result.success:
        print("Flow executed successfully!")
        for i, step_result in enumerate(result.results):
            print(f"Step {i+1} result: {step_result}")
    else:
        print(f"Error executing flow: {result.error}")

# Run the async function
asyncio.run(run_flow())
```

## Flow Types

The Flow Management module supports the following flow types:

| Flow Type | Description | Use Case |
|-----------|-------------|----------|
| `SEQUENTIAL` | Execute steps in sequence | When steps depend on previous steps |
| `PARALLEL` | Execute steps in parallel | When steps can be executed independently |
| `CONDITIONAL` | Execute steps based on conditions | When steps should only be executed if certain conditions are met |
| `PLANNING` | Use planning to determine steps | When the steps need to be dynamically determined |
| `RETRY` | Retry steps on failure | When steps might fail and should be retried |

## Flow Step Structure

A flow step is defined with the following structure:

```python
{
    "tool_name": "name_of_tool",  # Required: The name of the tool to use
    "parameters": {               # Optional: Parameters for the tool
        "param1": "value1",
        "param2": "value2"
    },
    "condition": "context['key'] == 'value'",  # Optional: Python expression for conditional execution
    "retry_count": 0,             # Optional: Current retry count (usually 0)
    "max_retries": 3,             # Optional: Maximum number of retries
    "retry_delay": 1.0            # Optional: Delay between retries in seconds
}
```

## Flow Result Structure

A flow execution result has the following structure:

```python
{
    "success": True,              # Whether the flow executed successfully
    "results": [                  # List of results from each step
        {
            "success": True,
            "result": "Step 1 result"
        },
        {
            "success": True,
            "result": "Step 2 result"
        }
    ],
    "error": None                 # Error message if the flow failed
}
```

## Flow Types in Detail

### Sequential Flow

Sequential flows execute steps one after another. Each step waits for the previous step to complete before starting.

```python
result = flow_manager("execute_flow", 
    flow_type="sequential",
    steps=[
        {"tool_name": "tool1", "parameters": {"param1": "value1"}},
        {"tool_name": "tool2", "parameters": {"param2": "value2"}},
        {"tool_name": "tool3", "parameters": {"param3": "value3"}}
    ]
)
```

### Parallel Flow

Parallel flows execute all steps simultaneously. The flow completes when all steps have completed.

```python
result = flow_manager("execute_flow", 
    flow_type="parallel",
    steps=[
        {"tool_name": "tool1", "parameters": {"param1": "value1"}},
        {"tool_name": "tool2", "parameters": {"param2": "value2"}},
        {"tool_name": "tool3", "parameters": {"param3": "value3"}}
    ]
)
```

### Conditional Flow

Conditional flows execute steps only if their condition evaluates to True. The condition is a Python expression that can reference the context.

```python
result = flow_manager("execute_flow", 
    flow_type="conditional",
    steps=[
        {
            "tool_name": "tool1", 
            "parameters": {"param1": "value1"},
            "condition": "True"  # Always execute
        },
        {
            "tool_name": "tool2", 
            "parameters": {"param2": "value2"},
            "condition": "context.get('key') == 'value'"  # Only execute if condition is met
        }
    ],
    context={"key": "value"}
)
```

### Planning Flow

Planning flows use a planning agent to determine the steps to execute. The planning agent is a tool that generates a plan based on the initial steps and context.

```python
result = flow_manager("execute_flow", 
    flow_type="planning",
    steps=[
        {
            "tool_name": "planning", 
            "parameters": {
                "goal": "Scrape data from a website",
                "available_tools": ["browser_use", "python_execute"]
            }
        }
    ],
    context={"website": "https://example.com"}
)
```

### Retry Flow

Retry flows automatically retry steps that fail, up to a maximum number of retries with a configurable delay between retries.

```python
result = flow_manager("execute_flow", 
    flow_type="retry",
    steps=[
        {
            "tool_name": "tool1", 
            "parameters": {"param1": "value1"},
            "max_retries": 3,
            "retry_delay": 2.0
        }
    ]
)
```

## Context Usage

The context is a dictionary that can be used to share data between steps. It is passed to each step and can be modified by steps.

```python
result = flow_manager("execute_flow", 
    flow_type="sequential",
    steps=[
        {
            "tool_name": "browser_use",
            "parameters": {
                "action": "navigate",
                "url": "https://example.com"
            }
        },
        {
            "tool_name": "python_execute",
            "parameters": {
                "code": """
                # Access the context
                website = context.get('website', 'unknown')
                
                # Modify the context
                context['processed'] = True
                context['data'] = {'title': 'Example Website'}
                
                # Return a result
                result = f"Processed {website}"
                """
            }
        }
    ],
    context={"website": "https://example.com"}
)
```

## Integration with MCP Server

The FlowManagerTool class can be integrated with the MCP server through the OpenManus integration module:

```python
from hanx_tools.openmanus.integration import register_with_mcp_server

# Register all OpenManus tools (including FlowManagerTool) with the MCP server
register_with_mcp_server(mcp_server)
```

## Best Practices

1. **Step Granularity**: Keep steps focused on a single task for better error handling and reusability:

   ```python
   # Good: Focused steps
   steps = [
       {"tool_name": "browser_use", "parameters": {"action": "navigate", "url": "https://example.com"}},
       {"tool_name": "browser_use", "parameters": {"action": "extract_text", "selector": "h1"}},
       {"tool_name": "browser_use", "parameters": {"action": "close"}}
   ]
   
   # Bad: Monolithic step
   steps = [
       {"tool_name": "python_execute", "parameters": {"code": """
           # Do everything in one step
           # Navigate, extract text, close browser
       """}}
   ]
   ```

2. **Error Handling**: Use retry flows for operations that might fail temporarily:

   ```python
   steps = [
       {
           "tool_name": "browser_use", 
           "parameters": {"action": "navigate", "url": "https://example.com"},
           "max_retries": 3,
           "retry_delay": 2.0
       }
   ]
   ```

3. **Context Management**: Use the context to share data between steps:

   ```python
   # Step 1: Extract data
   {
       "tool_name": "browser_use",
       "parameters": {"action": "extract_text", "selector": "h1"}
   }
   
   # Step 2: Process data from context
   {
       "tool_name": "python_execute",
       "parameters": {
           "code": """
           # Get the result from the previous step
           previous_result = context.get('results', [{}])[-1].get('result', {})
           
           # Process the data
           text = previous_result.get('text', '')
           result = f"Processed: {text.upper()}"
           """
       }
   }
   ```

4. **Flow Type Selection**: Choose the appropriate flow type for your use case:

   - Use `SEQUENTIAL` for steps that depend on previous steps
   - Use `PARALLEL` for independent steps that can run simultaneously
   - Use `CONDITIONAL` when steps should only run under certain conditions
   - Use `PLANNING` when steps need to be determined dynamically
   - Use `RETRY` for steps that might fail temporarily

5. **Resource Management**: Close resources (like browsers) when done:

   ```python
   steps = [
       {"tool_name": "browser_use", "parameters": {"action": "navigate", "url": "https://example.com"}},
       {"tool_name": "browser_use", "parameters": {"action": "extract_text", "selector": "h1"}},
       # Always include a cleanup step
       {"tool_name": "browser_use", "parameters": {"action": "close"}}
   ]
   ```

## Example: Web Scraping Workflow

```python
def scrape_website(url, selectors):
    # Define the flow steps
    steps = [
        # Step 1: Navigate to the website
        {
            "tool_name": "browser_use",
            "parameters": {
                "action": "navigate",
                "url": url
            },
            "max_retries": 3,
            "retry_delay": 2.0
        }
    ]
    
    # Add steps for each selector
    for selector_name, selector in selectors.items():
        steps.append({
            "tool_name": "browser_use",
            "parameters": {
                "action": "extract_text",
                "selector": selector
            },
            "condition": "context.get('results', [{}])[-1].get('success', False)"  # Only if navigation succeeded
        })
    
    # Add cleanup step
    steps.append({
        "tool_name": "browser_use",
        "parameters": {
            "action": "close"
        }
    })
    
    # Execute the flow
    result = flow_manager("execute_flow", 
        flow_type="sequential",
        steps=steps,
        context={"url": url}
    )
    
    if result["success"]:
        # Process the results
        data = {}
        for i, (selector_name, _) in enumerate(selectors.items()):
            # Skip the navigation result (i=0) and cleanup result (i=len(selectors)+1)
            if 0 < i <= len(selectors):
                data[selector_name] = result["results"][i].get("text", "")
        
        return {"success": True, "data": data}
    else:
        return {"success": False, "error": result["error"]}

# Example usage
result = scrape_website(
    "https://example.com",
    {
        "title": "h1",
        "description": "meta[name='description']",
        "content": "#main-content"
    }
)

if result["success"]:
    print(f"Scraped data: {result['data']}")
else:
    print(f"Error: {result['error']}")
```

## Troubleshooting

- **Tool Not Found**: If a tool is not found, ensure it's registered with the tool collection.
- **Condition Evaluation Error**: If a condition fails to evaluate, check the syntax and ensure all referenced variables are in the context.
- **Planning Tool Not Available**: If using a planning flow, ensure the planning tool is registered.
- **Parallel Execution Issues**: If parallel execution fails, check for resource contention or race conditions.
- **Context Access**: If steps can't access context data, ensure the data is being properly stored in the context. 