# Claude Code Commands Reference - fstrent_spec_tasks

## Overview

This document provides a complete reference for all `fstrent_spec_tasks` custom commands available in Claude Code.

**Command Prefix**: `/project:`  
**Total Commands**: 7  
**Location**: `.claude/commands/`

---

## Quick Reference

| Command | Purpose | Usage |
|---------|---------|-------|
| `/project:new-task` | Create new task | `/project:new-task Implement user authentication` |
| `/project:update-task` | Update task status | `/project:update-task Task 007 to completed` |
| `/project:report-bug` | Report bug | `/project:report-bug Login button not responding` |
| `/project:start-planning` | Start project planning | `/project:start-planning E-commerce platform` |
| `/project:add-feature` | Add feature document | `/project:add-feature Shopping cart` |
| `/project:quality-report` | Generate quality report | `/project:quality-report monthly` |
| `/project:status` | Project status overview | `/project:status` |

---

## Command Details

### 1. `/project:new-task` - Create New Task

**Purpose**: Create a new task with proper structure and YAML frontmatter

**Usage**:
```
/project:new-task [task description]
```

**Examples**:
```
/project:new-task Implement user authentication
/project:new-task Add dark mode toggle to settings
/project:new-task Refactor database connection pooling
```

**What It Does**:
1. Prompts for task details (type, priority, subsystems)
2. Creates task file in `.fstrent_spec_tasks/tasks/`
3. Updates `TASKS.md` with new entry
4. Ensures proper YAML schema and formatting

**Prompts You'll Receive**:
- Task type (feature, bug_fix, enhancement, etc.)
- Priority level (critical, high, medium, low)
- Related feature
- Affected subsystems
- Dependencies

**Files Created/Modified**:
- `.fstrent_spec_tasks/tasks/task{id}_{description}.md`
- `.fstrent_spec_tasks/TASKS.md`

---

### 2. `/project:update-task` - Update Task Status

**Purpose**: Update task status and track progress

**Usage**:
```
/project:update-task [task identifier] [optional: new status]
```

**Examples**:
```
/project:update-task Task 007
/project:update-task Task 007 to completed
/project:update-task Implement authentication to in-progress
```

**What It Does**:
1. Identifies the task file
2. Prompts for new status if not provided
3. Updates task file YAML frontmatter
4. Updates `TASKS.md` emoji indicator
5. Adds completion notes if completed

**Status Transitions**:
- `pending` → `in-progress` → `completed`
- `pending` → `failed`
- `in-progress` → `failed`

**Emoji Updates**:
- `[ ]` Pending
- `[🔄]` In-Progress
- `[✅]` Completed
- `[❌]` Failed

**Files Modified**:
- `.fstrent_spec_tasks/tasks/task{id}_{description}.md`
- `.fstrent_spec_tasks/TASKS.md`

---

### 3. `/project:report-bug` - Report Bug

**Purpose**: Document bugs with proper tracking and task creation

**Usage**:
```
/project:report-bug [bug description]
```

**Examples**:
```
/project:report-bug Login button not responding
/project:report-bug Search returns no results for valid queries
/project:report-bug Shopping cart total calculation incorrect
```

**What It Does**:
1. Gathers bug details (severity, source, reproduction)
2. Creates entry in `BUGS.md`
3. Creates bug fix task
4. Updates `TASKS.md`
5. Links bug and task together

**Prompts You'll Receive**:
- Severity (critical, high, medium, low)
- Source (user_reported, development, testing, production)
- Affected features
- Reproduction steps
- Expected vs actual behavior

**Severity Guidelines**:
- **Critical**: System crashes, data loss (fix same day)
- **High**: Major feature broken (fix 1-2 days)
- **Medium**: Minor issues (fix 3-7 days)
- **Low**: Cosmetic issues (fix next release)

**Files Created/Modified**:
- `.fstrent_spec_tasks/BUGS.md`
- `.fstrent_spec_tasks/tasks/task{id}_fix_{description}.md`
- `.fstrent_spec_tasks/TASKS.md`

