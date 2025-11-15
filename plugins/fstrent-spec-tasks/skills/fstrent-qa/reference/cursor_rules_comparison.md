# Cursor Rules vs Claude Code Skill Comparison - QA

## Overview

This document compares the Cursor fstrent_spec_tasks QA rules with the Claude Code fstrent-qa Skill for bug tracking and quality management.

## Core Functionality Comparison

| Feature | Cursor Rules | Claude Code Skill | Compatible |
|---------|-------------|-------------------|------------|
| **Bug Tracking** | BUGS.md format | BUGS.md format | ✅ 100% |
| **Bug Classification** | 4 severity levels | 4 severity levels | ✅ Identical |
| **Source Attribution** | 4 sources | 4 sources | ✅ Same |
| **Bug-Task Integration** | Automatic | Automatic | ✅ Compatible |
| **Retroactive Documentation** | ✅ | ✅ | ✅ Same criteria |
| **Quality Metrics** | ✅ | ✅ | ✅ Compatible |

## File Format Compatibility

### ✅ 100% Compatible

Both systems use identical BUGS.md format and bug task files.

**BUGS.md Structure:**
```markdown
# Bug Tracking

## Active Bugs

### Bug ID: BUG-001
- **Title**: [Brief description]
- **Severity**: [Critical/High/Medium/Low]
- **Source**: [User Reported/Development/Testing/Production]
- **Feature Impact**: [Affected features]
- **Status**: [Open/Investigating/Fixing/Testing/Closed]
- **Task Reference**: Task 015
- **Created**: 2025-10-19
- **Assigned**: Developer Name
```

**Bug Task File:**
```yaml
---
id: 15
title: '[BUG] Description'
type: bug_fix
status: pending
priority: critical
bug_reference: BUG-001
severity: critical
source: production
---
```

## Workflow Comparison

### Reporting a Bug

**In Cursor:**
1. User: "Report a bug - login button not working"
2. Cursor applies QA rules
3. Creates BUGS.md entry
4. Creates bug fix task
5. Updates TASKS.md

**In Claude Code:**
1. User: "Report a bug - login button not working"
2. Claude activates fstrent-qa Skill
3. Creates BUGS.md entry
4. Creates bug fix task
5. Updates TASKS.md

**Result:** Identical files created

## Key Differences

### Activation
- **Cursor**: Always-on rules, `/fstrent_spec_tasks_qa` command
- **Claude Code**: Natural language activation on bug-related requests

### Context
- **Cursor**: Rules in `.cursor/rules/fstrent_spec_tasks/rules/qa.mdc`
- **Claude Code**: Skill in `.claude/skills/fstrent-qa/SKILL.md`

### File Organization
Both create same files in `.fstrent_spec_tasks/`:
- `BUGS.md`
- `tasks/task{id}_fix_{description}.md`

## Feature Parity Matrix

| Feature | Cursor | Claude | Compatible |
|---------|--------|--------|------------|
| Bug Classification (4 levels) | ✅ | ✅ | ✅ |
| Source Attribution (4 types) | ✅ | ✅ | ✅ |
| BUGS.md Format | ✅ | ✅ | ✅ |
| Bug Task Integration | ✅ | ✅ | ✅ |
| Bug Lifecycle Tracking | ✅ | ✅ | ✅ |
| Retroactive Documentation | ✅ | ✅ | ✅ |
| Quality Metrics | ✅ | ✅ | ✅ |
| Quality Gates | ✅ | ✅ | ✅ |

## Best Practices for Dual-IDE Teams

1. **Shared BUGS.md**: Both IDEs read/write same file
2. **Bug Tasks**: Both create identical task files
3. **Version Control**: Commit BUGS.md and bug tasks
4. **No Conflicts**: File formats are identical

## Summary

The Cursor QA rules and Claude Code QA Skill are **100% compatible**. Teams can use both IDEs interchangeably for bug tracking and quality management with zero friction.

