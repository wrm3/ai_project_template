"""
OpenManus Module
This module provides tools for browser automation, Python code execution, flow management, and planning.
"""

import os
import sys
import importlib.util
import types
from pathlib import Path

# Define the modules that should be exposed
__all__ = [
    'browser_use',
    'flow_management',
    'integration',
    'planning',
    'python_execute',
    'tool_collection'
]

# Create a module proxy for openmanus to handle circular imports
class OpenManusModuleProxy(types.ModuleType):
    """Module proxy for openmanus to handle circular imports."""
    
    def __init__(self):
        super().__init__('openmanus')
        self.__path__ = []
        self.__file__ = __file__
        self.__spec__ = types.SimpleNamespace(
            name='openmanus',
            loader=None,
            origin=__file__,
            submodule_search_locations=[],
            parent=None,
            has_location=True
        )
    
    def __getattr__(self, name):
        # Try to import from the actual module
        try:
            # Get the current directory
            current_dir = Path(__file__).parent
            
            # Check if the module exists
            module_path = current_dir / f"{name}.py"
            if module_path.exists():
                # Import the module
                spec = importlib.util.spec_from_file_location(f"hanx.hanx_tools.openmanus.{name}", str(module_path))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module
            else:
                raise ImportError(f"Cannot import {name} from openmanus")
        except (ImportError, AttributeError):
            raise ImportError(f"Cannot import {name} from openmanus")

# Register the proxy module
sys.modules['hanx.hanx_tools.openmanus.openmanus'] = OpenManusModuleProxy()
sys.modules['openmanus'] = OpenManusModuleProxy()

# Import the modules for convenience
for module_name in __all__:
    try:
        # Use relative imports to avoid circular dependencies
        module_path = Path(__file__).parent / f"{module_name}.py"
        if module_path.exists():
            spec = importlib.util.spec_from_file_location(f"hanx.hanx_tools.openmanus.{module_name}", str(module_path))
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"hanx.hanx_tools.openmanus.{module_name}"] = module
            spec.loader.exec_module(module)
            globals()[module_name] = module
    except Exception as e:
        print(f"Error importing {module_name}: {e}")
