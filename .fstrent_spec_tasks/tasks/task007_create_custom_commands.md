---
id: 007
title: 'Create custom commands for common operations'
type: feature
status: completed
priority: high
feature: Claude Code Commands
subsystems: [commands_system, user_experience]
project_context: 'Provide quick access to common fstrent_spec_tasks operations through slash commands'
dependencies: [001, 002, 003, 006]
---

# Task 007: Create Custom Commands for Common Operations

## Objective
Create Claude Code custom commands that provide quick, user-invoked access to common `fstrent_spec_tasks` operations, complementing the Skills with explicit command-based workflows.

## Background
Claude Code supports custom commands (slash commands) that users can invoke explicitly. While Skills are model-invoked based on context, commands provide direct, predictable access to specific operations.

## Commands to Create

### 1. `/project:new-task` - Create New Task
**Purpose**: Quick task creation with guided prompts

**Workflow**:
1. Prompt for task title
2. Prompt for task type (feature, bug_fix, etc.)
3. Prompt for priority
4. Generate task file
5. Update TASKS.md

**Template**:
```markdown
Please create a new task with the following information:

Task Title: $ARGUMENTS

I'll guide you through creating a properly structured task:
1. What type of task is this? (feature/bug_fix/enhancement/refactor)
2. What priority? (critical/high/medium/low)
3. Which feature does this relate to?
4. Which subsystems are affected?

I'll then create the task file and update TASKS.md.
```

### 2. `/project:update-task` - Update Task Status
**Purpose**: Quick task status updates

**Workflow**:
1. Identify task from argument
2. Prompt for new status
3. Update task file
4. Update TASKS.md

**Template**:
```markdown
Please update the status of task: $ARGUMENTS

I'll help you update this task:
1. What's the new status? (pending/in-progress/completed/failed)
2. Any additional notes to add?

I'll update the task file and TASKS.md accordingly.
```

### 3. `/project:report-bug` - Report Bug
**Purpose**: Quick bug reporting with automatic task creation

**Workflow**:
1. Gather bug details
2. Create BUGS.md entry
3. Create bug fix task
4. Update TASKS.md

**Template**:
```markdown
Please report a bug: $ARGUMENTS

I'll help you document this bug properly:
1. What severity? (critical/high/medium/low)
2. How was it discovered? (user_reported/development/testing/production)
3. Which features are affected?
4. Can you provide reproduction steps?

I'll create a BUGS.md entry and corresponding bug fix task.
```

### 4. `/project:start-planning` - Start Project Planning
**Purpose**: Initialize project planning with PRD creation

**Workflow**:
1. Run scope validation questions
2. Create PLAN.md
3. Create PROJECT_CONTEXT.md
4. Create initial feature documents

**Template**:
```markdown
Let's start planning your project: $ARGUMENTS

I'll guide you through the planning process:
1. First, I'll ask the 5 essential scope validation questions
2. Then we'll create a comprehensive PLAN.md
3. We'll set up PROJECT_CONTEXT.md
4. Finally, we'll outline initial features

This ensures we build the right thing at the right complexity level.
```

### 5. `/project:add-feature` - Add Feature Document
**Purpose**: Create new feature specification

**Workflow**:
1. Gather feature details
2. Create feature document
3. Update PLAN.md
4. Create initial tasks

**Template**:
```markdown
Let's add a new feature: $ARGUMENTS

I'll help you document this feature:
1. What's the feature overview?
2. What are the key requirements?
3. What user stories does this address?
4. What are the technical considerations?

I'll create a feature document and update PLAN.md.
```

### 6. `/project:quality-report` - Generate Quality Report
**Purpose**: Generate quality metrics report

**Workflow**:
1. Analyze BUGS.md
2. Calculate metrics
3. Generate report
4. Identify trends

**Template**:
```markdown
Generating quality metrics report for: $ARGUMENTS

I'll analyze your project's quality metrics:
1. Bug discovery rate
2. Resolution time
3. Severity distribution
4. Feature impact analysis
5. Quality gate performance

I'll create a comprehensive quality report.
```

### 7. `/project:status` - Project Status Overview
**Purpose**: Quick project status summary

**Workflow**:
1. Read TASKS.md
2. Read BUGS.md
3. Summarize status
4. Highlight blockers

**Template**:
```markdown
Generating project status overview...

I'll provide a comprehensive status update:
1. Active tasks and their status
2. Open bugs by severity
3. Recent completions
4. Blockers and dependencies
5. Next priorities

This gives you a quick snapshot of project health.
```

## Implementation Plan

### Step 1: Create Command Files
Create `.claude/commands/` directory with:
- `new-task.md`
- `update-task.md`
- `report-bug.md`
- `start-planning.md`
- `add-feature.md`
- `quality-report.md`
- `status.md`

### Step 2: Test Commands
- Verify each command activates correctly
- Test with various arguments
- Validate file creation
- Check error handling

### Step 3: Document Commands
- Add to README
- Create command reference guide
- Include examples

## Acceptance Criteria

- [ ] All 7 commands created
- [ ] Commands activate with `/project:` prefix
- [ ] Commands integrate with Skills
- [ ] Commands create proper files
- [ ] Commands update TASKS.md correctly
- [ ] Error handling is graceful
- [ ] Documentation is complete
- [ ] Commands tested and validated

## Testing Plan

1. Test each command individually
2. Test with various arguments
3. Test error cases
4. Verify file creation
5. Verify TASKS.md updates
6. Test command help text

## Resource Requirements

- Claude Code command documentation
- Existing Skills for integration
- Command template examples

## Success Metrics

- All commands work correctly
- User experience is smooth
- Commands provide value
- Integration with Skills is seamless

## Notes

- Commands should complement Skills, not duplicate
- Keep commands focused and simple
- Provide clear guidance in prompts
- Handle errors gracefully

