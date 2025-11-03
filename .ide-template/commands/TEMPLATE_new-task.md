# {IDE_DISPLAY_NAME} Command: new-task

Create a new task in the fstrent_spec_tasks system.

## Usage

```
{COMMAND_PREFIX}new-task Brief description of the task
```

## What This Command Does

1. Gathers task information (type, priority, subsystems, dependencies)
2. Creates task file in `.fstrent_spec_tasks/tasks/` with YAML frontmatter
3. Updates TASKS.md with new entry
4. Validates format and IDs

## Examples

```
{COMMAND_PREFIX}new-task Implement user authentication with JWT
{COMMAND_PREFIX}new-task Fix login bug with special characters
{COMMAND_PREFIX}new-task Add email notification system
```

## Output

Creates:
- Task file: `.fstrent_spec_tasks/tasks/task042_name.md`
- TASKS.md entry: `- [ ] Task 042: Description`

Provides:
- Task ID and location
- Summary of details
- Next steps
