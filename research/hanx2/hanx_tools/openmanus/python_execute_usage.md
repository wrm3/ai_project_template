# OpenManus Python Execute Module

The `python_execute.py` module provides a secure Python execution environment for the Hanx project. It enables the execution of Python code in a sandboxed environment with controlled access to modules and builtins, protecting against potentially harmful operations.

## Basic Usage

### Using the python_execute Function (via .cursorrules)

```python
# Execute simple Python code
result = python_execute("""
import math
result = math.sqrt(16) + math.pi
""")

if result["success"]:
    print(f"Result: {result['result']}")
    print(f"Output: {result['stdout']}")
else:
    print(f"Error: {result['error']}")
    if "violations" in result:
        print("Security violations:")
        for violation in result["violations"]:
            print(f"  - {violation}")

# Execute code with custom parameters
result = python_execute(
    """
import numpy as np
result = np.mean([1, 2, 3, 4, 5])
""",
    allowed_modules={"numpy", "math", "random"},
    timeout=5,
    max_output_length=5000
)

if result["success"]:
    print(f"Result: {result['result']}")
else:
    print(f"Error: {result['error']}")
```

### Using the PythonExecute Class Directly

```python
from hanx_tools.openmanus.python_execute import PythonExecute, CodeValidator

# Create a custom validator
validator = CodeValidator(
    allowed_modules={"math", "random", "numpy"},
    allowed_builtins={"print", "len", "range", "list", "dict", "set"}
)

# Create a Python executor with custom settings
executor = PythonExecute(
    validator=validator,
    timeout=10,
    max_memory=200 * 1024 * 1024  # 200 MB
)

# Validate code without executing it
code = """
import os
os.system('rm -rf /')
"""
violations = executor.validate_code(code)
if violations:
    print("Security violations detected:")
    for violation in violations:
        print(f"  - {violation}")
else:
    print("Code is safe to execute")

# Execute safe code
safe_code = """
import math
result = sum([math.factorial(i) for i in range(5)])
"""
result = executor.execute_code(safe_code)
if result["success"]:
    print(f"Result: {result['result']}")
else:
    print(f"Error: {result['error']}")
```

## Security Features

The Python Execute module includes several security features:

1. **Code Validation**: All code is validated using an AST visitor that checks for potentially dangerous operations.
2. **Restricted Modules**: Only a predefined set of safe modules can be imported.
3. **Restricted Builtins**: Only a predefined set of safe builtins can be used.
4. **Execution Timeout**: Code execution is limited to a configurable timeout.
5. **Memory Limits**: Memory usage is limited to a configurable maximum.

### Default Allowed Modules

```python
ALLOWED_MODULES = {
    'math', 'random', 'datetime', 'collections', 'itertools',
    'functools', 'operator', 're', 'json', 'csv', 'io',
    'typing', 'enum', 'dataclasses'
}
```

### Default Allowed Builtins

```python
ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
    'chr', 'complex', 'dict', 'divmod', 'enumerate', 'filter', 'float',
    'format', 'frozenset', 'hash', 'hex', 'int', 'isinstance', 'issubclass',
    'iter', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 'ord',
    'pow', 'print', 'range', 'repr', 'reversed', 'round', 'set', 'slice',
    'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
}
```

## Parameters

### python_execute Function

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `code` | `str` | Python code to execute | (required) |
| `allowed_modules` | `Set[str]` | Set of module names that are allowed to be imported | `ALLOWED_MODULES` |
| `allowed_builtins` | `Set[str]` | Set of builtin names that are allowed to be used | `ALLOWED_BUILTINS` |
| `timeout` | `int` | Maximum execution time in seconds | `10` |
| `max_output_length` | `int` | Maximum length of captured output | `10000` |

### PythonExecute Class

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `validator` | `CodeValidator` | The code validator to use | `None` (creates default) |
| `timeout` | `int` | Maximum execution time in seconds | `30` |
| `max_memory` | `int` | Maximum memory usage in bytes | `100 * 1024 * 1024` (100 MB) |
| `allowed_modules` | `List[str]` | List of allowed modules | `None` (uses default) |

## Return Value

The `python_execute` function and `execute_code` method return a dictionary with the following keys:

### Success Case

```python
{
    "success": True,
    "result": <result variable value>,
    "stdout": <captured standard output>,
    "stderr": <captured standard error>
}
```

### Error Case

