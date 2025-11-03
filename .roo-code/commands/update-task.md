# Roo-Code Command: update-task

Update an existing task's status or details.

## Usage

```
/update-task {task_id} {updates}
```

## Examples

**Update status to in-progress:**
```
/update-task 042 status=in-progress
```

**Mark task as completed:**
```
/update-task 042 status=completed
```

**Update priority:**
```
/update-task 042 priority=critical
```

**Add assignee:**
```
/update-task 042 assigned_to="John Doe"
```

## What This Command Does

1. **Locates Task** - Finds task file by ID
2. **Updates YAML** - Modifies frontmatter fields
3. **Updates TASKS.md** - Syncs master list status emoji
4. **Adds Metadata** - Includes completion date if applicable
5. **Validates** - Ensures both files stay synchronized

## Status Changes

Available status values:
- `pending` - Not started yet
- `in-progress` - Currently working on it
- `completed` - Successfully finished
- `failed` - Blocked or abandoned

## What Gets Updated

**Task File YAML:**
```yaml
---
status: completed
completed_date: '2025-11-02'
---
```

**TASKS.md Entry:**
```markdown
- [✅] Task 042: Implement user authentication
```

## Validation

The command will:
- ✅ Verify task ID exists
- ✅ Validate status value
- ✅ Update both files atomically
- ✅ Add completion date if completed
- ✅ Maintain file format and structure
