# Roo-Code Command: new-task

Create a new task in the fstrent_spec_tasks system.

## Usage

```
/new-task Brief description of the task
```

## What This Command Does

1. **Gathers Information** - Asks you for:
   - Task type (feature, bug_fix, enhancement, etc.)
   - Priority level (critical, high, medium, low)
   - Related feature (if applicable)
   - Affected subsystems
   - Dependencies on other tasks

2. **Creates Task File** - Generates:
   - Task file in `.fstrent_spec_tasks/tasks/` with YAML frontmatter
   - Comprehensive task description
   - Acceptance criteria
   - Implementation notes
   - Testing plan

3. **Updates TASKS.md** - Adds new entry with:
   - Proper emoji status indicator `[ ]`
   - Task ID and title
   - Correct phase/category

4. **Ensures Quality** - Validates:
   - YAML schema is correct
   - File naming follows convention
   - No duplicate task IDs
   - Cross-references are accurate

## Examples

```
/new-task Implement user authentication with JWT
```

```
/new-task Fix login bug with special characters in password
```

```
/new-task Add email notification system
```

## Response Format

The command will create:

**Task File:** `.fstrent_spec_tasks/tasks/task042_implement_auth.md`
```yaml
---
id: 042
title: 'Implement User Authentication'
type: feature
status: pending
priority: high
---

# Task 042: Implement User Authentication
...
```

**TASKS.md Entry:**
```markdown
- [ ] Task 042: Implement user authentication with JWT
```

## After Task Creation

The AI will provide:
- Task ID and file location
- Summary of task details
- Next steps to begin work
- Links to related documentation
