---
name: fstrent-qa
description: Track bugs, manage quality assurance, and document fixes in .fstrent_spec_tasks/ folder. Use when reporting bugs, tracking issues, documenting fixes, or managing quality processes. Triggers on requests mentioning bugs, issues, quality, fixes, or QA.
---

# fstrent Quality Assurance Skill

Track bugs, manage quality assurance processes, and document fixes using the fstrent_spec_tasks QA system. This Skill provides structured bug tracking that integrates with task management and feature documentation.

## System Overview

The fstrent_spec_tasks QA system uses:
- **BUGS.md**: `.fstrent_spec_tasks/BUGS.md` - Centralized bug tracking
- **Bug Tasks**: `.fstrent_spec_tasks/tasks/` - Bug fix task files
- **Task Integration**: Links to TASKS.md for bug resolution tracking
- **Feature Integration**: Links to features/ for impact assessment

## Bug Tracking System

### Bug Classification

**Severity Levels:**
- **Critical**: System crashes, data loss, security vulnerabilities
- **High**: Major feature failures, performance degradation >50%
- **Medium**: Minor feature issues, usability problems
- **Low**: Cosmetic issues, enhancement requests

**Source Attribution:**
- **User Reported**: Issues reported by end users or stakeholders
- **Development**: Bugs discovered during feature development
- **Testing**: Issues found during QA or automated testing
- **Production**: Live environment issues requiring immediate attention

### BUGS.md Structure

**Location**: `.fstrent_spec_tasks/BUGS.md`

**Format**:
```markdown
# Bug Tracking

## Active Bugs

### Bug ID: BUG-001
- **Title**: [Brief description of the issue]
- **Severity**: [Critical/High/Medium/Low]
- **Source**: [User Reported/Development/Testing/Production]
- **Feature Impact**: [List affected features]
- **Status**: [Open/Investigating/Fixing/Testing/Closed]
- **Task Reference**: [Link to task in TASKS.md]
- **Created**: [Date]
- **Assigned**: [Developer/Team]

### Bug ID: BUG-002
[Additional bugs...]

## Closed Bugs

### Bug ID: BUG-XXX
[Resolved bugs for reference...]
```

### Bug Entry Template

```markdown
### Bug ID: BUG-{number}
- **Title**: {Brief description}
- **Severity**: {Critical|High|Medium|Low}
- **Source**: {User Reported|Development|Testing|Production}
- **Feature Impact**: {affected features}
- **Status**: {Open|Investigating|Fixing|Testing|Closed}
- **Task Reference**: Task {id}
- **Created**: {date}
- **Assigned**: {developer}

**Description**:
{Detailed description of the issue}

**Reproduction Steps**:
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Expected Behavior**:
{What should happen}

**Actual Behavior**:
{What actually happens}

**Environment**:
- OS: {operating system}
- Version: {software version}
- Browser: {if applicable}
```

## Bug Task Integration

### When a Bug is Identified

**Process**:
1. Create BUGS.md entry with bug details
2. Create corresponding task in TASKS.md with `[BUG]` prefix
3. Create task file in tasks/ folder with bug_fix type
4. Link bug to affected features in feature documents
5. Track resolution through task completion

### Bug Task File Format

**Filename**: `task{id}_fix_{bug_description}.md`

**YAML Frontmatter**:
```yaml
---
id: {next_available_id}
title: '[BUG] {Brief description of the issue}'
type: bug_fix
status: pending
priority: {critical|high|medium|low}
feature: {affected_feature}
subsystems: {affected_subsystems}
project_context: 'Resolves {bug_type} affecting {system_component}, maintaining {expected_behavior}'
bug_reference: BUG-{number}
severity: {critical|high|medium|low}
source: {user_reported|development|testing|production}
reproduction_steps: '{step_by_step_instructions}'
expected_behavior: '{what_should_happen}'
actual_behavior: '{what_actually_happens}'
---

# Task {id}: [BUG] {Description}

## Objective
Fix {bug_type} that causes {problem}

## Bug Details
**Bug Reference**: BUG-{number}
**Severity**: {level}
**Source**: {source}

## Reproduction Steps
1. {Step 1}
2. {Step 2}
3. {Step 3}

## Expected vs Actual Behavior
**Expected**: {what_should_happen}
**Actual**: {what_actually_happens}

## Fix Implementation
{Technical approach to fix}

## Acceptance Criteria
- [ ] Bug can no longer be reproduced
- [ ] Fix doesn't introduce regressions
- [ ] Tests added to prevent recurrence
- [ ] Documentation updated if needed

## Testing Plan
- Test original reproduction steps
- Test related functionality
- Run regression tests
```

### Bug Lifecycle

1. **Discovery**: Bug identified and reported
2. **Documentation**: Entry created in BUGS.md
3. **Task Creation**: Bug fix task created
4. **Investigation**: Root cause analysis (Status: Investigating)
5. **Fix Implementation**: Solution developed (Status: Fixing)
6. **Testing**: Fix validated (Status: Testing)
7. **Closure**: Bug resolved (Status: Closed)

