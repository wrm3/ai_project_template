#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Service
This script runs the MCP service, which provides a REST API for interacting with
the multi-agent system.
"""

import os
import sys
import logging
import argparse
from pathlib import Path
import importlib.util
import json
import time
from typing import Dict, Any, List, Optional

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/mcp_service.log")
    ]
)
logger = logging.getLogger("mcp_service")

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

# Add hanx directories to Python path
add_hanx_to_python_path()

# Try to import FastAPI for the REST API
try:
    from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    logger.warning("FastAPI not installed. Running in CLI mode only.")
    HAS_FASTAPI = False

class MCPService:
    """MCP Service class for managing the multi-agent system."""
    
    def __init__(self):
        """Initialize the MCP service."""
        self.initialized = os.path.exists(".initialized")
        if not self.initialized:
            logger.error("MCP environment not initialized. Please run hanx_mcp/mcp_init.py first.")
            sys.exit(1)
        
        # Load agent modules
        self.load_agent_modules()
        
        # Initialize state
        self.state = {
            "status": "idle",
            "current_task": None,
            "tasks": [],
            "agents": {
                "planner": {"status": "idle"},
                "executor": {"status": "idle"}
            }
        }
    
    def load_agent_modules(self):
        """Load agent modules dynamically."""
        self.agents = {}
        
        # Define agent modules to load
        agent_modules = [
            ("planner", "hanx_agents.agent_planner"),
            ("executor", "hanx_agents.agent_executor"),
            ("rag", "hanx_agents.agent_rag_librarian"),
            ("youtube", "hanx_agents.agent_youtube_researcher")
        ]
        
        for agent_name, module_path in agent_modules:
            try:
                spec = importlib.util.find_spec(module_path)
                if spec is None:
                    logger.warning(f"Agent module {module_path} not found.")
                    continue
                
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.agents[agent_name] = module
                logger.info(f"Loaded agent module: {agent_name}")
            except Exception as e:
                logger.error(f"Error loading agent module {module_path}: {e}")
    
    def run_agent(self, agent_name: str, **kwargs) -> Dict[str, Any]:
        """Run an agent with the given parameters."""
        if agent_name not in self.agents:
            logger.error(f"Agent {agent_name} not found.")
            return {"status": "error", "message": f"Agent {agent_name} not found."}
        
        try:
            # Update agent status
            self.state["agents"][agent_name] = {"status": "running"}
            
            # Run the agent
            agent_module = self.agents[agent_name]
            result = agent_module.main(**kwargs)
            
            # Update agent status
            self.state["agents"][agent_name] = {"status": "idle"}
            
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Error running agent {agent_name}: {e}")
            # Update agent status
            self.state["agents"][agent_name] = {"status": "error", "error": str(e)}
            return {"status": "error", "message": str(e)}
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the MCP service."""
        return self.state
    
    def update_state(self, new_state: Dict[str, Any]) -> Dict[str, Any]:
        """Update the state of the MCP service."""
        self.state.update(new_state)
        return self.state

# Create MCP service instance
mcp_service = MCPService()

# If FastAPI is available, create a REST API
if HAS_FASTAPI:
    app = FastAPI(title="MCP Service API", description="API for interacting with the MCP service")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    class AgentRequest(BaseModel):
        """Request model for running an agent."""
        agent_name: str
        parameters: Dict[str, Any]
    
    class StateUpdate(BaseModel):
        """Request model for updating the state."""
        state: Dict[str, Any]
    
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {"message": "MCP Service API"}
    
    @app.get("/state")
    async def get_state():
        """Get the current state of the MCP service."""
        return mcp_service.get_state()
    
    @app.post("/state")
    async def update_state(state_update: StateUpdate):
        """Update the state of the MCP service."""
        return mcp_service.update_state(state_update.state)
    
    @app.post("/run_agent")
    async def run_agent(agent_request: AgentRequest, background_tasks: BackgroundTasks):
        """Run an agent with the given parameters."""
        # Run the agent in the background
        background_tasks.add_task(
            mcp_service.run_agent,
            agent_request.agent_name,
            **agent_request.parameters
        )
        return {"status": "accepted", "message": f"Agent {agent_request.agent_name} started."}
    
    def start_api_server():
        """Start the API server."""
        uvicorn.run(app, host="0.0.0.0", port=8000)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="MCP Service")
    parser.add_argument("--api", action="store_true", help="Start the API server")
    parser.add_argument("--agent", type=str, help="Run an agent")
    parser.add_argument("--params", type=str, help="Parameters for the agent (JSON)")
    args = parser.parse_args()
    
    if args.api:
        if not HAS_FASTAPI:
            logger.error("FastAPI not installed. Cannot start API server.")
            sys.exit(1)
        logger.info("Starting API server...")
        start_api_server()
    elif args.agent:
        params = {}
        if args.params:
            try:
                params = json.loads(args.params)
            except json.JSONDecodeError:
                logger.error("Invalid JSON parameters.")
                sys.exit(1)
        
        logger.info(f"Running agent {args.agent}...")
        result = mcp_service.run_agent(args.agent, **params)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 