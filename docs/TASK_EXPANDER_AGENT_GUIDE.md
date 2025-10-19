# Task Expander Agent - User Guide

## Overview

The Task Expander Agent automatically assesses task complexity and expands complex tasks into manageable sub-tasks.

**Location**: `.claude/agents/task-expander.md`  
**Activation**: Automatic (proactive) or Manual (explicit)  
**Purpose**: Break down complex work into actionable sub-tasks

---

## How It Works

### 1. Complexity Assessment

The agent evaluates tasks using 8 criteria:

| Criteria | Points | What It Checks |
|----------|--------|----------------|
| Estimated Effort | 4 | Takes >2-3 days |
| Cross-Subsystem | 3 | Affects 3+ subsystems |
| Multiple Components | 3 | Changes 3+ unrelated modules |
| High Uncertainty | 2 | Unclear requirements |
| Multiple Outcomes | 2 | 4+ distinct deliverables |
| Dependency Blocking | 2 | Blocks other tasks |
| Numerous Criteria | 1 | Very long requirements |
| Story Points | 1 | >5 story points |

### 2. Decision Matrix

```
Score 0-3:  Simple    → No expansion
Score 4-6:  Moderate  → Ask user
Score 7-10: Complex   → Expansion required
Score 11+:  Very High → Immediate expansion
```

### 3. Sub-Task Creation

If expansion is needed:
- Creates 3-8 logical sub-tasks
- Aligns with subsystem boundaries
- Sets up proper dependencies
- Updates all files automatically

---

## Usage Examples

### Example 1: Automatic Expansion

**You say**:
> "Create a task to implement complete user authentication with email/password, OAuth, 2FA, and password reset"

**Agent responds**:
```
🔍 Analyzing task complexity...

Complexity Score: 12/10 (High Complexity)
- Estimated Effort: 4 points (5-7 days)
- Cross-Subsystem: 3 points (auth, database, API, frontend, email)
- Multiple Components: 3 points (login, register, OAuth, 2FA, reset)
- Multiple Outcomes: 2 points (6 distinct features)

This task MUST be expanded.

Proposed breakdown:
1. Setup authentication infrastructure
2. Implement email/password auth
3. Add OAuth integration
4. Implement 2FA
5. Add password reset flow
6. Create frontend components

Shall I create these sub-tasks?
```

### Example 2: Manual Expansion

**You say**:
> "Expand task 42"

**Agent responds**:
```
Reading Task 42...

Task: "Implement user dashboard with analytics, notifications, and settings"

Complexity Score: 8/10 (Complex)

Proposed breakdown:
1. Create dashboard layout and navigation
2. Implement analytics widgets
3. Add notification system
4. Build settings interface

Creating sub-tasks...
✅ Done!
```

### Example 3: Simple Task (No Expansion)

**You say**:
> "Create a task to add a dark mode toggle"

**Agent responds**:
```
Complexity Score: 2/10 (Simple)

This task is straightforward and doesn't need expansion.

Creating single task...
✅ Task created!
```

---

## Sub-Task Structure

### File Naming

Format: `task{parent}.{sub}_description.md`

Examples:
- `task42.1_setup_database.md`
- `task42.2_implement_api.md`
- `task42.3_build_frontend.md`

### TASKS.md Format

```markdown
- [ ] Task 42: Implement user authentication
  - [ ] Task 42.1: Setup authentication infrastructure
  - [ ] Task 42.2: Implement email/password auth
  - [ ] Task 42.3: Add OAuth integration
  - [ ] Task 42.4: Implement 2FA
  - [ ] Task 42.5: Add password reset flow
  - [ ] Task 42.6: Create frontend components
```

### Dependencies

Sub-tasks can depend on each other:
```yaml
dependencies: ["42.1", "42.2"]  # Depends on sub-tasks 42.1 and 42.2
```

---

## When Agent Activates

### Automatic Activation

Agent activates when you:
- Mention multiple subsystems
- Describe work taking >2 days
- List many requirements
- Mention >5 story points
- Describe complex features

### Manual Activation

Say any of these:
- "Expand this task"
- "Break down task 42"
- "Is this too complex?"
- "Create sub-tasks"
- "This seems too big"

---

## Best Practices

### Creating Tasks That Benefit from Expansion

**Good** (will trigger expansion):
```
"Implement complete e-commerce checkout with cart, payment processing,
order confirmation, inventory updates, and email notifications"
```

