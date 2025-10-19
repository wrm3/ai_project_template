# Quality Assurance Rules

> Detailed implementation rules for the fstrent-qa Skill.
> These rules are derived from Cursor's fstrent_spec_tasks system
> and maintain 100% cross-IDE compatibility.

## Overview

These rules provide comprehensive guidance for quality assurance using the fstrent_spec_tasks system. They cover bug tracking, severity classification, retroactive documentation, quality metrics, and integration with the task and planning systems.

## Bug Classification Rules

### Severity Levels

**Critical**:
- System crashes or becomes unusable
- Data loss or corruption
- Security vulnerabilities
- Complete feature failure affecting all users
- **Response Time**: Immediate (< 1 hour)
- **Priority**: Always highest

**High**:
- Major feature failures affecting many users
- Performance degradation > 50%
- Workaround exists but difficult
- Significant user impact
- **Response Time**: Same day (< 8 hours)
- **Priority**: High

**Medium**:
- Minor feature issues affecting some users
- Usability problems
- Easy workaround available
- Moderate user impact
- **Response Time**: Within week (< 5 days)
- **Priority**: Medium

**Low**:
- Cosmetic issues
- Enhancement requests
- Minor inconveniences
- Minimal user impact
- **Response Time**: Next sprint (< 2 weeks)
- **Priority**: Low

### Bug Source Attribution

**User Reported**:
- Issues reported by end users or stakeholders
- Often discovered in production
- May lack technical details
- Requires reproduction and analysis

**Development**:
- Bugs discovered during feature development
- Found by developers during coding
- Usually well-documented
- Can be fixed immediately

**Testing**:
- Issues found during QA or automated testing
- Discovered before production
- Systematic testing uncovered
- Detailed reproduction steps

**Production**:
- Live environment issues
- Affecting real users
- Requires immediate attention
- May need hotfix deployment

## Bug Tracking Rules

### BUGS.md File Format

**Location**: `.fstrent_spec_tasks/BUGS.md`

**Purpose**: Centralized bug tracking integrated with task system

**Structure**:
```markdown
# Bug Tracking

## Active Bugs

### Bug ID: BUG-001
- **Title**: [Brief description]
- **Severity**: [Critical/High/Medium/Low]
- **Source**: [User Reported/Development/Testing/Production]
- **Feature Impact**: [List affected features]
- **Status**: [Open/Investigating/Fixing/Testing/Closed]
- **Task Reference**: [Link to task in TASKS.md]
- **Created**: [Date]
- **Assigned**: [Developer/Team]

## Closed Bugs
[Archived resolved bugs]
```

### Bug ID Assignment

**Format**: `BUG-{number}`
- Sequential numbering (BUG-001, BUG-002, etc.)
- Zero-padded to 3 digits
- Never reuse IDs
- Separate from task IDs

**ID Determination**:
1. Read BUGS.md
2. Find highest bug number
3. New ID = max + 1

### Bug Status Lifecycle

**Status Flow**:
```
Open → Investigating → Fixing → Testing → Closed
                                      ↓
                                  Reopened → Investigating
```

**Status Definitions**:
- **Open**: Bug reported, not yet investigated
- **Investigating**: Root cause analysis in progress
- **Fixing**: Solution being implemented
- **Testing**: Fix being verified
- **Closed**: Bug resolved and verified
- **Reopened**: Bug reoccurred after closure

### Bug-Task Integration

**When Bug Identified**:
1. Create BUGS.md entry with bug details
2. Create corresponding task in TASKS.md with `[BUG]` prefix
3. Create task file in `tasks/` folder with bug type
4. Link bug to affected features in feature documents
5. Track resolution through task completion

**Bug Task YAML Template**:
```yaml
---
id: {next_available_id}
title: '[BUG] {Brief description of the issue}'
type: bug_fix
status: pending
priority: {severity_level}
feature: {affected_feature}
subsystems: {affected_subsystems}
project_context: 'Resolves {bug_type} affecting {system_component}'
bug_reference: BUG-{number}
severity: {critical|high|medium|low}
source: {user_reported|development|testing|production}
reproduction_steps: {step_by_step_instructions}
expected_behavior: {what_should_happen}
actual_behavior: {what_actually_happens}
---
```

