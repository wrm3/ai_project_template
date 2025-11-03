# Task Management System Rules

**CRITICAL:** These rules apply to ALL AI assistants working with the fstrent_spec_tasks system.

---

## Overview

This project uses the **fstrent_spec_tasks** task management system - a file-based, cross-IDE compatible system for tracking development tasks. Both Claude Code and Cursor (and other IDEs) read and write the same files.

**Key Principle:** Tasks are documented in `.fstrent_spec_tasks/` using YAML frontmatter + Markdown content.

---

## Task File Format - YAML FRONTMATTER REQUIRED

### CRITICAL: Every Task File Must Have YAML Frontmatter

**Correct Format:**
```yaml
---
id: 001
title: 'Task Title Here'
type: feature
status: pending
priority: high
---

# Task 001: Task Title Here

## Objective
What needs to be accomplished...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

**WRONG - Missing YAML:**
```markdown
# Task 001: Task Title

**Task ID**: 001
**Status**: Complete

## Overview
This format is WRONG - no YAML frontmatter!
```

### Required YAML Fields

**Minimum required fields:**
```yaml
---
id: {number}           # Sequential ID: 001, 002, 003, etc.
title: 'Task Title'    # Brief, actionable title (use quotes)
type: feature|task|bug_fix|retroactive_fix
status: pending|in-progress|completed|failed
priority: critical|high|medium|low
---
```

**Optional but recommended fields:**
```yaml
feature: 'Feature Name'                    # Related feature
subsystems: [component1, component2]       # Affected components
project_context: 'Brief description'       # How task relates to project
dependencies: [001, 002]                   # Task IDs that must complete first
estimated_effort: '4-6 hours'              # Time estimate
created_date: '2025-10-21'                # ISO format
completed_date: '2025-10-22'              # ISO format
assigned_to: 'Developer Name'              # Who's working on it
---
```

### Why YAML Frontmatter Is Required

1. **Cross-IDE Compatibility**: Both Claude Code and Cursor parse YAML metadata
2. **Automated Processing**: The fstrent-task-management skill reads YAML fields
3. **Structured Queries**: Can filter/search tasks by status, priority, type
4. **Dependency Tracking**: System validates dependencies using YAML data
5. **Status Management**: Automated status updates require YAML structure

**Without YAML frontmatter, the task management system CANNOT process your task files!**

---

## File Locations

### Task Files
**Location:** `.fstrent_spec_tasks/tasks/`
**Naming:** `task{id}_descriptive_name.md`
**Examples:**
- `task001_setup_database.md`
- `task042_implement_authentication.md`
- `task153_fix_login_bug.md`

### Master Task List
**Location:** `.fstrent_spec_tasks/TASKS.md`
**Purpose:** Central checklist with status indicators for all tasks

### Supporting Files
- `PROJECT_CONTEXT.md` - Project mission and goals
- `PLAN.md` - Product Requirements Document
- `BUGS.md` - Bug tracking (subset of tasks)
- `features/` - Feature documentation folder

---

## Task Creation Workflow

### Step-by-Step Process

1. **Determine Next Task ID**
   - Read `.fstrent_spec_tasks/TASKS.md`
   - Find highest task number
   - New task ID = max + 1
   - Zero-pad to 3 digits (001, 002, etc.)

2. **Create Task File**
   - Filename: `.fstrent_spec_tasks/tasks/task{id}_descriptive_name.md`
   - Start with YAML frontmatter (all required fields)
   - Add markdown content (objective, criteria, notes)

3. **Update TASKS.md**
   - Add entry: `- [ ] Task {id}: {Brief description}`
   - Place in appropriate phase/section
   - Maintain consistent formatting

4. **Verify Both Files**
   - Task file has valid YAML
   - TASKS.md entry added
   - ID matches between files
   - No duplicate IDs

### Example Task Creation

**Task File (`.fstrent_spec_tasks/tasks/task042_implement_auth.md`):**
```yaml
---
id: 042
title: 'Implement User Authentication'
type: feature
status: pending
priority: high
feature: 'User Management'
subsystems: [auth, database, api]
estimated_effort: '8-12 hours'
dependencies: [001, 041]
---

# Task 042: Implement User Authentication

