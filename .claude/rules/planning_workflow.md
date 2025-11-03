# Planning - PRD Before Coding

## When to Use Planning Skill

**Starting new project or major feature?** Create a Product Requirements Document (PRD) first.

**Invoke:** `fstrent-planning` skill
**Triggers:** "create PRD", "plan feature", "start planning", "define requirements"

---

## Why PRD First?

**Common mistake:** Jumping straight into code without planning

**Consequences:**
- ❌ Scope creep during development
- ❌ Missing requirements discovered late
- ❌ Rework and wasted effort
- ❌ Unclear success criteria

**Better approach:**
- ✅ PRD defines clear scope
- ✅ Stakeholder alignment before coding
- ✅ Success metrics defined upfront
- ✅ Prevents mid-development pivots

---

## PRD Location and Format

**File:** `.fstrent_spec_tasks/PLAN.md`

**Preferred structure:**
```markdown
# Project/Feature Name

## Vision & Goals
What problem are we solving? Why does this matter?

## Core Features
What will we build? (High-level list)

## Out of Scope
What are we explicitly NOT building? (Prevents scope creep)

## Success Metrics
How do we know this succeeded? (Measurable criteria)

## Technical Approach
High-level architecture and key decisions

## Timeline & Milestones
Major phases and deliverables
```

---

## Workflow

### ✅ Correct Sequence

1. **Planning** - Create PRD, get feedback
2. **Task Breakdown** - Break PRD into tasks
3. **Implementation** - Build according to tasks
4. **Validation** - Measure against success metrics

### ❌ Wrong Sequence

1. ~~Start coding~~
2. ~~Realize unclear requirements~~
3. ~~Ask for clarification mid-development~~
4. ~~Rework completed code~~

---

## Integration with Tasks

**PRD → Tasks:**
- Each feature in PRD becomes multiple tasks
- Use `fstrent-task-management` skill to create tasks
- Reference PRD in task `project_context` field

**Example task linking to PRD:**
```yaml
---
id: 042
title: 'Implement User Authentication'
project_context: 'Core security feature defined in PLAN.md section 3.2'
feature: 'User Management'
---
```

---

## Full Planning Workflow

**For complete planning guidance:**
- `.claude/skills/fstrent-planning/SKILL.md` - Planning skill overview
- `.claude/skills/fstrent-planning/rules.md` - Detailed planning rules

**Skill provides:**
- PRD templates and examples
- Feature definition guidelines
- Success metric frameworks
- Stakeholder collaboration patterns
