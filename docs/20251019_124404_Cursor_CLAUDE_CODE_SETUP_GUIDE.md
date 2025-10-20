# Claude Code Setup Guide - fstrent_spec_tasks

## 🚀 Quick Start (5 Minutes)

Get up and running with `fstrent_spec_tasks` in 5 minutes:

```bash
# 1. Navigate to your project
cd your-project

# 2. Copy the .claude folder to your project
# (This contains Skills, Commands, and Agent)

# 3. Initialize the system
# Create .fstrent_spec_tasks directory
mkdir .fstrent_spec_tasks

# 4. Start Claude Code
claude

# 5. Try your first command
> /project:status
```

**That's it!** You're ready to use the system. Continue reading for detailed setup and usage.

---

## 📋 Table of Contents

1. [What You're Getting](#what-youre-getting)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [First Steps](#first-steps)
6. [Common Workflows](#common-workflows)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

---

## 🎯 What You're Getting

`fstrent_spec_tasks` is a comprehensive task management, project planning, and QA system for Claude Code (and Cursor).

### Features

**3 Comprehensive Skills**:
- **fstrent-task-management**: Create, track, and manage tasks with sub-tasks
- **fstrent-planning**: Create PRDs, features, and project plans
- **fstrent-qa**: Track bugs, generate quality metrics

**7 Custom Commands**:
- `/project:new-task` - Create new task
- `/project:update-task` - Update task status
- `/project:report-bug` - Report bug
- `/project:start-planning` - Start project planning
- `/project:add-feature` - Add feature document
- `/project:quality-report` - Generate quality report
- `/project:status` - Project status overview

**1 Intelligent Agent**:
- **task-expander**: Automatically assesses complexity and expands complex tasks into sub-tasks

**Key Benefits**:
- ✅ 100% compatible with Cursor
- ✅ Shared files between both IDEs
- ✅ Comprehensive documentation (~68,500 words)
- ✅ Working examples and templates
- ✅ Production-ready and tested

---

## ✅ Prerequisites

### Required
- **Claude Code** (latest version)
- **Git** (for version control)
- **Text editor** (for viewing files)

### Recommended
- **Cursor** (for cross-IDE compatibility)
- **GitHub account** (for collaboration)

### System Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux
- **Disk Space**: ~10 MB
- **Memory**: Minimal (< 50 MB)

---

## 📦 Installation

### Method 1: Manual Installation (Recommended for Learning)

1. **Create Project Structure**
   ```bash
   cd your-project
   
   # Create Claude Code directory
   mkdir -p .claude/skills .claude/commands .claude/agents
   
   # Create fstrent_spec_tasks directory
   mkdir -p .fstrent_spec_tasks/tasks .fstrent_spec_tasks/features
   ```

2. **Copy Skills**
   ```bash
   # Copy the three Skills folders:
   # - .claude/skills/fstrent-task-management/
   # - .claude/skills/fstrent-planning/
   # - .claude/skills/fstrent-qa/
   ```

3. **Copy Commands**
   ```bash
   # Copy all 7 command files:
   # - .claude/commands/new-task.md
   # - .claude/commands/update-task.md
   # - .claude/commands/report-bug.md
   # - .claude/commands/start-planning.md
   # - .claude/commands/add-feature.md
   # - .claude/commands/quality-report.md
   # - .claude/commands/status.md
   ```

4. **Copy Agent**
   ```bash
   # Copy the agent file:
   # - .claude/agents/task-expander.md
   ```

5. **Create Core Files**
   ```bash
   # Create empty core files
   touch .fstrent_spec_tasks/PLAN.md
   touch .fstrent_spec_tasks/TASKS.md
   touch .fstrent_spec_tasks/BUGS.md
   touch .fstrent_spec_tasks/PROJECT_CONTEXT.md
   ```

6. **Verify Installation**
   ```bash
   # Check directory structure
   ls -la .claude/
   ls -la .fstrent_spec_tasks/
   ```

### Method 2: Git Clone (Fastest)

```bash
# Clone the repository
git clone https://github.com/fstrent/fstrent-spec-tasks.git

# Copy to your project
cp -r fstrent-spec-tasks/.claude your-project/
cp -r fstrent-spec-tasks/.fstrent_spec_tasks your-project/

# Clean up
rm -rf fstrent-spec-tasks
```

### Method 3: Plugin Installation (Future)

```bash
# When available as plugin
/plugin marketplace add fstrent/claude-plugins
/plugin install fstrent-spec-tasks@fstrent
```

---

## ⚙️ Configuration

### Basic Configuration (Required)

1. **Initialize TASKS.md**
   
   Create `.fstrent_spec_tasks/TASKS.md`:
   ```markdown
   # Project Tasks
   
   ## Active Tasks
   
   ### Phase 1: Initial Setup
   - [ ] Task 001: Setup project structure
   
   ---
   **Legend:**
   - `[ ]` - Pending
   - `[🔄]` - In Progress
   - `[✅]` - Completed
   - `[❌]` - Failed/Blocked
   ```

2. **Initialize PROJECT_CONTEXT.md**
   
   Create `.fstrent_spec_tasks/PROJECT_CONTEXT.md`:
   ```markdown
   # Project Context
   
   ## Mission
   [Your project's mission statement]
   
   ## Current Phase
   Phase 1: Initial Setup
   
   ## Success Criteria
   - [ ] Criterion 1
   - [ ] Criterion 2
   ```

3. **Start Claude Code**
   ```bash
   cd your-project
   claude
   ```

### Optional Configuration

#### 1. Git Integration

Add to `.gitignore`:
```gitignore
# Keep fstrent_spec_tasks files
# .fstrent_spec_tasks/

# Keep Claude Code config
# .claude/

# Ignore temporary files
.fstrent_spec_tasks/memory/
```

#### 2. Team Configuration

For teams, commit `.claude/` and `.fstrent_spec_tasks/` to Git:
```bash
git add .claude/
git add .fstrent_spec_tasks/
git commit -m "Add fstrent_spec_tasks system"
git push
```

#### 3. Personal Preferences

Create `.claude/settings.json` (optional):
```json
{
  "fstrent_spec_tasks": {
    "auto_archive": true,
    "default_priority": "medium",
    "emoji_style": "windows-safe"
  }
}
```

---

## 🎓 First Steps

### Step 1: Verify Installation

```bash
# In Claude Code:
> What skills are available?
```

**Expected Response**: Claude should list the three fstrent_spec_tasks Skills.

### Step 2: Check Status

```bash
> /project:status
```

**Expected Response**: Project status overview showing your tasks, bugs, and features.

### Step 3: Create Your First Task

```bash
> /project:new-task Setup development environment
```

**What Happens**:
1. Claude prompts for task details
2. Task file created in `.fstrent_spec_tasks/tasks/`
3. TASKS.md updated
4. Task is ready to track

### Step 4: Start Project Planning (Optional)

```bash
> /project:start-planning My Awesome Project
```

**What Happens**:
1. Claude asks scope validation questions
2. PLAN.md created with PRD structure
3. PROJECT_CONTEXT.md updated
4. Ready for feature planning

### Step 5: Explore Commands

Try each command:
```bash
> /project:new-task [description]
> /project:update-task [task-id]
> /project:report-bug [description]
> /project:add-feature [feature-name]
> /project:quality-report
> /project:status
```

---

## 🔄 Common Workflows

### Workflow 1: Daily Development

**Morning**:
```bash
# Check status
> /project:status

# Start working on a task
> /project:update-task Task 001 to in-progress
```

**During Development**:
```bash
# Report bugs as you find them
> /project:report-bug Login button not responding

# Create new tasks as needed
> /project:new-task Add error handling to API
```

**End of Day**:
```bash
# Update completed tasks
> /project:update-task Task 001 to completed

# Check status
> /project:status
```

### Workflow 2: Starting a New Feature

```bash
# 1. Plan the feature
> /project:add-feature User Authentication

# 2. Create implementation task
> /project:new-task Implement user authentication

# 3. Agent expands complex task (automatic)
# Claude: "This task is complex (score: 8/10). Shall I expand it?"
> Yes

# 4. Work through sub-tasks
> /project:update-task Task 002.1 to in-progress
> /project:update-task Task 002.1 to completed
> /project:update-task Task 002.2 to in-progress
```

### Workflow 3: Bug Management

```bash
# 1. Report bug
> /project:report-bug Cart total calculation incorrect

# 2. Bug entry created in BUGS.md
# 3. Bug fix task created automatically

# 4. Work on bug fix
> /project:update-task Task 003 to in-progress

# 5. Complete and close
> /project:update-task Task 003 to completed
# Bug automatically marked as closed
```

### Workflow 4: Quality Review

```bash
# 1. Generate quality report
> /project:quality-report weekly

# 2. Review metrics and trends

# 3. Create improvement tasks
> /project:new-task Improve test coverage in auth module

# 4. Track improvements
> /project:status
```

---

## 🐛 Troubleshooting

### Skills Not Loading

**Problem**: Skills don't appear or activate

**Solutions**:
1. Check file structure:
   ```bash
   ls -la .claude/skills/
   # Should show: fstrent-task-management, fstrent-planning, fstrent-qa
   ```

2. Verify SKILL.md files exist:
   ```bash
   ls .claude/skills/*/SKILL.md
   ```

3. Check YAML frontmatter syntax in SKILL.md files

4. Restart Claude Code:
   ```bash
   exit
   claude
   ```

### Commands Not Working

**Problem**: `/project:` commands don't activate

**Solutions**:
1. Check command files exist:
   ```bash
   ls .claude/commands/
   ```

2. Verify command file format (must be .md)

3. Try typing full command:
   ```bash
   /project:status
   ```

4. Restart Claude Code

### Agent Not Activating

**Problem**: Task-expander agent doesn't assess complexity

**Solutions**:
1. Check agent file exists:
   ```bash
   ls .claude/agents/task-expander.md
   ```

2. Verify YAML frontmatter in agent file

3. Try explicit activation:
   ```bash
   > Expand this task
   ```

4. Check task description mentions complexity indicators

### Files Not Creating

**Problem**: Commands don't create files

**Solutions**:
1. Check directory exists:
   ```bash
   mkdir -p .fstrent_spec_tasks/tasks
   ```

2. Check permissions:
   ```bash
   ls -la .fstrent_spec_tasks/
   ```

3. Verify TASKS.md exists and is writable

4. Check for file system errors

### Cross-IDE Issues

**Problem**: Files created in Claude Code don't appear in Cursor

**Solutions**:
1. Refresh file explorer in Cursor

2. Check file was actually created:
   ```bash
   ls .fstrent_spec_tasks/tasks/
   ```

3. Verify both IDEs are looking at same directory

4. Check Git status:
   ```bash
   git status
   ```

---

## 📚 Next Steps

### Learn More

1. **Read Command Reference**
   - See `docs/CLAUDE_CODE_COMMANDS_REFERENCE.md`
   - Detailed guide for all 7 commands

2. **Explore Skills**
   - Task Management: `.claude/skills/fstrent-task-management/`
   - Planning: `.claude/skills/fstrent-planning/`
   - QA: `.claude/skills/fstrent-qa/`

3. **Understand Agent**
   - See `docs/TASK_EXPANDER_AGENT_GUIDE.md`
   - Learn about complexity assessment

4. **Review Examples**
   - Check `examples/` folders in each Skill
   - See working templates and demonstrations

### Advanced Usage

1. **Cursor Compatibility**
   - See `docs/CURSOR_COMPATIBILITY_GUIDE.md` (Task 011)
   - Learn about cross-IDE workflows

2. **Team Collaboration**
   - Use Git for version control
   - Coordinate task assignments
   - Share PLAN.md and TASKS.md

3. **Customization**
   - Modify Skills for your workflow
   - Create custom commands
   - Adjust agent behavior

4. **Integration**
   - Connect with external tools
   - Automate workflows
   - Build on the system

### Get Help

- **Documentation**: See `docs/` folder
- **Examples**: Check Skill `examples/` folders
- **Issues**: Report on GitHub
- **Community**: Join discussions

---

## 🎉 You're Ready!

You now have a complete task management, planning, and QA system set up in Claude Code.

### Quick Reference Card

**Daily Commands**:
- `/project:status` - Check project status
- `/project:new-task [desc]` - Create task
- `/project:update-task [id]` - Update task
- `/project:report-bug [desc]` - Report bug

**Planning Commands**:
- `/project:start-planning [name]` - Start planning
- `/project:add-feature [name]` - Add feature

**Quality Commands**:
- `/project:quality-report` - Generate report

### Remember

- ✅ Skills activate automatically based on context
- ✅ Commands provide explicit, guided workflows
- ✅ Agent helps with complex task breakdown
- ✅ All files work in both Claude Code and Cursor
- ✅ System is production-ready and tested

**Happy coding!** 🚀

---

**Last Updated**: 2025-10-19  
**Version**: 1.0  
**For**: Claude Code users

