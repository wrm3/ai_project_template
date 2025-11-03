# Always-Active Rules for {IDE_DISPLAY_NAME}

These rules apply to EVERY interaction with the AI assistant in {IDE_DISPLAY_NAME}.

## CRITICAL: YAML Frontmatter Required

ALL task files MUST have YAML frontmatter:

```yaml
---
id: 042
title: 'Task Description'
type: feature|bug_fix|task|enhancement
status: pending|in-progress|completed|failed
priority: critical|high|medium|low
---
```

## File Locations

- **Task Files:** `.fstrent_spec_tasks/tasks/task{id}_name.md`
- **Master List:** `.fstrent_spec_tasks/TASKS.md`
- **Context:** `.fstrent_spec_tasks/PROJECT_CONTEXT.md`
- **Plan:** `.fstrent_spec_tasks/PLAN.md`

## Status Synchronization

When updating task status, ALWAYS update BOTH:
1. Task file YAML: `status: completed`
2. TASKS.md entry: `[✅] Task 042: ...`

## Status Emojis

- `[ ]` - Pending
- `[🔄]` - In Progress
- `[✅]` - Completed
- `[❌]` - Failed

## Cross-IDE Compatibility

This project supports multiple IDEs. All changes must work in:
- Claude Code, Cursor, Roo-Code, Cline, Windsurf, {IDE_DISPLAY_NAME}

**Shared data:** `.fstrent_spec_tasks/` is shared across ALL IDEs.

## Response Format

Include in every response:
1. Current timestamp
2. Tools/commands used
3. Files modified
4. Next steps
