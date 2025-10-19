---
id: 005
title: 'Add example files to Skills'
type: feature
status: completed
priority: medium
feature: Claude Code Skills
subsystems: [skills_system, documentation]
project_context: 'Provide concrete examples similar to webapp-testing pattern, demonstrating real-world usage of the Skills'
dependencies: [001, 002, 003]
---

# Task 005: Add Example Files to Skills

## Objective
Add `examples/` folders to each of the three core Skills, containing real-world example files that demonstrate proper usage. This follows the pattern established by Anthropic's webapp-testing Skill.

## Background
Analysis of Anthropic's webapp-testing Skill shows it includes an `examples/` folder with working Python scripts demonstrating different use cases. Our Skills would benefit from concrete examples showing:
- Properly formatted task files
- Complete PLAN.md examples
- Bug tracking examples
- Workflow demonstrations

## Acceptance Criteria
- [ ] Create `examples/` folder in each Skill directory
- [ ] Add realistic, working examples
- [ ] Examples demonstrate best practices
- [ ] Examples show common use cases
- [ ] Examples are referenced from SKILL.md
- [ ] All examples are properly formatted

## Implementation Plan

### For fstrent-task-management/examples/
1. **simple_task.md**
   - Basic feature task example
   - Shows minimal required fields
   - Demonstrates proper YAML frontmatter

2. **complex_task_with_subtasks.md**
   - Parent task with sub-tasks
   - Shows dependency management
   - Demonstrates sub-task numbering (42.1, 42.2, etc.)

3. **bug_fix_task.md**
   - Bug fix task example
   - Shows bug reference integration
   - Demonstrates reproduction steps

4. **retroactive_task.md**
   - Retroactive fix documentation
   - Shows completed task format
   - Demonstrates lessons learned capture

5. **TASKS.md**
   - Sample master task list
   - Shows proper emoji usage
   - Demonstrates task organization

### For fstrent-planning/examples/
1. **minimal_prd.md**
   - Simplified PRD for small project
   - Shows essential sections only
   - Good for quick projects

2. **complete_prd.md**
   - Full 10-section PRD
   - Comprehensive example
   - Shows all optional sections

3. **feature_document.md**
   - Individual feature specification
   - Shows feature-task integration
   - Demonstrates acceptance criteria

4. **scope_validation_example.md**
   - Completed scope validation questionnaire
   - Shows decision-making process
   - Demonstrates over-engineering prevention

### For fstrent-qa/examples/
1. **BUGS.md**
   - Sample bug tracking file
   - Shows multiple bug entries
   - Demonstrates status transitions

2. **critical_bug_entry.md**
   - Critical severity bug example
   - Shows production issue format
   - Demonstrates urgency indicators

3. **bug_fix_workflow.md**
   - Complete bug lifecycle example
   - Shows status progression
   - Demonstrates resolution documentation

4. **quality_metrics_report.md**
   - Sample quality metrics
   - Shows metric calculations
   - Demonstrates trend analysis

## File Structure
```
.claude/skills/
├── fstrent-task-management/
│   ├── SKILL.md
│   ├── reference/
│   └── examples/
│       ├── simple_task.md
│       ├── complex_task_with_subtasks.md
│       ├── bug_fix_task.md
│       ├── retroactive_task.md
│       └── TASKS.md
├── fstrent-planning/
│   ├── SKILL.md
│   ├── reference/
│   └── examples/
│       ├── minimal_prd.md
│       ├── complete_prd.md
│       ├── feature_document.md
│       └── scope_validation_example.md
└── fstrent-qa/
    ├── SKILL.md
    ├── reference/
    └── examples/
        ├── BUGS.md
        ├── critical_bug_entry.md
        ├── bug_fix_workflow.md
        └── quality_metrics_report.md
```

## Testing Plan
1. Verify all example files are created
2. Validate YAML frontmatter in examples
3. Check markdown formatting
4. Ensure examples follow best practices
5. Test that examples can be used as templates

## Resource Requirements
- Existing task files from real projects
- Sample PRDs and feature documents
- Bug tracking examples
- Quality metrics data

## Success Metrics
- All example folders created with complete files
- Examples are realistic and useful
- Users can copy examples as starting points
- Examples demonstrate best practices clearly

## Notes
- Examples should be based on real-world scenarios
- Use realistic data, not "foo/bar" placeholders
- Include comments explaining key decisions
- Show both simple and complex cases
- Maintain consistency with SKILL.md guidance

