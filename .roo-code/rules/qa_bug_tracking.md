# QA and Bug Tracking Rules (Roo-Code)

For complete QA documentation, see: `.claude/rules/qa_bug_tracking.md`

## Quick Reference

### Bug Reporting
Use `/report-bug` command to create structured bug reports.

### Bug File Structure
```yaml
---
id: BUG-042
title: 'Login fails with special characters'
severity: critical|high|medium|low
status: open|investigating|fixed|wont_fix
found_in: '1.2.0'
---

# Bug 042: Login Fails with Special Characters

## Description
Users cannot log in when password contains @ symbol.

## Steps to Reproduce
1. Create account with password: Test@123
2. Attempt to login
3. Error: "Invalid credentials"

## Expected Behavior
Login should succeed with valid credentials.

## Actual Behavior
Login fails, error returned.

## Environment
- Browser: Chrome 119
- OS: Windows 11
- Version: 1.2.0
```

### Bug Severity Levels
- **Critical** - System down, data loss, security breach
- **High** - Major feature broken, workaround exists
- **Medium** - Minor feature issue, low impact
- **Low** - Cosmetic issue, enhancement

### Bug Workflow
1. **Report** - Use `/report-bug` command
2. **Investigate** - Reproduce and analyze
3. **Fix** - Create task to resolve
4. **Test** - Verify fix works
5. **Close** - Update status to fixed

### Quality Reports
Use `/quality-report` command for:
- Bug statistics
- Test coverage metrics
- Code quality scores
- Technical debt assessment

For complete QA rules, see `.claude/rules/qa_bug_tracking.md`
