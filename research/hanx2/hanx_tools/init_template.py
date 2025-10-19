#!/usr/bin/env python3
"""
GitHub Template Initialization Script

This script initializes a fresh installation of the hanx template from GitHub.
It sets up the required environment, directories, and configuration files.

Usage:
    python hanx_tools/init_template.py

The script will:
1. Create necessary directories
2. Set up environment variables
3. Initialize hanx_learned.md with basic lessons
4. Set up the multi-agent system
5. Install dependencies using UV
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess
import platform
import json

# Define constants
REQUIRED_DIRS = [
    "hanx_tools/temp_tools",
    "hanx_data",
    "hanx_tools/templates",
    "youtube_downloads",
    ".cursor"
]

REQUIRED_FILES = {
    ".env": "sample.env",
    "hanx_learned.md": "hanx_tools/templates/hanx_learned_template.md",
    "hanx_plan.md": "hanx_tools/templates/hanx_plan_template.md"
}

def print_header(message):
    """Print a formatted header message"""
    print("\n" + "=" * 80)
    print(f" {message}")
    print("=" * 80)

def create_directories():
    """Create required directories if they don't exist"""
    print_header("Creating required directories")
    
    for directory in REQUIRED_DIRS:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Creating directory: {directory}")
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            print(f"Directory already exists: {directory}")

def initialize_files():
    """Initialize required files from templates"""
    print_header("Initializing required files")
    
    for target_file, template_file in REQUIRED_FILES.items():
        target_path = Path(target_file)
        template_path = Path(template_file)
        
        if not target_path.exists() and template_path.exists():
            print(f"Creating {target_file} from template {template_file}")
            shutil.copy(template_path, target_path)
        elif not target_path.exists():
            print(f"Warning: Template file {template_file} not found. Skipping {target_file}")
        else:
            print(f"File already exists: {target_file}")

def setup_environment():
    """Set up environment variables"""
    print_header("Setting up environment variables")
    
    env_file = Path(".env")
    sample_env = Path("sample.env")
    
    if not env_file.exists() and sample_env.exists():
        print("Creating .env file from sample.env")
        shutil.copy(sample_env, env_file)
        print("Please edit the .env file to add your API keys")
    elif not env_file.exists():
        print("Warning: sample.env not found. Creating empty .env file")
        with open(env_file, "w") as f:
            f.write("# Environment variables\n")
            f.write("# Add your API keys here\n")
            f.write("OPENAI_API_KEY=\n")
            f.write("ANTHROPIC_API_KEY=\n")
    else:
        print(".env file already exists")

def setup_uv():
    """Set up UV dependency management"""
    print_header("Setting up UV dependency management")
    
    if platform.system() == "Windows":
        uv_script = "uv.bat"
    else:
        uv_script = "./uv.sh"
    
    if not Path(uv_script).exists():
        print(f"Warning: {uv_script} not found. Creating it...")
        if platform.system() == "Windows":
            create_uv_bat()
        else:
            create_uv_sh()
    
    try:
        print("Creating virtual environment")
        if platform.system() == "Windows":
            subprocess.run(["python", "-m", "venv", ".uv-venv"], check=True)
            subprocess.run([uv_script, "setup"], check=True)
        else:
            subprocess.run(["python3", "-m", "venv", ".uv-venv"], check=True)
            subprocess.run(["bash", uv_script, "setup"], check=True)
        print("UV setup completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running UV setup: {e}")
        print("Please run UV setup manually")

