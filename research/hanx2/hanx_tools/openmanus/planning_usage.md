# OpenManus Planning Module

The `planning.py` module provides enhanced planning capabilities for the Hanx project, leveraging the OpenManus planning system. It enables the generation and execution of structured plans using LLMs, with support for different planning strategies.

## Basic Usage

### Using the planning_enhancer Function (via .cursorrules)

```python
# Generate a plan
result = planning_enhancer("generate_plan", 
    goal="Scrape data from a website, analyze it with an LLM, and store the results in a database",
    available_tools=[
        {"name": "browser_use", "description": "Web browsing and interaction capabilities"},
        {"name": "llm_query", "description": "Query an LLM with a prompt"},
        {"name": "mysql_query", "description": "Execute SQL queries on a MySQL database"}
    ]
)

# Check if the plan was generated successfully
if result["success"]:
    plan = result["plan"]
    print(f"Plan goal: {plan['goal']}")
    print(f"Plan reasoning: {plan['reasoning']}")
    print("Plan steps:")
    for i, step in enumerate(plan["steps"]):
        print(f"  Step {i+1}: {step['tool_name']} - {step['description']}")
else:
    print(f"Error generating plan: {result['error']}")

# Execute a plan
execution_result = planning_enhancer("execute_plan", plan=plan)
if execution_result["success"]:
    print("Plan executed successfully!")
    print(f"Results: {execution_result['results']}")
else:
    print(f"Error executing plan: {execution_result['error']}")
```

### Using the PlanningEnhancer Class Directly

```python
from hanx_tools.openmanus.planning import PlanningEnhancer
from hanx_tools.openmanus.tool_collection import ToolCollection

# Create a tool collection
tool_collection = ToolCollection()

# Register tools with the collection
# ... (register your tools)

# Create a planning enhancer
planning_enhancer = PlanningEnhancer(tool_collection)

# Generate a plan
plan = await planning_enhancer.generate_plan(
    goal="Scrape data from a website, analyze it with an LLM, and store the results in a database"
)

# Execute the plan
result = await planning_enhancer.execute_plan(plan)
```

## Actions

The planning_enhancer function supports the following actions:

| Action | Description | Parameters |
|--------|-------------|------------|
| `generate_plan` | Generate a plan to achieve a goal | `goal` (required): The goal to achieve<br>`available_tools` (optional): List of available tools<br>`context` (optional): Additional context for planning |
| `execute_plan` | Execute a previously generated plan | `plan` (required): The plan to execute<br>`context` (optional): Additional context for execution |

## Plan Structure

A plan consists of the following components:

```json
{
  "goal": "The overall goal of the plan",
  "reasoning": "Reasoning behind the plan structure",
  "steps": [
    {
      "tool_name": "Name of the tool to use",
      "parameters": {
        "param1": "value1",
        "param2": "value2"
      },
      "description": "Description of what this step does",
      "reasoning": "Reasoning behind this step"
    },
    // More steps...
  ]
}
```

## Integration with MCP Server

The planning module can be integrated with the MCP server through the PlanningTool class:

```python
from hanx_tools.openmanus.planning import PlanningTool

# Create a planning tool
planning_tool = PlanningTool()

# Register the tool with the MCP server
server.register_tool("planning_enhancer", planning_tool)
```

## Best Practices

1. **Clear Goals**: Provide clear, specific goals for plan generation
2. **Tool Availability**: Make sure all necessary tools are available and registered
3. **Context Inclusion**: Include relevant context for more effective planning
4. **Error Handling**: Always check for success/error in the result
5. **Plan Validation**: Review generated plans before execution
6. **Incremental Planning**: For complex tasks, consider breaking them into smaller plans

## Example: Web Scraping Workflow

```python
# Generate a plan for web scraping
result = planning_enhancer("generate_plan", 
    goal="Scrape product information from an e-commerce website and save it to a CSV file",
    available_tools=[
        {"name": "browser_use", "description": "Web browsing and interaction capabilities"},
        {"name": "file_processors", "description": "File reading and writing capabilities"}
    ],
    context={
        "website": "https://example.com/products",
        "data_points": ["name", "price", "description", "rating"],
        "output_file": "products.csv"
    }
)

# Execute the plan
if result["success"]:
    execution_result = planning_enhancer("execute_plan", plan=result["plan"])
    if execution_result["success"]:
        print(f"Successfully scraped {len(execution_result['results'])} products")
    else:
        print(f"Error executing plan: {execution_result['error']}")
else:
    print(f"Error generating plan: {result['error']}")
```

## Troubleshooting

- **Missing Tools**: Ensure all required tools are registered with the tool collection
- **Unclear Goals**: If plans are not effective, try providing more specific goals
- **Execution Failures**: Check individual step results for detailed error information
- **LLM Issues**: If planning quality is poor, try adjusting the LLM provider or model
- **Context Limitations**: For complex tasks, provide more detailed context 