"""
Utility functions for handling Windows paths in a cross-platform manner.
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

def list_files_with_pattern(directory: Union[str, pathlib.Path], pattern: str) -> List[str]:
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