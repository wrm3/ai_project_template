# Claude Code Starter Template

## 🎯 Purpose
A minimal, reusable starter template for new projects with Claude Code. This template provides the structure and examples - you'll customize it for each project and rely on your personal `~/.claude/` setup for universal tools.

---

## 📁 Template Structure

```
project-name/
├── CLAUDE.md                          # Project documentation (customize per project)
├── .mcp.json                          # Project-specific MCP config (optional)
├── .claude/                           # Project-level Claude Code config
│   ├── agents/                        # Project-specific agents only
│   │   └── README.md                 # Guide for creating agents
│   ├── commands/                      # Project-specific commands only
│   │   └── README.md                 # Guide for creating commands
│   └── skills/                        # Project-specific skills only
│       └── README.md                 # Guide for creating skills
├── .gitignore                         # Excludes sensitive files
├── README.md                          # Project setup instructions
└── docs/
    └── CLAUDE_SETUP.md               # How to set up Claude Code for this project
```

---

## 📄 Template Files

### **CLAUDE.md** (Customize for each project)
```markdown
# [PROJECT NAME]

> **Last Updated:** [DATE]
> **Maintained by:** [YOUR NAME/TEAM]

## Project Overview
[Brief description - 2-3 sentences about what this project does]

## Technology Stack
- **Language:** [e.g., Python 3.11]
- **Framework:** [e.g., FastAPI]
- **Database:** [e.g., PostgreSQL 15]
- **Frontend:** [e.g., React 18 + TypeScript]
- **Infrastructure:** [e.g., Docker, AWS]

## Repository Structure
```
/src          - Application source code
/tests        - Test files
/docs         - Documentation
/scripts      - Utility scripts
/.claude      - Claude Code configuration
```

## Development Guidelines

### Code Style
- [Language-specific style guide]
- [Linting/formatting tools]
- [Naming conventions]

### Git Workflow
- Branch naming: `feature/`, `bugfix/`, `hotfix/`
- Commit message format: [Convention]
- PR requirements: [Review process]

### Testing Strategy
- Unit tests required for new features
- Integration tests for API endpoints
- E2E tests for critical user flows

## Important Commands

### Development
\`\`\`bash
# Start development server
[command]

# Run tests
[command]

# Run linter
[command]
\`\`\`

### Database
\`\`\`bash
# Run migrations
[command]

# Seed database
[command]
\`\`\`

### Deployment
\`\`\`bash
# Build for production
[command]

# Deploy to staging
[command]
\`\`\`

## Project-Specific Context

### Database Schema
[Key tables and relationships]

### API Endpoints
[Important endpoints and their purposes]

### Business Logic Notes
[Important domain knowledge, rules, gotchas]

## Common Tasks

### Adding a New Feature
1. [Step-by-step process]

### Debugging Issues
1. [Common debugging approaches]

### Working with [Specific Component]
[Component-specific guidance]

## External Dependencies

### Required MCP Servers
- [List MCPs needed - e.g., "Requires postgres MCP for database access"]

### Required Skills
- [List project-specific skills if any]

## Resources
- Design Doc: [Link]
- API Documentation: [Link]
- Staging Environment: [Link]
- Production Dashboard: [Link]

---

## Notes for Claude Code
- Always run tests before committing
- Follow the project's error handling patterns
- Keep functions under 50 lines when possible
- Document complex business logic
```

---

### **.mcp.json** (Project-specific connections only)
```json
{
  "$schema": "https://github.com/modelcontextprotocol/servers/blob/main/schema.json",
  "mcpServers": {
    "project-database": {
      "comment": "Project-specific database connection",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${PROJECT_DB_URL}"
      }
    },
    "project-api": {
      "comment": "Project-specific API access",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

**NOTE:** Sensitive credentials should use environment variables, never hardcoded!

---

### **.claude/skills/README.md**
```markdown
# Project Skills

This folder contains project-specific Skills that teach Claude about this project's conventions and patterns.

## Creating a New Skill

1. Create a folder: `.claude/skills/skill-name/`
2. Add `SKILL.md` with:
   ```markdown
   ---
   name: Skill Name
   description: What this skill does and when to use it
   ---
   
   # Instructions
   [Your skill content]
   ```

## Example Skills for This Project

Consider creating skills for:
- **Project Architecture**: Explain the system design and component relationships
- **Database Conventions**: Schema patterns, naming conventions, query patterns
- **Testing Patterns**: How to write tests in this project
- **Deployment Process**: Steps for deploying changes
- **Error Handling**: Project-specific error patterns

## Universal Skills

Keep universal skills in `~/.claude/skills/` instead:
- General code review patterns
- Personal coding style preferences
- Cross-project utilities
```

---

### **.claude/agents/README.md**
```markdown
# Project Agents

