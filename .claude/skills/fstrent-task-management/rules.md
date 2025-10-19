# Task Management Rules

> Detailed implementation rules for the fstrent-task-management Skill.
> These rules are derived from Cursor's fstrent_spec_tasks system
> and maintain 100% cross-IDE compatibility.

## Overview

These rules provide comprehensive guidance for implementing task management using the fstrent_spec_tasks system. They cover task file formats, YAML validation, status management, file naming conventions, and integration with the broader project management ecosystem.

## Core Task Management Rules

### Task File Creation

**Location**: `.fstrent_spec_tasks/tasks/`

**Naming Convention**: `task{id}_descriptive_name.md`
- ID must be zero-padded to 3 digits (001, 002, etc.)
- Descriptive name uses underscores, lowercase
- Examples: `task001_setup_database.md`, `task042_implement_auth.md`

**Creation Process**:
1. Determine next available task ID
2. Create task file with proper naming
3. Add YAML frontmatter with required fields
4. Add task content (objective, criteria, notes)
5. Update TASKS.md with new entry

### YAML Frontmatter Validation

**Required Fields**:
```yaml
---
id: {number}                    # Sequential ID (001, 002, etc.)
title: 'Task Title'             # Brief, actionable title
type: task|bug_fix|feature|retroactive_fix
status: pending|in-progress|completed|failed
priority: critical|high|medium|low
---
```

**Optional Fields**:
```yaml
feature: Feature Name           # Related feature (optional)
subsystems: [list]              # Affected system components
project_context: 'Brief description'
dependencies: [task_ids]        # Tasks that must complete first
estimated_effort: 'time estimate'
created_date: 'YYYY-MM-DD'
completed_date: 'YYYY-MM-DD'
assigned_to: 'Developer name'
```

**Validation Rules**:
- `id` must be unique across all tasks
- `title` must be non-empty string
- `type` must be one of allowed values
- `status` must be one of allowed values
- `priority` must be one of allowed values
- `dependencies` must reference existing task IDs
- Dates must be in ISO format (YYYY-MM-DD)

### Status Management Rules

**Status Lifecycle**:
```
pending → in-progress → completed
                     ↓
                   failed
```

**Status Update Procedure**:
1. **Start Task** (`pending` → `in-progress`):
   - Update task file YAML: `status: in-progress`
   - Update TASKS.md: `[ ]` → `[🔄]`
   - Optional: Add `started_date` field

2. **Complete Task** (`in-progress` → `completed`):
   - Update task file YAML: `status: completed`
   - Update TASKS.md: `[🔄]` → `[✅]`
   - Add `completed_date` field
   - Document actual effort if estimated

3. **Fail Task** (`in-progress` → `failed`):
   - Update task file YAML: `status: failed`
   - Update TASKS.md: `[🔄]` → `[❌]`
   - Add failure reason in task notes
   - Consider creating new task for retry

**Atomic Updates**:
- Task file and TASKS.md must be updated together
- Never update one without the other
- Use transaction-like approach (update both or neither)

### Windows Emoji Requirements

**Status Indicators**:
- `[ ]` - Pending (checkbox, not emoji)
- `[🔄]` - In Progress (counterclockwise arrows)
- `[✅]` - Completed (check mark button)
- `[❌]` - Failed (cross mark)

**Why These Emojis**:
- Windows-safe (render correctly on Windows 10/11)
- Clear visual distinction
- Supported across all terminals and IDEs
- Part of Unicode standard

**Usage in TASKS.md**:
```markdown
- [ ] Task 001: Setup database
- [🔄] Task 002: Implement authentication
- [✅] Task 003: Create user interface
- [❌] Task 004: Deploy to production (failed)
```

### Task ID Assignment

**Sequential Assignment**:
- Start at 001
- Increment by 1 for each new task
- Never reuse IDs (even for deleted tasks)
- Zero-pad to 3 digits (001-999)
- After 999, use 4 digits (1000-9999)

**ID Determination**:
1. Read all existing task files
2. Extract ID from each filename
3. Find maximum ID
4. New ID = max ID + 1

**Sub-Task IDs**:
- Format: `{parent_id}.{sub_id}`
- Example: `042.1`, `042.2`, `042.3`
- Sub-IDs are strings, not numbers
- Filename: `task042.1_setup_database.md`

### TASKS.md Update Procedures

**File Structure**:
```markdown
# Project Name - Task List

## Active Tasks

### Phase 1: Foundation
- [ ] Task 001: Setup project
- [🔄] Task 002: Configure environment

### Phase 2: Development
- [ ] Task 010: Implement feature A
- [ ] Task 011: Implement feature B

## Completed Tasks
- [✅] Task 000: Initial planning

## Blocked Tasks
- [ ] Task 020: Deploy (blocked by Task 002)
```

**Update Rules**:
- Group tasks by phase or category
- Keep active tasks at top
- Move completed tasks to "Completed Tasks" section
- Document blocked tasks with blocking reason
- Maintain consistent formatting

**Atomic Update Pattern**:
```
1. Read current TASKS.md
2. Locate task entry by ID
3. Update status emoji
4. Write back to TASKS.md
5. Verify update succeeded
```

