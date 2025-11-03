---
name: fstrent-task-management
description: Manage project tasks using the fstrent_spec_tasks system. Use when creating, updating, tracking, or viewing tasks in .fstrent_spec_tasks/ folder. Handles task files, TASKS.md updates, status management, and task queries. Triggers on requests mentioning tasks, todos, work items, or task status.
---

# fstrent Task Management Skill

Manage project tasks using the fstrent_spec_tasks task management system. This Skill provides capabilities for creating, updating, tracking, and organizing development tasks in a structured, file-based system compatible with multiple AI IDEs.

## System Overview

The fstrent_spec_tasks system uses a file-based approach where:
- **Master checklist**: `.fstrent_spec_tasks/TASKS.md` - Central task list with status indicators
- **Individual tasks**: `.fstrent_spec_tasks/tasks/task{id}_descriptive_name.md` - Detailed task files
- **Features**: `.fstrent_spec_tasks/features/` - Feature documentation referenced by tasks
- **Project context**: `.fstrent_spec_tasks/PROJECT_CONTEXT.md` - Project goals and scope

## Task File Structure

### File Naming Convention
- Format: `task{id}_descriptive_name.md`
- Examples: `task001_setup_database.md`, `task042_implement_auth.md`
- Location: `.fstrent_spec_tasks/tasks/`

### YAML Frontmatter Format
Every task file begins with YAML frontmatter containing metadata:

```yaml
---
id: {number}                    # Sequential ID (001, 002, etc.)
title: 'Task Title'             # Brief, actionable title
type: task|bug_fix|feature|retroactive_fix
status: pending|in-progress|completed|failed
priority: critical|high|medium|low
feature: Feature Name           # Related feature (optional)
subsystems: [list]              # Affected system components
project_context: 'Brief description of how this task relates to project goals'
dependencies: [task_ids]        # Tasks that must complete first
estimated_effort: 'time estimate'  # Optional: story points or hours
---
```

### Task Content Structure
After the YAML frontmatter, include:

1. **Objective**: Clear, actionable goal
2. **Acceptance Criteria**: Specific, measurable outcomes (checklist format)
3. **Implementation Notes**: Technical details, approach, considerations
4. **Testing Plan**: How to verify completion (optional)
5. **Resources Needed**: Dependencies, documentation, tools (optional)

## Task Operations

### Creating a New Task

**Process:**
1. Determine next available task ID by reading `.fstrent_spec_tasks/TASKS.md`
2. Create task file: `.fstrent_spec_tasks/tasks/task{id}_descriptive_name.md`
3. Add YAML frontmatter with all required fields
4. Add task content (objective, acceptance criteria, notes)
5. Update `.fstrent_spec_tasks/TASKS.md` with new entry

**TASKS.md Entry Format:**
```markdown
- [ ] Task {id}: {Brief description}
```

**Example:**
```markdown
- [ ] Task 001: Setup database schema
- [ ] Task 002: Implement user authentication
```

### Updating Task Status

**Status Transitions:**
- `pending` → `in-progress`: Task work has started
- `in-progress` → `completed`: Task successfully finished
- `in-progress` → `failed`: Task blocked or abandoned
- Any status → `pending`: Reset if needed

**Process:**
1. Update `status` field in task file's YAML frontmatter
2. Update corresponding entry in `.fstrent_spec_tasks/TASKS.md`

**Status Indicators (Windows-safe emojis):**
- `[ ]` - pending (not started)
- `[🔄]` - in-progress (actively working)
- `[✅]` - completed (finished successfully)
- `[❌]` - failed (blocked or abandoned)

**Example TASKS.md Updates:**
```markdown
- [ ] Task 001: Setup database schema
- [🔄] Task 002: Implement user authentication (in progress)
- [✅] Task 003: Create login page (completed)
- [❌] Task 004: Legacy system integration (blocked)
```

### Viewing Tasks

**To view all tasks:**
Read `.fstrent_spec_tasks/TASKS.md` for overview

**To view specific task details:**
Read `.fstrent_spec_tasks/tasks/task{id}_*.md`

