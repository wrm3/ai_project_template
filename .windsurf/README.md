# Windsurf IDE Integration

Welcome to **fstrent_spec_tasks** for Windsurf IDE!

## What Is This?

This directory contains Windsurf-specific integration for the fstrent_spec_tasks system - a comprehensive task management, planning, and QA framework that works across multiple AI-powered IDEs.

## Quick Start

### 1. Initialize the System

```
/windsurf:setup
```

This creates:
- `.fstrent_spec_tasks/` directory with all templates
- `PLAN.md` for product requirements
- `TASKS.md` for task tracking
- `BUGS.md` for bug management
- Project structure

### 2. Create Your First Task

```
/windsurf:new-task
```

### 3. Start Planning

```
/windsurf:planning
```

### 4. Check Status

```
/windsurf:status
```

## Available Commands

| Command | Purpose |
|---------|---------|
| `/windsurf:setup` | Initialize fstrent_spec_tasks system |
| `/windsurf:new-task` | Create new task |
| `/windsurf:update-task` | Update task status |
| `/windsurf:planning` | Start planning workflow |
| `/windsurf:qa` | Enter QA/bug tracking mode |
| `/windsurf:status` | Show project status |

## How It Works

### Shared Data Model

```
.fstrent_spec_tasks/         # Shared across all IDEs
├── PLAN.md                  # Product requirements
├── TASKS.md                 # Master task list
├── BUGS.md                  # Bug tracking
├── tasks/                   # Individual task files
└── features/                # Feature documents

.windsurf/                   # Windsurf-specific
├── rules/                   # AI behavior rules
└── commands/                # Slash commands
```

### Cross-IDE Compatible

The `.fstrent_spec_tasks/` directory is shared across:
- ✅ **Windsurf** (you are here!)
- ✅ **Cursor** (via `.cursor/rules/`)
- ✅ **Claude Code** (via `.claude/skills/`)
- ✅ **Any IDE** (via `agents.md`)

Teams can use different IDEs without conflicts!

## File Structure

```
.windsurf/
├── README.md                           # This file
├── rules/
│   └── fstrent_spec_tasks/
│       ├── README.md                   # System overview
│       ├── rules/
│       │   ├── _index.md               # Rule index
│       │   ├── core.md                 # Task management
│       │   ├── planning.md             # Planning & PRD
│       │   ├── qa.md                   # Bug tracking
│       │   ├── workflow.md             # Workflow management
│       │   └── code_review.md          # Code review
│       └── commands/
│           ├── setup.md                # /windsurf:setup
│           ├── new_task.md             # /windsurf:new-task
│           ├── update_task.md          # /windsurf:update-task
│           ├── planning.md             # /windsurf:planning
│           ├── qa.md                   # /windsurf:qa
│           └── status.md               # /windsurf:status
```

## Key Features

### Task Management
- YAML-based task files
- Clear status progression: `[ ]` → `[📋]` → `[🔄]` → `[✅]`
- Windows-safe emojis
- Git-friendly format

### Planning System
- 27-question requirements framework
- Product Requirements Document (PRD) generation
- Feature documentation
- Scope validation

### QA & Bug Tracking
- Bug classification (Critical/High/Medium/Low)
- Design fix documentation
- Retroactive documentation
- Quality metrics

### Workflow Management
- Task expansion and breakdown
- Complexity assessment
- Methodology integration (Kanban, DevOps)
- Mermaid diagram generation

## Integration with agents.md

This system works alongside the `agents.md` standard:
- **agents.md**: Universal AI instructions (works with all IDEs)
- **Windsurf rules**: Windsurf-specific features and commands

Both are complementary, not conflicting!

## Getting Help

### Documentation
- **Full Setup Guide**: [docs/WINDSURF_ADAPTATION_GUIDE.md](../../docs/WINDSURF_ADAPTATION_GUIDE.md)
- **Main README**: [README.md](../../README.md)
- **agents.md**: [agents.md](../../agents.md)

### Common Questions

**Q: Do I need to install anything?**
A: No! The rules are automatically loaded when you open the project in Windsurf.

**Q: Can I use this with Cursor or Claude Code?**
A: Yes! All three share the same `.fstrent_spec_tasks/` directory. Use whichever IDE you prefer.

**Q: What if commands don't work?**
A: Make sure you're in the project root directory and try refreshing Windsurf's AI context.

## Quick Reference

### Task Status Emojis
- `[ ]` = Not started (no file created yet)
- `[📋]` = Ready (file created, can start)
- `[🔄]` = In progress
- `[✅]` = Completed
- `[❌]` = Failed/blocked

### Priority Levels
- `critical` = Blocking issue, immediate attention
- `high` = Important, schedule soon
- `medium` = Normal priority
- `low` = Nice to have, when time permits

### File Naming
- Tasks: `taskXXX_description.md` (e.g., `task042_add_authentication.md`)
- Subtasks: `taskXXX-Y_description.md` (e.g., `task042-1_setup_passport.md`)
- Features: `feature-name.md` (e.g., `user-authentication.md`)

## Next Steps

1. Run `/windsurf:setup` to initialize
2. Read [docs/WINDSURF_ADAPTATION_GUIDE.md](../../docs/WINDSURF_ADAPTATION_GUIDE.md) for detailed guide
3. Create your first task with `/windsurf:new-task`
4. Start planning with `/windsurf:planning`

---

**Version**: 1.0.0
**Compatible with**: Windsurf IDE, agents.md standard
**Cross-IDE**: Works with Cursor and Claude Code
