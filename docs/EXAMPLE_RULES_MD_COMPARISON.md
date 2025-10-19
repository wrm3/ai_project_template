# Example: rules.md Pattern Analysis

## Current Structure (What We Have)

```
.claude/skills/fstrent-task-management/
├── SKILL.md (4,800 words - everything in one file)
├── reference/
│   ├── cursor_rules_comparison.md
│   ├── task_templates.md
│   ├── windows_emoji_guide.md
│   └── yaml_schema.md
└── examples/
    ├── simple_task.md
    ├── complex_task_with_subtasks.md
    └── ...
```

## Proposed Structure (With rules.md)

```
.claude/skills/fstrent-task-management/
├── SKILL.md (1,500 words - high-level overview)
├── rules.md (3,300 words - detailed implementation rules)
├── reference/
│   ├── cursor_rules_comparison.md
│   ├── task_templates.md
│   ├── windows_emoji_guide.md
│   └── yaml_schema.md
└── examples/
    ├── simple_task.md
    ├── complex_task_with_subtasks.md
    └── ...
```

---

## What Would Move from SKILL.md to rules.md

### SKILL.md (Lightweight - What & When)

**Keep in SKILL.md**:
- Skill name and description (YAML frontmatter)
- Brief system overview (2-3 paragraphs)
- When to use this skill
- Key capabilities (bullet list)
- Quick reference (file locations)
- Links to reference materials

**Example SKILL.md (Condensed)**:
```markdown
---
name: fstrent-task-management
description: Manage project tasks using fstrent_spec_tasks system
---

# fstrent Task Management Skill

Manage project tasks in .fstrent_spec_tasks/ folder.

## When to Use
- Creating new tasks
- Updating task status
- Tracking task progress
- Querying task information

## Key Capabilities
- Task file creation and updates
- TASKS.md master list management
- Status tracking with Windows-safe emojis
- Task dependencies and sub-tasks

## File Locations
- Master list: `.fstrent_spec_tasks/TASKS.md`
- Task files: `.fstrent_spec_tasks/tasks/`
- Features: `.fstrent_spec_tasks/features/`

## Detailed Rules
See `rules.md` for complete implementation guidelines.

## Reference Materials
- `reference/yaml_schema.md` - YAML format details
- `reference/task_templates.md` - Task templates
- `examples/` - Working examples
```

---

### rules.md (Detailed - How)

**Move to rules.md**:
- File naming conventions (detailed)
- YAML frontmatter rules (complete schema)
- Task content structure (detailed format)
- Status management rules
- Windows emoji requirements
- Task ID assignment rules
- TASKS.md update procedures
- Sub-task creation rules
- Dependency management
- Error handling procedures

