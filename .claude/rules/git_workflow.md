# Git Workflow Standards

These standards apply to ALL git operations in this project.

---

## Commit Message Format

**Format:** `type(scope): description`

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons, etc.)
- **refactor**: Code refactoring (no functional changes)
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependencies, build config
- **perf**: Performance improvements

### Examples

```bash
feat(auth): add OAuth2 login support
fix(api): resolve null pointer in user endpoint
docs(readme): update installation instructions
refactor(database): simplify query builder logic
test(user): add integration tests for registration
chore(deps): update dependencies to latest versions
```

---

## Branching Strategy

### Branch Naming

**Format:** `type/short-description`

**Examples:**
```
feature/user-authentication
fix/login-button-crash
docs/api-documentation
refactor/database-layer
```

### Main Branches

- **main**: Production-ready code
- **develop**: Integration branch (if using GitFlow)

### Workflow

1. **Create branch from main:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit:**
   ```bash
   git add .
   git commit -m "feat(feature): add new functionality"
   ```

3. **Push to remote:**
   ```bash
   git push -u origin feature/your-feature-name
   ```

4. **Create Pull Request** via GitHub/GitLab/etc.

---

## Commit Best Practices

### DO

✅ **Write clear, concise commit messages**
```bash
git commit -m "fix(auth): resolve session timeout issue"
```

✅ **Commit logical units of work**
- One feature = one commit (or series of related commits)
- Don't mix unrelated changes

✅ **Use present tense**
- "add feature" not "added feature"
- "fix bug" not "fixed bug"

✅ **Reference issues when applicable**
```bash
git commit -m "fix(api): resolve timeout issue (#123)"
```

### DON'T

❌ **Vague messages**
```bash
git commit -m "fix stuff"  # Bad
git commit -m "updates"    # Bad
git commit -m "wip"        # Bad (except for temp branches)
```

❌ **Commit sensitive data**
- No passwords, API keys, secrets
- Use `.gitignore` for sensitive files
- Check `.env`, `credentials.json`, etc.

❌ **Commit large binary files**
- Use Git LFS for large files if necessary
- Keep repo size manageable

---

## Before Committing

### Pre-Commit Checklist

1. **Run tests:**
   ```bash
   # Project-specific test command
   npm test  # or pytest, or cargo test, etc.
   ```

2. **Check status:**
   ```bash
   git status  # Review what's staged
   git diff    # Review actual changes
   ```

3. **Verify no secrets:**
   ```bash
   # Check for common secret patterns
   git diff | grep -i "password\|api_key\|secret\|token"
   ```

4. **Update documentation** if needed

---

## Pull Request Guidelines

### PR Title Format

Same as commit message format:
```
feat(auth): add OAuth2 login support
```

### PR Description Template

```markdown
## Summary
[Brief description of what this PR does]

## Changes
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Related Issues
Closes #123
```

### Before Creating PR

1. ✅ Rebase on latest main:
   ```bash
   git checkout main
   git pull origin main
   git checkout your-branch
   git rebase main
   ```

2. ✅ Resolve any conflicts

3. ✅ Ensure all tests pass

4. ✅ Update documentation

5. ✅ Self-review your changes

---

## Git Hooks (Recommended)

### Pre-Commit Hook

Automatically run checks before commits:

**Location:** `.git/hooks/pre-commit`

```bash
#!/bin/bash

# Run tests
npm test || { echo "Tests failed. Commit aborted."; exit 1; }

# Check for secrets
if git diff --cached | grep -i "password\|api_key\|secret\|token"; then
    echo "Warning: Possible secret detected. Review changes."
    exit 1
fi

echo "Pre-commit checks passed!"
```

---

## Common Git Commands

### Essential Operations

```bash
# Check status
git status

# Stage changes
git add .                    # All changes
git add file.txt             # Specific file
git add *.js                 # Pattern

# Commit
git commit -m "type(scope): description"

# Push
git push origin branch-name

# Pull latest
git pull origin main

# Create branch
git checkout -b feature/name

# Switch branches
git checkout branch-name

# View history
git log --oneline --graph --all
```

### Undoing Changes

```bash
# Unstage file
git reset HEAD file.txt

# Discard changes (careful!)
git checkout -- file.txt

# Amend last commit (if not pushed)
git commit --amend

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1  # DANGEROUS!
```

---

## .gitignore Essentials

**Always ignore:**

```gitignore
# Dependencies
node_modules/
.venv/
venv/
__pycache__/

# Environment files
.env
.env.local
*.env

# IDE files
.vscode/
.idea/
*.swp

# Build outputs
dist/
build/
*.pyc
*.pyo

# Logs
*.log
logs/

# OS files
.DS_Store
Thumbs.db

# Secrets
credentials.json
secrets/
*.key
*.pem
```

---

## Collaborative Workflow

### When Working on Team Projects

1. **Pull before starting work:**
   ```bash
   git pull origin main
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Commit regularly:**
   - Small, logical commits
   - Clear commit messages

4. **Stay updated with main:**
   ```bash
   git fetch origin
   git rebase origin/main  # Or merge if preferred
   ```

5. **Create PR when ready:**
   - Request reviews
   - Address feedback
   - Ensure CI passes

6. **Merge and clean up:**
   ```bash
   # After merge
   git checkout main
   git pull origin main
   git branch -d feature/your-feature
   ```

---

## Emergency Procedures

### Accidentally Committed Secrets

**Immediate action:**

```bash
# Remove file from last commit
git rm --cached secrets.txt
git commit --amend

# If already pushed - force push (DANGEROUS, coordinate with team)
git push --force origin branch-name

# Rotate all exposed credentials immediately!
```

**Better:** Use `git-secrets` or similar tools to prevent this.

### Broken Main Branch

1. Don't panic
2. Identify breaking commit
3. Revert or fix forward
4. Communicate with team

```bash
# Revert commit
git revert <commit-hash>
git push origin main
```

---

**Remember:** Good git hygiene prevents headaches. Commit early, commit often, commit clearly.
