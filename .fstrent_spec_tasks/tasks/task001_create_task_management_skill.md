---
id: 001
title: 'Create fstrent-task-management Skill'
type: feature
status: completed
priority: high
feature: Claude Code Skills
subsystems: [skills_system, file_io]
project_context: 'Core Skill that enables Claude Code to read/write tasks in .fstrent_spec_tasks/ folder, maintaining compatibility with Cursor'
dependencies: []
estimated_effort: '4-6 hours'
---

# Task 001: Create fstrent-task-management Skill

## Objective
Create a Claude Code Skill that provides task management capabilities compatible with Cursor's fstrent_spec_tasks system.

## Acceptance Criteria
- [ ] SKILL.md created with proper YAML frontmatter
- [ ] Skill description triggers on task-related requests
- [ ] Skill can read existing TASKS.md file
- [ ] Skill can create new task files in correct format
- [ ] Skill can update task status (pending/in-progress/completed/failed)
- [ ] Skill maintains YAML frontmatter compatibility with Cursor
- [ ] Skill updates TASKS.md master checklist
- [ ] Uses Windows-safe emojis ([ ], [🔄], [✅], [❌])

## Implementation Notes

### File Location
`.claude/skills/fstrent-task-management/SKILL.md`

### YAML Frontmatter
```yaml
---
name: fstrent-task-management
description: Manage project tasks using the fstrent_spec_tasks system. Use when creating, updating, tracking, or viewing tasks in .fstrent_spec_tasks/ folder. Handles task files, TASKS.md updates, and status management.
---
```

### Skill Content Structure
1. **Overview**: Explain fstrent_spec_tasks system
2. **Task File Format**: Document YAML frontmatter structure
3. **Task Operations**:
   - Creating tasks
   - Updating status
   - Reading tasks
   - Listing tasks
4. **File Locations**:
   - `.fstrent_spec_tasks/TASKS.md` - Master checklist
   - `.fstrent_spec_tasks/tasks/task{id}_name.md` - Individual tasks
5. **Status Management**: Emoji usage and status transitions
6. **Integration**: How to work with PLAN.md and features

### Key Rules to Include
- Task ID format: Sequential numbers (001, 002, etc.)
- Filename format: `task{id}_descriptive_name.md`
- YAML fields: id, title, type, status, priority, feature, subsystems, project_context, dependencies
- Status values: pending, in-progress, completed, failed
- Priority values: critical, high, medium, low

### References to Create
Consider adding `references/task-format.md` with detailed examples if SKILL.md gets too long.

## Testing Plan
1. Create sample project with existing Cursor tasks
2. Use Claude Code to read existing tasks
3. Create new task via natural language
4. Update task status
5. Verify file format matches Cursor expectations
6. Test with Cursor to ensure compatibility

## Resources Needed
- Access to `.cursor/rules/fstrent_spec_tasks/rules/rules.mdc` for reference
- Sample task files from Cursor projects
- Anthropic Skills documentation: https://github.com/anthropics/skills

## Success Metrics
- Skill activates correctly for task-related requests
- 100% file format compatibility with Cursor
- Zero data corruption
- Natural language interaction works smoothly