---

### 4. `/project:start-planning` - Start Project Planning

**Purpose**: Initialize comprehensive project planning with PRD creation

**Usage**:
```
/project:start-planning [project name/description]
```

**Examples**:
```
/project:start-planning E-commerce platform for small business
/project:start-planning Task management app
/project:start-planning Customer portal redesign
```

**What It Does**:
1. Runs scope validation (5 essential questions)
2. Creates comprehensive `PLAN.md` (PRD)
3. Creates `PROJECT_CONTEXT.md`
4. Creates `SUBSYSTEMS.md`
5. Sets up `features/` folder
6. Creates initial feature documents

**Scope Validation Questions**:
1. User context (personal, team, broader)
2. Security requirements (minimal, standard, enhanced)
3. Scalability expectations (basic, moderate, high)
4. Feature complexity (minimal, standard, feature-rich)
5. Integration requirements (standalone, basic, standard)

**Benefits**:
- ✅ Prevents over-engineering
- ✅ Clarifies scope boundaries
- ✅ Aligns team on goals
- ✅ Creates comprehensive documentation

**Files Created**:
- `.fstrent_spec_tasks/PLAN.md`
- `.fstrent_spec_tasks/PROJECT_CONTEXT.md`
- `.fstrent_spec_tasks/SUBSYSTEMS.md`
- `.fstrent_spec_tasks/features/` (folder)

---

### 5. `/project:add-feature` - Add Feature Document

**Purpose**: Create detailed feature specification

**Usage**:
```
/project:add-feature [feature name/description]
```

**Examples**:
```
/project:add-feature User authentication
/project:add-feature Shopping cart
/project:add-feature Real-time notifications
```

**What It Does**:
1. Gathers feature requirements
2. Creates feature document in `features/` folder
3. Updates `PLAN.md` with feature reference
4. Optionally creates initial implementation tasks

**Prompts You'll Receive**:
- Feature overview
- Functional requirements
- Non-functional requirements
- User stories
- Technical considerations
- Acceptance criteria
- Priority level

**Feature Document Sections**:
- Overview
- Requirements (functional & non-functional)
- User Stories (with acceptance criteria)
- Technical Considerations
- Acceptance Criteria
- Related Tasks
- Testing Strategy

**Files Created/Modified**:
- `.fstrent_spec_tasks/features/{feature-name}.md`
- `.fstrent_spec_tasks/PLAN.md`
- Optionally: task files and `TASKS.md`

---

### 6. `/project:quality-report` - Generate Quality Report

**Purpose**: Generate comprehensive quality metrics and analysis

**Usage**:
```
/project:quality-report [optional: period]
```

**Examples**:
```
/project:quality-report
/project:quality-report weekly
/project:quality-report monthly
/project:quality-report last 30 days
```

**What It Does**:
1. Analyzes `BUGS.md` for bug data
2. Calculates quality metrics
3. Identifies trends
4. Assesses quality gate performance
5. Generates comprehensive report

**Metrics Calculated**:
- Bug discovery rate
- Bug resolution time
- Severity distribution
- Feature impact analysis
- Regression rate
- Quality gate performance

**Report Sections**:
- Executive Summary
- Bug Metrics
- Quality Gates Performance
- Trends (6-month view)
- Achievements
- Focus Areas
- Recommendations

**Report Formats**:
- **Daily**: Quick status update
- **Weekly**: Detailed metrics and trends
- **Monthly**: Comprehensive analysis

**Output**: Markdown report saved to `docs/quality_report_{date}.md`

---

### 7. `/project:status` - Project Status Overview

**Purpose**: Quick comprehensive project status snapshot

**Usage**:
```
/project:status [optional: focus area]
```

**Examples**:
```
/project:status
/project:status tasks
/project:status bugs
/project:status features
```

