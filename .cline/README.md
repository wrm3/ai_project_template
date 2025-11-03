# Cline Configuration for fstrent_spec_tasks

**Version:** 1.0
**Last Updated:** November 2025
**Status:** Production Ready

## Overview

This directory contains Cline-specific configuration for the **fstrent_spec_tasks** system - a comprehensive, file-based task management and workflow system that works across all AI coding IDEs.

Cline is a popular VS Code extension that brings AI coding assistance with a focus on simplicity and efficiency.

## What is Cline?

**Cline** is a VS Code extension that provides:
- AI-powered code completion and generation
- Chat-based development interface
- File editing and project management
- Multi-model support (Claude, GPT-4, etc.)
- Simple, focused user experience

**VS Code Marketplace:** Search for "Cline" in VS Code extensions

## Directory Structure

```
.cline/
├── README.md           # This file
├── settings.json      # Cline configuration
└── rules/            # Combined rules file
    └── fstrent_spec_tasks.md
```

**Note:** Cline uses a simplified structure with consolidated rules compared to other IDEs.

## Quick Start

### 1. Prerequisites

- VS Code installed
- Cline extension installed from marketplace
- Git repository initialized
- API key configured for AI model

### 2. Installation

Cline will automatically detect the `.cline/` configuration when you open this project.

### 3. Using Cline Commands

Cline uses natural language commands in its chat interface:

```
Create a new task for user authentication

Update task 042 to completed status

Show me the project status

Start planning a new notifications feature

Generate a quality report
```

## Available Commands (Natural Language)

Cline doesn't use slash commands like other IDEs. Instead, use natural language:

### Task Management

**Create Task:**
```
Create a new task: Implement user authentication with JWT tokens
```

**Update Task:**
```
Update task 042 status to completed
Mark task 42 as in-progress
```

**View Status:**
```
Show project status
What tasks are pending?
Which tasks are in progress?
```

### Planning

**Start Planning:**
```
Let's plan a new feature for real-time notifications
Start planning user authentication system
```

**Add Feature:**
```
Add a new feature: Email notification system
```

### Quality Assurance

**Quality Report:**
```
Generate a quality report
Show me quality metrics
```

**Report Bug:**
```
Report a bug: Login fails with special characters
```

**Code Review:**
```
Review the code in src/auth/
Perform code review on recent changes
```

### GitHub Integration

**Fix Issue:**
```
Fix GitHub issue #123
Work on issue 123 from GitHub
```

## Core Rules

All fstrent_spec_tasks rules are consolidated in `.cline/rules/fstrent_spec_tasks.md`.

### Key Principles

1. **YAML Frontmatter Required** - All task files must have YAML metadata
2. **File-Based System** - Tasks stored in `.fstrent_spec_tasks/`
3. **Cross-IDE Compatible** - Works with Claude Code, Cursor, Roo-Code, Windsurf
4. **Status Synchronization** - Task file and TASKS.md always match

### Task File Format

```yaml
---
id: 042
title: 'Implement User Authentication'
type: feature
status: pending
priority: high
---

# Task 042: Implement User Authentication

## Objective
Create secure user authentication system...

## Acceptance Criteria
- [ ] Password hashing implemented
- [ ] JWT tokens working
- [ ] Login endpoint created
```

### Status Emojis

In TASKS.md:
- `[ ]` - Pending
- `[🔄]` - In Progress
- `[✅]` - Completed
- `[❌]` - Failed

## Configuration

### settings.json

The `.cline/settings.json` file contains minimal configuration:

```json
{
  "cline.taskSystem": "fstrent_spec_tasks",
  "cline.taskDirectory": ".fstrent_spec_tasks",
  "cline.rulesFile": ".cline/rules/fstrent_spec_tasks.md"
}
```

## Integration with Other IDEs

### Shared Data Layer

All IDEs share the same data:

```
.fstrent_spec_tasks/     # SHARED ACROSS ALL IDEs
├── TASKS.md             # Master task list
├── PLAN.md              # Project plan
├── PROJECT_CONTEXT.md   # Project context
├── BUGS.md              # Bug tracking
├── tasks/               # Individual task files
└── features/            # Feature documentation
```

### IDE-Specific Directories

Each IDE has its own configuration:

- `.claude/` - Claude Code configuration
- `.cursor/` - Cursor IDE rules (.mdc format)
- `.roo-code/` - Roo-Code configuration
- `.cline/` - **Cline configuration** (you are here)
- `.windsurf/` - Windsurf IDE configuration

All IDEs can work on the same project simultaneously without conflicts!

## Best Practices for Cline Users

### 1. Use Natural Language

Cline excels at understanding intent. Be clear and specific:

✅ Good:
```
Create a new high-priority task for implementing JWT authentication
with bcrypt password hashing. This should include login endpoint,
token validation, and rate limiting.
```

❌ Less Effective:
```
new task auth
```

### 2. Request Context

Ask Cline to review project context before starting:

```
Review the project context and current tasks before we begin
```

### 3. Break Down Complex Work

For large features, work iteratively:

```
Let's plan the authentication feature first, then break it into tasks
```

### 4. Request Reviews

