---
name: Task Management
description: Manage project tasks using fstrent_tasks system. Use when creating tasks, updating task status, planning features, or organizing project work.
allowed-tools: Read, Write, Edit
---

# Task Management Skill

## Overview
This Skill provides expertise in using the fstrent_tasks task management system integrated via MCP tools.

## Capabilities
- Create and manage tasks
- Update task status
- Track project progress
- Organize features and requirements
- Maintain project context
- Archive completed work

## Task Management System Structure
```
.fstrent_spec_tasks/
├── tasks/                       # Individual task files
│   └── task{id}_name.md
├── features/                    # Feature documentation
│   └── feature-name.md
├── TASKS.md                     # Master task checklist
├── PLAN.md                      # Product Requirements Document
├── PROJECT_CONTEXT.md           # Project goals and context
├── SUBSYSTEMS.md                # Component registry
└── FILE_REGISTRY.md             # File documentation
```

## When to Use
Use this Skill when:
- Creating new tasks
- Updating task status
- Planning features
- Tracking project progress
- Organizing work
- User mentions: "task", "todo", "plan", "feature", "track progress"

## Task Workflow

### 1. Creating Tasks
**Task File Format:** `task{id}_descriptive_name.md`

**YAML Frontmatter:**
```yaml
---
id: {number}
title: 'Task Title'
type: task|bug_fix|feature
status: pending|in-progress|completed|failed
priority: critical|high|medium|low
feature: Feature Name
subsystems: [affected_subsystems]
project_context: Brief connection to project goal
dependencies: [task_ids]
---
```

### 2. Task Status Indicators
- `[ ]` - Pending (not started)
- `[🔄]` - In Progress (actively working)
- `[✅]` - Completed (finished successfully)
- `[❌]` - Failed (abandoned or blocked)

### 3. Updating TASKS.md
Always update the master checklist when task status changes:
```markdown
## Active Tasks
- [ ] Task 001: Description
- [🔄] Task 002: Description (in progress)
- [✅] Task 003: Description (completed)
```

### 4. Feature Planning
Create feature documents in `features/` folder:
```markdown
# Feature: [Name]

## Overview
Brief description

## Requirements
- Requirement 1
- Requirement 2

## User Stories
- As a [user], I want [action] so that [benefit]

## Technical Considerations
- Subsystems affected
- Dependencies
- Integration points

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

## MCP Tool Integration
This Skill works with fstrent_tasks MCP tools:
- `fstrent_tasks_setup` - Initialize task system
- `get_datetime` - Get timestamps for task updates

## Best Practices

### Task Creation
- Use clear, actionable titles
- Include acceptance criteria
- Specify dependencies
- Link to related features
- Estimate effort when possible

### Task Updates
- Update status immediately when starting/completing
- Keep TASKS.md synchronized
- Document blockers and issues
- Archive completed tasks periodically

### Project Planning
- Start with PROJECT_CONTEXT.md
- Create PLAN.md for major features
- Break large tasks into subtasks
- Track subsystem relationships

### File Organization
- One task per file
- Descriptive filenames
- Consistent YAML format
- Clear documentation

## Task Complexity Assessment
**Simple Task (proceed normally):**
- Single file changes
- Clear requirements
- < 1 day effort

**Complex Task (consider expansion):**
- Multiple subsystems affected
- Unclear requirements
- > 2 days effort
- Multiple dependencies

**High Complexity (must expand):**
- Cross-cutting concerns
- Architectural changes
- > 1 week effort
- Break into subtasks: `task{parent}.{sub}_name.md`

## Progress Tracking
Monitor project health through:
- Task completion rate
- Blocked tasks
- Feature progress
- Subsystem impact
- Dependency chains

## Common Commands
```bash
# View all tasks
cat .fstrent_spec_tasks/TASKS.md

# View project plan
cat .fstrent_spec_tasks/PLAN.md

# View project context
cat .fstrent_spec_tasks/PROJECT_CONTEXT.md

# List task files
ls .fstrent_spec_tasks/tasks/
```

## Integration with Other Systems
- Links to bug tracking (BUGS.md)
- References features and requirements
- Tracks file changes (FILE_REGISTRY.md)
- Documents subsystems (SUBSYSTEMS.md)

## Resources
- Task templates in `.fstrent_spec_tasks/tasks/`
- Feature templates in `.fstrent_spec_tasks/features/`
- Planning templates in PLAN.md
- Context templates in PROJECT_CONTEXT.md

