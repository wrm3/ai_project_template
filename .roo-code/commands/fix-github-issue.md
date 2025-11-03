# Roo-Code Command: fix-github-issue

Link a task to a GitHub issue and begin work.

## Usage
```
/fix-github-issue #{issue_number}
```

## Example
```
/fix-github-issue #123
```

## Process
1. Fetches GitHub issue details
2. Creates or links to existing task
3. Adds GitHub reference to task metadata
4. Provides context and requirements
5. Suggests implementation approach

## Task Metadata Added
```yaml
---
github_issue: 123
github_url: 'https://github.com/user/repo/issues/123'
---
```

## Benefits
- Tracks GitHub issue → task relationship
- Automatic issue reference in commits
- Status synchronization
- Clear audit trail
