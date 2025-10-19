# Cursor Compatibility Guide

## Cross-IDE Collaboration with fstrent_spec_tasks

This guide explains how `fstrent_spec_tasks` achieves 100% compatibility between Claude Code and Cursor, enabling seamless workflows whether you work solo or in teams.

---

## Table of Contents

1. [Overview](#overview)
2. [How It Works](#how-it-works)
3. [Architecture](#architecture)
4. [Installation in Both IDEs](#installation-in-both-ides)
5. [Using Both IDEs](#using-both-ides)
6. [Team Collaboration](#team-collaboration)
7. [Feature Comparison](#feature-comparison)
8. [Best Practices](#best-practices)
9. [Common Scenarios](#common-scenarios)
10. [Troubleshooting](#troubleshooting)

---

## Overview

### What is Cross-IDE Compatibility?

`fstrent_spec_tasks` is designed to work seamlessly in **both Claude Code and Cursor** with:

- ✅ **100% shared data** - All tasks, plans, and bugs in one place
- ✅ **Zero duplication** - No need to maintain separate systems
- ✅ **No conflicts** - Both IDEs read/write the same files safely
- ✅ **Full feature parity** - Same capabilities in both IDEs
- ✅ **Team-ready** - Multiple developers, multiple IDEs, one system

### Why This Matters

**For Individuals**:
- Use the best IDE for each task
- Switch freely without losing context
- Learn new IDEs without abandoning your system
- Future-proof your workflow

**For Teams**:
- Developers choose their preferred IDE
- Everyone sees the same tasks and plans
- No "translation" between systems
- Git-based collaboration works perfectly

### The Key Insight

Instead of creating separate systems for each IDE, we use:

1. **Shared Data Layer**: IDE-agnostic markdown files (`.fstrent_spec_tasks/`)
2. **IDE-Specific Interfaces**: Each IDE has its own way to interact with the data
   - **Cursor**: Uses `.cursor/rules/` and commands
   - **Claude Code**: Uses `.claude/skills/`, `.claude/agents/`, `.claude/commands/`

**Result**: Both IDEs work with the same files, but each uses its native features.

---

## How It Works

### The Shared Directory

All project data lives in **`.fstrent_spec_tasks/`**:

```
.fstrent_spec_tasks/
├── PLAN.md                    # Product Requirements Document
├── TASKS.md                   # Master task checklist
├── BUGS.md                    # Bug tracking
├── PROJECT_CONTEXT.md         # Project mission and goals
├── SUBSYSTEMS.md              # Component registry
├── FILE_REGISTRY.md           # File documentation
├── MCP_TOOLS_INVENTORY.md     # Available tools
├── tasks/                     # Individual task files
│   ├── task001_example.md
│   └── task002_example.md
└── features/                  # Feature documentation
    ├── feature1.md
    └── feature2.md
```

**This directory is IDE-agnostic** - it contains only standard markdown files with YAML frontmatter. No IDE-specific syntax.

### IDE-Specific Interfaces

#### Cursor Interface

```
.cursor/
└── rules/
    └── fstrent_spec_tasks/
        ├── commands/          # Cursor commands
        │   ├── fstrent_spec_tasks_setup.md
        │   ├── fstrent_spec_tasks_plan.md
        │   ├── fstrent_spec_tasks_qa.md
        │   └── fstrent_spec_tasks_workflow.md
        └── rules/             # Cursor rules (.mdc files)
            ├── _index.mdc
            ├── rules.mdc
            ├── plans.mdc
            ├── qa.mdc
            └── workflow.mdc
```

**Purpose**: Tells Cursor's AI how to read/write the shared files.

#### Claude Code Interface

```
.claude/
├── skills/                    # Claude Code Skills
│   ├── fstrent-task-management/
│   │   ├── SKILL.md
│   │   ├── reference/
│   │   └── examples/
│   ├── fstrent-planning/
│   │   ├── SKILL.md
│   │   ├── reference/
│   │   └── examples/
│   └── fstrent-qa/
│       ├── SKILL.md
│       ├── reference/
│       └── examples/
├── agents/                    # Claude Code Agents
│   └── task-expander.md
└── commands/                  # Claude Code Commands
    ├── new-task.md
    ├── update-task.md
    ├── report-bug.md
    ├── start-planning.md
    ├── add-feature.md
    ├── quality-report.md
    └── status.md
```

**Purpose**: Tells Claude Code's AI how to read/write the shared files.

### The Magic

Both interfaces:
1. Read from the same `.fstrent_spec_tasks/` files
2. Write to the same `.fstrent_spec_tasks/` files
3. Use the same file formats (markdown + YAML)
4. Follow the same conventions (task IDs, status emojis, etc.)

**Result**: Perfect compatibility with zero conflicts.

---

## Architecture

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Git Repository                          │
│                                                             │
│  .fstrent_spec_tasks/  ← Shared by both IDEs              │
│  ├── PLAN.md                                               │
│  ├── TASKS.md                                              │
│  ├── BUGS.md                                               │
│  └── tasks/                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
                ┌──────────┴──────────┐
                │                     │
        ┌───────▼──────┐      ┌──────▼───────┐
        │   Cursor     │      │ Claude Code  │
        │              │      │              │
        │ .cursor/     │      │ .claude/     │
        │ └── rules/   │      │ ├── skills/  │
        │              │      │ ├── agents/  │
        │              │      │ └── commands/│
        └──────────────┘      └──────────────┘
```

### Key Principles

1. **Single Source of Truth**: `.fstrent_spec_tasks/` is the only place data lives
2. **IDE Interfaces**: Each IDE has its own "view" of the data
3. **No Translation**: IDEs read/write directly, no conversion needed
4. **Git-Friendly**: All files are text-based, merge-friendly
5. **Human-Readable**: You can edit files manually if needed

---

## Installation in Both IDEs

### Prerequisites

- Git repository initialized
- Either Cursor, Claude Code, or both installed

### Option 1: Install for Both IDEs (Recommended)

If you want maximum flexibility, install both interfaces:

#### Step 1: Install Cursor Interface

```bash
# In your project directory
# Use the fstrent_tasks MCP server
```

In Cursor, run the MCP tool:
```
fstrent_tasks_setup
```

This creates:
- `.fstrent_spec_tasks/` (shared data)
- `.cursor/rules/fstrent_spec_tasks/` (Cursor interface)

#### Step 2: Install Claude Code Interface

```bash
# In the same project directory
# Clone the Claude Code interface
git clone https://github.com/your-username/fstrent-spec-tasks-claude.git .claude-temp
cp -r .claude-temp/.claude .
cp -r .claude-temp/.claude-plugin .
rm -rf .claude-temp
```

Or manually create the `.claude/` structure following the [Claude Code Setup Guide](CLAUDE_CODE_SETUP_GUIDE.md).

#### Step 3: Verify Installation

Check that you have:
```
your-project/
├── .fstrent_spec_tasks/      ← Shared data
├── .cursor/                  ← Cursor interface
│   └── rules/
│       └── fstrent_spec_tasks/
└── .claude/                  ← Claude Code interface
    ├── skills/
    ├── agents/
    └── commands/
```

### Option 2: Install for One IDE Only

If you only use one IDE, install just that interface:

**For Cursor Only**:
- Run `fstrent_tasks_setup` MCP tool
- You get `.fstrent_spec_tasks/` and `.cursor/rules/`

**For Claude Code Only**:
- Follow the [Claude Code Setup Guide](CLAUDE_CODE_SETUP_GUIDE.md)
- You get `.fstrent_spec_tasks/` and `.claude/`

**Note**: You can always add the other IDE interface later without any data migration!

---

## Using Both IDEs

### Switching Between IDEs

You can switch freely between Cursor and Claude Code:

1. **Close one IDE**
2. **Open the other IDE** in the same project directory
3. **Continue working** - all your tasks, plans, and bugs are there

**No export/import needed!** Both IDEs see the same files.

### Concurrent Usage

You can even have **both IDEs open simultaneously** on the same project:

- ✅ **Safe**: Both IDEs read/write the same files
- ✅ **No conflicts**: Standard file locking prevents corruption
- ✅ **Real-time**: Changes appear after file refresh

**Best Practice**: If both are open, manually refresh files after making changes in one IDE.

### File Synchronization

#### Git-Based Sync (Recommended)

```bash
# After making changes in Cursor
git add .fstrent_spec_tasks/
git commit -m "Update tasks"
git push

# Switch to Claude Code
git pull
# Changes are now available
```

#### Local Sync (Same Machine)

If both IDEs are on the same machine:
- Changes are **instant** (same filesystem)
- Just refresh the file in the other IDE

#### Cloud Sync (Dropbox, OneDrive, etc.)

If your project is in a cloud-synced folder:
- Changes sync automatically
- Wait a few seconds for sync to complete
- Refresh files in the other IDE

---

## Team Collaboration

### Scenario 1: Team with Mixed IDEs

**Setup**:
- Developer A uses Cursor
- Developer B uses Claude Code
- Both work on the same Git repository

**Workflow**:

1. **Developer A (Cursor)**:
   ```bash
   # Create a new task
   # Cursor creates: .fstrent_spec_tasks/tasks/task042_new_feature.md
   # Cursor updates: .fstrent_spec_tasks/TASKS.md
   
   git add .fstrent_spec_tasks/
   git commit -m "Add task 042: New feature"
   git push
   ```

2. **Developer B (Claude Code)**:
   ```bash
   git pull
   # Claude Code reads: .fstrent_spec_tasks/tasks/task042_new_feature.md
   # Claude Code sees task in: .fstrent_spec_tasks/TASKS.md
   
   # Work on the task
   # Claude Code updates: .fstrent_spec_tasks/tasks/task042_new_feature.md
   # Claude Code updates status in: .fstrent_spec_tasks/TASKS.md
   
   git add .fstrent_spec_tasks/
   git commit -m "Complete task 042"
   git push
   ```

3. **Developer A (Cursor)**:
   ```bash
   git pull
   # Cursor sees the completed task
   # Cursor can archive it or create follow-up tasks
   ```

**Result**: Seamless collaboration with zero friction.

### Scenario 2: Code Review Across IDEs

**Setup**:
- Reviewer uses Cursor
- Developer uses Claude Code

**Workflow**:

1. **Developer (Claude Code)** creates a feature branch:
   ```bash
   git checkout -b feature/new-api
   # Work on tasks, update .fstrent_spec_tasks/
   git push origin feature/new-api
   ```

2. **Reviewer (Cursor)** checks out the branch:
   ```bash
   git checkout feature/new-api
   # Cursor reads all .fstrent_spec_tasks/ files
   # Reviewer can see tasks, plans, and context
   # Reviewer can add bug reports or feedback
   git push origin feature/new-api
   ```

3. **Developer (Claude Code)** sees feedback:
   ```bash
   git pull
   # Claude Code shows new bugs or comments
   # Developer addresses feedback
   ```

**Result**: Full context preserved across IDEs.

### Scenario 3: Pair Programming

**Setup**:
- Two developers, one screen
- One uses Cursor, other prefers Claude Code

**Workflow**:

1. **Screen sharing** with live coding
2. **Driver** uses their preferred IDE (e.g., Cursor)
3. **Navigator** follows along in their IDE (e.g., Claude Code)
4. **Switch roles** without switching IDEs
5. **Both see the same files** in real-time

**Result**: Each developer uses their preferred tool.

### Git Best Practices

#### What to Commit

**Always commit**:
- `.fstrent_spec_tasks/` (shared data)
- `.cursor/rules/` (Cursor interface)
- `.claude/` (Claude Code interface)

**Never commit**:
- IDE-specific temp files
- User-specific settings (unless team-wide)

#### Merge Conflicts

If you get merge conflicts in `.fstrent_spec_tasks/`:

1. **Task files** (`tasks/*.md`):
   - Usually no conflicts (different tasks)
   - If conflict: Keep both changes, renumber if needed

2. **TASKS.md**:
   - Most common conflict point
   - Resolve by merging both task lists
   - Keep task IDs unique

3. **PLAN.md**:
   - Rare conflicts
   - Resolve by discussing with team
   - Use feature branches for major changes

**Example Resolution**:

```markdown
# TASKS.md conflict
<<<<<<< HEAD
- [ ] Task 042: Feature A
=======
- [ ] Task 042: Feature B
>>>>>>> feature-branch

# Resolution: Renumber one task
- [ ] Task 042: Feature A
- [ ] Task 043: Feature B
```

---

## Feature Comparison

### What Works in Both IDEs

| Feature | Cursor | Claude Code | Notes |
|---------|--------|-------------|-------|
| **Task Management** | ✅ | ✅ | Full parity |
| **Planning (PRD)** | ✅ | ✅ | Full parity |
| **Bug Tracking** | ✅ | ✅ | Full parity |
| **Feature Docs** | ✅ | ✅ | Full parity |
| **Task Status** | ✅ | ✅ | Same emojis |
| **Sub-tasks** | ✅ | ✅ | Same format |
| **Dependencies** | ✅ | ✅ | Same syntax |
| **Quality Metrics** | ✅ | ✅ | Full parity |
| **File Registry** | ✅ | ✅ | Full parity |
| **MCP Tools** | ✅ | ✅ | Full parity |

### IDE-Specific Features

#### Cursor-Specific

| Feature | Description | Cross-IDE Impact |
|---------|-------------|------------------|
| **`.mdc` Rules** | Cursor's rule file format | None - only affects Cursor |
| **Rule Commands** | `/fstrent_spec_tasks_*` | None - Claude has equivalents |
| **Progressive Rules** | Multi-level rule disclosure | None - Claude uses Skills |

#### Claude Code-Specific

| Feature | Description | Cross-IDE Impact |
|---------|-------------|------------------|
| **Skills** | Self-contained packages | None - only affects Claude |
| **Subagents** | Specialized AI assistants | None - Cursor has rules |
| **Commands** | `/project:*` commands | None - Cursor has equivalents |
| **Progressive Disclosure** | Metadata → SKILL.md → Resources | None - Cursor has rules |

### Choosing the Right IDE

**Use Cursor if**:
- You prefer Cursor's UI/UX
- You're already invested in Cursor
- You like the rule-based approach
- You want MCP server integration (both support this)

**Use Claude Code if**:
- You prefer Claude Code's UI/UX
- You like the Skills/Agents model
- You want progressive disclosure
- You prefer command-based workflows

**Use Both if**:
- You want maximum flexibility
- You work in teams with mixed preferences
- You want to learn both tools
- You like having options

**The Truth**: It doesn't matter! Both work identically with your data.

---

## Best Practices

### 1. Commit Both Interfaces

Always commit both `.cursor/` and `.claude/` to Git:

```bash
git add .cursor/ .claude/ .fstrent_spec_tasks/
git commit -m "Update task system"
```

**Why**: Team members can use either IDE without setup.

### 2. Use Descriptive Commit Messages

```bash
# Good
git commit -m "Add task 042: Implement user authentication"
git commit -m "Complete task 038: Fix login bug"
git commit -m "Update PLAN.md: Add security requirements"

# Bad
git commit -m "Update tasks"
git commit -m "Changes"
```

**Why**: Clear history helps both IDEs and humans.

### 3. Keep Task IDs Unique

When creating tasks in parallel:

```bash
# Developer A creates task 042
# Developer B creates task 043 (not 042)
```

**Why**: Prevents merge conflicts.

**Tip**: Use a task ID registry or assign ranges to developers.

### 4. Sync Frequently

```bash
# Before starting work
git pull

# After completing a task
git add .fstrent_spec_tasks/
git commit -m "Complete task 042"
git push
```

**Why**: Reduces merge conflicts and keeps everyone in sync.

### 5. Use Feature Branches for Major Work

```bash
# For large features
git checkout -b feature/new-auth-system

# Work on multiple related tasks
# Commit frequently
# Merge when complete
```

**Why**: Isolates work and makes review easier.

### 6. Document IDE-Specific Workflows

If your team uses both IDEs, document common workflows:

```markdown
# TEAM_WORKFLOWS.md

## Creating a Task

### In Cursor
1. Run `/fstrent_spec_tasks_setup` if first time
2. Use Cursor's AI to create task file
3. Update TASKS.md

### In Claude Code
1. Run `/project:new-task` command
2. Or use `fstrent-task-management` Skill
3. Task file and TASKS.md updated automatically
```

**Why**: Reduces confusion and onboarding time.

### 7. Use Consistent Status Emojis

Both IDEs use the same emojis:

- `[ ]` - Pending
- `[🔄]` - In Progress
- `[✅]` - Completed
- `[❌]` - Failed/Cancelled

**Why**: Visual consistency across IDEs.

### 8. Keep `.fstrent_spec_tasks/` Clean

Don't put non-system files in `.fstrent_spec_tasks/`:

```bash
# Good
.fstrent_spec_tasks/
├── PLAN.md
├── TASKS.md
└── tasks/

# Bad
.fstrent_spec_tasks/
├── PLAN.md
├── TASKS.md
├── my_notes.txt        ← Don't do this
└── random_file.md      ← Don't do this
```

**Why**: Keeps the system focused and predictable.

---

## Common Scenarios

### Scenario 1: Starting a New Project

**Question**: Should I set up both IDEs from the start?

**Answer**: 

**If solo**: Set up your preferred IDE first. Add the other later if needed.

**If team**: Set up both from the start. This lets everyone choose their IDE.

**Steps**:
1. Initialize Git repository
2. Install Cursor interface (MCP tool)
3. Install Claude Code interface (manual or plugin)
4. Commit everything
5. Team members clone and start working

### Scenario 2: Migrating from Cursor to Claude Code

**Question**: I've been using Cursor. How do I add Claude Code support?

**Answer**:

1. **Your data is already compatible!** `.fstrent_spec_tasks/` works with both.
2. Just add the Claude Code interface:
   ```bash
   # Follow Claude Code Setup Guide
   # This adds .claude/ folder
   ```
3. Commit the new `.claude/` folder:
   ```bash
   git add .claude/
   git commit -m "Add Claude Code support"
   ```
4. Done! You can now use both IDEs.

**Data Migration**: **NONE NEEDED!** Your tasks, plans, and bugs work as-is.

### Scenario 3: Migrating from Claude Code to Cursor

**Question**: I've been using Claude Code. How do I add Cursor support?

**Answer**:

1. **Your data is already compatible!** `.fstrent_spec_tasks/` works with both.
2. Just add the Cursor interface:
   ```bash
   # In Cursor, run MCP tool
   fstrent_tasks_setup
   ```
3. Cursor creates `.cursor/rules/fstrent_spec_tasks/`
4. Commit the new `.cursor/` folder:
   ```bash
   git add .cursor/
   git commit -m "Add Cursor support"
   ```
5. Done! You can now use both IDEs.

**Data Migration**: **NONE NEEDED!** Your tasks, plans, and bugs work as-is.

### Scenario 4: Team Member Joins with Different IDE

**Question**: New team member prefers Claude Code, but we use Cursor. What do we do?

**Answer**:

**Nothing!** If you've committed both interfaces:

1. New member clones the repository
2. Opens in Claude Code
3. Starts working immediately

**If you only have Cursor interface**:

1. Add Claude Code interface (one time)
2. Commit to Git
3. New member pulls and starts working

**Result**: Zero friction for new team members.

### Scenario 5: Switching IDEs Mid-Project

**Question**: Can I switch IDEs in the middle of a project?

**Answer**:

**Yes, instantly!**

1. Close current IDE
2. Open other IDE in same directory
3. Continue working

**No export, no import, no conversion.** All your work is there.

### Scenario 6: Using Both IDEs Simultaneously

**Question**: Can I have both IDEs open at once?

**Answer**:

**Yes!** Both can be open on the same project:

1. Open Cursor in project directory
2. Open Claude Code in same project directory
3. Work in either IDE
4. Refresh files in the other IDE to see changes

**Use Case**: 
- Use Cursor for coding
- Use Claude Code for planning
- Switch based on task type

### Scenario 7: Resolving Merge Conflicts

**Question**: What if two people edit the same task file?

**Answer**:

**Rare, but possible:**

1. **Different tasks**: No conflict (different files)
2. **Same task**: Git merge conflict

**Resolution**:
```bash
# Open the conflicted file
# Merge both changes manually
# Or choose one version

git add .fstrent_spec_tasks/tasks/task042_example.md
git commit -m "Resolve task 042 conflict"
```

**Prevention**: 
- Assign tasks to specific developers
- Use feature branches
- Communicate about overlapping work

---

## Troubleshooting

### Issue 1: Changes Not Appearing in Other IDE

**Symptoms**: Made changes in Cursor, don't see them in Claude Code (or vice versa).

**Causes**:
1. Files not saved
2. Files not refreshed
3. Git not synced

**Solutions**:

1. **Save files** in the IDE where you made changes
2. **Refresh files** in the other IDE:
   - Cursor: Right-click file → Reload from Disk
   - Claude Code: File → Reload from Disk
3. **Sync via Git**:
   ```bash
   # In IDE where you made changes
   git add .fstrent_spec_tasks/
   git commit -m "Update tasks"
   git push
   
   # In other IDE
   git pull
   ```

### Issue 2: Task IDs Conflict

**Symptoms**: Two tasks with the same ID (e.g., both named `task042_*.md`).

**Causes**:
- Two developers created tasks simultaneously
- Merge conflict not resolved properly

**Solutions**:

1. **Renumber one task**:
   ```bash
   # Rename file
   mv task042_duplicate.md task043_duplicate.md
   
   # Update task ID in file
   # Change: id: 042
   # To:     id: 043
   
   # Update TASKS.md
   # Add entry for task 043
   ```

2. **Update references**:
   - Check for dependencies on the renumbered task
   - Update any references in other tasks

**Prevention**: 
- Assign task ID ranges to developers
- Sync frequently
- Use feature branches

### Issue 3: IDE Not Recognizing System

**Symptoms**: 
- Cursor: Rules not loading
- Claude Code: Skills not appearing

**Causes**:
1. Interface not installed
2. Files in wrong location
3. IDE needs restart

**Solutions**:

1. **Verify installation**:
   ```bash
   # Check for Cursor interface
   ls .cursor/rules/fstrent_spec_tasks/
   
   # Check for Claude Code interface
   ls .claude/skills/fstrent-task-management/
   ```

2. **Reinstall if missing**:
   - Cursor: Run `fstrent_tasks_setup` MCP tool
   - Claude Code: Follow setup guide

3. **Restart IDE**: Close and reopen the IDE

4. **Check file locations**: Ensure files are in correct directories

### Issue 4: Git Merge Conflicts in TASKS.md

**Symptoms**: Merge conflict in `.fstrent_spec_tasks/TASKS.md`.

**Causes**:
- Multiple developers adding tasks simultaneously

**Solutions**:

1. **Open TASKS.md** in a text editor
2. **Find conflict markers**:
   ```markdown
   <<<<<<< HEAD
   - [ ] Task 042: Feature A
   =======
   - [ ] Task 042: Feature B
   >>>>>>> feature-branch
   ```
3. **Merge both changes**:
   ```markdown
   - [ ] Task 042: Feature A
   - [ ] Task 043: Feature B
   ```
4. **Save and commit**:
   ```bash
   git add .fstrent_spec_tasks/TASKS.md
   git commit -m "Resolve TASKS.md conflict"
   ```

**Prevention**: 
- Pull before creating tasks
- Use feature branches
- Coordinate task creation

### Issue 5: Different Behavior Between IDEs

**Symptoms**: Feature works in Cursor but not Claude Code (or vice versa).

**Causes**:
1. Interface not updated
2. IDE-specific feature (not shared)
3. Bug in one interface

**Solutions**:

1. **Check versions**: Ensure both interfaces are up-to-date
2. **Verify it's a shared feature**: Check feature comparison table
3. **Report bug**: If it should work, report to maintainers

**Remember**: Core features (tasks, plans, bugs) work identically. Only IDE-specific features differ.

### Issue 6: Performance Issues with Large Projects

**Symptoms**: IDE slow when working with many tasks.

**Causes**:
- Too many active tasks
- Large task files
- Many files in `.fstrent_spec_tasks/`

**Solutions**:

1. **Archive completed tasks**:
   ```bash
   # Move old tasks to memory/
   mv .fstrent_spec_tasks/tasks/task001_*.md .fstrent_spec_tasks/memory/
   ```

2. **Split large files**:
   - Break TASKS.md into sections
   - Use feature-specific task lists

3. **Clean up old data**:
   - Archive old bugs
   - Remove obsolete features

**Prevention**: Regular maintenance and archival.

---

## Summary

### Key Takeaways

1. **100% Compatible**: Both IDEs work with the same files
2. **Zero Duplication**: One system, two interfaces
3. **Team-Ready**: Everyone can use their preferred IDE
4. **Git-Friendly**: Standard text files, easy merging
5. **Future-Proof**: Add more IDE support anytime

### Quick Reference

| Aspect | Cursor | Claude Code | Shared |
|--------|--------|-------------|--------|
| **Data Location** | `.fstrent_spec_tasks/` | `.fstrent_spec_tasks/` | ✅ |
| **Interface Location** | `.cursor/rules/` | `.claude/` | ❌ |
| **File Format** | Markdown + YAML | Markdown + YAML | ✅ |
| **Task Status** | `[ ]` `[🔄]` `[✅]` `[❌]` | `[ ]` `[🔄]` `[✅]` `[❌]` | ✅ |
| **Commands** | `/fstrent_spec_tasks_*` | `/project:*` | ❌ |
| **Core Features** | All | All | ✅ |

### Next Steps

1. **Install both interfaces** (if working in a team)
2. **Test switching** between IDEs
3. **Set up Git workflows** for your team
4. **Document team conventions** (optional)
5. **Start collaborating** with zero friction

### Resources

- [Claude Code Setup Guide](CLAUDE_CODE_SETUP_GUIDE.md) - Install Claude Code interface
- [Cursor Setup Guide](https://github.com/your-repo/cursor-setup) - Install Cursor interface
- [Example Project](../example-project/) - See both IDEs in action
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions

---

**Questions?** Check the [Troubleshooting](#troubleshooting) section or open an issue on GitHub.

**Ready to collaborate?** Both IDEs are waiting! 🚀

