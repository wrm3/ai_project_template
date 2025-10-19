# Claude Code Project Template

## 📋 Project Overview
This is a template project for setting up new development projects with comprehensive AI assistant integration across multiple IDEs (Cursor, Windsurf, Roo-Code, Claude Code).

## 🎯 Purpose
Provide a standardized starting point for projects that includes:
- Task management system (fstrent_tasks)
- AI assistant configuration for multiple IDEs
- MCP (Model Context Protocol) tool integration
- Project documentation templates

## 🛠️ Technology Stack
- **Task Management**: fstrent_tasks system via MCP
- **IDEs Supported**: Cursor, Windsurf, Roo-Code, Claude Code
- **MCP Tools**: Database access, browser automation, web scraping, datetime utilities
- **Version Control**: Git

## 📁 Folder Structure
```
/
├── CLAUDE.md                    # This file - Claude Code main reference
├── .claude/                     # Claude Code specific configuration
│   ├── agents/                  # Claude Code subagents
│   ├── commands/                # Claude Code custom commands
│   └── skills/                  # Claude Code Skills
├── .cursor/                     # Cursor IDE configuration
│   └── rules/                   # Cursor rule files
├── .fstrent_spec_tasks/        # Task management system
│   ├── tasks/                   # Active task files
│   ├── features/                # Feature documentation
│   ├── TASKS.md                 # Master task checklist
│   ├── PLAN.md                  # Product Requirements Document
│   ├── PROJECT_CONTEXT.md       # Project context and goals
│   └── SUBSYSTEMS.md            # Component registry
├── docs/                        # Project documentation
└── temp_scripts/                # Test and utility scripts
```

## 🎨 Development Guidelines

### Task Management
- Use fstrent_tasks system for all task tracking
- Create task files in `.fstrent_spec_tasks/tasks/`
- Update TASKS.md for all task status changes
- Use Windows-safe emojis: `[ ]` pending, `[🔄]` in-progress, `[✅]` completed

### Code Standards
- Follow language-specific best practices
- Write clear, maintainable code
- Document complex logic
- Test before committing

### AI Assistant Usage
- Leverage MCP tools for database, browser, and web operations
- Use task management system for planning and tracking
- Reference project context before starting new work
- Keep documentation updated

## 🚀 Important Commands

### Task Management
```bash
# Initialize fstrent_tasks system (if not already done)
# Use MCP tool: fstrent_tasks_setup

# View current tasks
cat .fstrent_spec_tasks/TASKS.md

# View project plan
cat .fstrent_spec_tasks/PLAN.md
```

### Development Workflow
```bash
# Create new feature branch
git checkout -b feature/your-feature-name

# Run tests (project-specific)
# Add your test commands here

# Build (project-specific)
# Add your build commands here
```

## 🧪 Testing Approach
- Test scripts go in `temp_scripts/` folder
- Document test procedures in `docs/`
- Use MCP tools for automated testing where applicable

## 📚 Additional Documentation
- See `.cursor/rules/` for Cursor-specific AI assistant rules
- See `.claude/skills/` for Claude Code Skills
- See `docs/` for project-specific documentation

## 🔗 MCP Tools Available
- **fstrent_mcp_tasks**: Task management, datetime utilities
- **fstrent_mcp_mysql**: Database query and update operations
- **fstrent_mcp_browser_use**: Browser automation and web scraping
- **fstrent_mcp_computer_use**: GUI automation and screenshots

## 📝 Notes
- This project supports multiple AI IDEs simultaneously
- Each IDE has its own configuration folder
- Task management system is IDE-agnostic
- Keep all documentation updated as project evolves

---
*Last updated: 2025-10-19*