## Objective
Create secure user authentication system with JWT tokens and password hashing.

## Acceptance Criteria
- [ ] Password hashing with bcrypt
- [ ] JWT token generation and validation
- [ ] Login endpoint with credential verification
- [ ] Token refresh mechanism
- [ ] Security headers implemented

## Implementation Notes
- Use bcrypt with cost factor 12
- JWT expiration: 1 hour (access), 7 days (refresh)
- Store refresh tokens in database
- Rate limit login attempts (5 per minute)

## Testing Plan
- Unit tests for all auth functions
- Integration tests for login flow
- Security testing with OWASP guidelines
```

**TASKS.md Entry:**
```markdown
### Phase 2: Core Features
- [✅] Task 001: Setup database schema
- [✅] Task 041: Create user model
- [ ] Task 042: Implement user authentication
```

---

## Status Management

### Status Values and Meanings

**pending** ([ ])
- Task defined but not started
- Ready to begin work

**in-progress** ([🔄])
- Actively being worked on
- Should have only 1-3 tasks in this state at a time

**completed** ([✅])
- Successfully finished
- Acceptance criteria met
- Tested and verified

**failed** ([❌])
- Blocked or abandoned
- Cannot complete as planned
- Document reason in task notes

### Status Update Process

**When status changes:**

1. **Update Task File YAML:**
   ```yaml
   status: in-progress  # Changed from pending
   ```

2. **Update TASKS.md Entry:**
   ```markdown
   - [🔄] Task 042: Implement user authentication
   ```

3. **Add Completion Date (if completed):**
   ```yaml
   status: completed
   completed_date: '2025-10-21'
   ```

**CRITICAL:** Always update BOTH files together. Never update one without the other.

### Windows-Safe Status Emojis

Use these EXACT emojis in TASKS.md:
- `[ ]` - Pending (checkbox, not emoji)
- `[🔄]` - In Progress (counterclockwise arrows)
- `[✅]` - Completed (check mark button)
- `[❌]` - Failed (cross mark)

**Why these specific emojis?**
- Render correctly on Windows 10/11
- Clear visual distinction
- Supported across all terminals and IDEs
- Part of Unicode standard

---

## When to Create Tasks

### Always Create Tasks For:

✅ New features or functionality
✅ Bug fixes (especially if taking >1 hour)
✅ Refactoring efforts
✅ Database schema changes
✅ API endpoint additions
✅ Security improvements
✅ Performance optimizations
✅ Documentation work (if substantial)
✅ Testing infrastructure
✅ Deployment procedures

### Don't Create Tasks For:

❌ Typo fixes (just fix them)
❌ Comment updates
❌ Formatting changes
❌ Trivial config tweaks
❌ One-line bug fixes

**Rule of Thumb:** If it takes more than 30 minutes or affects multiple files, create a task.

---

## Sub-Tasks for Complex Work

### When to Use Sub-Tasks

Create sub-tasks when:
- Task spans multiple days
- Task affects 3+ subsystems
- Task has distinct sequential phases
- Breaking down would improve clarity

### Sub-Task Structure

**Parent Task:**
```yaml
---
id: 042
title: 'Implement User Authentication'
type: feature
status: in-progress
priority: high
has_subtasks: true
subtasks: ["042.1", "042.2", "042.3"]
---
```

**Sub-Task Files:**
- `task042.1_password_hashing.md`
- `task042.2_jwt_implementation.md`
- `task042.3_login_endpoint.md`

**Sub-Task YAML:**
```yaml
---
id: "042.1"              # String ID for sub-tasks
title: 'Implement Password Hashing'
type: task
status: completed
priority: high
parent_task: 042
---
```

**TASKS.md Format:**
```markdown
- [🔄] Task 042: Implement user authentication
  - [✅] Task 042.1: Password hashing
  - [🔄] Task 042.2: JWT implementation
  - [ ] Task 042.3: Login endpoint
