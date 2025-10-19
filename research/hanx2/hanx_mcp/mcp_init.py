#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Initialization Script
This script initializes the MCP environment by setting up necessary directories,
checking dependencies, and preparing the system for operation.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/mcp_init.log")
    ]
)
logger = logging.getLogger("mcp_init")

def add_hanx_to_python_path():
    """Add hanx directories to Python path"""
    # Get the current directory (should be hanx_mcp)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the parent directory (should be the project root)
    parent_dir = os.path.dirname(current_dir)
    
    # Add parent directory to path if not already there
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    # Ensure hanx_tools is in the path
    hanx_tools_dir = os.path.join(parent_dir, "hanx_tools")
    if os.path.exists(hanx_tools_dir) and hanx_tools_dir not in sys.path:
        sys.path.insert(0, hanx_tools_dir)
    
    # Ensure hanx_apis is in the path
    hanx_apis_dir = os.path.join(parent_dir, "hanx_apis")
    if os.path.exists(hanx_apis_dir) and hanx_apis_dir not in sys.path:
        sys.path.insert(0, hanx_apis_dir)
    
    # Ensure hanx_agents is in the path
    hanx_agents_dir = os.path.join(parent_dir, "hanx_agents")
    if os.path.exists(hanx_agents_dir) and hanx_agents_dir not in sys.path:
        sys.path.insert(0, hanx_agents_dir)
    
    # Ensure hanx_mcp is in the path
    hanx_mcp_dir = os.path.join(parent_dir, "hanx_mcp")
    if os.path.exists(hanx_mcp_dir) and hanx_mcp_dir not in sys.path:
        sys.path.insert(0, hanx_mcp_dir)
    
    # Log the Python path for debugging
    logger.info(f"Python path: {sys.path}")

def check_environment():
    """Check if all required environment variables are set."""
    required_vars = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in your .env file or environment.")
        return False
    
    return True

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import hanx_agents
        import hanx_tools
        import hanx_apis
        logger.info("All required Python packages are installed.")
        return True
    except ImportError as e:
        logger.error(f"Missing required Python package: {e}")
        logger.error("Please run 'uv pip install -r requirements.txt' to install all dependencies.")
        return False

def setup_directories():
    """Set up necessary directories for the MCP environment."""
    directories = [
        "data",
        "logs",
        "hanx_tools/temp_tools",
        "token_logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    return True

def initialize_mcp():
    """Initialize the MCP environment."""
    logger.info("Initializing MCP environment...")
    
    # Add hanx directories to Python path
    add_hanx_to_python_path()
    
    # Check environment variables
    if not check_environment():
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Set up directories
    if not setup_directories():
        return False
    
    # Create .initialized file to indicate successful initialization
    with open(".initialized", "w") as f:
        f.write("MCP environment initialized successfully.\n")
        f.write(f"Timestamp: {subprocess.check_output('date').decode().strip()}\n")
    
    logger.info("MCP environment initialized successfully.")
    return True

def main():
    """Main function."""
    # Add hanx directories to Python path first
    add_hanx_to_python_path()
    
    if os.path.exists(".initialized"):
        logger.info("MCP environment already initialized.")
        logger.info("To reinitialize, delete the .initialized file and run this script again.")
        return True
    
    return initialize_mcp()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 