**Example rules.md**:
```markdown
# Task Management Rules

## File Naming Convention

### Format
- Pattern: `task{id}_descriptive_name.md`
- ID: Zero-padded 3 digits (001, 002, ..., 999)
- Descriptive name: lowercase with underscores
- Extension: `.md`

### Examples
✅ Good:
- `task001_setup_database.md`
- `task042_implement_user_auth.md`
- `task123_fix_login_bug.md`

❌ Bad:
- `task1_setup.md` (not zero-padded)
- `task-042-implement-auth.md` (hyphens instead of underscores)
- `Task001_Setup.md` (capital letters)
- `task001.md` (no descriptive name)

### Location
All task files MUST be in: `.fstrent_spec_tasks/tasks/`

## YAML Frontmatter Rules

### Required Fields
Every task file MUST have these fields:
- `id`: Integer (001, 002, etc.)
- `title`: String (brief, actionable)
- `status`: Enum (pending|in-progress|completed|failed)
- `priority`: Enum (critical|high|medium|low)

### Optional Fields
- `type`: Enum (task|bug_fix|feature|retroactive_fix)
- `feature`: String (related feature name)
- `subsystems`: Array of strings
- `project_context`: String (how task relates to project)
- `dependencies`: Array of task IDs
- `estimated_effort`: String (time estimate)
- `created_date`: String (YYYY-MM-DD)
- `completed_date`: String (YYYY-MM-DD)

### Field Validation Rules

**id**:
- MUST be unique
- MUST be sequential (no gaps preferred)
- MUST match filename ID
- Format: Integer (001, 002, 003, ...)

**title**:
- MUST be brief (< 100 characters)
- MUST be actionable (start with verb)
- MUST be specific
- Examples: "Set up database schema", "Fix login bug", "Implement user authentication"

**status**:
- MUST be one of: pending, in-progress, completed, failed
- Default: pending
- Transitions:
  - pending → in-progress (when work starts)
  - in-progress → completed (when done)
  - in-progress → failed (if abandoned)
  - Any status → pending (if reopened)

**priority**:
- MUST be one of: critical, high, medium, low
- Default: medium
- Definitions:
  - critical: Blocking, must fix immediately
  - high: Important, should do soon
  - medium: Normal priority
  - low: Nice to have, can wait

### Example Valid YAML
```yaml
---
id: 042
title: 'Implement user authentication'
type: feature
status: in-progress
priority: high
feature: User Management
subsystems: [authentication, database, api]
project_context: 'Core security feature required before public launch'
dependencies: [001, 038]
estimated_effort: '8 hours'
created_date: '2025-10-15'
---
```

## Status Management Rules

### Windows-Safe Emojis
MUST use these specific emojis in TASKS.md:
- `[ ]` - Pending (empty checkbox)
- `[🔄]` - In Progress (counterclockwise arrows)
- `[✅]` - Completed (white check mark)
- `[❌]` - Failed/Cancelled (cross mark)

**Why these specific emojis?**
- Cross-platform compatibility
- Windows Terminal safe
- Git-friendly (no encoding issues)
- Visually distinct

### Status Update Procedure
When updating task status:

1. Update task file YAML frontmatter
2. Update TASKS.md entry
3. Add completion date if completed
4. Update dependent tasks if needed

Example:
```markdown
# In task file
status: completed
completed_date: '2025-10-19'

# In TASKS.md
- [✅] Task 042: Implement user authentication
```

## Task Creation Rules

### Step-by-Step Process

1. **Determine Next ID**
   - Read TASKS.md
   - Find highest existing ID
   - Increment by 1
   - Zero-pad to 3 digits

2. **Create Task File**
   - Filename: `task{id}_descriptive_name.md`
   - Location: `.fstrent_spec_tasks/tasks/`
   - Start with YAML frontmatter
   - Add task content

3. **Update TASKS.md**
   - Add entry in appropriate section
   - Use correct status emoji
   - Include task ID and title
   - Maintain chronological order

4. **Verify**
   - Task file exists
   - YAML is valid
   - TASKS.md updated
   - No duplicate IDs

### Task Content Requirements

After YAML frontmatter, include:

**Objective** (Required):
- Clear, actionable goal
- One sentence preferred
- Specific and measurable

**Acceptance Criteria** (Required):
- Checklist format
- Specific, verifiable outcomes
- 3-7 criteria typical
- Use `- [ ]` format

**Implementation Notes** (Optional):
- Technical approach
- Design decisions
- Constraints
- Dependencies

**Testing Plan** (Optional):
- How to verify
- Test cases
- Validation steps

## Sub-Task Rules

### When to Create Sub-Tasks
Create sub-tasks if task complexity score ≥ 7:
- Estimated effort > 2-3 days
- Affects multiple subsystems
- Multiple distinct outcomes
- High uncertainty

### Sub-Task Naming
- Format: `task{parent_id}.{sub_id}_descriptive_name.md`
- Example: `task042.1_setup_auth_database.md`
- Sub-task IDs: String format (e.g., "42.1", "42.2")

### Sub-Task YAML
```yaml
---
id: "42.1"  # String, not integer
title: 'Setup authentication database'
type: task
status: pending
priority: high
parent_task: 42  # Reference parent
dependencies: []
---
```

## TASKS.md Update Rules

### File Structure
```markdown
# Project Name - Task List

## Active Tasks

