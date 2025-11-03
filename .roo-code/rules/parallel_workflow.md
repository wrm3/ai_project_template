# Parallel Workflow Rules (Roo-Code)

For complete parallel workflow documentation, see: `.claude/rules/parallel_workflow_rules.md`

## Quick Reference

### When to Use Parallel Tasks
- Multiple independent features
- Separate subsystems/modules
- No shared dependencies
- Different team members

### SubAgents System
Roo-Code supports the SubAgents system for parallel execution:

**Available SubAgents:**
- backend-developer
- frontend-developer
- database-expert
- test-runner
- code-reviewer
- security-auditor
- devops-engineer
- technical-writer

### Parallel Task Example
```markdown
## Task 050: User Management System

### Sub-Tasks (Can run in parallel)
- Task 050.1: Database schema (database-expert)
- Task 050.2: API endpoints (backend-developer)
- Task 050.3: Frontend UI (frontend-developer)
- Task 050.4: Tests (test-runner)
```

### Coordination Points
Define synchronization points:
```markdown
## Phase 1: Parallel Development
- All sub-tasks run independently

## Phase 2: Integration (sync point)
- Merge all work
- Integration testing
- Fix conflicts

## Phase 3: Review (sync point)
- Code review
- Security audit
- Documentation review
```

### Conflict Prevention
- Clear module boundaries
- Separate files/directories
- Define interfaces upfront
- Regular synchronization

For complete parallel workflow rules, see `.claude/rules/parallel_workflow_rules.md`