```

---

## Dependency Management

### Declaring Dependencies

In task YAML:
```yaml
dependencies: [001, 002, 042]
```

**Meaning:** This task cannot start until tasks 001, 002, and 042 are completed.

### Validation Rules

- All dependency IDs must exist
- No circular dependencies
- Dependency graph must be acyclic (DAG)

### Checking Dependencies

Before starting a task:
1. Read task file
2. Check `dependencies` field
3. For each dependency ID:
   - Verify that task status = `completed`
4. If all complete → can start
5. If any incomplete → task is blocked

---

## Common Mistakes to Avoid

### ❌ WRONG: No YAML Frontmatter

```markdown
# Task 042: Implement Authentication

**Status**: Complete
**Priority**: High

## Description
This is WRONG - missing YAML frontmatter!
```

**Problem:** Task management system cannot parse this file.

### ❌ WRONG: Invalid YAML Syntax

```yaml
---
id: 042
title: Missing quotes cause parse error
status: complete  # WRONG - should be 'completed'
---
```

**Problem:** YAML parser will fail.

### ❌ WRONG: Inconsistent Updates

**Task file says:**
```yaml
status: completed
```

**But TASKS.md says:**
```markdown
- [ ] Task 042: Still shows pending!
```

**Problem:** Files out of sync - always update both together.

### ❌ WRONG: Missing Required Fields

```yaml
---
id: 042
title: 'Implement Auth'
# Missing: type, status, priority
---
```

**Problem:** System requires minimum fields for processing.

### ✅ CORRECT: Complete YAML with All Fields

```yaml
---
id: 042
title: 'Implement User Authentication'
type: feature
status: pending
priority: high
feature: 'User Management'
subsystems: [auth, database]
estimated_effort: '8-12 hours'
---

# Task 042: Implement User Authentication

## Objective
Create secure authentication system...
```

---

## Integration with Skills

### The fstrent-task-management Skill

**Location:** `.claude/skills/fstrent-task-management/`

**When invoked:**
- Automatically creates tasks with correct format
- Validates YAML frontmatter
- Updates TASKS.md
- Checks dependencies
- Manages status transitions

**How to invoke:**
- User mentions "task", "todo", "work item"
- User requests task creation/update
- User asks about project progress

**Skill reads these rules:** The skill's `rules.md` file contains detailed implementation rules that expand on these guidelines.

---

## Why This System Exists

### Cross-IDE Compatibility

**The Problem:**
- Developers use different AI IDEs (Claude Code, Cursor, Windsurf, etc.)
- Each IDE has different task management approaches
- Switching IDEs means losing task context

**The Solution:**
- Shared file-based system (`.fstrent_spec_tasks/`)
- All IDEs read/write same files
- YAML provides structured, parseable metadata
- No database needed - just files in git

### Benefits

1. **Universal Access** - Works in any IDE
2. **Git-Friendly** - Plain text, easy diffs
3. **Human Readable** - Can edit with any text editor
4. **Structured Data** - YAML enables automation
5. **Team Collaboration** - Everyone sees same tasks
6. **No Vendor Lock-in** - Not tied to specific tool

---

## Quick Reference

### Task File Checklist

When creating a task file:

☐ 1. YAML frontmatter at top of file
☐ 2. All required fields (id, title, type, status, priority)
☐ 3. Optional fields as needed
☐ 4. Markdown content (objective, criteria, notes)
☐ 5. Entry added to TASKS.md
☐ 6. Both files use same task ID
☐ 7. No duplicate IDs in system

### Status Update Checklist

When changing task status:

☐ 1. Update `status` in task file YAML
☐ 2. Update emoji in TASKS.md entry
☐ 3. Add completion date if status=completed
☐ 4. Verify both files match
☐ 5. Commit both files together

### File Naming Checklist

☐ 1. Format: `task{id}_descriptive_name.md`
☐ 2. ID is zero-padded (001, 002, not 1, 2)
☐ 3. Descriptive name uses underscores
☐ 4. Name is lowercase
☐ 5. Location: `.fstrent_spec_tasks/tasks/`

---

## Troubleshooting

### "Task management skill doesn't recognize my tasks"

**Likely cause:** Missing or invalid YAML frontmatter

**Fix:** Add YAML frontmatter with all required fields at top of task file.

### "TASKS.md and task files don't match"

**Likely cause:** Updated one file but not the other

**Fix:** Always update both files together when changing status.

### "Cannot find next task ID"

**Likely cause:** TASKS.md missing or corrupted

**Fix:**
1. Check if `.fstrent_spec_tasks/TASKS.md` exists
2. Look at existing task files to find highest ID
3. New ID = max ID + 1

### "YAML parse error"

**Likely cause:** Invalid YAML syntax

**Common issues:**
- Missing quotes around title with special characters
- Invalid status value (use: pending, in-progress, completed, failed)
- Incorrect list syntax for arrays
- Missing closing `---` marker

**Fix:** Validate YAML syntax, check against examples above.

---

## Examples

### Minimal Task File

```yaml
---
id: 001
title: 'Setup Project Repository'
type: task
status: pending
priority: high
---

