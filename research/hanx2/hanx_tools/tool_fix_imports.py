import os
import sys
import ast
import importlib
import subprocess
from pathlib import Path

# List of common packages that might need to be installed
COMMON_PACKAGES = {
    'moviepy': 'moviepy',
    'oracledb': 'oracledb',
    'markdown': 'markdown',
    'docx': 'python-docx',
    'trello': 'py-trello',
    'whisper': 'openai-whisper',
    'pytubefix': 'pytubefix',
    'pydub': 'pydub',
    'youtube_transcript_api': 'youtube-transcript-api',
    'pypdf': 'pypdf',
    'docx2txt': 'docx2txt',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'requests': 'requests',
    'beautifulsoup4': 'beautifulsoup4',
    'selenium': 'selenium',
    'pillow': 'pillow',
    'psycopg2': 'psycopg2-binary',
    'chromadb': 'chromadb',
    'langchain': 'langchain',
    'sentence_transformers': 'sentence-transformers',
}

# Modules that should be imported with relative imports
PROJECT_MODULES = {
    'hanx_agents': ['agent_', 'base_agent'],
    'hanx_apis': ['api_'],
    'hanx_tools': ['tool_', 'path_utils'],
    'hanx_mcp': ['mcp_'],
    'hanx_tools.openmanus': ['browser_use', 'flow_management', 'integration', 'planning', 'python_execute', 'tool_collection'],
}

def get_imports_from_file(file_path):
    """Extract all import statements from a Python file using AST."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        tree = ast.parse(content)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append((name.name, None, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ''
                for name in node.names:
                    imports.append((name.name, module, node.lineno))
        
        return imports, content
    except Exception as e:
        print(f"Error parsing {file_path}: {str(e)}")
        return [], ""

def check_import(module_name):
    """Check if a module can be imported."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def is_project_module(import_name):
    """Check if an import is from our project modules."""
    for module_prefix, submodules in PROJECT_MODULES.items():
        if import_name.startswith(module_prefix):
            return True
        for submodule in submodules:
            if import_name.startswith(submodule):
                return True
    return False

def get_missing_packages():
    """Get a list of missing packages that need to be installed."""
    missing_packages = []
    for module, package in COMMON_PACKAGES.items():
        if not check_import(module):
            missing_packages.append(package)
    return missing_packages

def fix_relative_imports(file_path):
    """Analyze and fix relative imports in a file."""
    imports, content = get_imports_from_file(file_path)
    if not imports:
        return False, "Failed to parse file"
    
    # Get the absolute path and convert to Path object
    abs_path = os.path.abspath(file_path)
    file_path = Path(abs_path)
    
    # Get the project root directory
    project_root = Path(os.getcwd())
    
    # Try to get the relative path within the project
    try:
        rel_path = file_path.relative_to(project_root)
        parent_module = str(rel_path.parent).replace('\\', '.').replace('/', '.')
    except ValueError:
        # If the file is not within the project directory, skip it
        return False, "File not in project directory"
    
    changes = []
    for name, module, lineno in imports:
        # Skip if it's already a relative import
        if module and module.startswith('.'):
            continue
        
        # Check if it's a project module that should be imported relatively
        if module:
            full_import = f"{module}.{name}"
            for proj_module, submodules in PROJECT_MODULES.items():
                # If importing from another module in the same package
                if parent_module.startswith(proj_module) and module.startswith(proj_module):
                    # Calculate relative path
                    rel_depth = len(parent_module.split('.')) - len(proj_module.split('.'))
                    rel_module = '.' * rel_depth + module[len(proj_module)+1:]
                    changes.append((f"from {module} import {name}", f"from {rel_module} import {name}", lineno))
                    break
                
                # If importing a submodule directly
                for submodule in submodules:
                    if module.endswith(submodule) or name == submodule:
                        # Find the appropriate project module
                        for proj_mod, _ in PROJECT_MODULES.items():
                            if module.startswith(proj_mod):
                                rel_depth = len(parent_module.split('.')) - len(proj_mod.split('.'))
                                rel_module = '.' * rel_depth + module[len(proj_mod)+1:]
                                changes.append((f"from {module} import {name}", f"from {rel_module} import {name}", lineno))
                                break
        else:
            # Direct imports
            for proj_module, submodules in PROJECT_MODULES.items():
                for submodule in submodules:
                    if name.startswith(submodule):
                        # Find which project module it belongs to
                        for proj_mod, _ in PROJECT_MODULES.items():
                            if name in [f"{proj_mod}.{sub}" for sub in submodules]:
                                rel_depth = len(parent_module.split('.')) - len(proj_mod.split('.'))
                                rel_name = name[len(proj_mod)+1:]
                                changes.append((f"import {name}", f"from {'.'*rel_depth} import {rel_name}", lineno))
                                break
    
    if changes:
        # Apply changes
        lines = content.split('\n')
        for old, new, lineno in sorted(changes, key=lambda x: x[2], reverse=True):
            if old in lines[lineno-1]:
                lines[lineno-1] = lines[lineno-1].replace(old, new)
        
        new_content = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        return True, f"Fixed {len(changes)} imports"
    
    return False, "No changes needed"

def install_missing_packages():
    """Install missing packages."""
    missing = get_missing_packages()
    if missing:
        print(f"\nInstalling missing packages: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing packages: {e}")
            return False
    return True

def main():
    # Get all Python files in the project
    python_files = []
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    # Check for missing packages
    print("Checking for missing packages...")
    install_missing_packages()
    
    # Fix relative imports
    print("\nAnalyzing and fixing relative imports...")
    fixed_files = []
    for file_path in python_files:
        print(f"Checking {file_path}...")
        fixed, message = fix_relative_imports(file_path)
        if fixed:
            fixed_files.append((file_path, message))
    
    # Print results
    print("\n=== IMPORT FIX RESULTS ===\n")
    
    if not fixed_files:
        print("No files needed import fixes!")
    else:
        for file_path, message in fixed_files:
            print(f"{file_path}: {message}")
    
    # Print summary
    print(f"\nSummary: Fixed imports in {len(fixed_files)} out of {len(python_files)} files.")
    print("\nNext steps:")
    print("1. Run 'python check_imports.py' again to verify all import issues are resolved")
    print("2. Check if any additional packages need to be installed")
    print("3. Update requirements.txt with any new dependencies")

if __name__ == "__main__":
    main() 