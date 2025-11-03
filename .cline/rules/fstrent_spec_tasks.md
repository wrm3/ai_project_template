# fstrent_spec_tasks Rules for Cline

This file consolidates all fstrent_spec_tasks rules for Cline.

## Core Principle

This project uses **fstrent_spec_tasks** - a file-based, cross-IDE task management system.

**All task data is in `.fstrent_spec_tasks/`** - shared across Claude Code, Cursor, Roo-Code, Cline, and Windsurf.

## CRITICAL: YAML Frontmatter Required

**Every task file MUST have YAML frontmatter:**

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

**Without YAML frontmatter, the system CANNOT process the task!**

## File Locations

- **Task Files:** `.fstrent_spec_tasks/tasks/task{id}_name.md`
- **Master List:** `.fstrent_spec_tasks/TASKS.md`
- **Context:** `.fstrent_spec_tasks/PROJECT_CONTEXT.md`
- **Plan:** `.fstrent_spec_tasks/PLAN.md`
- **Bugs:** `.fstrent_spec_tasks/BUGS.md`
- **Features:** `.fstrent_spec_tasks/features/`

## Task Creation Process

1. **Find Next ID:**
   - Read `.fstrent_spec_tasks/TASKS.md`
   - Find highest task number
   - New ID = max + 1 (zero-padded: 001, 002, etc.)

2. **Create Task File:**
   - Filename: `.fstrent_spec_tasks/tasks/task{id}_descriptive_name.md`
   - Add YAML frontmatter with all required fields
   - Add markdown content

3. **Update TASKS.md:**
   - Add entry: `- [ ] Task {id}: Brief description`
   - Place in appropriate section
   - Use proper emoji for status

4. **Verify:**
   - Both files created
   - IDs match
   - No duplicates

## Status Management

**Status Values:**
- `pending` - Not started
- `in-progress` - Currently working
- `completed` - Successfully finished
- `failed` - Blocked or abandoned

**Emojis in TASKS.md:**
- `[ ]` - Pending
- `[🔄]` - In Progress
- `[✅]` - Completed
- `[❌]` - Failed

**When changing status, ALWAYS update both files:**

1. Task file YAML: `status: completed`
2. TASKS.md entry: `[✅] Task 042: ...`

## Planning Workflow

1. **Gather Requirements** - Ask questions to understand needs
2. **Create PRD** - Document in `.fstrent_spec_tasks/PLAN.md`
3. **Validate Scope** - Ensure minimal viable solution
4. **Break Down Tasks** - Create individual task files
5. **Define Criteria** - Clear acceptance criteria

## Quality Assurance

1. **Bug Reporting** - Track in `.fstrent_spec_tasks/BUGS.md`
2. **Code Review** - Check security, style, best practices
3. **Testing** - Ensure adequate test coverage
4. **Documentation** - Keep docs synchronized with code

## Git Workflow

**Branch Naming:**
```
feature/task-042-user-authentication
bugfix/bug-123-login-issue
```

**Commit Messages:**
```
Task 042: Implement user authentication

- Add password hashing
- Implement JWT tokens
- Create login endpoint
```

**Pre-Commit:**
- Tests passing
- Code formatted
- Documentation updated
- Task status updated

## Python Projects

- Use `uv` for virtual environments
- Check for existing venv before creating
- Activate venv before running commands
- Keep requirements.txt updated

## Cross-IDE Compatibility

Changes must work in:
- Claude Code
- Cursor
- Roo-Code
- Cline (you are here)
- Windsurf

**All IDEs share `.fstrent_spec_tasks/`** - no IDE-specific task data!

## Documentation Standards

**Code Comments:**
- Explain WHY, not WHAT
- Document complex logic
- Include examples in docstrings

**README Files:**
- Setup instructions
- Usage examples
- Configuration details

**API Documentation:**
- Endpoint descriptions
- Request/response examples
- Error codes

## Natural Language Commands for Cline

Users will ask you to:
- "Create a new task for..."
- "Update task 042 to completed"
- "Show project status"
- "Start planning a feature..."
- "Generate quality report"
- "Review this code"
- "Report a bug about..."
- "Fix GitHub issue #123"

Interpret these naturally and follow the rules above.

## Task Types

- **feature** - New functionality
- **bug_fix** - Fix a defect
- **task** - General work item
- **enhancement** - Improve existing feature
- **refactor** - Code improvement without behavior change
- **testing** - Add or improve tests
- **documentation** - Documentation work

## Priority Levels

- **critical** - System down, urgent fix needed
- **high** - Important feature or serious bug
- **medium** - Normal priority
- **low** - Nice to have, low impact

## Sub-Tasks

For complex work, create sub-tasks:

```yaml
---
id: "042.1"
title: 'Subtask Description'
parent_task: 042
---
```

Parent task:
```yaml
---
id: 042
has_subtasks: true
subtasks: ["042.1", "042.2", "042.3"]
---
```

## Dependencies

Declare in YAML:
```yaml
dependencies: [001, 002, 041]
```

Meaning: Cannot start until tasks 001, 002, and 041 are completed.

## Common Mistakes to Avoid

❌ Missing YAML frontmatter
❌ Updating only task file OR TASKS.md (must update both)
❌ Invalid status values
❌ Duplicate task IDs
❌ Breaking cross-IDE compatibility

## Validation Checklist

When creating/updating tasks:
- [ ] YAML frontmatter present
- [ ] All required fields included
- [ ] Task file created/updated
- [ ] TASKS.md entry added/updated
- [ ] IDs are unique and sequential
- [ ] Status emojis correct
- [ ] Both files synchronized

## For More Details

See complete documentation:
- `agents.md` - Universal instructions
- `.claude/skills/fstrent-task-management/SKILL.md` - Full task system docs
- `.claude/skills/fstrent-planning/SKILL.md` - Planning process
- `.claude/skills/fstrent-qa/SKILL.md` - QA guidelines
- Example tasks in `.fstrent_spec_tasks/tasks/`

## Remember

- Always use YAML frontmatter
- Always update both files when changing status
- Cross-IDE compatibility is critical
- Natural language is fine - interpret user intent
- When in doubt, ask for clarification