# Task 001: Setup Project Repository

## Objective
Initialize git repository with proper structure.

## Acceptance Criteria
- [ ] Repository created on GitHub
- [ ] Initial folder structure created
- [ ] README.md added
- [ ] .gitignore configured
```

### Comprehensive Task File

```yaml
---
id: 042
title: 'Implement User Authentication System'
type: feature
status: in-progress
priority: critical
feature: 'User Management'
subsystems: [auth, database, api, security]
project_context: 'Core security feature required before public launch'
dependencies: [001, 040, 041]
estimated_effort: '12-16 hours'
created_date: '2025-10-20'
assigned_to: 'Backend Team'
---

# Task 042: Implement User Authentication System

## Objective
Create secure, production-ready user authentication with JWT tokens, password hashing, and session management.

## Acceptance Criteria
- [ ] Password hashing implemented with bcrypt (cost factor 12)
- [ ] JWT token generation and validation working
- [ ] Login endpoint with credential verification
- [ ] Token refresh mechanism implemented
- [ ] Session management with Redis
- [ ] Rate limiting on auth endpoints (5 req/min per IP)
- [ ] Security headers configured (CORS, CSP, etc.)
- [ ] Audit logging for auth events
- [ ] Unit tests with >90% coverage
- [ ] Integration tests for complete flow
- [ ] Security audit completed
- [ ] Documentation updated

## Implementation Notes

### Password Security
- Use bcrypt with cost factor 12
- Require minimum 8 characters, mix of types
- Check against common password database
- Implement password strength meter

### JWT Strategy
- Access token expiration: 1 hour
- Refresh token expiration: 7 days
- Store refresh tokens in Redis with user ID
- Rotate refresh tokens on each use
- Revocation list for compromised tokens

### Rate Limiting
- 5 login attempts per minute per IP
- Exponential backoff after failures
- CAPTCHA after 3 failed attempts
- Log suspicious patterns

### Security Considerations
- Use secure HTTP-only cookies for tokens
- Implement CSRF protection
- Add security headers (HSTS, CSP, etc.)
- Sanitize all inputs
- Prevent timing attacks on credential checks

## Testing Plan

### Unit Tests
- Password hashing/verification
- JWT creation/validation
- Rate limiter logic
- Session management

### Integration Tests
- Complete registration flow
- Login with valid credentials
- Login with invalid credentials
- Token refresh process
- Session expiration handling
- Rate limit enforcement

### Security Tests
- OWASP Top 10 vulnerabilities
- Penetration testing
- SQL injection attempts
- XSS attack vectors
- CSRF attack simulation

## Resources Needed
- bcrypt library documentation
- JWT specification (RFC 7519)
- OWASP authentication guidelines
- Redis session store setup
- Security audit checklist

## Success Metrics
- All acceptance criteria met
- All tests passing (>90% coverage)
- Security audit shows no critical issues
- Performance: <100ms login response time
- Documentation complete and reviewed
```

---

## Enforcement

**These rules are MANDATORY for all AI assistants working with this project.**

Before creating or modifying any task file:
1. ✅ Check this rules file
2. ✅ Verify YAML frontmatter present
3. ✅ Confirm all required fields included
4. ✅ Update TASKS.md with task entry
5. ✅ Validate no duplicate IDs

**If you're unsure about task format, refer to:**
- This rules file
- `.claude/skills/fstrent-task-management/SKILL.md`
- `.claude/skills/fstrent-task-management/rules.md`
- Example tasks in `.fstrent_spec_tasks/tasks/`

---

**Remember:** YAML frontmatter is REQUIRED. Without it, the task management system cannot process your tasks!
