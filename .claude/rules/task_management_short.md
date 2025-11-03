# Task Management - Critical Format Requirement

**⚠️ CRITICAL:** All task files MUST have YAML frontmatter or they will break the task management system.

## Required YAML Format

Every task file in `.fstrent_spec_tasks/tasks/` MUST start with:

```yaml
---
id: {number}
title: 'Task Title'
type: task|bug_fix|feature|retroactive_fix
status: pending|in-progress|completed|failed
priority: critical|high|medium|low
feature: 'Feature Name'
subsystems: [list, of, systems]
estimated_effort: 'time estimate'
created_date: 'YYYY-MM-DD'
---
```

## File Naming

Format: `task{id}_descriptive_name.md`
Examples: `task001_setup_database.md`, `task062_right_align_status.md`

## Common Mistakes to Avoid

❌ **WRONG:** Creating task file without YAML frontmatter
❌ **WRONG:** Missing `---` delimiters
❌ **WRONG:** Using tabs instead of spaces in YAML
❌ **WRONG:** Forgetting to update TASKS.md

✅ **RIGHT:** Always include complete YAML frontmatter
✅ **RIGHT:** Update both task file AND TASKS.md
✅ **RIGHT:** Use fstrent-task-management skill for guidance

## When You Need More Help

For complete task management instructions, invoke:
```
/skill fstrent-task-management
```

This loads the full task management skill with:
- Complete YAML schema reference
- Task creation workflow
- Status update procedures
- Windows emoji guide
- Example task files