```python
{
    "success": False,
    "error": <error message>,
    "traceback": <exception traceback>,  # Only if execution failed
    "violations": <list of security violations>,  # Only if validation failed
    "stdout": <captured standard output>,  # If available
    "stderr": <captured standard error>  # If available
}
```

## Integration with MCP Server

The PythonExecute class can be integrated with the MCP server through the OpenManus integration module:

```python
from hanx_tools.openmanus.integration import register_with_mcp_server

# Register all OpenManus tools (including PythonExecute) with the MCP server
register_with_mcp_server(mcp_server)
```

## Best Practices

1. **Validate First**: For critical code, validate before executing:

   ```python
   from hanx_tools.openmanus.python_execute import PythonExecute
   
   executor = PythonExecute()
   violations = executor.validate_code(user_code)
   if violations:
       print("Security violations detected:")
       for violation in violations:
           print(f"  - {violation}")
   else:
       result = executor.execute_code(user_code)
   ```

2. **Custom Module Allowlists**: For specific use cases, provide a custom set of allowed modules:

   ```python
   # For data science tasks
   result = python_execute(
       data_science_code,
       allowed_modules={"numpy", "pandas", "matplotlib", "scipy", "math", "random"}
   )
   
   # For text processing tasks
   result = python_execute(
       text_processing_code,
       allowed_modules={"re", "string", "collections", "itertools"}
   )
   ```

3. **Result Variable**: Use a `result` variable to return values from your code:

   ```python
   result = python_execute("""
   import math
   
   # Calculations
   x = math.sqrt(16)
   y = math.pi * 2
   
   # Set the result variable to return the value
   result = {"x": x, "y": y, "sum": x + y}
   """)
   
   if result["success"]:
       print(f"Result: {result['result']}")  # Access the returned dictionary
   ```

4. **Error Handling**: Always check for success and handle errors appropriately:

   ```python
   result = python_execute(user_code)
   if not result["success"]:
       if "violations" in result:
           print("Security violations detected:")
           for violation in result["violations"]:
               print(f"  - {violation}")
       else:
           print(f"Execution error: {result['error']}")
           print(f"Traceback: {result['traceback']}")
   ```

5. **Resource Limits**: Set appropriate timeout and memory limits for your use case:

   ```python
   # For quick calculations
   result = python_execute(quick_code, timeout=1)
   
   # For more complex operations
   result = python_execute(
       complex_code,
       timeout=30,
       max_output_length=50000
   )
   ```

## Example: Data Processing Workflow

```python
def process_data(data):
    # Define the processing code
    code = f"""
import json
import math
from collections import Counter

# Parse the input data
data = json.loads('''{json.dumps(data)}''')

# Process the data
processed = []
for item in data:
    if 'value' in item:
        processed.append({
            'id': item['id'],
            'normalized': item['value'] / 100,
            'squared': math.pow(item['value'], 2)
        })

# Calculate statistics
values = [item['value'] for item in data if 'value' in item]
stats = {{
    'count': len(values),
    'sum': sum(values),
    'mean': sum(values) / len(values) if values else 0,
    'max': max(values) if values else 0,
    'min': min(values) if values else 0
}}

# Count categories
categories = [item.get('category', 'unknown') for item in data]
category_counts = dict(Counter(categories))

# Set the result
result = {{
    'processed': processed,
    'stats': stats,
    'categories': category_counts
}}
"""
    
    # Execute the code
    result = python_execute(code)
    
    if result["success"]:
        return result["result"]
    else:
        print(f"Error processing data: {result['error']}")
        return None

# Example usage
data = [
    {"id": 1, "value": 42, "category": "A"},
    {"id": 2, "value": 73, "category": "B"},
    {"id": 3, "value": 29, "category": "A"},
    {"id": 4, "category": "C"}
]

processed_data = process_data(data)
if processed_data:
    print(f"Processed {len(processed_data['processed'])} items")
    print(f"Statistics: {processed_data['stats']}")
    print(f"Category counts: {processed_data['categories']}")
```

## Troubleshooting

- **Security Violations**: If you encounter security violations, review the list of allowed modules and builtins.
- **Execution Timeout**: If your code times out, increase the timeout parameter or optimize your code.
- **Memory Limits**: If your code exceeds memory limits, increase the max_memory parameter or optimize your code.
- **Module Not Found**: If a module is not found, ensure it's in the allowed_modules list and installed in the environment.
- **Syntax Errors**: If your code has syntax errors, they will be reported in the error message. 