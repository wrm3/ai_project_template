# Cursor Rules vs Claude Code Skill Comparison

## Overview

This document provides a side-by-side comparison of the Cursor fstrent_spec_tasks rules system and the Claude Code fstrent-task-management Skill, helping users understand the differences and migrate between IDEs.

## Core Functionality Comparison

| Feature | Cursor Rules | Claude Code Skill | Notes |
|---------|-------------|-------------------|-------|
| **Activation** | Always active via `.cursorrules` | Activates on task-related requests | Claude uses natural language triggers |
| **Task Creation** | Rule-guided prompts | Skill-guided conversation | Both create same file format |
| **File Operations** | Direct file manipulation | Uses Read/Write/Edit tools | Same end result |
| **Status Updates** | Emoji indicators in TASKS.md | Same emoji indicators | 100% compatible |
| **YAML Format** | Defined in rules.mdc | Defined in SKILL.md | Identical format |
| **Sub-tasks** | Supported (task42.1, 42.2) | Supported (same format) | Full compatibility |
| **Dependencies** | Array in frontmatter | Array in frontmatter | Identical |

## File Format Compatibility

### ✅ 100% Compatible

Both systems use **identical** file formats:

**Task File Structure:**
```yaml
---
id: 001
title: 'Task Title'
status: pending
priority: high
feature: Feature Name
subsystems: [subsystem1, subsystem2]
project_context: 'Brief description'
dependencies: []
---

# Task 001: Task Title

## Objective
[Task description]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

**TASKS.md Format:**
```markdown
# Project Name - Task List

## Active Tasks
- [ ] Task 001: Task Title
- [🔄] Task 002: In Progress Task
- [✅] Task 003: Completed Task
```

## Workflow Comparison

### Creating a Task

**In Cursor:**
1. User: "Create a task to implement user authentication"
2. Cursor applies rules from `.cursor/rules/fstrent_spec_tasks/rules/rules.mdc`
3. Creates `task001_implement_user_auth.md`
4. Updates `TASKS.md`

**In Claude Code:**
1. User: "Create a task to implement user authentication"
2. Claude activates `fstrent-task-management` Skill
3. Creates `task001_implement_user_auth.md`
4. Updates `TASKS.md`

**Result:** Identical files created in both IDEs

### Updating Task Status

**In Cursor:**
1. User: "Mark task 001 as in-progress"
2. Cursor updates task file status field
3. Updates TASKS.md emoji to `[🔄]`

**In Claude Code:**
1. User: "Mark task 001 as in-progress"
2. Claude updates task file status field
3. Updates TASKS.md emoji to `[🔄]`

**Result:** Identical status updates

## Key Differences

### 1. Activation Method

**Cursor:**
- Rules are always active
- Automatically applied to all conversations
- Configured in `.cursor/rules/` directory

**Claude Code:**
- Skills activate based on user intent
- Natural language triggers (mentions of "task", "create", "update")
- Configured in `.claude/skills/` directory

### 2. Context Awareness

**Cursor:**
- Rules provide context via `.cursorrules` file
- Progressive disclosure through rule hierarchy
- Commands: `/fstrent_spec_tasks_setup`, etc.

**Claude Code:**
- Skills provide context via SKILL.md
- Progressive disclosure through reference/ folder
- Natural language activation (no slash commands needed)

### 3. File Organization

**Cursor:**
```
.cursor/
└── rules/
    └── fstrent_spec_tasks/
        ├── commands/
        │   ├── fstrent_spec_tasks_setup.md
        │   ├── fstrent_spec_tasks_plan.md
        │   ├── fstrent_spec_tasks_qa.md
        │   └── fstrent_spec_tasks_workflow.md
        └── rules/
            ├── _index.mdc
            ├── rules.mdc
            ├── plans.mdc
            ├── qa.mdc
            └── workflow.mdc
```

**Claude Code:**
```
.claude/
└── skills/
    ├── fstrent-task-management/
    │   ├── SKILL.md
    │   ├── reference/
    │   └── examples/
    ├── fstrent-planning/
    │   ├── SKILL.md
    │   ├── reference/
    │   └── examples/
    └── fstrent-qa/
        ├── SKILL.md
        ├── reference/
        └── examples/
