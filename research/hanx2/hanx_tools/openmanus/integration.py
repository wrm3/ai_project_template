"""
OpenManus Integration for Hanx.

This module provides a unified interface for registering OpenManus tools
with both the .cursorrules interface and the MCP server.
"""

import importlib
import inspect
import os
import sys
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from loguru import logger

from .browser_use import BrowserUseTool
from .flow_management import FlowManagerTool
from .planning import PlanningTool
from .python_execute import PythonExecute
from .tool_collection import Tool, ToolCollection, ToolCollectionTool


class OpenManusIntegration:
    """
    Integration manager for OpenManus tools.
    
    This class provides methods for registering OpenManus tools with
    both the .cursorrules interface and the MCP server.
    """
    
    def __init__(self):
        """Initialize the OpenManusIntegration."""
        self.tools = {}
        
        # Try to import and initialize tools
        try:
            from .browser_use import BrowserUseTool
            self.tools["browser_use"] = BrowserUseTool()
        except ImportError:
            logger.warning("BrowserUseTool not available")
        
        try:
            from .flow_management import FlowManagerTool
            self.tools["flow_manager"] = FlowManagerTool()
        except ImportError:
            logger.warning("FlowManagerTool not available")
        
        try:
            from .planning import PlanningTool
            self.tools["planning_enhancer"] = PlanningTool()
        except ImportError:
            logger.warning("PlanningTool not available")
        
        try:
            from .python_execute import PythonExecute
            self.tools["python_execute"] = PythonExecute()
        except ImportError:
            logger.warning("PythonExecute not available")
        
        try:
            from .tool_collection import ToolCollectionTool
            self.tools["tool_collection"] = ToolCollectionTool()
        except ImportError:
            logger.warning("ToolCollectionTool not available")
        
        # Create a shared tool collection
        self.tool_collection = ToolCollection()
        
        # Register tools with the tool collection
        for name, tool in self.tools.items():
            if isinstance(tool, Tool):
                self.tool_collection.register_tool(tool)
    
    def register_with_mcp_server(self, server) -> None:
        """
        Register OpenManus tools with an MCP server.
        
        Args:
            server: The MCP server to register tools with
        """
        for name, tool in self.tools.items():
            logger.info(f"Registering OpenManus tool {name} with MCP server")
            server.server.register_tool_handler(
                name=name,
                description=tool.__doc__ or f"OpenManus {name} tool",
                parameter_schema={
                    "type": "object",
                    "properties": {
                        "parameters": {
                            "type": "object",
                            "description": "Parameters for the tool"
                        }
                    },
                    "required": ["parameters"]
                },
                handler=lambda tool_call, tool=tool: self._handle_tool_call(tool_call, tool)
            )
    
    async def _handle_tool_call(self, tool_call, tool):
        """
        Handle a tool call from the MCP server.
        
        Args:
            tool_call: The tool call from the MCP server
            tool: The tool to call
        
        Returns:
            The result of the tool call
        """
        try:
            result = await tool.run(**tool_call.parameters)
            return {"content": str(result)}
        except Exception as e:
            logger.error(f"Error running tool: {e}")
            return {"error": str(e)}
    
    def register_with_cursorrules(self, globals_dict: Dict[str, Any]) -> None:
        """
        Register OpenManus tools with the .cursorrules interface.
        
        Args:
            globals_dict: The globals dictionary to register tools with
        """
        # Import the synchronous wrappers
        from .browser_use import browser_use
        from .flow_management import flow_manager
        from .planning import planning_enhancer
        from .python_execute import python_execute
        from .tool_collection import tool_collection
        
        # Register the synchronous wrappers
        globals_dict["browser_use"] = browser_use
        globals_dict["flow_manager"] = flow_manager
        globals_dict["planning_enhancer"] = planning_enhancer
        globals_dict["python_execute"] = python_execute
        globals_dict["tool_collection"] = tool_collection
        
        logger.info("Registered OpenManus tools with .cursorrules interface")
    
    def get_tool(self, name: str) -> Optional[Any]:
        """
        Get a tool by name.
        
        Args:
            name: The name of the tool to get
            
        Returns:
            Optional[Any]: The tool, or None if not found
        """
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """
        List all available tools.
        
        Returns:
            List[str]: List of tool names
        """
        return list(self.tools.keys())
    
    def get_tool_collection(self) -> ToolCollection:
        """
        Get the shared tool collection.
        
        Returns:
            ToolCollection: The shared tool collection
        """
        return self.tool_collection


# Create a singleton instance
_instance = None

def get_integration() -> OpenManusIntegration:
    """
    Get the singleton OpenManusIntegration instance.
    
    Returns:
        OpenManusIntegration: The singleton instance
    """
    global _instance
    if _instance is None:
        _instance = OpenManusIntegration()
    return _instance