### Sub-Task Creation Rules

**When to Create Sub-Tasks**:
- Task complexity score ≥ 7 (see workflow rules)
- Task spans multiple subsystems
- Task has distinct, sequential phases
- Task estimated > 2-3 developer days

**Sub-Task Structure**:
```
Parent: task042_implement_authentication.md
Sub-tasks:
  - task042.1_setup_database.md
  - task042.2_create_api.md
  - task042.3_build_ui.md
```

**Sub-Task YAML**:
```yaml
---
id: "042.1"              # String ID for sub-tasks
title: 'Setup Database'
type: task
status: pending
priority: high
parent_task: 042
dependencies: []        # Can depend on other tasks/sub-tasks
---
```

**Parent Task Update**:
- Add `has_subtasks: true` field
- Add `subtasks: [042.1, 042.2, 042.3]` field
- Parent status = `in-progress` when any subtask started
- Parent status = `completed` when all subtasks completed

### Dependency Management

**Dependency Types**:
- **Hard Dependency**: Task cannot start until dependency completes
- **Soft Dependency**: Task can start but may need rework
- **Blocking**: Task blocks another task from starting

**Dependency Declaration**:
```yaml
dependencies: [001, 002, 003]  # Task IDs
```

**Dependency Validation**:
- All dependency IDs must exist
- No circular dependencies allowed
- Dependency graph must be acyclic (DAG)

**Dependency Checking**:
```
Before starting task:
1. Read task file
2. Check dependencies field
3. For each dependency ID:
   - Read dependency task file
   - Verify status = completed
4. If all dependencies completed → can start
5. If any dependency not completed → blocked
```

### Error Handling

**File Not Found**:
- Task file missing → Error, cannot proceed
- TASKS.md missing → Create from template
- Feature file missing → Warning, continue

**Invalid YAML**:
- Syntax error → Fail with clear error message
- Missing required field → Fail with field name
- Invalid field value → Fail with allowed values

**Concurrent Updates**:
- Read-modify-write pattern
- Check file timestamp before write
- Retry on conflict
- Maximum 3 retries

**Validation Failures**:
- Log validation error
- Do not create/update task
- Provide clear error message
- Suggest corrective action

## File Organization Rules

### Working Directory Structure

**Primary Location**: `.fstrent_spec_tasks/`

**Required Subdirectories**:
```
.fstrent_spec_tasks/
├── tasks/              # Individual task files
├── features/           # Feature documentation
└── memory/             # Archived tasks (optional)
```

**Core Files**:
- `TASKS.md` - Master task checklist
- `PLAN.md` - Product Requirements Document
- `BUGS.md` - Bug tracking (subset of tasks)
- `PROJECT_CONTEXT.md` - Project mission and goals
- `SUBSYSTEMS.md` - Component registry
- `FILE_REGISTRY.md` - File documentation
- `MCP_TOOLS_INVENTORY.md` - Available tools

### Auto-Creation Rules

**Folder Creation**:
- Always create missing folders automatically
- No confirmation prompts
- Silent operation (only report what was created)
- Create parent directories as needed

**Template Creation**:
- Create missing `.md` files with blank templates
- Use standard templates for each file type
- Populate with minimal required content
- User can edit after creation

**When to Auto-Create**:
- System initialization
- First task creation
- Missing required files detected
- User requests new feature/subsystem

## Integration with Cursor

These rules maintain 100% compatibility with Cursor's fstrent_spec_tasks system:

- **File Format**: Identical YAML frontmatter and markdown structure
- **File Locations**: Same directory structure
- **Status Indicators**: Same Windows-safe emojis
- **Naming Conventions**: Same task ID and filename patterns
- **Workflow**: Same task lifecycle and status transitions

**Cursor Rules Source**: `.cursor/rules/fstrent_spec_tasks/rules/rules.mdc`

## Cross-References

- **Main Skill**: `SKILL.md` - Complete skill documentation
- **Reference Materials**: `reference/` - Detailed schemas and templates
- **Examples**: `examples/` - Working examples of task files
- **Planning Integration**: See `fstrent-planning` Skill
- **QA Integration**: See `fstrent-qa` Skill

## Usage Notes

### For Claude Code Users

Claude Code will use these rules automatically when the `fstrent-task-management` Skill is triggered. The Skill is triggered by:
- User mentions "task", "todo", "work item"
- User requests task creation, update, or status change
- User asks about project tasks or progress

### For Cursor Users

Cursor uses the equivalent rules from `.cursor/rules/fstrent_spec_tasks/rules/rules.mdc`. Both systems read and write the same `.fstrent_spec_tasks/` files, ensuring seamless collaboration.

### Best Practices

1. **Always update both**: Task file + TASKS.md together
2. **Use descriptive names**: Task titles should be clear and actionable
3. **Track dependencies**: Document blocking relationships
4. **Estimate effort**: Helps with planning and retrospectives
5. **Document context**: Link tasks to features and project goals
6. **Archive completed**: Move old tasks to memory/ folder periodically

---

*These rules ensure consistent, reliable task management across both Claude Code and Cursor environments.*