def create_uv_bat():
    """Create the uv.bat script for Windows"""
    with open("uv.bat", "w") as f:
        f.write("""@echo off
REM UV Dependency Management Script for Windows
REM This script provides commands for managing dependencies using UV

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="setup" goto setup
if "%1"=="create" goto create
if "%1"=="compile" goto compile
if "%1"=="sync" goto sync
if "%1"=="add" goto add
if "%1"=="activate" goto activate
if "%1"=="run" goto run
goto unknown

:help
echo UV Dependency Management Script
echo.
echo Commands:
echo   setup    - Set up the environment (create venv, compile requirements, install packages)
echo   create   - Create a new virtual environment
echo   compile  - Update the lockfile from requirements.txt
echo   sync     - Install packages from the lockfile
echo   add      - Add a package to requirements.txt and install it
echo   activate - Activate the virtual environment
echo   run      - Run a command in the virtual environment
echo.
goto end

:setup
echo Setting up UV environment...
call :create
call :compile
call :sync
goto end

:create
echo Creating virtual environment...
python -m venv .uv-venv
goto end

:compile
echo Compiling requirements.txt to requirements.lock...
.uv-venv\\Scripts\\python -m pip install uv
.uv-venv\\Scripts\\uv pip compile requirements.txt -o requirements.lock
goto end

:sync
echo Installing packages from requirements.lock...
.uv-venv\\Scripts\\uv pip sync requirements.lock
goto end

:add
if "%2"=="" (
    echo Error: Package name required
    echo Usage: uv.bat add package_name
    goto end
)
echo Adding package %2...
echo %2 >> requirements.txt
call :compile
call :sync
goto end

:activate
echo Activating virtual environment...
echo Run: .uv-venv\\Scripts\\activate
goto end

:run
if "%2"=="" (
    echo Error: Command required
    echo Usage: uv.bat run command
    goto end
)
echo Running command in virtual environment...
.uv-venv\\Scripts\\%2 %3 %4 %5 %6 %7 %8 %9
goto end

:unknown
echo Unknown command: %1
echo Run 'uv.bat help' for usage information
goto end

:end
""")
        print("Created uv.bat script")

def create_uv_sh():
    """Create the uv.sh script for Unix"""
    with open("uv.sh", "w") as f:
        f.write("""#!/bin/bash
# UV Dependency Management Script for Unix
# This script provides commands for managing dependencies using UV

function show_help {
    echo "UV Dependency Management Script"
    echo ""
    echo "Commands:"
    echo "  setup    - Set up the environment (create venv, compile requirements, install packages)"
    echo "  create   - Create a new virtual environment"
    echo "  compile  - Update the lockfile from requirements.txt"
    echo "  sync     - Install packages from the lockfile"
    echo "  add      - Add a package to requirements.txt and install it"
    echo "  activate - Activate the virtual environment"
    echo "  run      - Run a command in the virtual environment"
    echo ""
}

function create_venv {
    echo "Creating virtual environment..."
    python3 -m venv .uv-venv
}

function compile_requirements {
    echo "Compiling requirements.txt to requirements.lock..."
    ./.uv-venv/bin/pip install uv
    ./.uv-venv/bin/uv pip compile requirements.txt -o requirements.lock
}

function sync_packages {
    echo "Installing packages from requirements.lock..."
    ./.uv-venv/bin/uv pip sync requirements.lock
}

function add_package {
    if [ -z "$1" ]; then
        echo "Error: Package name required"
        echo "Usage: ./uv.sh add package_name"
        return 1
    fi
    echo "Adding package $1..."
    echo "$1" >> requirements.txt
    compile_requirements
    sync_packages
}

function activate_venv {
    echo "Activating virtual environment..."
    echo "Run: source ./.uv-venv/bin/activate"
}

function run_command {
    if [ -z "$1" ]; then
        echo "Error: Command required"
        echo "Usage: ./uv.sh run command"
        return 1
    fi
    echo "Running command in virtual environment..."
    ./.uv-venv/bin/python "$@"
}

case "$1" in
    help)
        show_help
        ;;
    setup)
        create_venv
        compile_requirements
        sync_packages
        ;;
    create)
        create_venv
        ;;
    compile)
        compile_requirements
        ;;
    sync)
        sync_packages
        ;;
    add)
        add_package "$2"
        ;;
    activate)
        activate_venv
        ;;
    run)
        shift
        run_command "$@"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run './uv.sh help' for usage information"
        exit 1
        ;;
esac
""")
        os.chmod("uv.sh", 0o755)
        print("Created uv.sh script")

def initialize_template():
    """Main function to initialize the template"""
    print_header("Initializing hanx GitHub template")
    
    # Check if this is a fresh installation
    if Path(".initialized").exists():
        print("Template already initialized. Delete .initialized file to force reinitialization")
        return
    
    # Create directories
    create_directories()
    
    # Initialize files
    initialize_files()
    
    # Set up environment
    setup_environment()
    
    # Set up UV
    setup_uv()
    
    # Mark as initialized
    with open(".initialized", "w") as f:
        f.write(f"Initialized at: {os.path.basename(__file__)}\n")
    
    print_header("Initialization complete")
    print("Please edit the .env file to add your API keys")
    print("Run 'uv.bat activate' (Windows) or 'source ./uv.sh activate' (Unix) to activate the environment")

if __name__ == "__main__":
    initialize_template() 