**Synchronization Rules**:
- Bug status in BUGS.md = task status in TASKS.md
- Task completion → bug closure
- Task failure → bug reopened
- Keep both files in sync

## Retroactive Documentation Rules

### Purpose

Capture and document design fixes, bug resolutions, and improvements completed in chat for historical context and memory preservation.

### When to Document Retroactively

**Activation Points**:
- After completing any unplanned fix
- After solving unexpected problem
- After implementing improvement not in plan
- After debugging session

**Scope Assessment Criteria**:

**Document as retroactive task if**:
- ✅ Fix required > 15 minutes of work
- ✅ Solution affects multiple files or subsystems
- ✅ Fix provides value for future reference
- ✅ Resolution required technical analysis or debugging
- ✅ Solution not obvious or straightforward

**Skip documentation if**:
- ❌ Simple typo corrections
- ❌ Minor formatting adjustments
- ❌ Clarification-only conversations
- ❌ Trivial changes

### Retroactive Task Template

```yaml
---
id: {next_available_id}
title: '[RETROACTIVE] {Description of fix/improvement}'
type: retroactive_fix
status: completed
priority: {original_urgency_level}
created_date: '{fix_completion_date}'
completed_date: '{fix_completion_date}'
project_context: 'Documents previously completed {solution_type} that addressed {project_need}'
subsystems: {affected_subsystems}
estimated_effort: '{actual_time_spent}'
actual_effort: '{actual_time_spent}'
---
```

### Retroactive Documentation Workflow

1. **Fix Assessment**:
   - Review completed chat work
   - Apply scope criteria
   - Determine if documentation warranted

2. **Task Creation**:
   - Generate task file using retroactive template
   - Mark status as `completed`
   - Document actual effort

3. **System Integration**:
   - Add entry to TASKS.md with `[✅]` status
   - Link to affected features
   - Update subsystem documentation

4. **Archive**:
   - Archive to memory if appropriate
   - Add to completed tasks section
   - Document lessons learned

## Quality Metrics Rules

### Bug Discovery Rate

**Definition**: Number of bugs found per development cycle

**Calculation**:
```
Bug Discovery Rate = Total Bugs Found / Time Period
```

**Tracking**:
- Count new bugs in BUGS.md
- Group by time period (sprint, week, month)
- Track by source (user, development, testing)

**Interpretation**:
- Increasing rate → quality issues or more testing
- Decreasing rate → improving quality or less testing
- Stable rate → consistent quality level

### Bug Resolution Time

**Definition**: Average time from bug discovery to resolution

**Calculation**:
```
Resolution Time = (Closed Date - Created Date)
Average = Sum of Resolution Times / Number of Bugs
```

**Tracking**:
- Record created date in BUGS.md
- Record closed date when resolved
- Calculate per severity level
- Track trends over time

**Targets**:
- Critical: < 1 day
- High: < 3 days
- Medium: < 1 week
- Low: < 2 weeks

### Bug Severity Distribution

**Definition**: Breakdown of bugs by severity level

**Calculation**:
```
Distribution = Count per Severity / Total Bugs
```

**Tracking**:
- Count bugs by severity in BUGS.md
- Calculate percentages
- Track changes over time

**Healthy Distribution**:
- Critical: < 5%
- High: < 15%
- Medium: 30-40%
- Low: 40-50%

### Feature Impact Analysis

**Definition**: Which features are most affected by bugs

**Tracking**:
- Count bugs per feature
- Calculate bug density (bugs / feature size)
- Identify high-risk features

**Actions**:
- Focus testing on high-impact features
- Consider refactoring problematic features
- Improve documentation for complex features

### Regression Rate

**Definition**: Percentage of fixes that introduce new bugs

**Calculation**:
```
Regression Rate = (Bugs Caused by Fixes / Total Fixes) × 100%
```

**Tracking**:
- Tag bugs caused by previous fixes
- Calculate rate per time period
- Monitor trends

**Target**: < 10% regression rate

## Quality Gates Rules

### Code Review Gate

**Requirements**:
- All code changes require review
- Reviewer must be different from author
- Review checklist completed
- All comments addressed

**Review Checklist**:
- [ ] Code follows project standards
- [ ] Tests included and passing
- [ ] Documentation updated
- [ ] No obvious bugs or issues
- [ ] Performance acceptable
- [ ] Security considerations addressed

