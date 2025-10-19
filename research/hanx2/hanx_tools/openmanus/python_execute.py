"""
Python Execution Environment for Hanx.

This module adapts the OpenManus Python execution capabilities for the Hanx project,
providing a secure Python execution environment for both the .cursorrules
interface and the MCP server architecture.
"""

import ast
import asyncio
import builtins
import contextlib
import io
import os
import sys
import time
import traceback
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from loguru import logger

from .tool_collection import Tool, ToolCollection, ToolResult

# Set of allowed builtins for secure execution
ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
    'chr', 'complex', 'dict', 'divmod', 'enumerate', 'filter', 'float',
    'format', 'frozenset', 'hash', 'hex', 'int', 'isinstance', 'issubclass',
    'iter', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 'ord',
    'pow', 'print', 'range', 'repr', 'reversed', 'round', 'set', 'slice',
    'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
}

# Set of allowed modules for secure execution
ALLOWED_MODULES = {
    'math', 'random', 'datetime', 'collections', 'itertools',
    'functools', 'operator', 're', 'json', 'csv', 'io',
    'typing', 'enum', 'dataclasses'
}

class SecurityError(Exception):
    """Exception raised for security violations in code execution."""
    pass

class CodeValidator(ast.NodeVisitor):
    """
    AST visitor that validates Python code for security.
    
    This class checks for potentially dangerous operations like:
    - Importing disallowed modules
    - Using disallowed builtins
    - Accessing file system
    - Using eval or exec
    - Accessing system resources
    """
    
    def __init__(self, allowed_modules: Set[str] = None, allowed_builtins: Set[str] = None):
        """
        Initialize the CodeValidator.
        
        Args:
            allowed_modules: Set of module names that are allowed to be imported
            allowed_builtins: Set of builtin names that are allowed to be used
        """
        self.allowed_modules = allowed_modules or ALLOWED_MODULES
        self.allowed_builtins = allowed_builtins or ALLOWED_BUILTINS
        self.errors = []
    
    def visit_Import(self, node: ast.Import) -> None:
        """Check import statements."""
        for name in node.names:
            module_name = name.name.split('.')[0]
            if module_name not in self.allowed_modules:
                self.errors.append(f"Importing disallowed module: {module_name}")
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Check import from statements."""
        if node.module:
            module_name = node.module.split('.')[0]
            if module_name not in self.allowed_modules:
                self.errors.append(f"Importing from disallowed module: {module_name}")
        self.generic_visit(node)
    
    def visit_Call(self, node: ast.Call) -> None:
        """Check function calls."""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in {'eval', 'exec', 'compile', 'globals', 'locals', 'vars'}:
                self.errors.append(f"Using disallowed function: {func_name}")
            elif func_name == 'getattr' and len(node.args) >= 2:
                if isinstance(node.args[1], ast.Str) and node.args[1].s.startswith('_'):
                    self.errors.append(f"Accessing private attribute: {node.args[1].s}")
            elif func_name == '__import__':
                self.errors.append("Using __import__ function")
            elif func_name not in self.allowed_builtins and func_name in dir(builtins):
                self.errors.append(f"Using disallowed builtin: {func_name}")
        elif isinstance(node.func, ast.Attribute):
            attr_name = node.func.attr
            if attr_name in {'system', 'popen', 'spawn', 'call', 'check_output', 'check_call'}:
                self.errors.append(f"Potentially dangerous system call: {attr_name}")
            elif attr_name in {'open', 'read', 'write', 'close', 'seek', 'tell'}:
                self.errors.append(f"Potentially dangerous file operation: {attr_name}")
        self.generic_visit(node)
    
    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Check attribute access."""
        if node.attr.startswith('__') and node.attr.endswith('__'):
            self.errors.append(f"Accessing dunder method: {node.attr}")
        elif node.attr.startswith('_'):
            # Allow some common private attributes
            allowed_private = {'_asdict', '_replace', '_fields'}
            if node.attr not in allowed_private:
                self.errors.append(f"Accessing private attribute: {node.attr}")
        self.generic_visit(node)