Ask for code review before committing:

```
Review the authentication code I just wrote for security issues
```

### 5. Sync Regularly

Check project status to stay aligned:

```
Show me current project status and next priorities
```

## Cline-Specific Workflows

### Feature Development Workflow

1. **Plan:**
   ```
   Let's plan a new user authentication feature
   ```

2. **Create Tasks:**
   ```
   Break down the authentication feature into individual tasks
   ```

3. **Implement:**
   ```
   Let's work on task 042 - implement password hashing
   ```

4. **Review:**
   ```
   Review the code for task 042
   ```

5. **Update:**
   ```
   Mark task 042 as completed
   ```

### Bug Fix Workflow

1. **Report:**
   ```
   Report a bug: users can't log in with emails containing + symbol
   ```

2. **Investigate:**
   ```
   Let's investigate the login bug and find the root cause
   ```

3. **Fix:**
   ```
   Create a task to fix the email validation issue
   ```

4. **Test:**
   ```
   Help me write tests for the email validation fix
   ```

5. **Close:**
   ```
   Mark the bug as fixed and update task status
   ```

## File Locations Reference

### Task Files
**Location:** `.fstrent_spec_tasks/tasks/`
**Naming:** `task{id}_descriptive_name.md`
**Example:** `task042_implement_authentication.md`

### Master Task List
**Location:** `.fstrent_spec_tasks/TASKS.md`
**Purpose:** Central checklist with status indicators

### Project Documentation
- **Context:** `.fstrent_spec_tasks/PROJECT_CONTEXT.md`
- **Plan:** `.fstrent_spec_tasks/PLAN.md`
- **Bugs:** `.fstrent_spec_tasks/BUGS.md`
- **Features:** `.fstrent_spec_tasks/features/`

## Troubleshooting

### Cline Not Following Rules

**Problem:** Cline not respecting fstrent_spec_tasks format

**Solutions:**
1. Explicitly mention the rules:
   ```
   Follow the fstrent_spec_tasks rules when creating this task
   ```
2. Check that `.cline/rules/fstrent_spec_tasks.md` exists
3. Restart VS Code to reload configuration

### Task Files Not Created Properly

**Problem:** Missing YAML frontmatter

**Solutions:**
1. Ask Cline to validate:
   ```
   Ensure the task file has proper YAML frontmatter
   ```
2. Reference example tasks:
   ```
   Create the task file following the same format as task001
   ```

### Status Sync Issues

**Problem:** TASKS.md and task file out of sync

**Solutions:**
1. Ask Cline to sync:
   ```
   Update both the task file and TASKS.md for task 042
   ```
2. Always request both updates together:
   ```
   Mark task 042 as completed in both the task file and master list
   ```

## Advanced Usage

### Custom Instructions

You can add project-specific instructions to Cline's chat:

```
For this project, always:
1. Create task files with YAML frontmatter
2. Update TASKS.md when changing status
3. Use descriptive commit messages
4. Run tests before marking tasks complete
```

### Multi-File Edits

Cline can edit multiple files at once:

```
Update task 042 status to completed in both the task file
and TASKS.md, then commit the changes with a proper message
```

### Context Preservation

Cline maintains conversation context. Use this for complex workflows:

```
First, show me all pending high-priority tasks.
Then let's review task 042.
Finally, update it to in-progress and begin implementation.
```

## Resources

### Documentation
- **Main Documentation:** `agents.md` in project root
- **Task System Guide:** `.claude/skills/fstrent-task-management/SKILL.md`
- **Planning Guide:** `.claude/skills/fstrent-planning/SKILL.md`
- **QA Guide:** `.claude/skills/fstrent-qa/SKILL.md`

### Examples
- **Example Tasks:** `.fstrent_spec_tasks/tasks/`
- **Example Project:** `example-project/`

### External Links
- **agents.md Standard:** https://agents.md
- **Cline Extension:** VS Code Marketplace
- **fstrent_spec_tasks GitHub:** (your repository URL)

## Migration from Other IDEs

### From Any IDE to Cline

The `.fstrent_spec_tasks/` data is universal:

1. Install Cline extension in VS Code
2. Open the project
3. Start chatting with Cline
4. All task files work immediately!

No migration needed - just use natural language commands instead of slash commands.

### From Cline to Other IDEs

If you want to try other IDEs:

1. All your task data is preserved
2. Other IDEs have their own configurations
3. Can use multiple IDEs on same project
4. No data conversion required

## Support

### Getting Help

1. **Ask Cline:**
   ```
   How do I create a new task in the fstrent_spec_tasks system?
   ```

2. **Check Documentation:** Review `agents.md` and this README

3. **Review Examples:** Look at existing task files

### Reporting Issues

If you find issues:

```
Report a bug: Cline not creating YAML frontmatter in task files
```

### Contributing

To improve the Cline configuration:

1. Test changes in Cline
2. Ensure cross-IDE compatibility
3. Update documentation
4. Submit pull request

---

**Happy Coding with Cline!** 🤖

The fstrent_spec_tasks system + Cline's natural language interface = Powerful, intuitive development workflow.

**Tip:** Just talk to Cline naturally - it understands what you want to do!
