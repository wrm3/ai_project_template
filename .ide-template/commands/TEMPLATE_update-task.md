# {IDE_DISPLAY_NAME} Command: update-task

Update existing task status or details.

## Usage

```
{COMMAND_PREFIX}update-task {task_id} {updates}
```

## Examples

```
{COMMAND_PREFIX}update-task 042 status=in-progress
{COMMAND_PREFIX}update-task 042 status=completed
{COMMAND_PREFIX}update-task 042 priority=critical
```

## What Gets Updated

- Task file YAML frontmatter
- TASKS.md entry (status emoji)
- Completion date (if completed)

Both files updated atomically.
