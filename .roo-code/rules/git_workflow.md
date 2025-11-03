# Git Workflow Rules (Roo-Code)

For complete git documentation, see: `.claude/rules/git_workflow.md`

## Quick Reference

### Branch Naming
```
feature/task-042-user-authentication
bugfix/bug-123-login-special-chars
hotfix/critical-security-patch
refactor/cleanup-auth-module
```

### Commit Message Format
```
Task 042: Implement user authentication

- Add password hashing with bcrypt
- Implement JWT token generation
- Create login endpoint
- Add rate limiting

Closes: #42
```

### Commit Guidelines
- **First line:** Brief summary (50 chars max)
- **Blank line**
- **Body:** Detailed explanation
- **Footer:** Issue references

### Pre-Commit Checklist
- [ ] All tests passing
- [ ] Code follows style guide
- [ ] No console.log() or debugging code
- [ ] Documentation updated
- [ ] Task file status updated

### Pull Request Process
1. Create feature branch from main
2. Make changes, commit frequently
3. Push to remote
4. Create PR with description
5. Request code review
6. Address feedback
7. Merge when approved

### Task File Commits
Always commit task files together:
```bash
git add .fstrent_spec_tasks/tasks/task042*.md
git add .fstrent_spec_tasks/TASKS.md
git commit -m "Task 042: Update status to completed"
```

For complete git rules, see `.claude/rules/git_workflow.md`
