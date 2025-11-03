# {IDE_DISPLAY_NAME} Configuration for fstrent_spec_tasks

**Version:** 1.0
**IDE:** {IDE_DISPLAY_NAME}
**Configuration Directory:** `{CONFIG_DIR}`

## Overview

This directory contains {IDE_DISPLAY_NAME}-specific configuration for the **fstrent_spec_tasks** system - a comprehensive, file-based task management and workflow system that works across all AI coding IDEs.

## What is {IDE_DISPLAY_NAME}?

**{IDE_DISPLAY_NAME}** is {IDE_DESCRIPTION}.

**Official Site:** {IDE_URL}

## Directory Structure

```
{CONFIG_DIR}
├── README.md           # This file
├── {SETTINGS_FILE}    # Configuration
├── rules/             # Core behavior rules
│   ├── always.md
│   ├── task_management.md
│   ├── planning_workflow.md
│   ├── qa_bug_tracking.md
│   ├── git_workflow.md
│   ├── documentation.md
│   ├── python_env.md
│   └── parallel_workflow.md
└── commands/          # Custom commands
    ├── new-task.md
    ├── update-task.md
    ├── status.md
    ├── start-planning.md
    ├── quality-report.md
    ├── review.md
    ├── add-feature.md
    ├── report-bug.md
    └── fix-github-issue.md
```

## Quick Start

### Prerequisites

- {IDE_DISPLAY_NAME} installed
- Git repository initialized
- API key configured for AI model

### Using Commands

{IDE_DISPLAY_NAME} supports custom commands using the `{COMMAND_PREFIX}` prefix:

```
{COMMAND_PREFIX}new-task Implement user authentication
{COMMAND_PREFIX}update-task 042 status=completed
{COMMAND_PREFIX}status
```

## Available Commands

- `{COMMAND_PREFIX}new-task` - Create new task
- `{COMMAND_PREFIX}update-task` - Update task status
- `{COMMAND_PREFIX}status` - Project status report
- `{COMMAND_PREFIX}start-planning` - Begin feature planning
- `{COMMAND_PREFIX}quality-report` - Generate QA report
- `{COMMAND_PREFIX}review` - Code review workflow
- `{COMMAND_PREFIX}add-feature` - Add new feature
- `{COMMAND_PREFIX}report-bug` - Report and track bug
- `{COMMAND_PREFIX}fix-github-issue` - Fix GitHub issue

## Core Rules

All fstrent_spec_tasks rules are in `{RULES_DIR}`.

### Key Principles

1. **YAML Frontmatter Required** - All task files must have YAML metadata
2. **File-Based System** - Tasks stored in `.fstrent_spec_tasks/`
3. **Cross-IDE Compatible** - Works with all supported IDEs
4. **Status Synchronization** - Task file and TASKS.md always match

## Integration with Other IDEs

### Shared Data Layer

All IDEs share the same data in `.fstrent_spec_tasks/`:

```
.fstrent_spec_tasks/     # SHARED ACROSS ALL IDEs
├── TASKS.md             # Master task list
├── PLAN.md              # Project plan
├── PROJECT_CONTEXT.md   # Project context
├── tasks/               # Individual task files
└── features/            # Feature documentation
```

### Supported IDEs

- Claude Code (`.claude/`)
- Cursor (`.cursor/`)
- Windsurf (`.windsurf/`)
- Roo-Code (`.roo-code/`)
- Cline (`.cline/`)
- **{IDE_DISPLAY_NAME} (`{CONFIG_DIR}`)** ← You are here

## Best Practices

1. Use commands for task management
2. Check status regularly
3. Follow planning process
4. Maintain quality standards
5. Sync with team frequently

## Troubleshooting

### Commands Not Working

Check that:
- Configuration directory exists
- Settings file is valid
- Commands directory contains command files
- IDE loaded configuration

### Rules Not Applying

Verify:
- Rules directory exists
- Rule files are valid markdown
- Settings specify correct rules path

## Resources

- **Main Docs:** `agents.md`
- **Task Guide:** `.claude/skills/fstrent-task-management/SKILL.md`
- **Planning Guide:** `.claude/skills/fstrent-planning/SKILL.md`
- **Examples:** `.fstrent_spec_tasks/tasks/`

---

**Happy Coding with {IDE_DISPLAY_NAME}!**
