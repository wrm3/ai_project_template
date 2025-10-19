---
id: 008
title: 'Create task-expander subagent'
type: feature
status: completed
priority: high
feature: Task Expansion
subsystems: [agents_system, task_management, automation]
project_context: 'Automatically assess task complexity and expand complex tasks into manageable sub-tasks using established complexity criteria'
dependencies: [001, 006, 007]
---

# Task 008: Create Task-Expander Subagent

## Objective
Create a Claude Code subagent that automatically assesses task complexity and expands complex tasks into logical sub-tasks, following the complexity assessment criteria from Cursor's `fstrent_spec_tasks` workflow rules.

## Background
The Cursor `fstrent_spec_tasks` system includes a comprehensive task expansion workflow with:
- **Complexity scoring** (1-10+ scale with 8 criteria)
- **Automatic expansion** for tasks scoring ≥7
- **Sub-task creation** with proper file structure
- **Subsystem alignment** for logical breakdown

This subagent will bring this capability to Claude Code.

## Complexity Assessment Criteria

### Scoring System (1-10+ scale)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Estimated Effort** | 4 | Task takes >2-3 developer days |
| **Cross-Subsystem Impact** | 3 | Affects multiple subsystems |
| **Multiple Components** | 3 | Changes across unrelated modules |
| **High Uncertainty** | 2 | Requirements unclear or unknown challenges |
| **Multiple Outcomes** | 2 | Several distinct, verifiable outcomes |
| **Dependency Blocking** | 2 | Large prerequisite for subsequent tasks |
| **Numerous Criteria** | 1 | Exceptionally long requirements |
| **Story Points** | 1 | Task assigned >5 story points |

### Complexity Matrix

```
0-3 points  | Simple Task    | Proceed normally
4-6 points  | Moderate Task  | Consider expansion
7-10 points | Complex Task   | Expansion required (MANDATORY)
11+ points  | High Complex   | Must expand before creation
```

## Sub-Task File Format

**Filename**: `task{parent_id}.{sub_id}_descriptive_name.md`

**Examples**:
- `task42.1_setup_database.md`
- `task42.2_create_api.md`
- `task42.3_build_frontend.md`

**YAML Frontmatter**:
```yaml
---
id: "42.1"              # String ID for sub-tasks
title: 'Setup Database'
type: task
status: pending
priority: high
parent_task: 42
dependencies: []        # Can depend on other tasks/sub-tasks
---
```

## Agent Implementation

### Agent File: `.claude/agents/task-expander.md`

The agent will:
1. **Assess Complexity**: Score tasks using 8 criteria
2. **Determine Action**: Expand if score ≥7
3. **Break Down Tasks**: Create logical sub-task breakdown
4. **Generate Files**: Create sub-task files with proper structure
5. **Update TASKS.md**: Add sub-task entries
6. **Update Parent**: Link parent to sub-tasks

### Activation Triggers

**Proactive** (automatic):
- When user creates a task with multiple components
- When task description is very long
- When task mentions multiple subsystems
- When task has >5 story points

**Explicit** (manual):
- User says "expand this task"
- User says "break down task X"
- User asks "is this task too complex?"

## Acceptance Criteria

- [ ] Agent file created in `.claude/agents/`
- [ ] Complexity assessment logic implemented
- [ ] Sub-task generation works correctly
- [ ] File naming follows convention (task{id}.{sub_id})
- [ ] YAML frontmatter is valid
- [ ] TASKS.md updates correctly
- [ ] Parent task references sub-tasks
- [ ] Subsystem alignment works
- [ ] Proactive activation works
- [ ] Manual activation works
- [ ] Documentation complete
- [ ] Testing complete

## Implementation Plan

### Step 1: Create Agent File
Create `.claude/agents/task-expander.md` with:
- Agent metadata (name, description, tools)
- Complexity assessment instructions
- Sub-task generation logic
- File creation procedures
- TASKS.md update logic

### Step 2: Implement Complexity Scoring
Detailed instructions for:
- Evaluating each of 8 criteria
- Calculating total score
- Determining expansion threshold
- Documenting reasoning