**To view tasks by status:**
Parse TASKS.md and filter by status indicators

**To view project context:**
Read `.fstrent_spec_tasks/PROJECT_CONTEXT.md` for goals and scope

### Listing Tasks

**Common queries:**
- "Show all tasks" → Read TASKS.md
- "Show pending tasks" → Filter by `[ ]`
- "Show in-progress tasks" → Filter by `[🔄]`
- "Show completed tasks" → Filter by `[✅]`
- "Show task 5" → Read task005_*.md

## Task Types

### Standard Task (`type: task`)
Regular development work, features, improvements

### Bug Fix (`type: bug_fix`)
Fixing defects or issues. Should reference BUGS.md entry.

**Additional fields for bug fixes:**
```yaml
bug_reference: BUG-{number}
severity: critical|high|medium|low
reproduction_steps: 'How to reproduce'
expected_behavior: 'What should happen'
actual_behavior: 'What actually happens'
```

### Feature Task (`type: feature`)
Major feature implementation. Should reference feature document.

**Link to feature:**
```yaml
feature: Feature Name  # Must match .fstrent_spec_tasks/features/{feature-name}.md
```

### Retroactive Fix (`type: retroactive_fix`)
Documents work completed in chat without prior task planning.

**Additional fields:**
```yaml
created_date: '{completion_date}'
completed_date: '{completion_date}'
actual_effort: '{time_spent}'
```

## Task Complexity and Sub-Tasks

### When to Create Sub-Tasks
If a task is complex (affects multiple subsystems, >2-3 days effort, many acceptance criteria), break it into sub-tasks.

### Sub-Task Naming Convention
- Parent: `task042_implement_authentication.md`
- Sub-tasks: `task42.1_setup_auth_db.md`, `task42.2_create_auth_api.md`, `task42.3_add_auth_ui.md`

### Sub-Task YAML Format
```yaml
---
id: "42.1"              # String ID for sub-tasks
title: 'Setup Auth Database'
type: task
status: pending
priority: high
parent_task: 42         # Reference to parent
dependencies: []        # Can depend on sibling sub-tasks
---
```

## Task Dependencies

### Specifying Dependencies
```yaml
dependencies: [1, 3, 5]  # Task IDs that must complete first
```

### Dependency Rules
- Tasks with dependencies should not start until dependencies are completed
- Check dependency status before starting work
- Update dependent tasks when blockers are resolved

## Integration with Other Systems

### Link to Features
Tasks reference features via the `feature` field:
```yaml
feature: User Authentication  # Links to features/user-authentication.md
```

### Link to Bugs
Bug fix tasks reference BUGS.md:
```yaml
bug_reference: BUG-001  # Links to entry in BUGS.md
```

### Link to Project Context
All tasks should align with project goals in PROJECT_CONTEXT.md. The `project_context` field explains this connection.

## File Organization Rules

### Core Files (Always in .fstrent_spec_tasks/)
- `TASKS.md` - Master task checklist
- `tasks/` - Individual task files
- `features/` - Feature documentation
- `PLAN.md` - Product requirements
- `PROJECT_CONTEXT.md` - Project goals
- `BUGS.md` - Bug tracking

### Documentation (Goes in docs/)
- Project documentation
- API documentation
- Architecture diagrams
- Setup guides
- Migration files

### Test Scripts (Goes in temp_scripts/)
- Test automation scripts
- Utility scripts
- Validation scripts

## Auto-Creation Rules

When working with tasks, automatically create missing folders and files:

**Auto-create folders:**
- `.fstrent_spec_tasks/` if it doesn't exist
- `.fstrent_spec_tasks/tasks/` if it doesn't exist
- `docs/` if needed for documentation
- `temp_scripts/` if needed for test scripts

**Auto-create template files:**
- `TASKS.md` with blank template if missing
- `PROJECT_CONTEXT.md` with template if missing

**No confirmation needed** - Create files and folders silently, report what was created.

## Best Practices

### Task Creation
1. Use clear, actionable titles
2. Include specific acceptance criteria
3. Specify dependencies upfront
4. Link to related features
5. Estimate effort when possible

