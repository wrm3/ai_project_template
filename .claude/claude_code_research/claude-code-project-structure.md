# Claude Code Project Structure Template

## 📁 Complete Folder Architecture

```
your-project/
├── CLAUDE.md                          # Main project documentation (REQUIRED)
├── .mcp.json                          # Model Context Protocol config (optional)
├── .claude/                           # Project-level Claude Code config
│   ├── agents/                        # Project-specific subagents
│   │   ├── test-runner.md            # Example: automated testing agent
│   │   ├── code-reviewer.md          # Example: code review agent
│   │   └── laravel-planner.md        # Example: architecture planning agent
│   ├── commands/                      # Custom slash commands
│   │   ├── fix-github-issue.md       # Example: /project:fix-github-issue
│   │   └── review.md                 # Example: /project:review
│   └── skills/                        # Project-specific Skills
│       ├── brand-guidelines/          # Example Skill
│       │   ├── SKILL.md              # Required: Skill definition
│       │   ├── logo-files/           # Optional: Supporting resources
│       │   └── templates/            # Optional: Templates
│       └── webapp-testing/            # Another example Skill
│           ├── SKILL.md
│           ├── fixtures/
│           └── scripts/
└── [your project files...]

# User-level (not in project, in home directory)
~/.claude/
├── agents/                            # Personal agents (all projects)
│   └── my-personal-agent.md
├── commands/                          # Personal commands (all projects)
│   └── my-workflow.md
└── skills/                            # Personal Skills (all projects)
    └── my-coding-style/
        └── SKILL.md
```

---

## 📄 Key Files & Folders Explained

### **CLAUDE.md** (Project Root - REQUIRED)
**Purpose:** Primary reference file that helps Claude understand your entire project

**What it contains:**
- Project overview and purpose
- Technology stack
- Folder structure explanation
- Development conventions and coding standards
- Important commands (build, test, dev server)
- Testing approaches
- Any project-specific context

**How to create:**
```bash
cd your-project
claude
# In the Claude Code prompt:
/init
```

**Example structure:**
```markdown
# Project Overview
Brief description of your project, its purpose, and main technologies.

## Technology Stack
- Frontend: React 18, TypeScript
- Backend: Node.js, Express
- Database: PostgreSQL

## Folder Structure
- `/src` - Source code
- `/tests` - Test files
- `/docs` - Documentation

## Development Guidelines
- Use TypeScript strict mode
- Follow Airbnb style guide
- Write tests for all new features

## Important Commands
- `npm run dev` - Start development server
- `npm test` - Run test suite
- `npm run build` - Build for production
```

**Documentation:** [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

---

### **.claude/agents/** (Subagents)
**Purpose:** Specialized AI subagents for specific workflows with their own context and tool permissions

**Key characteristics:**
- Each agent operates in its own context (prevents context pollution)
- Can have different tool access levels
- Project agents take precedence over user agents
- Automatically invoked or explicitly called

**File format:** Markdown with YAML frontmatter

**Example: test-runner.md**
```markdown
---
name: test-runner
description: Run test suite, diagnose failures, and fix them. Use PROACTIVELY after code changes.
tools: Read, Edit, Write, Grep, Glob, Bash
---

# Test Runner Agent

## Instructions
1. Run the appropriate test command for the project
2. If tests fail, analyze the failures
3. Fix failures while preserving original test intent
4. Re-run to verify fixes

## When to Use
- After code changes (proactively)
- When explicitly asked to run tests
- When debugging test failures
```

**Usage:**
```bash
# Explicit invocation
> Use the test-runner subagent to fix failing tests

# Automatic invocation (if description includes "PROACTIVELY")
# Claude will use it automatically when relevant
```

**Documentation:** [Subagents - Claude Docs](https://docs.claude.com/en/docs/claude-code/sub-agents)

---

### **.claude/commands/** (Custom Slash Commands)
**Purpose:** Reusable prompt templates for repeated workflows

**Key characteristics:**
- Accessed via `/` menu in Claude Code
- Can include `$ARGUMENTS` placeholder for parameters
- Project commands: `.claude/commands/`
- Personal commands: `~/.claude/commands/`

**Example: fix-github-issue.md**
```markdown
Please analyze and fix the GitHub issue: $ARGUMENTS.

1. Read the issue details
2. Locate relevant code
3. Implement the fix
4. Write/update tests
5. Create a commit with clear message
```

**Usage:**
```bash
> /project:fix-github-issue 1234
```

**Documentation:** [Claude Code Best Practices - Custom Commands](https://www.anthropic.com/engineering/claude-code-best-practices)

---

### **.claude/skills/** (Project Skills)
**Purpose:** Modular capabilities with instructions, scripts, and resources that extend Claude's abilities

**Key characteristics:**
- **Model-invoked** (Claude decides when to use them automatically)
- Each Skill is a folder with `SKILL.md` + optional supporting files
- Progressive disclosure: only loads when relevant
- Can include executable code
- Works across Claude.ai, Claude Code, and API

**Required structure for each Skill:**
```
skill-name/
├── SKILL.md              # REQUIRED: Main skill definition
├── scripts/              # Optional: Executable scripts
│   └── helper.py
├── templates/            # Optional: File templates
│   └── report-template.md
└── resources/            # Optional: Supporting files
    └── logo.png
```

**SKILL.md format:**
```markdown
---
name: Brand Guidelines
description: Apply Acme Corp brand guidelines to presentations and documents. Use when creating PowerPoint, Word, or marketing materials.
allowed-tools: Read, Write, Edit  # Optional: restrict tool access
---

# Brand Guidelines Skill

## Overview
This Skill provides Acme Corp's official brand guidelines for creating consistent materials.

## Brand Colors
- Primary: #FF6B35 (Coral)
- Secondary: #004E89 (Navy Blue)
- Accent: #F7B801 (Gold)

## Typography
- Headers: Montserrat Bold
- Body: Open Sans Regular

## When to Apply
Use these guidelines when creating:
- PowerPoint presentations
- Word documents
- Marketing materials
- Reports for clients

## Resources
See the resources/ folder for logo files and font downloads.
```

**How Skills work:**
1. At startup, Claude loads only the `name` and `description` from all Skills
2. When your request matches a Skill's description, Claude loads the full `SKILL.md`
3. If needed, Claude accesses supporting files (scripts, templates, resources)
4. Claude can execute scripts or use resources to complete the task

**Project Skills vs Personal Skills:**
- **Project Skills** (`.claude/skills/`): Shared with team via git
- **Personal Skills** (`~/.claude/skills/`): Available only to you across all projects

**Testing a Skill:**
```bash
# After creating a Skill, test with relevant requests
> Create a PowerPoint presentation about Q3 results
# If the Skill's description matches, Claude will use it automatically

# View all available Skills
> /skills
```

**Documentation:**
- [Agent Skills - Claude Docs](https://docs.claude.com/en/docs/claude-code/skills)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Equipping Agents with Agent Skills (Engineering Blog)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

---

### **.mcp.json** (Model Context Protocol)
**Purpose:** Configure external tool integrations (Puppeteer, Sentry, databases, etc.)

**Example:**
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://localhost/mydb"
      }
    }
  }
}
```

**Documentation:** [Claude Code - MCP Configuration](https://www.anthropic.com/engineering/claude-code-best-practices)

---

## 🚀 Quick Start: Setting Up a New Project

### Step 1: Initialize Project
```bash
cd your-project
claude
# In Claude Code:
> /init
```

This creates your `CLAUDE.md` file.

### Step 2: Create Project Structure
```bash
# Create the .claude directory structure
mkdir -p .claude/agents
mkdir -p .claude/commands
mkdir -p .claude/skills
```

### Step 3: Add Your First Skill
```bash
# Create a Skill folder
mkdir -p .claude/skills/my-first-skill