## Retroactive Fix Documentation

### Purpose
Capture and document fixes, improvements, and solutions completed in chat for historical context and memory preservation.

### When to Document

**Document as retroactive task if**:
- ✅ Fix required >15 minutes of work
- ✅ Solution affects multiple files or subsystems
- ✅ Fix provides value for future reference
- ✅ Resolution required technical analysis or debugging

**Skip documentation if**:
- ❌ Simple typo corrections
- ❌ Minor formatting adjustments
- ❌ Clarification-only conversations

### Retroactive Task Template

**Filename**: `task{id}_retroactive_{description}.md`

**YAML Frontmatter**:
```yaml
---
id: {next_available_id}
title: '[RETROACTIVE] {Description of fix/improvement}'
type: retroactive_fix
status: completed
priority: {original_urgency_level}
created_date: '{fix_completion_date}'
completed_date: '{fix_completion_date}'
project_context: 'Documents previously completed {solution_type} that addressed {project_need}, maintaining {system_capability}'
subsystems: {affected_subsystems}
estimated_effort: '{actual_time_spent}'
actual_effort: '{actual_time_spent}'
---

# Task {id}: [RETROACTIVE] {Description}

## Objective
Document {fix_type} that was completed in chat

## What Was Fixed
{Description of the problem that was solved}

## Solution Implemented
{Description of the solution}

## Files Changed
- {file1}
- {file2}

## Impact
{How this fix improves the system}

## Lessons Learned
{Insights for preventing similar issues}
```

### Retroactive Documentation Workflow

1. **Fix Assessment**: Review completed chat work against scope criteria
2. **Task Creation**: Generate task file using retroactive template
3. **System Integration**: Add entry to TASKS.md with completed status
4. **Archive**: Archive to memory if task meets archival criteria

## Quality Management

### Quality Metrics

**Bug Metrics**:
- **Bug Discovery Rate**: Bugs found per development cycle
- **Bug Resolution Time**: Average time from discovery to resolution
- **Bug Severity Distribution**: Breakdown by severity level
- **Feature Impact Analysis**: Which features are most affected
- **Regression Rate**: Percentage of fixes that introduce new bugs

**Quality Gates**:
- Code review required for all changes
- Testing requirements (unit, integration, manual)
- Documentation standards
- Performance benchmarks
- Security scanning

### Quality Workflows

**Bug Reporting Workflow**:
1. User reports issue
2. Assess severity and source
3. Create BUGS.md entry
4. Create bug fix task
5. Assign to developer
6. Track through resolution

**Fix Verification Workflow**:
1. Developer implements fix
2. Update task status to Testing
3. Verify fix resolves issue
4. Run regression tests
5. Update BUGS.md status to Closed
6. Mark task as completed

**Quality Review Workflow**:
1. Review bug metrics weekly
2. Identify patterns and trends
3. Address high-impact areas
4. Update quality processes
5. Document improvements

## Bug Operations

### Report New Bug

**Process**:
1. Gather bug information (title, severity, steps, expected/actual behavior)
2. Determine next bug ID (read BUGS.md)
3. Create bug entry in BUGS.md
4. Create bug fix task file
5. Update TASKS.md with bug fix task
6. Link to affected features

### Update Bug Status

**Process**:
1. Read bug entry from BUGS.md
2. Update Status field
3. Update corresponding task status
4. Add notes about progress
5. Update timestamps

**Status Transitions**:
- Open → Investigating: Analysis started
- Investigating → Fixing: Root cause found, fix in progress
- Fixing → Testing: Fix implemented, ready for testing
- Testing → Closed: Fix verified, bug resolved
- Any → Open: Issue reopened

### Close Bug

**Process**:
1. Verify fix resolves issue
2. Update BUGS.md status to Closed
3. Move bug to "Closed Bugs" section
4. Mark corresponding task as completed
5. Document resolution details

### View Bug Status

**Process**:
1. Read BUGS.md
2. Display active bugs by severity
3. Show bugs by status
4. Calculate bug metrics
5. Identify high-priority items

## Integration with Other Systems

### Link to Tasks
- Every bug creates a corresponding bug fix task
- Task completion closes the bug
- Task status reflects bug resolution progress

### Link to Features
- Bugs reference affected features
- Feature documents list related bugs
- Feature impact assessment through bug analysis

### Link to Project Context
- Bug patterns inform architecture decisions
- Quality metrics influence project planning
- Bug fixes align with project goals

## File Organization

### Core QA Files
- `.fstrent_spec_tasks/BUGS.md` - Bug tracking
- `.fstrent_spec_tasks/tasks/` - Bug fix task files
- `.fstrent_spec_tasks/features/` - Feature impact documentation

### Auto-Creation
Automatically create missing files:
- `.fstrent_spec_tasks/BUGS.md` with template if missing
- Bug fix task files as needed
- Update TASKS.md automatically

## Best Practices

### Bug Reporting
1. Clear, descriptive titles
2. Detailed reproduction steps
3. Expected vs actual behavior
4. Environment information
5. Screenshots or logs if helpful