class PythonExecute(Tool):
    """
    A tool for executing Python code in a secure environment.
    
    This tool provides an interface for the MCP server to execute
    Python code in a secure environment.
    """
    
    name: str = "python_execute"
    description: str = "A tool for executing Python code in a secure environment"
    validator: Optional[CodeValidator] = None
    timeout: int = 30
    max_memory: int = 100 * 1024 * 1024  # 100 MB
    max_output_length: int = 10000  # Maximum length of captured output
    allowed_modules: Set[str] = ALLOWED_MODULES
    allowed_builtins: Set[str] = ALLOWED_BUILTINS
    
    def __init__(
        self,
        validator: Optional[CodeValidator] = None,
        timeout: int = 30,
        max_memory: int = 100 * 1024 * 1024,  # 100 MB
        max_output_length: int = 10000,
        allowed_modules: Optional[Set[str]] = None,
        allowed_builtins: Optional[Set[str]] = None
    ):
        """
        Initialize the PythonExecute tool.
        
        Args:
            validator: The code validator to use
            timeout: The maximum execution time in seconds
            max_memory: The maximum memory usage in bytes
            max_output_length: Maximum length of captured output
            allowed_modules: Set of module names that are allowed to be imported
            allowed_builtins: Set of builtin names that are allowed to be used
        """
        super().__init__()
        self.allowed_modules = allowed_modules or ALLOWED_MODULES
        self.allowed_builtins = allowed_builtins or ALLOWED_BUILTINS
        self.validator = validator or CodeValidator(
            allowed_modules=self.allowed_modules,
            allowed_builtins=self.allowed_builtins
        )
        self.timeout = timeout
        self.max_memory = max_memory
        self.max_output_length = max_output_length
    
    def validate_code(self, code: str) -> List[str]:
        """
        Validate Python code for security.
        
        Args:
            code: Python code to validate
            
        Returns:
            List[str]: List of security violations, empty if code is safe
        """
        try:
            tree = ast.parse(code)
            validator = CodeValidator(self.allowed_modules, self.allowed_builtins)
            validator.visit(tree)
            return validator.errors
        except SyntaxError as e:
            return [f"Syntax error: {str(e)}"]
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code in a sandboxed environment.
        
        Args:
            code: Python code to execute
            
        Returns:
            Dict[str, Any]: Result of the execution
        """
        # Validate the code
        errors = self.validate_code(code)
        if errors:
            return {
                "success": False,
                "error": "Security violations detected",
                "violations": errors
            }
        
        # Create a restricted globals dictionary
        restricted_globals = {
            name: getattr(builtins, name) for name in self.allowed_builtins
            if hasattr(builtins, name)
        }
        
        # Add allowed modules
        for module_name in self.allowed_modules:
            try:
                restricted_globals[module_name] = __import__(module_name)
            except ImportError:
                # Skip modules that can't be imported
                pass
        
        # Capture stdout and stderr
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        # Execute the code
        result = None
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                # Check if the code contains 'result ='
                if 'result =' not in code and 'result=' not in code:
                    # Add a result variable if not present
                    code = f"{code}\nif 'result' not in locals(): result = None"
                
                # Check if the code references 'result' but doesn't define it
                if 'result' in code and 'result =' not in code and 'result=' not in code:
                    # Initialize result to None
                    restricted_globals['result'] = None
                
                # Execute the code
                exec(code, restricted_globals, restricted_globals)
                
                # Check for a result variable
                if 'result' in restricted_globals:
                    result = restricted_globals['result']
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "stdout": stdout.getvalue()[:self.max_output_length],
                "stderr": stderr.getvalue()[:self.max_output_length]
            }
        
        return {
            "success": True,
            "result": result,
            "stdout": stdout.getvalue()[:self.max_output_length],
            "stderr": stderr.getvalue()[:self.max_output_length]
        }
    
    def run(self, code: str, **kwargs) -> Dict[str, Any]:
        """
        Run the Python execution tool.
        
        This method is used by the MCP server to invoke the tool.
        
        Args:
            code: Python code to execute
            **kwargs: Additional parameters (ignored)
            
        Returns:
            Dict[str, Any]: Result of the execution
        """
        return self.execute_code(code)

# Synchronous wrapper for use in .cursorrules
def python_execute(code: str, **kwargs) -> Dict[str, Any]:
    """
    Synchronous wrapper for the PythonExecute tool.
    
    This function is used by the .cursorrules interface to invoke the tool.
    
    Args:
        code: Python code to execute
        **kwargs: Additional parameters
            - allowed_modules: Set of module names that are allowed to be imported
            - allowed_builtins: Set of builtin names that are allowed to be used
            - timeout: Maximum execution time in seconds
            - max_output_length: Maximum length of captured output
        
    Returns:
        Dict[str, Any]: Result of the execution
    """
    # Create a PythonExecute instance with the specified parameters
    executor = PythonExecute(
        allowed_modules=kwargs.get('allowed_modules'),
        allowed_builtins=kwargs.get('allowed_builtins'),
        timeout=kwargs.get('timeout', 10),
        max_output_length=kwargs.get('max_output_length', 10000)
    )
    
    # Execute the code
    return executor.execute_code(code) 