**Simple** (won't trigger):
```
"Add a checkout button to the cart page"
```

### Working with Sub-Tasks

1. **Start with foundation sub-tasks** (usually .1, .2)
2. **Complete sub-tasks in order** when dependencies exist
3. **Update status** as you complete each sub-task
4. **Parent task completes** when all sub-tasks are done

### Customizing Breakdown

If you don't like the proposed breakdown:
```
You: "Expand task 42"
Agent: [proposes breakdown]
You: "Can you combine sub-tasks 2 and 3?"
Agent: [adjusts breakdown]
```

---

## Troubleshooting

### Agent Doesn't Activate

**Problem**: Created complex task but agent didn't activate

**Solutions**:
- Manually trigger: "Expand this task"
- Be more explicit: "This will take 5 days and affects database, API, and frontend"
- Check task description includes complexity indicators

### Too Many Sub-Tasks

**Problem**: Agent created 12 sub-tasks

**Solutions**:
- Ask agent to group some together
- Request high-level breakdown
- Manually adjust after creation

### Sub-Tasks Too Small

**Problem**: Sub-tasks are trivial

**Solutions**:
- Ask agent to combine sub-tasks
- Provide feedback for adjustment
- Manually merge sub-tasks

---

## Integration with Other Tools

### With Commands

Use commands on sub-tasks:
```
/project:update-task Task 42.1 to completed
/project:status  # Shows sub-task progress
```

### With Skills

Skills work with sub-tasks:
- Task Management Skill handles sub-tasks
- Planning Skill links sub-tasks to features
- QA Skill tracks bugs in sub-tasks

### With Cursor

Sub-tasks work identically in Cursor:
- Same file format
- Same YAML schema
- Same TASKS.md structure
- 100% compatible

---

## Examples by Project Type

### Web Application
```
Task: "Build user dashboard"
Sub-tasks:
1. Create dashboard layout
2. Implement data fetching
3. Build analytics widgets
4. Add user settings
5. Implement notifications
```

### API Development
```
Task: "Implement REST API"
Sub-tasks:
1. Design API schema
2. Create database models
3. Implement CRUD endpoints
4. Add authentication
5. Write API documentation
6. Add rate limiting
```

### Database Migration
```
Task: "Migrate to new database"
Sub-tasks:
1. Design new schema
2. Create migration scripts
3. Test migration process
4. Migrate data
5. Update application code
6. Verify data integrity
```

---

## Tips for Success

### 1. Be Descriptive
More detail = better complexity assessment
```
❌ "Add auth"
✅ "Implement complete authentication with email/password, OAuth, and 2FA"
```

### 2. Mention Subsystems
Helps agent create aligned sub-tasks
```
❌ "Build the feature"
✅ "Build feature affecting database, API, and frontend"
```

### 3. Estimate Effort
Triggers complexity scoring
```
❌ "Create dashboard"
✅ "Create dashboard (estimated 5 days)"
```

### 4. List Requirements
More criteria = higher complexity score
```
❌ "Add settings"
✅ "Add settings with profile, preferences, notifications, security, and billing"
```

---

## FAQ

**Q: Can I disable automatic expansion?**  
A: Yes, just decline when agent asks. It won't force expansion.

**Q: Can I manually expand simple tasks?**  
A: Yes, say "expand task X" even if it's simple.

**Q: What if I disagree with the breakdown?**  
A: Ask agent to adjust, or manually modify after creation.

**Q: Do sub-tasks count toward completion metrics?**  
A: Yes, each sub-task completion contributes to overall progress.

**Q: Can sub-tasks have their own sub-tasks?**  
A: Technically yes (task42.1.1), but not recommended. Keep it simple.

**Q: How do I know when to expand manually?**  
A: If a task feels overwhelming or has many distinct parts.

---

## Summary

The Task Expander Agent:
- ✅ Automatically assesses complexity
- ✅ Expands complex tasks logically
- ✅ Creates proper file structure
- ✅ Updates all files automatically
- ✅ Aligns with subsystems
- ✅ Sets up dependencies
- ✅ Works with Cursor
- ✅ Improves project manageability

**Result**: Complex work becomes manageable, organized, and trackable!

---

**Last Updated**: 2025-10-19  
**Version**: 1.0  
**Agent File**: `.claude/agents/task-expander.md`