# Create SKILL.md
cat > .claude/skills/my-first-skill/SKILL.md << 'EOF'
---
name: My First Skill
description: Brief description of what this Skill does and when to use it
---

# My First Skill

## Instructions
1. Step one
2. Step two
3. Step three

## When to Use
Describe the scenarios where Claude should use this Skill.
EOF
```

### Step 4: Test Your Setup
```bash
claude
> What Skills are available?
> /skills
```

---

## 📋 Best Practices

### For CLAUDE.md
- Keep it concise but comprehensive
- Update it as your project evolves
- Include examples of common tasks
- Document conventions clearly

### For Skills
- **One Skill = One Capability** (focused, not general)
- **Clear descriptions** with specific keywords users might mention
- **Start simple** - add complexity gradually
- **Include examples** in your SKILL.md
- **Test thoroughly** before sharing with team

### For Subagents
- Use for complex, repeatable workflows
- Give each agent clear, specific expertise
- Version control project agents
- Add "PROACTIVELY" or "MUST BE USED" for automatic invocation

### For Commands
- Create commands for frequently repeated tasks
- Use `$ARGUMENTS` for flexible parameters
- Keep commands focused and clear
- Document what each command does

---

## 🔄 Skills vs Subagents vs Commands

| Feature | **Skills** | **Subagents** | **Commands** |
|---------|-----------|---------------|--------------|
| **Invocation** | Model-invoked (automatic) | Model or user-invoked | User-invoked (manual) |
| **Purpose** | Add specialized capabilities | Delegate complex tasks | Quick workflow shortcuts |
| **Format** | Folder with SKILL.md | Markdown with YAML | Markdown templates |
| **Context** | Loads when relevant | Own context window | Uses main context |
| **Best For** | Domain expertise, workflows | Complex multi-step tasks | Repeated prompts |

---

## 🔗 Essential Links

### Official Documentation
- [Claude Code Quickstart](https://docs.claude.com/en/docs/claude-code/quickstart)
- [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Subagents Guide](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

### Engineering Blog Posts
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Equipping Agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

### Community Resources
- [Official Skills Repository (GitHub)](https://github.com/anthropics/skills)
- [Claude Code Subagents Collection](https://github.com/0xfurai/claude-code-subagents)

---

## ✅ Checklist for New Project

- [ ] Run `/init` to create CLAUDE.md
- [ ] Create `.claude/` folder structure
- [ ] Add project-specific Skills to `.claude/skills/`
- [ ] Create helpful subagents in `.claude/agents/`
- [ ] Set up custom commands in `.claude/commands/`
- [ ] Configure MCP if needed (`.mcp.json`)
- [ ] Commit `.claude/` folder to git
- [ ] Test all Skills and agents
- [ ] Update CLAUDE.md as project evolves

---

**Note:** Everything in `.claude/` should be committed to version control so your team gets the same capabilities!