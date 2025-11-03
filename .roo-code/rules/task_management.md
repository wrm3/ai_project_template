# Task Management Rules (Roo-Code)

For complete task management documentation, see: `.claude/rules/task_management.md`

This file contains Roo-Code-specific quick reference.

## Quick Reference

### Task File Structure
```yaml
---
id: 042
title: 'Brief Task Description'
type: feature|bug_fix|task|enhancement
status: pending|in-progress|completed|failed
priority: critical|high|medium|low
---

# Task 042: Brief Task Description

## Objective
What needs to be done...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### File Locations
- **Tasks:** `.fstrent_spec_tasks/tasks/task{id}_name.md`
- **Master List:** `.fstrent_spec_tasks/TASKS.md`
- **Context:** `.fstrent_spec_tasks/PROJECT_CONTEXT.md`

### Status Emojis (for TASKS.md)
- `[ ]` - Pending
- `[🔄]` - In Progress
- `[✅]` - Completed
- `[❌]` - Failed

### Creating Tasks in Roo-Code
Use the `/new-task` command for automatic task creation with proper YAML.

### Updating Tasks in Roo-Code
Use the `/update-task {id}` command to synchronize both task file and TASKS.md.

## Critical Rules

1. **YAML frontmatter is REQUIRED** - No exceptions
2. **Update both files** - Task file YAML + TASKS.md entry
3. **Sequential IDs** - Always use next available number
4. **Cross-IDE compatible** - Changes work in all supported IDEs

For detailed rules, see `.claude/rules/task_management.md`
