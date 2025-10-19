# Hanx Agents

This directory contains the agent components of the multi-agent system. Agents are responsible for complex, workflow-oriented tasks and coordinate with each other to accomplish goals.

## Agent Structure

The multi-agent system has been refactored into three main components:

1. `base_agent.py`: Contains common functionality for all agents, including environment loading, file operations, and LLM querying.
2. `agent_planner.py`: Implements the Planner agent, which is responsible for high-level planning, task breakdown, and progress evaluation.
3. `agent_executor.py`: Implements the Executor agent, which is responsible for executing tasks and reporting progress.

All agents inherit from the BaseAgent class, which provides common functionality and ensures consistent behavior across the system.

## Available Agents

The following agents are available in this directory:

- **PlannerAgent**: Performs high-level analysis and planning for tasks.
- **ExecutorAgent**: Executes specific tasks instructed by the Planner.
- **KnowledgeBaseAgent**: Manages and retrieves information from knowledge bases.
- **RAGLibrarianAgent**: Implements Retrieval-Augmented Generation for document search.
- **YouTubeResearcherAgent**: Extracts and analyzes information from YouTube videos.
- **ComputerUseAgent**: Controls the computer using OpenAI's computer-use-preview model and pyautogui.

### Base Agent

The BaseAgent class provides common functionality for all agents, including:

- Environment loading
- File operations (read, write, append)
- Plan status reading
- LLM querying
- Logging

Usage:
```python
from hanx_agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MyAgent")
    
    def run(self, args=None):
        # Implement agent-specific functionality
        pass

### Planner Agent

The Planner agent is responsible for high-level planning in the multi-agent system. It analyzes the current plan status, breaks down tasks, defines success criteria, and evaluates progress.

Usage:
```bash
python hanx_agents/agent_planner.py --prompt "Your planning prompt here"
python hanx_agents/agent_planner.py --prompt "Your planning prompt here" --file path/to/file.txt
python hanx_agents/agent_planner.py --prompt "Your planning prompt here" --provider anthropic
```

### Executor Agent

The Executor agent is responsible for executing specific tasks in the multi-agent system. It handles implementation details, runs tests, and reports progress back to the Planner.

Usage:
```bash
python hanx_agents/agent_executor.py --task "Task description" --update-section "Current Status / Progress Tracking" --content "Your update content"
python hanx_agents/agent_executor.py --task "Task description" --update-section "Executor's Feedback or Assistance Requests" --content "Your assistance request"
```

### YouTube Researcher Agent

The YouTube Researcher agent is responsible for extracting and analyzing data from YouTube videos. It can download videos, extract audio, transcribe content, and perform specialized analysis for different video types.

Usage:
```bash
python hanx_agents/agent_youtube_researcher.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --analysis-type "general|trading|framework"
```

### RAG Librarian Agent

The RAG Librarian agent is responsible for managing the Retrieval Augmented Generation (RAG) system. It can ingest various file types, YouTube transcripts, and web pages, and provide query functionality.

Usage:
```bash
python hanx_agents/agent_rag_librarian.py --ingest-file path/to/file.txt
python hanx_agents/agent_rag_librarian.py --ingest-youtube "https://www.youtube.com/watch?v=VIDEO_ID"
python hanx_agents/agent_rag_librarian.py --ingest-web "https://example.com"
python hanx_agents/agent_rag_librarian.py --query "Your query here"
```

### Knowledge Base Agent

The Knowledge Base agent is responsible for managing and querying the knowledge base. It can store and retrieve information, and provide answers to questions.

Usage:
```bash
python hanx_agents/agent_knowledge_base.py --store "key" "value"
python hanx_agents/agent_knowledge_base.py --retrieve "key"
python hanx_agents/agent_knowledge_base.py --query "Your question here"
```

## ComputerUseAgent

The ComputerUseAgent can control the computer using OpenAI's computer-use-preview model. It captures screenshots and executes actions like clicking, typing, and scrolling based on AI recommendations.

### Usage

```bash
python hanx_agents/agent_computer_use.py --task "Open the browser and search for OpenAI" --max-steps 10
```

### Parameters

- `--task`: The task to perform on the computer (default: "Help me navigate this screen")
- `--max-steps`: Maximum number of steps to execute (default: 10)

### Requirements

- OpenAI API key with access to the computer-use-preview model
- pyautogui library
- PIL (Pillow) library

### Safety Features

- PyAutoGUI's FAILSAFE is enabled (move mouse to upper-left corner to abort)
- Actions have a 0.5-second pause between them
- Maximum step limit to prevent infinite loops

## Creating New Agents

When creating new agents, follow these guidelines:

1. Inherit from the BaseAgent class to ensure consistent functionality and behavior.
2. Implement the `run` method to define the agent's specific functionality.
3. Follow the naming convention `agent_*.py` and place the file in the `hanx_agents/` directory.
4. Document the agent's usage in this README.md file.
5. Update the hanx_learned.md file with any lessons learned during development.

Example:
```python
#!/usr/bin/env python3
"""
My Custom Agent

This agent is responsible for [description of agent's responsibilities].

Usage:
    python hanx_agents/agent_my_custom.py --arg1 value1 --arg2 value2
"""

import argparse
from hanx_agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MyCustomAgent")
    
    def run(self, args=None):
        if args is None:
            args = {}
        
        # Implement agent-specific functionality
        
        return "Result of agent execution"

def main():
    parser = argparse.ArgumentParser(description="My Custom Agent")
    parser.add_argument("--arg1", help="Description of arg1")
    parser.add_argument("--arg2", help="Description of arg2")
    
    args = parser.parse_args()
    
    agent = MyCustomAgent()
    result = agent.run(vars(args))
    
    print(result)

if __name__ == "__main__":
    main() 