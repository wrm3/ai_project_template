# Hanx Template Initialization

## Overview
This template provides instructions for initializing a fresh installation of the hanx template from GitHub.
It sets up the required environment, directories, and configuration files.

## Initialization Steps

1. Create necessary directories:
   - hanx_tools/temp_tools
   - hanx_data
   - hanx_apis
   - hanx_agents

2. Set up environment variables in .env file:
   - OPENAI_API_KEY
   - ANTHROPIC_API_KEY
   - AZURE_OPENAI_API_KEY
   - AZURE_OPENAI_ENDPOINT
   - AZURE_OPENAI_MODEL_DEPLOYMENT

3. Initialize hanx_learned.md with basic lessons

4. Set up the multi-agent system:
   - Create hanx_plan.md with the template structure
   - Set up agent scripts

5. Install dependencies using UV:
   - Create UV installation scripts for Windows (.bat) and Unix (.sh)
   - Install required Python packages

## Required Files

- hanx_learned.md: Stores lessons learned and tool documentation
- hanx_plan.md: Contains the multi-agent scratchpad for planning and execution
- .env: Stores environment variables and API keys
- .initialized: Marks the project as initialized

## Directory Structure

```
project_root/
├── hanx_tools/
│   ├── temp_tools/
│   ├── data/
│   └── templates/
├── hanx_apis/
├── hanx_agents/
├── .env
├── hanx_learned.md
├── hanx_plan.md
└── .initialized
```

## Initialization Command

```bash
# Windows
python hanx_tools/init_template.py

# Unix/Linux/Mac
python3 hanx_tools/init_template.py
``` 