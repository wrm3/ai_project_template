# Task Management Rules for {IDE_DISPLAY_NAME}

For complete documentation, see: `.claude/rules/task_management.md`

## Quick Reference

### Task File Format
```yaml
---
id: 042
title: 'Brief Description'
type: feature|bug_fix|task|enhancement
status: pending|in-progress|completed|failed
priority: critical|high|medium|low
---

# Task 042: Brief Description

## Objective
What needs to be done...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### Creating Tasks in {IDE_DISPLAY_NAME}
Use `{COMMAND_PREFIX}new-task` command for automatic creation.

### Updating Tasks
Use `{COMMAND_PREFIX}update-task {id}` to sync both files.

## Critical Rules

1. YAML frontmatter REQUIRED
2. Update both task file + TASKS.md
3. Sequential IDs (001, 002, 003...)
4. Cross-IDE compatible