### Task Updates
1. Update status immediately when starting or completing
2. Keep TASKS.md synchronized with task files
3. Document blockers and issues
4. Update acceptance criteria as work progresses

### Task Organization
1. Break complex tasks into sub-tasks
2. Group related tasks by feature
3. Track dependencies explicitly
4. Archive completed tasks periodically (move to memory/)

### Status Management
1. Only one task should be `in-progress` per developer at a time
2. Mark tasks `completed` only when all acceptance criteria are met
3. Use `failed` status for blocked or abandoned work
4. Document reason for failure in task notes

## Common Workflows

### Workflow: Create Task from User Request
1. User requests: "Create a task to implement user login"
2. Read TASKS.md to determine next ID
3. Create task file with proper naming
4. Add YAML frontmatter with all fields
5. Add objective and acceptance criteria
6. Update TASKS.md with new entry
7. Confirm task created with ID

### Workflow: Update Task Status
1. User requests: "Mark task 5 as in progress"
2. Read task005_*.md file
3. Update `status: in-progress` in YAML
4. Update TASKS.md entry from `[ ]` to `[🔄]`
5. Confirm status updated

### Workflow: View Task Progress
1. User requests: "Show me task progress"
2. Read TASKS.md
3. Count tasks by status
4. Calculate completion percentage
5. List in-progress tasks
6. Identify blockers

### Workflow: Complete Task
1. User requests: "Complete task 3"
2. Read task003_*.md
3. Verify acceptance criteria are met
4. Update `status: completed` in YAML
5. Update TASKS.md entry from `[🔄]` to `[✅]`
6. Optionally archive to memory/
7. Confirm completion

## Error Handling

### Missing Files
If TASKS.md or task files are missing:
1. Check if `.fstrent_spec_tasks/` exists
2. Create directory structure if needed
3. Create template files
4. Inform user of initialization

### Invalid Task IDs
If user references non-existent task:
1. List available tasks
2. Suggest correct ID
3. Offer to create new task if intended

### Concurrent Edits
If file conflicts occur:
1. Read current file state
2. Merge changes if possible
3. Alert user to conflicts
4. Suggest using version control

## Examples

### Example: Create Simple Task
**User**: "Create a task to add password reset feature"

**Action**:
1. Read TASKS.md → Next ID is 015
2. Create `.fstrent_spec_tasks/tasks/task015_add_password_reset.md`:

```yaml
---
id: 015
title: 'Add Password Reset Feature'
type: feature
status: pending
priority: high
feature: User Authentication
subsystems: [auth, email, ui]
project_context: 'Enables users to recover accounts, improving user experience and reducing support burden'
dependencies: [12]
estimated_effort: '1-2 days'
---

# Task 015: Add Password Reset Feature

## Objective
Implement password reset functionality allowing users to securely reset forgotten passwords via email.

## Acceptance Criteria
- [ ] User can request password reset from login page
- [ ] System sends reset link to user's email
- [ ] Reset link expires after 24 hours
- [ ] User can set new password via reset link
- [ ] Old password is invalidated after reset
- [ ] User receives confirmation email after reset

## Implementation Notes
- Use secure token generation for reset links
- Store tokens in database with expiration
- Send emails via existing email service
- Add UI for reset request and password change
- Update authentication system to handle resets

## Testing Plan
- Test reset request flow
- Verify email delivery
- Test token expiration
- Test password update
- Verify old password invalidation
```

3. Update TASKS.md:
```markdown
- [ ] Task 015: Add password reset feature
```

4. Confirm: "Created Task 015: Add Password Reset Feature"

### Example: Update Task Status
**User**: "Start working on task 15"

**Action**:
1. Read task015_add_password_reset.md
2. Update YAML: `status: in-progress`
3. Update TASKS.md: `[🔄] Task 015: Add password reset feature`
4. Confirm: "Task 015 status updated to in-progress"

### Example: Complete Task
**User**: "Task 15 is done"

**Action**:
1. Read task015_add_password_reset.md
2. Review acceptance criteria
3. Update YAML: `status: completed`
4. Update TASKS.md: `[✅] Task 015: Add password reset feature`
5. Confirm: "Task 015 marked as completed. Great work!"