### Bug Fixing
1. Understand root cause before fixing
2. Write tests to prevent recurrence
3. Consider edge cases
4. Document fix rationale
5. Verify no regressions

### Quality Management
1. Regular bug triage meetings
2. Track bug metrics over time
3. Address high-severity bugs first
4. Learn from bug patterns
5. Continuous process improvement

### Documentation
1. Document significant fixes retroactively
2. Capture lessons learned
3. Update feature documentation
4. Maintain bug history
5. Archive resolved bugs

## Common Workflows

### Workflow: Report Bug

**User**: "I found a bug - the login button doesn't work"

**Action**:
1. Ask clarifying questions:
   - What happens when you click the button?
   - What should happen?
   - What browser/OS are you using?
   - Can you reproduce it consistently?

2. Create BUGS.md entry:
```markdown
### Bug ID: BUG-001
- **Title**: Login button not responding to clicks
- **Severity**: High
- **Source**: User Reported
- **Feature Impact**: User Authentication
- **Status**: Open
- **Task Reference**: Task 015
- **Created**: 2025-10-19
- **Assigned**: TBD

**Description**:
Login button on main page does not respond when clicked. No error messages displayed.

**Reproduction Steps**:
1. Navigate to homepage
2. Click "Login" button
3. Nothing happens

**Expected Behavior**:
Login modal should appear

**Actual Behavior**:
Button click has no effect

**Environment**:
- OS: Windows 11
- Browser: Chrome 118
- Version: 1.2.0
```

3. Create bug fix task file
4. Update TASKS.md: `- [ ] Task 015: [BUG] Fix login button not responding`
5. Confirm: "Bug BUG-001 reported and task created"

### Workflow: Update Bug Status

**User**: "I'm investigating bug 001"

**Action**:
1. Read BUG-001 from BUGS.md
2. Update Status to "Investigating"
3. Update task015 status to "in-progress"
4. Update TASKS.md: `[🔄] Task 015: [BUG] Fix login button not responding`
5. Confirm: "Bug BUG-001 status updated to Investigating"

### Workflow: Close Bug

**User**: "Bug 001 is fixed"

**Action**:
1. Read BUG-001 from BUGS.md
2. Update Status to "Closed"
3. Move to "Closed Bugs" section
4. Update task015 status to "completed"
5. Update TASKS.md: `[✅] Task 015: [BUG] Fix login button not responding`
6. Confirm: "Bug BUG-001 closed. Great work!"

### Workflow: Document Retroactive Fix

**User**: "We just fixed the performance issue in chat"

**Action**:
1. Assess scope (affects multiple files, required debugging)
2. Create retroactive task file:
```yaml
---
id: 016
title: '[RETROACTIVE] Fixed database query performance issue'
type: retroactive_fix
status: completed
priority: high
created_date: '2025-10-19'
completed_date: '2025-10-19'
project_context: 'Documents performance optimization that reduced query time from 5s to 0.2s'
subsystems: [database, api]
estimated_effort: '2 hours'
actual_effort: '2 hours'
---
```

3. Update TASKS.md: `[✅] Task 016: [RETROACTIVE] Fixed database query performance issue`
4. Confirm: "Retroactive task created to document the fix"

## Examples

### Example: Report Critical Bug

**User**: "The app crashes when saving data"

**Action**:
1. Gather details through questions
2. Create BUGS.md entry:

```markdown
### Bug ID: BUG-002
- **Title**: Application crashes on data save
- **Severity**: Critical
- **Source**: Production
- **Feature Impact**: Data Persistence, User Experience
- **Status**: Open
- **Task Reference**: Task 017
- **Created**: 2025-10-19
- **Assigned**: Dev Team

**Description**:
Application crashes immediately when user attempts to save data. No error message shown, app just closes.

**Reproduction Steps**:
1. Open application
2. Make any changes to data
3. Click "Save" button
4. Application crashes

**Expected Behavior**:
Data should be saved successfully with confirmation message

**Actual Behavior**:
Application terminates unexpectedly

**Environment**:
- OS: Windows 11
- Version: 1.2.0
- Occurs on all machines tested
```

3. Create critical priority bug fix task
4. Confirm: "Critical bug BUG-002 reported. This should be addressed immediately."

### Example: View Bug Status

**User**: "Show me all open bugs"

**Action**:
1. Read BUGS.md
2. Filter by Status: Open, Investigating, Fixing, Testing
3. Display:

```
Active Bugs (3):

Critical (1):
- BUG-002: Application crashes on data save [Open]

High (1):
- BUG-001: Login button not responding [Investigating]

Medium (1):
- BUG-003: UI alignment issue on mobile [Fixing]

Total: 3 active bugs
```

## Compatibility Notes

This Skill works with the same file format used by Cursor's fstrent_spec_tasks QA system. Bugs and fixes created in Claude Code can be viewed and updated in Cursor, and vice versa. The system uses:

- Standard markdown format for BUGS.md
- Consistent YAML frontmatter for bug fix tasks
- Git-friendly plain text files
- Cross-IDE compatible workflows

Teams can use both IDEs interchangeably for quality assurance activities.