### Testing Requirements Gate

**Requirements**:
- Unit tests for new code
- Integration tests for new features
- Manual testing for UI changes
- Regression testing for bug fixes

**Test Coverage Targets**:
- Critical code: 90%+ coverage
- Core features: 80%+ coverage
- Utilities: 70%+ coverage
- Overall: 75%+ coverage

### Documentation Standards Gate

**Requirements**:
- Code comments for complex logic
- API documentation for public interfaces
- User guides for new features
- README updates for setup changes

**Documentation Checklist**:
- [ ] Code comments added
- [ ] API docs updated
- [ ] User guide updated
- [ ] README current

### Performance Benchmarks Gate

**Requirements**:
- Performance tests for critical paths
- Benchmark results documented
- No performance regressions
- Optimization opportunities identified

**Performance Targets**:
- API response time: < 200ms
- Page load time: < 2 seconds
- Database queries: < 100ms
- Background jobs: < 5 minutes

### Security Scanning Gate

**Requirements**:
- Automated security scans pass
- No critical vulnerabilities
- Dependencies up to date
- Security best practices followed

**Security Checklist**:
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Authentication/authorization correct
- [ ] Sensitive data encrypted
- [ ] Dependencies scanned

## Bug Lifecycle Workflow

### 1. Bug Discovery

**Actions**:
- User reports issue or bug found in testing
- Initial triage and severity assessment
- Assign bug ID

### 2. Bug Documentation

**Actions**:
- Create BUGS.md entry
- Document reproduction steps
- Identify affected features
- Assign severity and source

### 3. Task Creation

**Actions**:
- Create bug fix task in TASKS.md
- Create task file in tasks/ folder
- Link to bug in BUGS.md
- Assign to developer

### 4. Investigation

**Actions**:
- Update bug status to "Investigating"
- Root cause analysis
- Impact assessment
- Identify affected subsystems

### 5. Fix Implementation

**Actions**:
- Update bug status to "Fixing"
- Implement solution
- Write tests
- Update documentation

### 6. Verification

**Actions**:
- Update bug status to "Testing"
- Verify fix works
- Run regression tests
- Test in multiple environments

### 7. Documentation

**Actions**:
- Document fix in task file
- Update feature documentation
- Capture lessons learned
- Update quality metrics

### 8. Closure

**Actions**:
- Update bug status to "Closed"
- Mark task as completed
- Move to closed bugs section
- Archive if appropriate

## Integration with Cursor

These rules maintain 100% compatibility with Cursor's fstrent_spec_tasks system:

- **File Format**: Identical BUGS.md structure and bug task format
- **File Locations**: Same directory structure
- **Bug IDs**: Same numbering scheme
- **Status Flow**: Same lifecycle and transitions
- **Integration**: Same bug-task-feature relationships

**Cursor Rules Source**: `.cursor/rules/fstrent_spec_tasks/rules/qa.mdc`

## Cross-References

- **Main Skill**: `SKILL.md` - Complete skill documentation
- **Reference Materials**: `reference/` - Bug classification, metrics, retroactive docs
- **Examples**: `examples/` - Sample BUGS.md, bug entries, workflows
- **Task Management**: See `fstrent-task-management` Skill
- **Planning Integration**: See `fstrent-planning` Skill

## Usage Notes

### For Claude Code Users

Claude Code will use these rules automatically when the `fstrent-qa` Skill is triggered. The Skill is triggered by:
- User mentions "bug", "issue", "defect"
- User reports a problem
- User requests quality metrics
- User asks about testing or QA

### For Cursor Users

Cursor uses the equivalent rules from `.cursor/rules/fstrent_spec_tasks/rules/qa.mdc`. Both systems read and write the same `.fstrent_spec_tasks/` files, ensuring seamless collaboration.

### Best Practices

1. **Report bugs immediately**: Don't wait, document as soon as found
2. **Provide reproduction steps**: Clear steps help fix bugs faster
3. **Link to features**: Track feature quality over time
4. **Document retroactively**: Capture unplanned fixes
5. **Track metrics**: Monitor quality trends
6. **Use quality gates**: Prevent bugs from reaching production
7. **Learn from bugs**: Capture lessons to prevent recurrence

---

*These rules ensure consistent, comprehensive quality assurance across both Claude Code and Cursor environments.*