## Compatibility Notes

This Skill is designed to work with the same file format used by Cursor's fstrent_spec_tasks rules system. Tasks created in Claude Code can be viewed and updated in Cursor, and vice versa. The system uses:

- Standard YAML frontmatter
- Markdown content
- Windows-safe emoji indicators
- Git-friendly plain text files

Teams can use both IDEs interchangeably without workflow disruption.

## Template Maintenance and Platform Architecture

### Platform Architecture Reference

When maintaining this template or adding new features, **ALWAYS** consult the [.ai_platform_architecture/](.ai_platform_architecture/) folder for platform-specific requirements and compatibility considerations.

**Key Documentation:**
- [.ai_platform_architecture/PLATFORM_COMPARISON.md](.ai_platform_architecture/PLATFORM_COMPARISON.md) - Cross-platform comparison table
- [.ai_platform_architecture/CLAUDE_CODE.md](.ai_platform_architecture/CLAUDE_CODE.md) - Claude Code specific architecture
- [.ai_platform_architecture/CURSOR.md](.ai_platform_architecture/CURSOR.md) - Cursor specific architecture
- [.ai_platform_architecture/README.md](.ai_platform_architecture/README.md) - Overview and maintenance schedule

### When to Reference Platform Architecture

**ALWAYS check `.ai_platform_architecture/` before:**
1. Adding new Skills, SubAgents, or Commands
2. Modifying task file formats or naming conventions
3. Creating new rules or instructions
4. Updating file organization structure
5. Making changes that affect cross-IDE compatibility

### Critical Platform Differences

**File Formats:**
- Cursor uses `.mdc` files (UNIQUE - won't work on other platforms)
- All other platforms use `.md` files
- Task files must use YAML frontmatter for cross-platform compatibility

**Skills and SubAgents:**
- Claude Code: ✅ Has Skills & SubAgents
- All other platforms: ❌ No equivalent (use rules/instructions instead)

**Commands:**
- Claude Code: `/command` (slash prefix)
- Cursor: `@command` (@ prefix)
- Others: See platform-specific docs

### Periodic Verification

**Quarterly Review (Every 3 Months):**
- [ ] Check all platform official documentation for updates
- [ ] Test template on each platform
- [ ] Update `.ai_platform_architecture/` documentation
- [ ] Update PLATFORM_COMPARISON.md comparison table
- [ ] Document any breaking changes

### Adding Features Cross-Platform

When adding features, ensure compatibility:

1. **Test on multiple platforms**: Claude Code and Cursor minimum
2. **Document compatibility**: Update platform-specific files
3. **Provide fallbacks**: For platform-specific features
4. **Update comparison**: Add to PLATFORM_COMPARISON.md table
5. **Migration guides**: Update if file structure changes

### Platform-Specific vs Universal Features

**Universal (work on all platforms):**
- `.fstrent_spec_tasks/` task management system
- Markdown documentation
- Basic file organization
- Standard project structure
- YAML frontmatter in task files

**Platform-Specific (limited availability):**
- **Skills/SubAgents**: Claude Code only
- **.mdc files**: Cursor only
- **Command prefixes**: Vary by platform (`/` vs `@`)
- **MCP UI**: Implementation varies by platform

### Template Maintenance Workflow

When maintaining this template:

1. **Check platform docs** in `.ai_platform_architecture/`
2. **Identify compatibility requirements** from PLATFORM_COMPARISON.md
3. **Test on primary platforms** (Claude Code + Cursor)
4. **Update platform-specific folders** (.claude/, .cursor/)
5. **Update documentation** in `.ai_platform_architecture/`
6. **Verify cross-platform** compatibility

### Resources

- **Official Platform Docs**: See `.ai_platform_architecture/README.md` for links
- **Comparison Table**: `.ai_platform_architecture/PLATFORM_COMPARISON.md`
- **Migration Guides**: In PLATFORM_COMPARISON.md
- **Verification Status**: `.ai_platform_architecture/README.md` status table

