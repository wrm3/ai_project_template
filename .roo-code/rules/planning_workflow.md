# Planning Workflow Rules (Roo-Code)

For complete planning documentation, see: `.claude/rules/planning_workflow.md`

## Quick Reference

### Planning Process
1. **Gather Requirements** - Use `/start-planning` command
2. **Create PRD** - Document in `.fstrent_spec_tasks/PLAN.md`
3. **Validate Scope** - Prevent over-engineering
4. **Break Down Tasks** - Create individual task files
5. **Define Success Criteria** - Clear acceptance criteria

### PRD Structure
```markdown
# Feature: Name

## Overview
Brief description...

## User Stories
- As a [user], I want [goal] so that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Approach
Implementation strategy...

## Out of Scope
What we're NOT building...
```

### Scope Validation
Before implementing, ask:
- Is this the simplest solution?
- Are we over-engineering?
- What's the minimum viable feature?
- Can we ship sooner with less?

### Feature Files
Create detailed feature docs in: `.fstrent_spec_tasks/features/`

For complete planning rules, see `.claude/rules/planning_workflow.md`
