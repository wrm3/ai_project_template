# Roo-Code Command: status

Generate a comprehensive project status report.

## Usage

```
/status
```

## What This Command Does

Analyzes the project and provides:

1. **Task Statistics**
   - Total tasks
   - Pending tasks
   - In-progress tasks
   - Completed tasks
   - Failed tasks

2. **Progress Metrics**
   - Completion percentage
   - Tasks by priority
   - Tasks by type
   - Recent activity

3. **Current Focus**
   - Tasks currently in progress
   - Blocked tasks
   - Next tasks to tackle

4. **Health Indicators**
   - Overdue tasks
   - Stalled work items
   - Dependency issues

## Example Output

```markdown
# Project Status Report
Generated: 2025-11-02 14:30:00

## Summary
- Total Tasks: 50
- Completed: 35 (70%)
- In Progress: 5 (10%)
- Pending: 8 (16%)
- Failed: 2 (4%)

## Current Focus
### In Progress
- [🔄] Task 042: Implement user authentication
- [🔄] Task 045: Add email notifications
- [🔄] Task 048: Database optimization

## Next Up
- [ ] Task 050: User profile page
- [ ] Task 051: Admin dashboard
- [ ] Task 052: API documentation

## Issues
⚠️ Task 037: Blocked by external dependency
⚠️ Task 043: Stalled for 7 days

## Recommendations
1. Review blocked tasks
2. Break down Task 050 (complexity: high)
3. Schedule code review for completed work
```

## Options

**Brief status:**
```
/status brief
```

**Detailed status:**
```
/status detailed
```

**Filter by priority:**
```
/status priority=high
```

**Filter by type:**
```
/status type=feature
```