### Step 3: Sub-Task Breakdown Logic
Instructions for:
- Identifying logical boundaries
- Aligning with subsystems
- Creating sequential dependencies
- Naming sub-tasks clearly

### Step 4: File Generation
Instructions for:
- Creating sub-task files
- Proper YAML frontmatter
- File naming convention
- Directory placement

### Step 5: Integration
Instructions for:
- Updating TASKS.md
- Linking parent to sub-tasks
- Setting up dependencies
- Maintaining consistency

### Step 6: Testing
Test cases for:
- Simple tasks (no expansion)
- Moderate tasks (optional expansion)
- Complex tasks (mandatory expansion)
- Very complex tasks (immediate expansion)

## Testing Plan

### Test Case 1: Simple Task (Score 0-3)
**Input**: "Add a button to the settings page"

**Expected**:
- Score: ~2 points
- Action: No expansion
- Result: Single task created

### Test Case 2: Moderate Task (Score 4-6)
**Input**: "Implement user profile page with avatar upload"

**Expected**:
- Score: ~5 points
- Action: Consider expansion (optional)
- Result: Ask user if they want expansion

### Test Case 3: Complex Task (Score 7-10)
**Input**: "Implement complete user authentication system with email/password, OAuth, 2FA, and password reset"

**Expected**:
- Score: ~8 points
- Action: Mandatory expansion
- Result: Break into sub-tasks:
  - task{id}.1: Setup database schema
  - task{id}.2: Implement email/password auth
  - task{id}.3: Add OAuth integration
  - task{id}.4: Implement 2FA
  - task{id}.5: Add password reset flow

### Test Case 4: Very Complex Task (Score 11+)
**Input**: "Build complete e-commerce platform with product catalog, shopping cart, checkout, payment processing, order management, inventory tracking, and admin dashboard"

**Expected**:
- Score: ~14 points
- Action: Immediate expansion required
- Result: Break into 8-10 sub-tasks aligned with subsystems

## Success Metrics

- Agent activates correctly (proactive and manual)
- Complexity scoring is accurate
- Sub-tasks are logical and actionable
- File structure is correct
- TASKS.md updates properly
- Parent-child relationships work
- User experience is smooth
- Documentation is clear

## Resources

### From Cursor Rules
- `.cursor/rules/fstrent_spec_tasks/rules/workflow.mdc`
- Complexity assessment criteria
- Sub-task creation process
- File naming conventions

### Claude Code Documentation
- Subagent creation guide
- Tool permissions
- Activation patterns

## Notes

- Agent should be helpful, not annoying
- Explain reasoning for expansion decisions
- Allow user to override if needed
- Provide clear sub-task breakdown
- Maintain consistency with existing system
- Document all decisions

## Example Agent Behavior

### Scenario: User Creates Complex Task

**User**: "Create a task to implement user authentication"

**Agent** (assesses complexity):
```
Analyzing task complexity...

Complexity Score: 8/10
- Estimated Effort: 4 points (3+ days)
- Cross-Subsystem: 3 points (auth, database, API, frontend)
- Multiple Components: 3 points (login, register, sessions)

This task is complex and should be expanded into sub-tasks.

Proposed breakdown:
1. Setup authentication database schema
2. Implement registration endpoint
3. Implement login endpoint
4. Add session management
5. Create frontend auth components
6. Add password reset flow

Shall I create these sub-tasks?
```

**User**: "Yes"

**Agent** (creates sub-tasks):
```
Creating sub-tasks...

✅ Created task42.1_setup_auth_database.md
✅ Created task42.2_implement_registration.md
✅ Created task42.3_implement_login.md
✅ Created task42.4_add_session_management.md
✅ Created task42.5_create_auth_components.md
✅ Created task42.6_add_password_reset.md
✅ Updated TASKS.md
✅ Updated parent task (Task 42)

Sub-tasks are ready! Start with task42.1.
```

---

**Status**: In Progress  
**Priority**: High  
**Complexity**: Medium (well-defined process from Cursor)

