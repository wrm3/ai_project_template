# Contributing to fstrent_spec_tasks Toolkit

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Pull Request Process](#pull-request-process)
5. [Coding Standards](#coding-standards)
6. [Documentation](#documentation)
7. [Issue Reporting](#issue-reporting)

---

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

**TL;DR**: Be respectful, inclusive, and professional.

---

## How Can I Contribute?

### Reporting Bugs

Found a bug? Please help us fix it!

1. **Check existing issues** - Someone may have already reported it
2. **Create a new issue** - Use the bug report template
3. **Provide details**:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment (OS, IDE, versions)
   - Error messages or screenshots

### Suggesting Enhancements

Have an idea for improvement?

1. **Check existing issues** - It may already be planned
2. **Create a feature request** - Use the feature request template
3. **Explain the use case** - Why is this needed?
4. **Describe the solution** - How should it work?

### Improving Documentation

Documentation improvements are always welcome!

- Fix typos or unclear explanations
- Add examples or use cases
- Improve setup instructions
- Translate documentation (future)

### Contributing Code

Ready to write code?

1. **Find an issue** - Look for "good first issue" or "help wanted" labels
2. **Comment on the issue** - Let others know you're working on it
3. **Fork the repository**
4. **Create a branch** - Use descriptive names (e.g., `fix-cursor-rules-loading`)
5. **Make your changes**
6. **Test thoroughly**
7. **Submit a pull request**

---

## Development Setup

### Prerequisites

- Git
- Python 3.11+ (for example project)
- Either Cursor or Claude Code (or both)
- Text editor for markdown files

### Setup Steps

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/fstrent-spec-tasks-toolkit.git
cd fstrent-spec-tasks-toolkit

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/fstrent-spec-tasks-toolkit.git

# 4. Create a branch
git checkout -b your-feature-branch

# 5. Make your changes
# Edit files...

# 6. Test your changes
# In Cursor: Open project, test rules
# In Claude Code: Open project, test skills

# 7. Commit your changes
git add .
git commit -m "Description of changes"

# 8. Push to your fork
git push origin your-feature-branch

# 9. Create pull request on GitHub
```

### Testing Your Changes

#### For Cursor Rules
```bash
# 1. Open project in Cursor
# 2. Verify rules load: Check .cursor/rules/
# 3. Test commands: Try /fstrent_spec_tasks_setup
# 4. Create test task: Verify file creation
# 5. Update TASKS.md: Verify updates work
```

#### For Claude Code Skills
```bash
# 1. Open project in Claude Code
# 2. Verify skills load: Check Skills panel
# 3. Test commands: Try /project:status
# 4. Create test task: Verify file creation
# 5. Test agent: Create complex task, verify expansion
```

#### For Example Project
```bash
cd example-project
pip install -r requirements.txt
python src/app.py
# Open http://localhost:5000
# Test all features
```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] Tests pass (if applicable)
- [ ] Documentation updated (if needed)
- [ ] Commit messages are clear
- [ ] Branch is up-to-date with main

### Submitting

1. **Create pull request** on GitHub
2. **Fill out the template** - Provide all requested information
3. **Link related issues** - Use "Fixes #123" or "Closes #456"
4. **Request review** - Tag maintainers if needed
5. **Respond to feedback** - Address review comments promptly

### PR Title Format

Use conventional commit format:

- `feat: Add new feature`
- `fix: Fix bug in Cursor rules`
- `docs: Update setup guide`
- `style: Format code`
- `refactor: Restructure task files`
- `test: Add tests`
- `chore: Update dependencies`

### PR Description Template

```markdown
## Description
[Clear description of changes]

## Motivation
[Why is this change needed?]

## Changes Made
- [Change 1]
- [Change 2]

## Testing
[How was this tested?]

## Screenshots (if applicable)
[Add screenshots]

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] Commit messages are clear
```

### Review Process

1. **Automated checks** - GitHub Actions run (if configured)
2. **Maintainer review** - Code review by maintainers
3. **Feedback** - Address any requested changes
4. **Approval** - PR approved by maintainer
5. **Merge** - PR merged to main branch

---

## Coding Standards

### General Principles

- **Clarity over cleverness** - Write code that's easy to understand
- **Consistency** - Follow existing patterns
- **Simplicity** - Keep it simple, avoid over-engineering
- **Documentation** - Comment complex logic

### Markdown Files

- Use **ATX-style headers** (`#` not underlines)
- **One sentence per line** for easier diffs
- **Consistent formatting** for lists and code blocks
- **Relative links** for internal references

### YAML Frontmatter

```yaml
---
id: 001
title: 'Task Title'
type: task
status: pending
priority: high
---
```

- **Required fields**: id, title, status, priority
- **Optional fields**: Add as needed
- **Consistent formatting**: Use same style throughout

### Python Code (Example Project)

- Follow **PEP 8** guidelines
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions **small and focused**

### File Naming

- **Lowercase with hyphens**: `feature-name.md`
- **Task files**: `task{id}_descriptive_name.md`
- **Feature files**: `feature-name.md`
- **No spaces**: Use hyphens or underscores

---

## Documentation

### What to Document

- **New features** - How to use them
- **API changes** - What changed and why
- **Breaking changes** - How to migrate
- **Examples** - Real-world usage
- **Troubleshooting** - Common issues

### Documentation Style

- **Clear and concise** - Get to the point
- **Examples** - Show, don't just tell
- **Step-by-step** - Break down complex processes
- **Screenshots** - Visual aids when helpful
- **Links** - Reference related documentation

### Where to Document

- **README.md** - Overview and quick start
- **docs/** - Detailed guides
- **Code comments** - Complex logic
- **CHANGELOG.md** - Version changes
- **Issue/PR** - Context for changes

---

## Issue Reporting

### Bug Reports

Use the bug report template and include:

1. **Description** - What's wrong?
2. **Steps to reproduce** - How to trigger the bug?
3. **Expected behavior** - What should happen?
4. **Actual behavior** - What actually happens?
5. **Environment**:
   - OS (Windows 11, macOS 14, Ubuntu 22.04)
   - IDE (Cursor 0.x.x, Claude Code 0.x.x)
   - Python version (if applicable)
6. **Error messages** - Full error text
7. **Screenshots** - If helpful

### Feature Requests

Use the feature request template and include:

1. **Problem** - What problem does this solve?
2. **Solution** - How should it work?
3. **Alternatives** - Other solutions considered?
4. **Use cases** - Who benefits and how?
5. **Examples** - Similar features elsewhere?

### Questions

For questions:

1. **Check documentation** - Answer may already exist
2. **Search issues** - Someone may have asked before
3. **Create discussion** - Use GitHub Discussions
4. **Be specific** - Provide context and details

---

## Recognition

Contributors will be:

- Listed in **CONTRIBUTORS.md** (if created)
- Mentioned in **release notes**
- Credited in **commit history**
- Thanked in **project updates**

---

## Getting Help

Need help contributing?

- **Documentation**: Check [docs/](docs/) folder
- **Discussions**: Use GitHub Discussions
- **Issues**: Ask in relevant issue
- **Discord**: Join our community (if available)

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Thank You!

Every contribution, no matter how small, makes this project better. Thank you for being part of the community!

**Questions?** Open an issue or start a discussion. We're here to help!

---

**Last Updated**: 2025-10-19

