# OpenManus Integration for Hanx

This package adapts OpenManus capabilities for the Hanx project, providing enhanced functionality for both the `.cursorrules` interface and the MCP server architecture.

## Overview

OpenManus is an open-source AI agent framework that provides a flexible and extensible system for building AI agents. This integration adapts OpenManus capabilities to work within the Hanx project, enhancing the existing multi-agent system with additional tools and workflows.

## Components

### Tool Collection (`tool_collection.py`)

The Tool Collection module provides a framework for managing and orchestrating tools. It includes:

- `ToolResult`: A class for representing the result of a tool execution
- `Tool`: A base class for all tools
- `ToolCollection`: A class for managing and orchestrating tools

### Python Execute (`python_execute.py`)

The Python Execute module provides a secure environment for executing Python code. It includes:

- `PythonExecute`: A class for executing Python code in a secure environment
- `CodeValidator`: A class for validating Python code against security constraints

### Flow Management (`flow_management.py`)

The Flow Management module provides a framework for managing complex workflows. It includes:

- `FlowType`: An enumeration of flow types (sequential, parallel, conditional, etc.)
- `FlowStep`: A class representing a step in a flow
- `FlowResult`: A class representing the result of a flow execution
- `FlowManager`: A class for managing and executing flows
- `FlowManagerTool`: A tool for managing flows via the MCP server

### Planning (`planning.py`)

The Planning module enhances planning capabilities using LLMs. It includes:

- `PlanStep`: A class representing a step in a plan
- `Plan`: A class representing a generated plan
- `PlanningEnhancer`: A class for generating and executing plans
- `PlanningTool`: A tool for enhanced planning via the MCP server

### Integration (`integration.py`)

The Integration module provides a unified interface for registering OpenManus tools with both the `.cursorrules` interface and the MCP server. It includes:

- `OpenManusIntegration`: A class for managing the integration of OpenManus tools
- Helper functions for registering tools with the MCP server and `.cursorrules` interface

## Usage

### With MCP Server

The OpenManus tools are automatically registered with the MCP server during initialization:

```python
# In hanx_mcp/mcp_server.py
from hanx_tools.openmanus import integration as openmanus_integration

# In the setup_tools method of HanxMCPServer
try:
    logger.info("Registering OpenManus tools with MCP server")
    openmanus_integration.register_with_mcp_server(self)
    logger.info("Successfully registered OpenManus tools")
except Exception as e:
    logger.error(f"Error registering OpenManus tools: {e}")
```

### With .cursorrules Interface

The OpenManus tools are automatically registered with the `.cursorrules` interface:

```python
# In .cursorrules
try:
    from hanx_tools.openmanus.integration import register_with_cursorrules
    register_with_cursorrules(globals())
except ImportError:
    print("OpenManus integration not available")
```

## Testing

The OpenManus integration includes a test suite to ensure proper functionality:

```bash
python -m unittest discover -s hanx_tools/openmanus/tests
```

## Dependencies

The OpenManus integration requires the following dependencies:

- Python 3.8+
- aiohttp
- pydantic
- loguru
- asyncio

These dependencies are included in the project's `requirements.txt` file.

## Development

To contribute to the OpenManus integration, follow these guidelines:

1. Add new tools by extending the `Tool` base class
2. Register new tools in the `OpenManusIntegration` class
3. Add tests for new tools in the `tests` directory
4. Update documentation in this README and in `hanx_learned.md`

## Next Steps

The following enhancements are planned for the OpenManus integration:

1. **Browser Capabilities**: Install the browser-use package to enable browser capabilities
2. **Comprehensive Tests**: Create more comprehensive tests for each tool
3. **Documentation**: Add examples of using the OpenManus tools
4. **Integration**: Integrate with existing Hanx tools to enhance functionality
5. **Additional Tools**: Add more tools from the OpenManus project as needed

## License

This package is licensed under the MIT License. 