---
name: Project Setup
description: Initialize new projects with proper structure, documentation, and configuration. Use when setting up new repositories or project scaffolding.
allowed-tools: Read, Write, Edit, Bash
---

# Project Setup Skill

## Overview
This Skill helps initialize new projects with standardized structure, documentation templates, and configuration files for multiple AI IDEs.

## Capabilities
- Create standard folder structure
- Initialize git repository
- Set up AI assistant configurations (Cursor, Claude Code, Windsurf, Roo-Code)
- Create documentation templates
- Initialize task management system
- Set up MCP tool configurations

## Standard Project Structure
```
project-name/
├── CLAUDE.md                    # Claude Code reference
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
├── .claude/                     # Claude Code config
│   ├── agents/
│   ├── commands/
│   └── skills/
├── .cursor/                     # Cursor IDE config
│   └── rules/
├── .fstrent_spec_tasks/        # Task management
│   ├── tasks/
│   ├── features/
│   ├── TASKS.md
│   └── PLAN.md
├── docs/                        # Documentation
└── temp_scripts/                # Test scripts
```

## When to Use
Use this Skill when:
- Starting a new project from scratch
- Converting an existing project to use AI assistant tools
- Setting up standardized development environment
- Creating project templates
- User mentions: "new project", "initialize", "setup", "scaffold"

## Setup Process

### 1. Create Base Structure
```bash
# Create main folders
mkdir -p docs temp_scripts

# Create AI IDE configurations
mkdir -p .claude/agents .claude/commands .claude/skills
mkdir -p .cursor/rules
```

### 2. Initialize Git
```bash
git init
# Create .gitignore with common patterns
```

### 3. Create Documentation
- CLAUDE.md - Main project reference
- README.md - Project overview
- docs/ folder for additional documentation

### 4. Initialize Task Management
Use MCP tool: `fstrent_tasks_setup` to initialize the task management system

### 5. Create Initial Files
- Project context documentation
- Basic configuration files
- Example templates

## Configuration Templates

### .gitignore Template
```
# Dependencies
node_modules/
venv/
__pycache__/

# IDE
.vscode/
.idea/

# Environment
.env
.env.local

# Build outputs
dist/
build/
*.pyc

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
```

### README.md Template
```markdown
# Project Name

## Description
Brief description of the project

## Setup
Installation and setup instructions

## Usage
How to use the project

## Development
Development guidelines and commands

## License
License information
```

## Best Practices
- Always create a comprehensive .gitignore
- Document the project structure in CLAUDE.md
- Set up task management from the start
- Include example configurations
- Create clear README with setup instructions
- Initialize version control early

## Resources
This Skill works with:
- fstrent_tasks MCP tool for task management
- Git for version control
- Multiple AI IDE configurations