def register_with_mcp_server(server) -> None:
    """
    Register OpenManus tools with an MCP server.
    
    Args:
        server: The MCP server to register tools with
    """
    integration = get_integration()
    integration.register_with_mcp_server(server)


def register_with_cursorrules(globals_dict: Dict[str, Any]) -> None:
    """
    Register OpenManus tools with the .cursorrules interface.
    
    Args:
        globals_dict: The globals dictionary to register tools with
    """
    integration = get_integration()
    integration.register_with_cursorrules(globals_dict)


def get_tool(name: str) -> Optional[Any]:
    """
    Get a tool by name.
    
    Args:
        name: The name of the tool to get
        
    Returns:
        Optional[Any]: The tool, or None if not found
    """
    integration = get_integration()
    return integration.get_tool(name)


def list_tools() -> List[str]:
    """
    List all available tools.
    
    Returns:
        List[str]: List of tool names
    """
    integration = get_integration()
    return integration.list_tools()


def get_tool_collection() -> ToolCollection:
    """
    Get the shared tool collection.
    
    Returns:
        ToolCollection: The shared tool collection
    """
    integration = get_integration()
    return integration.get_tool_collection()


def register_with_mcp_sdk(mcp):
    """
    Register OpenManus tools with the MCP SDK.
    
    Args:
        mcp: The FastMCP instance to register tools with
    """
    import logging
    from loguru import logger
    
    # Import OpenManus modules
    try:
        from .browser_use import browser_use
        
        @mcp.tool()
        def browser_use_tool(action: str, url: str = None, selector: str = None, text: str = None, timeout: int = 30):
            """Use browser automation to interact with web pages"""
            try:
                result = browser_use(action, url=url, selector=selector, text=text, timeout=timeout)
                return str(result)
            except Exception as e:
                logger.error(f"Error using browser: {e}")
                return f"Error using browser: {e}"
        
        logger.info("Registered OpenManus tool browser_use with MCP SDK")
    except ImportError as e:
        logger.warning(f"browser-use package not available. Install with 'pip install browser-use'")
    
    try:
        from .flow_management import flow_manager
        
        @mcp.tool()
        def flow_manager_tool(action: str, flow_type: str = None, steps: list = None, flow_id: str = None):
            """Manage complex workflows with sequential, parallel, and conditional execution"""
            try:
                result = flow_manager(action, flow_type=flow_type, steps=steps, flow_id=flow_id)
                return str(result)
            except Exception as e:
                logger.error(f"Error managing flow: {e}")
                return f"Error managing flow: {e}"
        
        logger.info("Registered OpenManus tool flow_manager with MCP SDK")
    except ImportError as e:
        logger.warning(f"Could not import flow_management: {e}")
    
    try:
        from .planning import planning_enhancer
        
        @mcp.tool()
        def planning_enhancer_tool(action: str, goal: str = None, constraints: list = None, plan_id: str = None):
            """Enhance planning capabilities using LLMs"""
            try:
                result = planning_enhancer(action, goal=goal, constraints=constraints, plan_id=plan_id)
                return str(result)
            except Exception as e:
                logger.error(f"Error enhancing planning: {e}")
                return f"Error enhancing planning: {e}"
        
        logger.info("Registered OpenManus tool planning_enhancer with MCP SDK")
    except ImportError as e:
        logger.warning(f"Could not import planning: {e}")
    
    try:
        from .python_execute import python_execute
        
        @mcp.tool()
        def python_execute_tool(action: str, code: str = None, timeout: int = 30):
            """Execute Python code in a secure environment"""
            try:
                result = python_execute(action, code=code, timeout=timeout)
                return str(result)
            except Exception as e:
                logger.error(f"Error executing Python code: {e}")
                return f"Error executing Python code: {e}"
        
        logger.info("Registered OpenManus tool python_execute with MCP SDK")
    except ImportError as e:
        logger.warning(f"Could not import python_execute: {e}")
    
    try:
        from .tool_collection import run_tool
        
        @mcp.tool()
        def tool_collection_tool(tool_name: str, action: str = None, **params):
            """Run a tool from the OpenManus tool collection"""
            try:
                result = run_tool(tool_name, action=action, **params)
                return str(result)
            except Exception as e:
                logger.error(f"Error running tool {tool_name}: {e}")
                return f"Error running tool {tool_name}: {e}"
        
        logger.info("Registered OpenManus tool tool_collection with MCP SDK")
    except ImportError as e:
        logger.warning(f"Could not import tool_collection: {e}")
    
    logger.info("Successfully registered OpenManus tools with MCP SDK") 