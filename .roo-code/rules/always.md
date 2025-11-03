# Always-Active Rules for Roo-Code

These rules apply to EVERY interaction with the AI assistant in Roo-Code.

## Critical: YAML Frontmatter Required

**ALL task files MUST have YAML frontmatter at the top:**

```yaml
---
id: 042
title: 'Task Description'
type: feature
status: pending
priority: high
---
```

**Without YAML frontmatter, the task management system CANNOT process the file!**

## File Locations

### Task System Files
- **Task Files:** `.fstrent_spec_tasks/tasks/task{id}_name.md`
- **Master List:** `.fstrent_spec_tasks/TASKS.md`
- **Project Context:** `.fstrent_spec_tasks/PROJECT_CONTEXT.md`
- **Project Plan:** `.fstrent_spec_tasks/PLAN.md`
- **Bug Tracking:** `.fstrent_spec_tasks/BUGS.md`

### Configuration Files
- **Roo-Code Rules:** `.roo-code/rules/`
- **Roo-Code Commands:** `.roo-code/commands/`
- **Settings:** `.roo-code/settings.json`
- **Universal Instructions:** `agents.md` (root)

## Status Synchronization

**CRITICAL:** When updating task status, ALWAYS update BOTH files:

1. **Task File YAML:**
   ```yaml
   status: completed
   ```

2. **TASKS.md Entry:**
   ```markdown
   - [✅] Task 042: Implement feature
   ```

**Never update one without the other!**

## Windows-Safe Emojis

Use these EXACT emojis in TASKS.md:
- `[ ]` - Pending
- `[🔄]` - In Progress
- `[✅]` - Completed
- `[❌]` - Failed

## Cross-IDE Compatibility

This project supports multiple IDEs. All changes must work in:
- ✅ Claude Code (`.claude/`)
- ✅ Cursor (`.cursor/`)
- ✅ Roo-Code (`.roo-code/`) ← You are here
- ✅ Cline (`.cline/`)
- ✅ Windsurf (`.windsurf/`)

**Shared Data:** `.fstrent_spec_tasks/` is shared across ALL IDEs.

## Before Every Task Creation

1. Read `.fstrent_spec_tasks/TASKS.md` to find next ID
2. Create task file with YAML frontmatter
3. Update TASKS.md with new entry
4. Verify both files are synchronized

## Response Format

In every response, include:
1. Current timestamp
2. Tools used during the interaction
3. Files created or modified
4. Next steps or recommendations

## Python Virtual Environments

When working with Python projects:
- Use `uv` for virtual environment management
- Check for existing venv before creating new one
- Activate venv before running Python commands

## File Size Awareness

If any file exceeds 800 lines:
- Suggest refactoring to smaller modules
- Become more insistent at 1000+ lines
- Offer to help with code organization

## Tool Awareness

Before starting work, check available tools:
- MCP servers (if configured)
- Git integration
- Testing frameworks
- Linting/formatting tools

Use tools whenever appropriate instead of manual work.
