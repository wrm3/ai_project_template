# Troubleshooting Guide

## Comprehensive troubleshooting for fstrent_spec_tasks system

This guide helps you diagnose and resolve common issues with the `fstrent_spec_tasks` system in both Claude Code and Cursor.

---

## Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Installation Issues](#installation-issues)
3. [Cursor-Specific Issues](#cursor-specific-issues)
4. [Claude Code-Specific Issues](#claude-code-specific-issues)
5. [Cross-IDE Issues](#cross-ide-issues)
6. [File System Issues](#file-system-issues)
7. [Git Workflow Issues](#git-workflow-issues)
8. [Performance Issues](#performance-issues)
9. [Advanced Troubleshooting](#advanced-troubleshooting)
10. [Getting Help](#getting-help)

---

## Quick Diagnostics

### Self-Check Procedure

Run through this quick checklist to identify common issues:

**Step 1: Verify Installation**
```bash
# Check if directories exist
ls -la .fstrent_spec_tasks/
ls -la .cursor/rules/fstrent_spec_tasks/  # If using Cursor
ls -la .claude/skills/                    # If using Claude Code

# Windows PowerShell
dir .fstrent_spec_tasks
dir .cursor\rules\fstrent_spec_tasks      # If using Cursor
dir .claude\skills                        # If using Claude Code
```

**Step 2: Check File Permissions**
```bash
# Unix/Mac
ls -la .fstrent_spec_tasks/TASKS.md

# Windows PowerShell
Get-Acl .fstrent_spec_tasks\TASKS.md | Format-List
```

**Step 3: Verify IDE Recognition**
- **Cursor**: Rules should appear in `.cursor/rules/`
- **Claude Code**: Skills should appear in Skills panel

**Step 4: Test Basic Operations**
- Can you read TASKS.md?
- Can you create a new task file?
- Can you update TASKS.md?

### Common Symptoms Quick Reference

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| IDE doesn't recognize system | Missing interface files | Reinstall interface |
| Can't create tasks | File permissions | Check permissions |
| Changes not appearing | Files not saved | Save and refresh |
| Git conflicts | Simultaneous edits | Resolve conflicts |
| Slow performance | Too many tasks | Archive old tasks |
| Commands not working | IDE needs restart | Restart IDE |

---

## Installation Issues

### Issue 1: Dependencies Not Installing

**Symptoms**:
- `pip install` fails
- Missing Python packages
- Import errors

**Diagnosis**:
```bash
# Check Python version
python --version  # Should be 3.11+

# Check pip
pip --version

# Try installing individually
pip install Flask
pip install Flask-SQLAlchemy
```

**Solutions**:

**Solution 1: Update pip**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Solution 2: Use virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate (Unix/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Solution 3: Check for conflicts**
```bash
# Clear pip cache
pip cache purge

# Reinstall
pip install -r requirements.txt --no-cache-dir
```

**Prevention**:
- Always use virtual environments
- Keep pip updated
- Pin dependency versions

---

### Issue 2: IDE Not Recognizing System

**Symptoms**:
- Rules/Skills not loading
- Commands not available
- AI doesn't know about system

**Diagnosis**:

**For Cursor**:
```bash
# Check if rules exist
ls .cursor/rules/fstrent_spec_tasks/

# Check rule files
ls .cursor/rules/fstrent_spec_tasks/rules/*.mdc
```

**For Claude Code**:
```bash
# Check if skills exist
ls .claude/skills/

# Check skill files
ls .claude/skills/fstrent-task-management/SKILL.md
```

**Solutions**:

**Solution 1: Reinstall Interface**

For Cursor:
```bash
# Use MCP tool
# In Cursor, run: fstrent_tasks_setup
```

For Claude Code:
```bash
# Copy from template or example
cp -r example-project/.claude .
cp -r example-project/.claude-plugin .
```

**Solution 2: Restart IDE**
- Close IDE completely
- Reopen project
- Wait for indexing to complete

**Solution 3: Check File Paths**
```bash
# Ensure you're in project root
pwd

# Check relative paths
ls -la | grep -E "(cursor|claude|fstrent)"
```

**Prevention**:
- Install both interfaces from start
- Commit interfaces to Git
- Document installation steps

---

### Issue 3: File Permission Errors

**Symptoms**:
- "Permission denied" errors
- Can't create/update files
- Can't write to directories

**Diagnosis**:
```bash
# Check permissions (Unix/Mac)
ls -la .fstrent_spec_tasks/

# Check ownership
ls -l .fstrent_spec_tasks/TASKS.md

# Windows PowerShell
Get-Acl .fstrent_spec_tasks | Format-List
```

**Solutions**:

**Solution 1: Fix Permissions (Unix/Mac)**
```bash
# Make directories writable
chmod -R u+w .fstrent_spec_tasks/

# Fix ownership
sudo chown -R $USER:$USER .fstrent_spec_tasks/
```

**Solution 2: Fix Permissions (Windows)**
```powershell
# Run PowerShell as Administrator
# Navigate to project directory
icacls .fstrent_spec_tasks /grant:r "$env:USERNAME:(OI)(CI)F" /T
```

**Solution 3: Check Disk Space**
```bash
# Unix/Mac
df -h .

# Windows PowerShell
Get-PSDrive C | Select-Object Used,Free
```

**Prevention**:
- Don't run IDE as root/admin
- Keep files owned by your user
- Ensure adequate disk space

---

### Issue 4: Path Issues (Windows)

**Symptoms**:
- "Path not found" errors
- Backslash vs forward slash issues
- Long path errors

**Diagnosis**:
```powershell
# Check path length
(Get-Location).Path.Length

# Check for special characters
Get-ChildItem .fstrent_spec_tasks -Recurse | Where-Object {$_.Name -match '[^\w\-\.]'}
```

**Solutions**:

**Solution 1: Enable Long Paths (Windows 10+)**
```powershell
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

**Solution 2: Use Shorter Path**
```powershell
# Move project closer to root
# Instead of: C:\Users\YourName\Documents\Projects\MyProject
# Use: C:\Projects\MyProject
```

**Solution 3: Use Forward Slashes in Code**
```python
# Good (works on all platforms)
path = "src/templates/index.html"

# Bad (Windows-specific)
path = "src\\templates\\index.html"
```

**Prevention**:
- Keep project paths short
- Avoid special characters in filenames
- Use `os.path.join()` in Python

---

## Cursor-Specific Issues

### Issue 1: Rules Not Loading

**Symptoms**:
- Cursor doesn't recognize system
- Commands don't work
- AI doesn't follow rules

**Diagnosis**:
```bash
# Check rules directory
ls -la .cursor/rules/fstrent_spec_tasks/

# Check rule files
cat .cursor/rules/fstrent_spec_tasks/rules/_index.mdc
```

**Solutions**:

**Solution 1: Restart Cursor**
1. Close all Cursor windows
2. Reopen project
3. Wait for indexing (bottom right status)

**Solution 2: Reload Rules**
1. Open Command Palette (Ctrl/Cmd + Shift + P)
2. Type "Reload Window"
3. Press Enter

**Solution 3: Reinstall Rules**
```bash
# Backup existing rules
mv .cursor .cursor.backup

# Reinstall using MCP tool
# In Cursor: Run fstrent_tasks_setup
```

**Prevention**:
- Commit `.cursor/` to Git
- Don't manually edit rule files
- Keep Cursor updated

---

### Issue 2: Commands Not Working

**Symptoms**:
- `/fstrent_spec_tasks_*` commands not recognized
- Commands do nothing
- Error messages

**Diagnosis**:
```bash
# Check command files
ls .cursor/rules/fstrent_spec_tasks/commands/

# Verify command syntax
cat .cursor/rules/fstrent_spec_tasks/commands/fstrent_spec_tasks_setup.md
```

**Solutions**:

**Solution 1: Use Correct Syntax**
```
# Correct
/fstrent_spec_tasks_setup

# Incorrect
fstrent_spec_tasks_setup
@fstrent_spec_tasks_setup
```

**Solution 2: Check Command Files**
```bash
# Ensure command files exist
ls .cursor/rules/fstrent_spec_tasks/commands/*.md

# Check file contents
head -20 .cursor/rules/fstrent_spec_tasks/commands/fstrent_spec_tasks_setup.md
```

**Solution 3: Restart and Retry**
1. Save all files
2. Restart Cursor
3. Try command again

**Prevention**:
- Learn correct command syntax
- Test commands after installation
- Keep command files in version control

---

### Issue 3: Cursor Performance Issues

**Symptoms**:
- Slow response time
- High CPU usage
- Freezing

**Diagnosis**:
```bash
# Check project size
du -sh .fstrent_spec_tasks/

# Count files
find .fstrent_spec_tasks -type f | wc -l

# Check for large files
find .fstrent_spec_tasks -type f -size +1M
```

**Solutions**:

**Solution 1: Archive Old Tasks**
```bash
# Create archive directory
mkdir -p .fstrent_spec_tasks/memory/

# Move old completed tasks
mv .fstrent_spec_tasks/tasks/task001_*.md .fstrent_spec_tasks/memory/
```

**Solution 2: Exclude Directories**
```json
// .cursor/settings.json
{
  "files.exclude": {
    "**/.fstrent_spec_tasks/memory": true
  }
}
```

**Solution 3: Disable Indexing for Large Files**
```json
// .cursor/settings.json
{
  "search.exclude": {
    "**/.fstrent_spec_tasks/memory": true,
    "**/node_modules": true
  }
}
```

**Prevention**:
- Archive tasks regularly
- Keep active task count <100
- Use `.cursorignore` for exclusions

---

## Claude Code-Specific Issues

### Issue 1: Skills Not Loading

**Symptoms**:
- Skills don't appear in Skills panel
- AI doesn't use skills
- Skill commands don't work

**Diagnosis**:
```bash
# Check skills directory
ls -la .claude/skills/

# Check skill files
cat .claude/skills/fstrent-task-management/SKILL.md | head -20
```

**Solutions**:

**Solution 1: Verify Skill Structure**
```bash
# Each skill should have SKILL.md
ls .claude/skills/*/SKILL.md

# Check YAML frontmatter
head -10 .claude/skills/fstrent-task-management/SKILL.md
```

**Solution 2: Restart Claude Code**
1. Close Claude Code
2. Clear cache (if option available)
3. Reopen project
4. Check Skills panel

**Solution 3: Reinstall Skills**
```bash
# Backup existing
mv .claude .claude.backup

# Copy from example
cp -r example-project/.claude .

# Restart Claude Code
```

**Prevention**:
- Commit `.claude/` to Git
- Don't modify SKILL.md frontmatter
- Keep Claude Code updated

---

### Issue 2: Commands Not Recognized

**Symptoms**:
- `/project:*` commands not working
- Commands not in autocomplete
- Error messages

**Diagnosis**:
```bash
# Check commands directory
ls .claude/commands/

# Verify command format
cat .claude/commands/new-task.md
```

**Solutions**:

**Solution 1: Use Correct Prefix**
```
# Correct
/project:new-task
/project:status

# Incorrect
/new-task
@project:new-task
```

**Solution 2: Check Command Files**
```bash
# Ensure commands exist
ls .claude/commands/*.md

# Check for $ARGUMENTS placeholder
grep -r "ARGUMENTS" .claude/commands/
```

**Solution 3: Reload Commands**
1. Open Command Palette
2. Type "Reload Commands" (if available)
3. Or restart Claude Code

**Prevention**:
- Learn command syntax
- Test commands after installation
- Keep commands in version control

---

### Issue 3: Agent Not Activating

**Symptoms**:
- `task-expander` agent not running
- Agent not appearing in suggestions
- Agent not working proactively

**Diagnosis**:
```bash
# Check agent file
cat .claude/agents/task-expander.md | head -20

# Verify YAML frontmatter
grep -A 5 "^---" .claude/agents/task-expander.md
```

**Solutions**:

**Solution 1: Check Agent Configuration**
```yaml
# Ensure frontmatter is correct
---
name: task-expander
description: Run test suite...
tools: Read, Edit, Write, Grep, Glob, Bash
---
```

**Solution 2: Explicitly Invoke Agent**
```
# In Claude Code chat
@task-expander Please analyze task 009 for complexity
```

**Solution 3: Check Tool Permissions**
- Ensure agent has required tool permissions
- Grant additional permissions if needed

**Prevention**:
- Don't modify agent frontmatter
- Test agents after installation
- Understand proactive vs explicit invocation

---

## Cross-IDE Issues

### Issue 1: Changes Not Appearing in Other IDE

**Symptoms**:
- Created task in Cursor, not in Claude Code
- Updated task in Claude Code, not in Cursor
- Files out of sync

**Diagnosis**:
```bash
# Check if files are saved
git status

# Check file timestamps
ls -lt .fstrent_spec_tasks/TASKS.md

# Check for unsaved changes
git diff .fstrent_spec_tasks/
```

**Solutions**:

**Solution 1: Save and Refresh**

In IDE where changes were made:
1. Save all files (Ctrl/Cmd + S)
2. Verify save (check file timestamp)

In other IDE:
1. Reload from disk (right-click file → Reload)
2. Or close and reopen file

**Solution 2: Sync via Git**
```bash
# In IDE where changes were made
git add .fstrent_spec_tasks/
git commit -m "Update tasks"
git push

# In other IDE
git pull
```

**Solution 3: Check File Watchers**
- Ensure IDE file watchers are enabled
- Check for file system notification issues
- Try manual refresh

**Prevention**:
- Save files explicitly
- Use Git for synchronization
- Enable auto-save in IDEs

---

### Issue 2: Different Behavior Between IDEs

**Symptoms**:
- Feature works in Cursor, not Claude Code
- Different output from same operation
- Inconsistent behavior

**Diagnosis**:
```bash
# Compare interface versions
git log .cursor/ .claude/

# Check for local modifications
git diff .cursor/
git diff .claude/
```

**Solutions**:

**Solution 1: Verify Core Feature**
- Check if it's a shared feature (tasks, plans, bugs)
- Or IDE-specific feature (commands, skills)

**Solution 2: Update Both Interfaces**
```bash
# Pull latest changes
git pull

# Ensure both interfaces are up-to-date
ls -lt .cursor/rules/fstrent_spec_tasks/
ls -lt .claude/skills/
```

**Solution 3: Report Bug**
- If core feature behaves differently, it's a bug
- Document exact steps to reproduce
- Report to maintainers

**Prevention**:
- Keep both interfaces updated
- Test in both IDEs before committing
- Understand IDE-specific vs shared features

---

### Issue 3: Git Merge Conflicts

**Symptoms**:
- Merge conflicts in TASKS.md
- Conflicts in task files
- Git refusing to merge

**Diagnosis**:
```bash
# Check for conflicts
git status

# View conflict markers
grep -n "<<<<<<" .fstrent_spec_tasks/TASKS.md
```

**Solutions**:

**Solution 1: Resolve TASKS.md Conflicts**
```bash
# Open TASKS.md in editor
# Find conflict markers:
<<<<<<< HEAD
- [ ] Task 042: Feature A
=======
- [ ] Task 042: Feature B
>>>>>>> feature-branch

# Resolve by merging both:
- [ ] Task 042: Feature A
- [ ] Task 043: Feature B

# Save and commit
git add .fstrent_spec_tasks/TASKS.md
git commit -m "Resolve task list conflict"
```

**Solution 2: Resolve Task File Conflicts**
```bash
# For different tasks, keep both
git add .fstrent_spec_tasks/tasks/task042_*.md
git add .fstrent_spec_tasks/tasks/task043_*.md

# For same task, choose one or merge manually
git checkout --ours .fstrent_spec_tasks/tasks/task042_*.md
# Or
git checkout --theirs .fstrent_spec_tasks/tasks/task042_*.md
```

**Solution 3: Use Merge Tool**
```bash
# Configure merge tool
git config --global merge.tool vscode

# Launch merge tool
git mergetool
```

**Prevention**:
- Pull before creating tasks
- Use feature branches
- Coordinate task IDs with team
- Commit and push frequently

---

## File System Issues

### Issue 1: Files Not Creating

**Symptoms**:
- New task files don't appear
- TASKS.md not updating
- "File not found" errors

**Diagnosis**:
```bash
# Check directory exists
ls -la .fstrent_spec_tasks/tasks/

# Check permissions
ls -ld .fstrent_spec_tasks/tasks/

# Check disk space
df -h .
```

**Solutions**:

**Solution 1: Create Missing Directories**
```bash
# Create tasks directory
mkdir -p .fstrent_spec_tasks/tasks/

# Create features directory
mkdir -p .fstrent_spec_tasks/features/

# Verify
ls -la .fstrent_spec_tasks/
```

**Solution 2: Fix Permissions**
```bash
# Unix/Mac
chmod -R u+w .fstrent_spec_tasks/

# Windows (PowerShell as Admin)
icacls .fstrent_spec_tasks /grant:r "$env:USERNAME:(OI)(CI)F" /T
```

**Solution 3: Check Disk Space**
```bash
# Free up space if needed
# Unix/Mac
df -h .

# Windows
Get-PSDrive C
```

**Prevention**:
- Ensure directories exist before operations
- Monitor disk space
- Keep adequate free space (>1GB)

---

### Issue 2: File Corruption

**Symptoms**:
- Files contain garbage characters
- YAML frontmatter broken
- Can't parse task files

**Diagnosis**:
```bash
# Check file encoding
file .fstrent_spec_tasks/TASKS.md

# Check for null bytes
grep -a '\x00' .fstrent_spec_tasks/TASKS.md

# Validate YAML
head -20 .fstrent_spec_tasks/tasks/task001_*.md
```

**Solutions**:

**Solution 1: Restore from Git**
```bash
# Check Git history
git log .fstrent_spec_tasks/TASKS.md

# Restore from last good commit
git checkout HEAD~1 .fstrent_spec_tasks/TASKS.md
```

**Solution 2: Fix Encoding**
```bash
# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 file.md > file_utf8.md
mv file_utf8.md file.md
```

**Solution 3: Manually Repair**
1. Open file in text editor
2. Fix YAML frontmatter
3. Remove invalid characters
4. Save with UTF-8 encoding

**Prevention**:
- Always use UTF-8 encoding
- Commit files frequently
- Use `.gitattributes` to enforce line endings

---

### Issue 3: Large File Problems

**Symptoms**:
- IDE slow with large files
- Git refuses to commit
- Out of memory errors

**Diagnosis**:
```bash
# Find large files
find .fstrent_spec_tasks -type f -size +1M -exec ls -lh {} \;

# Check file sizes
du -h .fstrent_spec_tasks/* | sort -h
```

**Solutions**:

**Solution 1: Split Large Files**
```bash
# Split TASKS.md by phase
# Create TASKS_PHASE1.md, TASKS_PHASE2.md, etc.

# Or archive old tasks
mkdir -p .fstrent_spec_tasks/memory/
mv .fstrent_spec_tasks/tasks/task0*.md .fstrent_spec_tasks/memory/
```

**Solution 2: Use Git LFS for Large Files**
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.db"
git lfs track "*.sqlite"

# Commit .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

**Solution 3: Exclude from IDE Indexing**
```json
// .cursor/settings.json or similar
{
  "files.exclude": {
    "**/*.db": true,
    "**/.fstrent_spec_tasks/memory": true
  }
}
```

**Prevention**:
- Archive old tasks regularly
- Keep active files <100KB
- Use Git LFS for databases
- Exclude large files from IDE indexing

---

## Git Workflow Issues

### Issue 1: Uncommitted Changes

**Symptoms**:
- Can't switch branches
- Can't pull updates
- Merge conflicts

**Diagnosis**:
```bash
# Check status
git status

# See what changed
git diff .fstrent_spec_tasks/
```

**Solutions**:

**Solution 1: Commit Changes**
```bash
# Add and commit
git add .fstrent_spec_tasks/
git commit -m "Update tasks"
```

**Solution 2: Stash Changes**
```bash
# Stash changes
git stash save "WIP: task updates"

# Do other work
git pull
git checkout other-branch

# Restore changes
git stash pop
```

**Solution 3: Discard Changes**
```bash
# Discard all changes (CAREFUL!)
git checkout -- .fstrent_spec_tasks/

# Or discard specific file
git checkout -- .fstrent_spec_tasks/TASKS.md
```

**Prevention**:
- Commit frequently
- Use descriptive commit messages
- Pull before starting work

---

### Issue 2: Detached HEAD State

**Symptoms**:
- "You are in 'detached HEAD' state"
- Commits not on any branch
- Lost work

**Diagnosis**:
```bash
# Check current state
git status

# See commit history
git log --oneline -10
```

**Solutions**:

**Solution 1: Create Branch from Detached HEAD**
```bash
# Create new branch
git checkout -b recovered-work

# Push to remote
git push -u origin recovered-work
```

**Solution 2: Return to Branch**
```bash
# If no changes to save
git checkout main

# If changes to save
git checkout -b temp-branch
git checkout main
git merge temp-branch
```

**Prevention**:
- Always work on branches
- Don't checkout specific commits
- Use `git switch` instead of `git checkout`

---

### Issue 3: Push Rejected

**Symptoms**:
- "Updates were rejected"
- "Non-fast-forward" error
- Can't push changes

**Diagnosis**:
```bash
# Check remote status
git fetch
git status

# See divergence
git log --oneline --graph --all
```

**Solutions**:

**Solution 1: Pull and Merge**
```bash
# Pull remote changes
git pull

# Resolve any conflicts
# Then push
git push
```

**Solution 2: Rebase**
```bash
# Rebase on remote
git pull --rebase

# Resolve conflicts if any
git rebase --continue

# Push
git push
```

**Solution 3: Force Push (CAREFUL!)**
```bash
# Only if you're sure
# And it's your personal branch
git push --force-with-lease
```

**Prevention**:
- Pull before pushing
- Communicate with team
- Use feature branches
- Never force push to main/master

---

## Performance Issues

### Issue 1: Slow IDE Response

**Symptoms**:
- IDE laggy or unresponsive
- High CPU usage
- Long wait times

**Diagnosis**:
```bash
# Check project size
du -sh .

# Count files
find . -type f | wc -l

# Check for large files
find . -type f -size +10M
```

**Solutions**:

**Solution 1: Archive Old Data**
```bash
# Archive old tasks
mkdir -p .fstrent_spec_tasks/memory/
mv .fstrent_spec_tasks/tasks/task00*.md .fstrent_spec_tasks/memory/

# Update TASKS.md to remove archived tasks
```

**Solution 2: Exclude Directories**
```bash
# Add to .gitignore
echo ".fstrent_spec_tasks/memory/" >> .gitignore

# Add to IDE exclude list
# .cursor/settings.json or similar
```

**Solution 3: Close Unused Files**
- Close all open files
- Restart IDE
- Only open files you need

**Prevention**:
- Archive regularly (monthly)
- Keep active tasks <100
- Use `.gitignore` and IDE excludes

---

### Issue 2: Memory Issues

**Symptoms**:
- "Out of memory" errors
- IDE crashes
- System slowdown

**Diagnosis**:
```bash
# Check memory usage (Unix/Mac)
top -o MEM

# Windows PowerShell
Get-Process | Sort-Object WS -Descending | Select-Object -First 10
```

**Solutions**:

**Solution 1: Increase IDE Memory**

For Cursor:
```json
// settings.json
{
  "window.memoryLimit": 4096
}
```

For Claude Code:
```json
// Similar setting if available
{
  "memory.limit": "4GB"
}
```

**Solution 2: Close Other Applications**
- Close unused browser tabs
- Close other IDEs
- Close memory-intensive apps

**Solution 3: Reduce Project Size**
```bash
# Remove node_modules if present
rm -rf node_modules/

# Remove build artifacts
rm -rf dist/ build/

# Archive old data
mv .fstrent_spec_tasks/memory/ ../archived/
```

**Prevention**:
- Monitor memory usage
- Close unused applications
- Archive old data regularly
- Use adequate RAM (8GB+ recommended)

---

### Issue 3: Database Performance

**Symptoms**:
- Slow queries
- Long load times
- Database locks

**Diagnosis**:
```bash
# Check database size
ls -lh *.db

# Check for locks
lsof *.db  # Unix/Mac

# Windows PowerShell
Get-Process | Where-Object {$_.Path -like "*python*"}
```

**Solutions**:

**Solution 1: Optimize Database**
```python
# In Python
import sqlite3
conn = sqlite3.connect('taskflow.db')
conn.execute('VACUUM')
conn.close()
```

**Solution 2: Add Indexes**
```python
# In app.py or migration script
db.create_index('idx_task_status', Task.status)
db.create_index('idx_task_priority', Task.priority)
```

**Solution 3: Archive Old Data**
```python
# Delete old completed tasks
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=90)
Task.query.filter(
    Task.status == 'completed',
    Task.updated_at < cutoff
).delete()
db.session.commit()
```

**Prevention**:
- Add indexes on frequently queried columns
- Archive old data regularly
- Use pagination for large result sets
- Close database connections properly

---

## Advanced Troubleshooting

### Diagnostic Tools

#### 1. System Check Script

Create `check_system.sh`:
```bash
#!/bin/bash

echo "=== fstrent_spec_tasks System Check ==="
echo ""

echo "1. Checking directories..."
[ -d .fstrent_spec_tasks ] && echo "✓ .fstrent_spec_tasks exists" || echo "✗ .fstrent_spec_tasks missing"
[ -d .cursor/rules/fstrent_spec_tasks ] && echo "✓ Cursor interface exists" || echo "✗ Cursor interface missing"
[ -d .claude/skills ] && echo "✓ Claude Code interface exists" || echo "✗ Claude Code interface missing"
echo ""

echo "2. Checking core files..."
[ -f .fstrent_spec_tasks/PLAN.md ] && echo "✓ PLAN.md exists" || echo "✗ PLAN.md missing"
[ -f .fstrent_spec_tasks/TASKS.md ] && echo "✓ TASKS.md exists" || echo "✗ TASKS.md missing"
[ -f .fstrent_spec_tasks/BUGS.md ] && echo "✓ BUGS.md exists" || echo "✗ BUGS.md missing"
echo ""

echo "3. Checking permissions..."
[ -w .fstrent_spec_tasks/TASKS.md ] && echo "✓ TASKS.md writable" || echo "✗ TASKS.md not writable"
echo ""

echo "4. Checking Git status..."
git status --short .fstrent_spec_tasks/
echo ""

echo "5. Counting tasks..."
echo "Task files: $(find .fstrent_spec_tasks/tasks -name '*.md' 2>/dev/null | wc -l)"
echo "Feature files: $(find .fstrent_spec_tasks/features -name '*.md' 2>/dev/null | wc -l)"
echo ""

echo "=== Check Complete ==="
```

Run with:
```bash
chmod +x check_system.sh
./check_system.sh
```

#### 2. Validate YAML Frontmatter

Create `validate_yaml.py`:
```python
#!/usr/bin/env python3
import yaml
import sys
from pathlib import Path

def validate_task_file(filepath):
    """Validate YAML frontmatter in task file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter
        if not content.startswith('---'):
            return False, "Missing frontmatter"
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Invalid frontmatter format"
        
        # Parse YAML
        frontmatter = yaml.safe_load(parts[1])
        
        # Check required fields
        required = ['id', 'title', 'status', 'priority']
        for field in required:
            if field not in frontmatter:
                return False, f"Missing required field: {field}"
        
        return True, "Valid"
    
    except Exception as e:
        return False, str(e)

# Check all task files
tasks_dir = Path('.fstrent_spec_tasks/tasks')
if not tasks_dir.exists():
    print("Tasks directory not found")
    sys.exit(1)

print("Validating task files...")
errors = []

for task_file in tasks_dir.glob('*.md'):
    valid, message = validate_task_file(task_file)
    if valid:
        print(f"✓ {task_file.name}")
    else:
        print(f"✗ {task_file.name}: {message}")
        errors.append((task_file.name, message))

if errors:
    print(f"\n{len(errors)} errors found")
    sys.exit(1)
else:
    print("\nAll task files valid")
    sys.exit(0)
```

Run with:
```bash
python validate_yaml.py
```

#### 3. Check File Encoding

```bash
# Check encoding of all markdown files
find .fstrent_spec_tasks -name '*.md' -exec file {} \;

# Should show: UTF-8 Unicode text
```

#### 4. Git History Analysis

```bash
# See recent changes to task system
git log --oneline --graph .fstrent_spec_tasks/ | head -20

# See who modified files
git log --format='%an' .fstrent_spec_tasks/ | sort | uniq -c

# Find when file was last modified
git log -1 --format='%ai' .fstrent_spec_tasks/TASKS.md
```

### Debug Mode

#### Enable Verbose Logging

For Flask app:
```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
app.config['DEBUG'] = True
```

For Git:
```bash
# Enable Git verbose mode
export GIT_TRACE=1
export GIT_CURL_VERBOSE=1

# Run Git command
git pull
```

### Log Analysis

#### Check IDE Logs

**Cursor**:
- Help → Toggle Developer Tools
- Console tab shows errors
- Look for red error messages

**Claude Code**:
- View → Output
- Select "Claude Code" from dropdown
- Look for error messages

#### Check System Logs

**Unix/Mac**:
```bash
# Check system logs
tail -f /var/log/system.log | grep -i error

# Check user logs
tail -f ~/Library/Logs/*.log
```

**Windows**:
```powershell
# Check Event Viewer
Get-EventLog -LogName Application -Newest 50 | Where-Object {$_.EntryType -eq "Error"}
```

---

## Getting Help

### Before Asking for Help

1. **Check this guide** - Most issues are covered here
2. **Search existing issues** - Someone may have had the same problem
3. **Try basic troubleshooting** - Restart, refresh, reinstall
4. **Gather information** - Error messages, steps to reproduce, system info

### Information to Include

When asking for help, provide:

1. **System Information**:
   ```bash
   # Operating system
   uname -a  # Unix/Mac
   systeminfo  # Windows
   
   # IDE version
   # Cursor: Help → About
   # Claude Code: Help → About
   
   # Python version
   python --version
   
   # Git version
   git --version
   ```

2. **Error Messages**:
   - Full error text
   - Stack traces
   - Console output

3. **Steps to Reproduce**:
   - What you did
   - What you expected
   - What actually happened

4. **Environment**:
   - Which IDE (Cursor, Claude Code, both)
   - Project size (number of tasks)
   - Recent changes

### Where to Get Help

1. **Documentation**:
   - [Claude Code Setup Guide](CLAUDE_CODE_SETUP_GUIDE.md)
   - [Cursor Compatibility Guide](CURSOR_COMPATIBILITY_GUIDE.md)
   - [Example Project](../example-project/)

2. **GitHub Issues**:
   - Search existing issues
   - Create new issue with template
   - Include all required information

3. **Community**:
   - Discord/Slack channel (if available)
   - Stack Overflow (tag: fstrent-spec-tasks)
   - Reddit (r/cursor, r/claudeai)

4. **Direct Support**:
   - Email: support@example.com
   - Response time: 1-2 business days

### Creating a Good Bug Report

```markdown
## Bug Report

### Description
[Clear description of the issue]

### Steps to Reproduce
1. [First step]
2. [Second step]
3. [Third step]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Environment
- OS: [e.g., Windows 11, macOS 14, Ubuntu 22.04]
- IDE: [Cursor 0.x.x / Claude Code 0.x.x]
- Python: [3.11.x]
- Git: [2.x.x]

### Error Messages
```
[Paste error messages here]
```

### Additional Context
[Any other relevant information]

### Attempted Solutions
[What you've tried already]
```

---

## Summary

### Most Common Issues

1. **IDE not recognizing system** → Restart IDE
2. **Files not syncing** → Save and refresh
3. **Git conflicts** → Pull before creating tasks
4. **Slow performance** → Archive old tasks
5. **Commands not working** → Check syntax, restart IDE

### Quick Fixes

- **Restart IDE** - Solves 50% of issues
- **Save and refresh** - Solves 30% of issues
- **Pull latest changes** - Solves 10% of issues
- **Check permissions** - Solves 5% of issues
- **Reinstall interface** - Solves remaining issues

### Prevention Tips

1. **Commit frequently** - Prevents data loss
2. **Pull before working** - Prevents conflicts
3. **Archive regularly** - Prevents performance issues
4. **Test in both IDEs** - Ensures compatibility
5. **Keep backups** - Enables recovery

### When in Doubt

1. Check this guide
2. Restart your IDE
3. Pull latest changes
4. Ask for help

---

**Remember**: Most issues have simple solutions. Don't hesitate to ask for help if you're stuck!

**Last Updated**: 2025-10-19  
**Version**: 1.0

