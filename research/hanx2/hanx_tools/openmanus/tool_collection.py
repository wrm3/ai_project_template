"""
Tool Collection for Hanx.

This module adapts the OpenManus tool collection system for the Hanx project,
providing tool orchestration and management capabilities for both the .cursorrules
interface and the MCP server architecture.
"""

from typing import Any, Dict, List, Optional, Set, Type, Union
import inspect
import json
import logging
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class ToolResult(BaseModel):
    """Result of a tool execution."""
    success: bool = True
    result: Any = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the result to a dictionary."""
        return {
            "success": self.success,
            "result": self.result,
            "error": self.error
        }
    
    def dict(self) -> Dict[str, Any]:
        """Alias for to_dict() for compatibility with pydantic v2."""
        return self.to_dict()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the result, similar to dict.get()."""
        if key == "success":
            return self.success
        elif key == "result":
            return self.result
        elif key == "error":
            return self.error
        return default

class Tool(BaseModel):
    """
    Base class for all tools.
    
    This class provides a common interface for all tools, with methods
    for running the tool and getting its schema.
    """
    
    name: str
    description: str
    
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    def run(self, **kwargs) -> ToolResult:
        """
        Run the tool with the specified parameters.
        
        Args:
            **kwargs: Parameters for the tool
            
        Returns:
            ToolResult: Result of the operation
        """
        try:
            result = self._run(**kwargs)
            return ToolResult(success=True, result=result)
        except Exception as e:
            logger.error(f"Error running tool {self.name}: {str(e)}")
            return ToolResult(success=False, error=str(e))
    
    def _run(self, **kwargs) -> Any:
        """
        Internal method to run the tool.
        
        This method should be overridden by subclasses.
        
        Args:
            **kwargs: Parameters for the tool
            
        Returns:
            Any: Result of the operation
        """
        raise NotImplementedError("Tool._run() must be implemented by subclasses")
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the schema for the tool.
        
        Returns:
            Dict[str, Any]: Schema for the tool
        """
        # Get the signature of the _run method
        sig = inspect.signature(self._run)
        
        # Create a schema for the parameters
        parameters = {}
        for name, param in sig.parameters.items():
            if name == "self":
                continue
                
            # Get the annotation if available
            annotation = param.annotation
            if annotation is inspect.Parameter.empty:
                annotation = Any
                
            # Get the default value if available
            default = None
            if param.default is not inspect.Parameter.empty:
                default = param.default
                
            # Add the parameter to the schema
            parameters[name] = {
                "type": str(annotation),
                "default": default
            }
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": parameters
        }

class ToolCollection:
    """
    A collection of tools for orchestration and management.
    
    This class provides a registry for tools and methods for discovering,
    registering, and executing tools.
    """
    
    def __init__(self, *tools: Tool):
        """
        Initialize the ToolCollection.
        
        Args:
            *tools: Tools to add to the collection
        """
        self._tools: Dict[str, Tool] = {}
        
        # Register the provided tools
        for tool in tools:
            self.register_tool(tool)
    
    def register_tool(self, tool: Tool) -> None:
        """
        Register a tool with the collection.
        
        Args:
            tool: The tool to register
        """
        if tool.name in self._tools:
            logger.warning(f"Tool {tool.name} already registered. Overwriting.")
            
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")
    
    def unregister_tool(self, tool_name: str) -> None:
        """
        Unregister a tool from the collection.
        
        Args:
            tool_name: The name of the tool to unregister
        """
        if tool_name in self._tools:
            del self._tools[tool_name]
            logger.info(f"Unregistered tool: {tool_name}")
        else:
            logger.warning(f"Tool {tool_name} not found in collection.")
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """
        Get a tool from the collection.
        
        Args:
            tool_name: The name of the tool to get
            
        Returns:
            Optional[Tool]: The tool, or None if not found
        """
        return self._tools.get(tool_name)
    
    def list_tools(self) -> List[str]:
        """
        List all tools in the collection.
        
        Returns:
            List[str]: List of tool names
        """
        return list(self._tools.keys())
    
    def get_tool_schemas(self) -> Dict[str, Dict[str, Any]]:
        """
        Get schemas for all tools in the collection.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of tool schemas
        """
        return {name: tool.get_schema() for name, tool in self._tools.items()}
    
    def run_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """
        Run a tool with the specified parameters.
        
        Args:
            tool_name: The name of the tool to run
            **kwargs: Parameters for the tool
            
        Returns:
            ToolResult: Result of the operation
        """
        tool = self.get_tool(tool_name)
        if tool is None:
            return ToolResult(
                success=False,
                error=f"Tool {tool_name} not found. Available tools: {', '.join(self.list_tools())}"
            )
            
        return tool.run(**kwargs)
    
    def run_tool_chain(self, chain: List[Dict[str, Any]]) -> List[ToolResult]:
        """
        Run a chain of tools.
        
        Args:
            chain: List of tool specifications, each with a "tool" key and optional parameters
            
        Returns:
            List[ToolResult]: List of results from each tool in the chain
        """
        results = []
        
        for step in chain:
            tool_name = step.get("tool")
            if tool_name is None:
                results.append(ToolResult(
                    success=False,
                    error="Tool specification missing 'tool' key"
                ))
                continue
                
            # Get parameters for the tool
            params = {k: v for k, v in step.items() if k != "tool"}
            
            # Run the tool
            result = self.run_tool(tool_name, **params)
            results.append(result)
            
            # Stop the chain if a tool fails
            if not result.success:
                break
        
        return results

# MCP Server Interface

class ToolCollectionTool(Tool):
    """
    A tool for managing and orchestrating tools.
    
    This tool provides an interface for the MCP server to interact with
    the ToolCollection.
    """
    
    name: str = "tool_collection"
    description: str = "A tool for managing and orchestrating tools"
    collection: Optional[ToolCollection] = None
    
    def __init__(self, collection: Optional[ToolCollection] = None):
        """
        Initialize the ToolCollectionTool.
        
        Args:
            collection: The tool collection to use
        """
        super().__init__()
        self.collection = collection or ToolCollection()
    
    def _run(self, action: str, **kwargs) -> Any:
        """
        Run the tool with the specified parameters.
        
        Args:
            action: The action to perform
            **kwargs: Parameters for the action
            
        Returns:
            Any: Result of the operation
        """
        if action == "list_tools":
            return self.collection.list_tools()
        elif action == "get_tool_schemas":
            return self.collection.get_tool_schemas()
        elif action == "run_tool":
            tool_name = kwargs.pop("tool_name", None)
            if tool_name is None:
                raise ValueError("Missing required parameter: tool_name")
                
            return self.collection.run_tool(tool_name, **kwargs).to_dict()
        elif action == "run_tool_chain":
            chain = kwargs.pop("chain", None)
            if chain is None:
                raise ValueError("Missing required parameter: chain")
                
            return [result.to_dict() for result in self.collection.run_tool_chain(chain)]
        else:
            raise ValueError(f"Unknown action: {action}")

# Synchronous wrapper for use in .cursorrules

def tool_collection(action: str, **kwargs) -> Dict[str, Any]:
    """
    Synchronous wrapper for the ToolCollection.
    
    This function is used by the .cursorrules interface to interact with
    the ToolCollection.
    
    Args:
        action: The action to perform
        **kwargs: Parameters for the action
        
    Returns:
        Dict[str, Any]: Result of the operation
    """
    # Create a singleton tool collection
    if not hasattr(tool_collection, "_collection"):
        tool_collection._collection = ToolCollection()
        
    # Create a tool for the collection
    tool = ToolCollectionTool(tool_collection._collection)
    
    try:
        result = tool._run(action, **kwargs)
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"Error in tool_collection: {str(e)}")
        return {"success": False, "error": str(e)}


def run_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """
    Run a tool from the collection.
    
    This function is used to run a tool from the collection.
    
    Args:
        tool_name: The name of the tool to run
        **kwargs: Parameters for the tool
        
    Returns:
        Dict[str, Any]: Result of the operation
    """
    # Create a singleton tool collection
    if not hasattr(run_tool, "_collection"):
        run_tool._collection = ToolCollection()
        
        # Register tools
        try:
            from .python_execute import PythonExecute
            run_tool._collection.register_tool(PythonExecute())
        except ImportError:
            logger.warning("PythonExecute not available")
        
        try:
            from .browser_use import BrowserUseTool
            run_tool._collection.register_tool(BrowserUseTool())
        except ImportError:
            logger.warning("BrowserUseTool not available")
        
        try:
            from .planning import PlanningTool
            run_tool._collection.register_tool(PlanningTool())
        except ImportError:
            logger.warning("PlanningTool not available")
        
        try:
            from .flow_management import FlowManagerTool
            run_tool._collection.register_tool(FlowManagerTool())
        except ImportError:
            logger.warning("FlowManagerTool not available")
    
    # Run the tool
    return run_tool._collection.run_tool(tool_name, **kwargs).to_dict() 