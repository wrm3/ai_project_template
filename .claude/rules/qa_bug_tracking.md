# QA - Bug Tracking and Documentation

## When to Use QA Skill

**Found a bug?** Document it properly before fixing.

**Invoke:** `fstrent-qa` skill
**Triggers:** "report bug", "document bug", "track issue", "quality assurance"

---

## Why Document Bugs?

**Common mistake:** Fix bugs immediately without documentation

**Consequences:**
- ❌ No record of what was broken
- ❌ Can't track patterns
- ❌ Might reoccur later
- ❌ No test case created
- ❌ Lost learning opportunity

**Better approach:**
- ✅ Document bug in BUGS.md
- ✅ Create task for fix
- ✅ Write test to prevent recurrence
- ✅ Track patterns and root causes

---

## Bug Documentation Location

**File:** `.fstrent_spec_tasks/BUGS.md`

**Format:**
```markdown
## Bug XXX: Brief Description

**Severity:** Critical|High|Medium|Low
**Status:** Open|In Progress|Fixed|Won't Fix
**Found:** YYYY-MM-DD
**Fixed:** YYYY-MM-DD (if fixed)

### Steps to Reproduce
1. Step one
2. Step two
3. Expected vs Actual

### Root Cause
Why did this happen?

### Fix
What was done to fix it?

### Prevention
How to prevent this in future?
```

---

## Bug Workflow

### 1. Discovery
- User reports issue OR developer finds bug

### 2. Documentation
- Add to BUGS.md with full details
- Assign severity level
- Document reproduction steps

### 3. Task Creation
- Create task in `.fstrent_spec_tasks/tasks/`
- Link to bug in BUGS.md
- Tag as `type: bug_fix`

### 4. Fix Implementation
- Implement fix
- Write test case
- Update task status

### 5. Closure
- Update BUGS.md status to "Fixed"
- Document fix and prevention
- Close related task

---

## When to Document

### ✅ Always Document
- Production bugs
- Bugs affecting users
- Recurring issues
- Complex bugs requiring investigation
- Security vulnerabilities

### ⚪ Optional Documentation
- Typos (just fix them)
- Obvious syntax errors
- One-line fixes in development

**Rule of Thumb:** If fix takes >30 minutes, document it.

---

## Integration with Tasks

**Bug → Task:**
```yaml
---
id: 105
title: 'Fix Login Timeout Issue'
type: bug_fix
status: in-progress
priority: high
project_context: 'Fixes Bug 012 in BUGS.md - login timeout after 5 minutes'
---
```

**Task → Bug:**
```markdown
## Bug 012: Login Timeout After 5 Minutes

**Related Task:** Task 105 (fix in progress)
**Severity:** High
**Status:** In Progress
```

---

## Full QA Workflow

**For complete QA guidance:**
- `.claude/skills/fstrent-qa/SKILL.md` - QA skill overview
- `.claude/skills/fstrent-qa/rules.md` - Detailed QA rules

**Skill provides:**
- Bug report templates
- Severity assessment guidelines
- Root cause analysis frameworks
- Test case creation patterns
- Quality metrics tracking