### Phase 1: Foundation
- [✅] Task 001: Setup project
- [🔄] Task 002: Create database

### Phase 2: Core Features
- [ ] Task 003: Implement API
- [ ] Task 004: Add authentication

## Completed Tasks Archive
(Older completed tasks)

## Task Statistics
Total: X
Completed: Y (Z%)
```

### Update Procedures

**Adding New Task**:
1. Find appropriate phase/section
2. Add at end of section
3. Use `[ ]` for pending status
4. Format: `- [ ] Task {id}: {title}`

**Updating Status**:
1. Find task entry
2. Update emoji only
3. Don't change task ID or title
4. Move to archive if completed (optional)

**Maintaining Order**:
- Tasks within phase: chronological by ID
- Phases: sequential (Phase 1, 2, 3...)
- Archive: reverse chronological (newest first)

## Error Handling

### Duplicate Task IDs
If duplicate ID detected:
1. Alert user
2. Suggest next available ID
3. Don't create file until resolved

### Invalid YAML
If YAML validation fails:
1. Show specific error
2. Provide correct format
3. Don't update TASKS.md until fixed

### Missing Dependencies
If dependency task doesn't exist:
1. Warn user
2. Suggest creating dependency first
3. Allow override if intentional

### File System Errors
If can't create/update files:
1. Check permissions
2. Verify directory exists
3. Provide clear error message
4. Suggest solutions

## Best Practices

### Task Titles
✅ Good:
- "Implement user authentication"
- "Fix login redirect bug"
- "Refactor database queries"

❌ Bad:
- "Do auth stuff" (too vague)
- "Authentication" (not actionable)
- "Fix bug" (not specific)

### Task Granularity
- 1-3 days of work ideal
- Break down if > 5 days
- Combine if < 2 hours

### Priority Assignment
- Critical: < 5% of tasks
- High: 20-30% of tasks
- Medium: 50-60% of tasks
- Low: 10-20% of tasks

### Dependencies
- Only list direct dependencies
- Avoid circular dependencies
- Keep dependency chains short (< 3 levels)
```

---

## Key Differences

| Aspect | SKILL.md | rules.md |
|--------|----------|----------|
| **Purpose** | What & When | How (detailed) |
| **Length** | Short (1-2K words) | Long (3-5K words) |
| **Content** | Overview, capabilities | Rules, procedures, validation |
| **When Read** | Always (lightweight) | When using skill (as needed) |
| **Audience** | Quick reference | Implementation guide |
| **Examples** | Minimal | Extensive |

---

## Benefits of Separation

### For Claude
1. **Faster Initial Load**: Reads lightweight SKILL.md first
2. **Progressive Disclosure**: Loads rules.md only when needed
3. **Better Context Management**: Can drop rules.md if not actively using
4. **Clearer Intent**: Knows when to load detailed rules

### For Developers
1. **Easier Maintenance**: Update rules without touching skill definition
2. **Better Organization**: Clear separation of concerns
3. **Easier Testing**: Can validate rules independently
4. **Better Documentation**: Rules are self-contained reference

### For Users
1. **Faster Response**: Claude doesn't load unnecessary detail
2. **Better Accuracy**: Detailed rules when actually needed
3. **Consistent Behavior**: Rules are explicit and complete

---

## Conclusion

**Current Approach** (Single SKILL.md):
- ✅ Works fine
- ✅ Simpler structure
- ❌ Loads all content always
- ❌ Harder to maintain

**Proposed Approach** (SKILL.md + rules.md):
- ✅ Progressive disclosure
- ✅ Better performance
- ✅ Easier maintenance
- ✅ Follows Anthropic pattern (if confirmed)
- ❌ More files to manage

**Recommendation**: 
Wait to confirm this is an official Anthropic pattern before refactoring. If it's just experimental or from a third-party video, our current structure is fine.

**Questions to Research**:
1. Is `rules.md` in official Anthropic Skills documentation?
2. Do Anthropic's example Skills use this pattern?
3. Is this a new feature or experimental?
4. What's the official recommendation?