```

## Migration Guide

### From Cursor to Claude Code

1. **Install Claude Code Skills:**
   - Copy `.claude/skills/` directory to your project
   - Skills will auto-activate when needed

2. **Continue Using Existing Files:**
   - Keep `.fstrent_spec_tasks/` directory as-is
   - No migration of data files needed
   - Both IDEs read/write same files

3. **Workflow Adjustment:**
   - Instead of slash commands, use natural language
   - "Create a task" instead of `/fstrent_spec_tasks_setup`
   - Skills activate automatically

### From Claude Code to Cursor

1. **Install Cursor Rules:**
   - Copy `.cursor/rules/` directory to your project
   - Rules will auto-activate

2. **Continue Using Existing Files:**
   - Keep `.fstrent_spec_tasks/` directory as-is
   - No migration of data files needed
   - Both IDEs read/write same files

3. **Workflow Adjustment:**
   - Use slash commands for quick access
   - `/fstrent_spec_tasks_setup` for initialization
   - Rules are always active

## Feature Parity Matrix

| Feature | Cursor | Claude Code | Compatible |
|---------|--------|-------------|------------|
| Task Creation | ✅ | ✅ | ✅ |
| Task Status Update | ✅ | ✅ | ✅ |
| Sub-task Creation | ✅ | ✅ | ✅ |
| Task Dependencies | ✅ | ✅ | ✅ |
| YAML Frontmatter | ✅ | ✅ | ✅ |
| Windows-safe Emojis | ✅ | ✅ | ✅ |
| Auto-folder Creation | ✅ | ✅ | ✅ |
| Feature Integration | ✅ | ✅ | ✅ |
| Bug References | ✅ | ✅ | ✅ |
| Retroactive Tasks | ✅ | ✅ | ✅ |
| Task Types | ✅ | ✅ | ✅ |
| Priority Levels | ✅ | ✅ | ✅ |
| Subsystem Tracking | ✅ | ✅ | ✅ |
| Project Context | ✅ | ✅ | ✅ |

## Best Practices for Dual-IDE Teams

### 1. Shared File Structure
- Keep `.fstrent_spec_tasks/` in version control
- Both IDEs read/write to same location
- No conflicts or duplication

### 2. IDE-Specific Folders
- Keep `.cursor/` for Cursor users
- Keep `.claude/` for Claude Code users
- Both in version control
- Each IDE ignores the other's folder

### 3. Team Workflow
- Task files are IDE-agnostic
- Any team member can update any task
- Status updates work across IDEs
- No "Cursor tasks" vs "Claude tasks"

### 4. Onboarding
- New team members choose their preferred IDE
- Install appropriate rules/skills
- Start working immediately
- No learning curve for switching

## Common Questions

### Q: Can I use both IDEs on the same project?
**A:** Yes! Both IDEs work with the same `.fstrent_spec_tasks/` files. You can switch between IDEs freely.

### Q: Will my tasks created in Cursor work in Claude Code?
**A:** Yes, 100%. Both use identical file formats and YAML frontmatter.

### Q: Do I need to migrate my existing tasks?
**A:** No migration needed. Both IDEs read the same files.

### Q: What if my team uses different IDEs?
**A:** Perfect! That's the goal. Everyone works with the same task files regardless of IDE choice.

### Q: Are there any incompatibilities?
**A:** No. The file formats are identical. The only difference is how you interact with the system (rules vs skills).

## Troubleshooting

### Issue: Claude Code not recognizing task files
**Solution:** Ensure `.claude/skills/fstrent-task-management/` exists with SKILL.md

### Issue: Cursor not applying rules
**Solution:** Ensure `.cursor/rules/fstrent_spec_tasks/` exists with rules.mdc

### Issue: Task files not updating
**Solution:** Check file permissions. Both IDEs need read/write access to `.fstrent_spec_tasks/`

### Issue: Different behavior between IDEs
**Solution:** Verify both are using latest versions of rules/skills. File formats should be identical.

## Summary

The Cursor rules and Claude Code Skills are **functionally equivalent** and **100% compatible**. The main difference is the activation method (always-on rules vs intent-based skills). Teams can use both IDEs interchangeably with zero friction.