**What It Does**:
1. Analyzes `TASKS.md` for task status
2. Analyzes `BUGS.md` for bug status
3. Analyzes `PLAN.md` for feature progress
4. Identifies blockers and risks
5. Highlights next priorities

**Status Report Sections**:

**📋 Task Summary**:
- Total tasks by status
- Completion rate
- Recent completions
- Tasks by priority

**🐛 Bug Summary**:
- Open bugs by severity
- Resolution rate
- Critical issues
- Long-standing bugs

**🎯 Feature Progress**:
- Total features
- Features completed
- Current focus
- Next features

**⚠️ Blockers & Risks**:
- Blocked tasks
- High-priority delays
- Critical bugs
- Resource constraints

**🚀 Next Priorities**:
- Top 3-5 priorities
- Recommended actions
- Quick wins

**Output**: Console output with formatted status report

---

## Command Integration with Skills

Commands and Skills work together seamlessly:

### Commands (User-Invoked)
- **Explicit**: User types `/project:command`
- **Predictable**: Same workflow every time
- **Quick**: Fast access to common operations
- **Guided**: Prompts for required information

### Skills (Model-Invoked)
- **Contextual**: Activated based on conversation
- **Flexible**: Adapts to user's natural language
- **Comprehensive**: Full system capabilities
- **Referenced**: Can access reference materials

### When to Use Each

**Use Commands When**:
- You want explicit, predictable behavior
- You're performing routine operations
- You want guided prompts
- You prefer structured workflows

**Use Skills When**:
- You're having natural conversation
- You need flexible, contextual help
- You want comprehensive guidance
- You're exploring or learning

---

## Best Practices

### 1. Command Arguments
- Provide descriptive arguments
- Be specific but concise
- Include key details upfront

**Good**:
```
/project:new-task Implement JWT authentication with refresh tokens
/project:report-bug Login fails with 500 error on production
```

**Less Good**:
```
/project:new-task auth
/project:report-bug bug
```

### 2. Follow Prompts
- Answer all prompted questions
- Provide complete information
- Be specific about requirements

### 3. Review Generated Files
- Check task files for accuracy
- Verify YAML frontmatter
- Confirm file placement

### 4. Use Consistent Naming
- Follow project naming conventions
- Be consistent with terminology
- Use clear, descriptive names

### 5. Leverage Both Commands and Skills
- Use commands for routine operations
- Use Skills for complex workflows
- Combine both for maximum productivity

---

## Troubleshooting

### Command Not Found
**Issue**: Command doesn't activate  
**Solution**: Ensure you're using `/project:` prefix

### Missing Information
**Issue**: Command asks for information you don't have  
**Solution**: Gather information first or skip optional fields

### File Not Created
**Issue**: Expected file wasn't created  
**Solution**: Check for errors, verify directory structure

### YAML Errors
**Issue**: Task file has YAML errors  
**Solution**: Manually fix or regenerate with command

---

## Examples by Workflow

### Starting a New Project
```
1. /project:start-planning My awesome project
2. /project:add-feature User authentication
3. /project:add-feature Product catalog
4. /project:new-task Setup project structure
5. /project:status
```

### Daily Development
```
1. /project:status
2. /project:update-task Task 007 to in-progress
3. /project:report-bug Search not working
4. /project:update-task Task 007 to completed
5. /project:status
```

### Quality Review
```
1. /project:quality-report weekly
2. /project:status bugs
3. Review and address critical issues
4. /project:quality-report (verify improvements)
```

---

## Command Reference Card

**Quick Commands**:
- New task: `/project:new-task [description]`
- Update: `/project:update-task [id]`
- Bug: `/project:report-bug [description]`
- Status: `/project:status`

**Planning Commands**:
- Plan: `/project:start-planning [project]`
- Feature: `/project:add-feature [name]`

**Quality Commands**:
- Report: `/project:quality-report [period]`

---

**Last Updated**: 2025-10-19  
**Version**: 1.0  
**Total Commands**: 7

