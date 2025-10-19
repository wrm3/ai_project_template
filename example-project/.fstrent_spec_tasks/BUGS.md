# TaskFlow - Bug Tracking

## Active Bugs

### Critical Bugs

#### BUG-001: Task deletion confirmation not showing
- **Severity**: Critical
- **Source**: User Reported
- **Feature Impact**: Task Management
- **Status**: Open
- **Task Reference**: Task 015
- **Created**: 2025-10-12
- **Assigned**: Development Team
- **Description**: Users can accidentally delete tasks without confirmation prompt
- **Impact**: High - Can lead to data loss
- **Workaround**: None
- **Priority**: Fix immediately

### High Priority Bugs

#### BUG-002: Priority filter not persisting across sessions
- **Severity**: High
- **Source**: Development
- **Feature Impact**: Task Filtering
- **Status**: Investigating
- **Task Reference**: TBD
- **Created**: 2025-10-13
- **Assigned**: Development Team
- **Description**: When user applies priority filter and closes browser, filter is not remembered on next visit
- **Impact**: Medium - Reduces user productivity
- **Workaround**: Reapply filter each session
- **Priority**: Fix in next sprint

### Medium Priority Bugs

#### BUG-003: Task due date display incorrect for different timezones
- **Severity**: Medium
- **Source**: Testing
- **Feature Impact**: Task Management, Due Dates
- **Status**: Open
- **Task Reference**: TBD
- **Created**: 2025-10-14
- **Assigned**: Unassigned
- **Description**: Due dates show in server timezone instead of user's local timezone
- **Impact**: Low-Medium - Confusing for users in different timezones
- **Workaround**: Manually calculate timezone difference
- **Priority**: Fix when time permits

## Resolved Bugs

### Recently Fixed

#### BUG-000: Flask app not starting on Windows
- **Severity**: Critical
- **Source**: Development
- **Feature Impact**: Application Startup
- **Status**: Closed
- **Task Reference**: Task 001
- **Created**: 2025-10-01
- **Resolved**: 2025-10-01
- **Assigned**: Development Team
- **Description**: Path separators causing issues on Windows
- **Resolution**: Updated path handling to use os.path.join()
- **Fix Verified**: Yes

## Bug Statistics

**Total Bugs**: 4  
**Active**: 3  
**Resolved**: 1

**By Severity**:
- Critical: 1 active
- High: 1 active
- Medium: 1 active
- Low: 0 active

**By Source**:
- User Reported: 1
- Development: 2
- Testing: 1
- Production: 0

**Average Resolution Time**: 0.5 days (based on 1 resolved bug)

## Bug Template

```yaml
---
id: BUG-{number}
title: '[BUG] {Brief description of the issue}'
severity: {critical|high|medium|low}
source: {user_reported|development|testing|production}
feature_impact: [affected_features]
status: {open|investigating|fixing|testing|closed}
task_reference: {task_id}
created_date: '{discovery_date}'
assigned_to: {developer}
---
```

## Bug Reporting Guidelines

### When to Report a Bug

- Application crashes or throws unhandled errors
- Feature doesn't work as specified in requirements
- Data loss or corruption occurs
- Security vulnerability discovered
- Performance degradation observed

### Bug Report Should Include

1. **Clear title** describing the issue
2. **Severity level** (critical/high/medium/low)
3. **Steps to reproduce** the issue
4. **Expected behavior** vs **actual behavior**
5. **Environment details** (browser, OS, etc.)
6. **Screenshots or error messages** if applicable
7. **Impact assessment** on users

### Severity Definitions

- **Critical**: System crashes, data loss, security issues, blocking users
- **High**: Major feature broken, significant impact on users
- **Medium**: Minor feature issues, workaround available
- **Low**: Cosmetic issues, minimal impact

## Bug Workflow

1. **Report** → Bug discovered and documented
2. **Triage** → Severity and priority assigned
3. **Investigate** → Root cause analysis
4. **Fix** → Solution implemented
5. **Test** → Fix verified
6. **Close** → Bug resolved and documented

