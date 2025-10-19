"""
Utility functions for handling files and paths in a cross-platform manner.
Part of the hanx_tools collection.
"""
import os
import pathlib
from typing import Union, List

def normalize_path(path: Union[str, pathlib.Path]) -> str:
    """
    Normalize a path to use the correct separators for the current OS.
    
    Args:
        path: The path to normalize
        
    Returns:
        str: The normalized path
    """
    return str(pathlib.Path(path))

def list_files(directory: Union[str, pathlib.Path], pattern: str = "*.*") -> List[str]:
    """
    List all files in a directory matching a glob pattern.
    
    Args:
        directory: The directory to search
        pattern: Glob pattern to match (e.g., "*.py")
        
    Returns:
        List[str]: List of matching file paths
    """
    directory = pathlib.Path(directory)
    return [str(p) for p in directory.glob(pattern)]

def is_unc_path(path: Union[str, pathlib.Path]) -> bool:
    """
    Check if a path is a UNC (Universal Naming Convention) path.
    
    Args:
        path: The path to check
        
    Returns:
        bool: True if the path is a UNC path
    """
    path_str = str(path)
    return path_str.startswith('\\\\') or path_str.startswith('//')

def get_file_extension(path: Union[str, pathlib.Path]) -> str:
    """
    Get the file extension from a path.
    
    Args:
        path: The path to get the extension from
        
    Returns:
        str: The file extension (including the dot)
    """
    return os.path.splitext(str(path))[1]

def get_file_name(path: Union[str, pathlib.Path]) -> str:
    """
    Get the file name from a path.
    
    Args:
        path: The path to get the file name from
        
    Returns:
        str: The file name (without the directory)
    """
    return os.path.basename(str(path))

def get_directory_name(path: Union[str, pathlib.Path]) -> str:
    """
    Get the directory name from a path.
    
    Args:
        path: The path to get the directory name from
        
    Returns:
        str: The directory name
    """
    return os.path.dirname(str(path))

def ensure_directory_exists(path: Union[str, pathlib.Path]) -> str:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        path: The directory path to ensure exists
        
    Returns:
        str: The normalized path to the directory
    """
    directory = pathlib.Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return str(directory) 