Project-specific subagents for specialized workflows in this codebase.

## When to Create a Project Agent

Create agents for:
- Project-specific testing workflows
- Custom deployment procedures
- Domain-specific code review
- Project-specific debugging patterns

## Example Agent Template

`.claude/agents/example-agent.md`:
```markdown
---
name: example-agent
description: Brief description of what this agent does. Use PROACTIVELY for automatic invocation.
tools: Read, Write, Edit, Grep, Bash
---

# Agent Name

## Purpose
[What this agent is for]

## Instructions
[Step-by-step instructions]

## When to Use
[Scenarios for using this agent]
```

## Universal Agents

Keep universal agents in `~/.claude/agents/` instead:
- General code review
- Git commit message generation
- Generic test runners
```

---

### **.gitignore**
```gitignore
# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Dependencies
node_modules/
__pycache__/
*.pyc
venv/
.venv/

# Build outputs
dist/
build/
*.egg-info/

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp

# DO NOT IGNORE - Keep Claude Code config
# .claude/
# CLAUDE.md
```

---

### **docs/CLAUDE_SETUP.md**
```markdown
# Setting Up Claude Code for This Project

## Prerequisites

### 1. Install Claude Code
```bash
# Installation instructions
```

### 2. Configure Personal Tools (One-time Setup)

These should be in your `~/.claude/` directory (NOT in this project):

#### Personal Skills
```bash
mkdir -p ~/.claude/skills
# Add your universal skills here
```

#### Personal Agents
```bash
mkdir -p ~/.claude/agents
# Add your universal agents here
```

#### Personal MCPs
Configure in Claude Code settings or `~/.config/claude/config.json`:
- Database connections (MySQL, PostgreSQL, Oracle)
- Cloud service integrations (AWS, GCP, Azure)
- General tools (Puppeteer, Sentry, etc.)

**Example Personal MCP Config:**
```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": {
        "MYSQL_CONNECTION_STRING": "${MYSQL_URL}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${POSTGRES_URL}"
      }
    }
  }
}
```

### 3. Initialize This Project

```bash
cd project-directory
claude

# In Claude Code prompt:
> /init

# Verify Claude understands the project:
> What does this project do?
> Explain the folder structure
> What are the key technologies?
```

### 4. Review CLAUDE.md

- Update project-specific information
- Add any missing context
- Customize for your team's needs

### 5. Add Project-Specific Skills (Optional)

If this project has unique patterns:
```bash
mkdir -p .claude/skills/project-conventions
# Create SKILL.md with project-specific knowledge
```

### 6. Test the Setup

```bash
> What skills are available?
> /skills
> What MCPs are connected?
```

## Troubleshooting

### Skills Not Loading
- Check YAML frontmatter syntax
- Verify file is named `SKILL.md` (not `skill.md`)
- Restart Claude Code: exit and run `claude` again

### MCP Connection Failed
- Check environment variables are set
- Verify credentials are correct
- Check MCP server is installed: `npx -y @modelcontextprotocol/server-[name]`

### Claude Doesn't Use My Skill
- Make description more specific
- Include trigger words users would say
- Test with explicit request: "Use the [skill-name] skill to..."

## Best Practices

### Do ✅
- Keep universal tools in `~/.claude/`
- Commit `.claude/` folder to git
- Update CLAUDE.md as project evolves
- Document project-specific patterns in Skills
- Use descriptive names for Skills and Agents

### Don't ❌
- Don't commit personal MCPs to git
- Don't hardcode credentials in `.mcp.json`
- Don't duplicate universal skills in project
- Don't create overly broad skills (keep focused)
```

---

## 🎯 Setup Instructions for a New Project

### 1. Copy This Template
```bash
cp -r claude-code-starter my-new-project
cd my-new-project
```

### 2. Customize CLAUDE.md
- Fill in project-specific details
- Add technology stack
- Document conventions
- Add important commands

### 3. Initialize with Claude Code
```bash
claude
> /init
```

### 4. Review and Adjust
- Test that Claude understands your project
- Add project-specific Skills if needed
- Create project-specific agents if needed
- Configure project MCPs if needed

### 5. Commit to Git
```bash
git init
git add .
git commit -m "Initial commit with Claude Code setup"
```

---

## 📚 Additional Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/quickstart)
- [Agent Skills Guide](https://docs.claude.com/en/docs/claude-code/skills)
- [Subagents Documentation](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [MCP Documentation](https://modelcontextprotocol.io/)

---

## 🤝 Contributing

When adding to this template:
1. Keep it minimal - only structure and examples
2. Document what belongs at user-level vs project-level
3. Provide clear customization instructions
4. Include examples but not your actual configs

---

**Remember:** This template provides the STRUCTURE. Your personal `~/.claude/` directory provides your TOOLS.