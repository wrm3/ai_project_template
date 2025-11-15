# fstrent-spec-tasks

**Comprehensive task management, project planning, and QA system with 100% cross-IDE compatibility**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/wrm3/ai_project_template)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)

---

## 📦 What's Included

### Skills (4)
- **fstrent-task-management** - Complete task lifecycle management with status tracking, priorities, and dependencies
- **fstrent-planning** - Project planning with PRD generation and 27-question framework
- **fstrent-qa** - Bug tracking, severity classification, and quality metrics
- **fstrent-code-reviewer** - Comprehensive code review with security and quality checks

### Agents (1)
- **task-expander** - Automatically breaks down complex tasks into manageable sub-tasks

### Commands (7)
- `/project:new-task` - Create a new task
- `/project:update-task` - Update task status
- `/project:status` - Get project overview
- `/project:report-bug` - Report a bug
- `/project:quality-report` - Generate quality metrics
- `/project:add-feature` - Add feature document
- `/project:start-planning` - Initialize project planning

---

## 🚀 Installation

### As Claude Code Plugin

```bash
# Add marketplace
/plugin marketplace add wrm3/ai_project_template

# Install this bundle
/plugin install fstrent-spec-tasks@wrm3
```

### As Project Template

```bash
# Clone repository
git clone https://github.com/wrm3/ai_project_template.git
cd ai_project_template

# Copy to your project
cp -r plugins/fstrent-spec-tasks/skills your-project/.claude/
cp -r plugins/fstrent-spec-tasks/agents your-project/.claude/
cp -r plugins/fstrent-spec-tasks/commands your-project/.claude/
```

---

## 💡 Quick Start

### Create Your First Task

```bash
# Using command
/project:new-task Implement user authentication

# Or just ask
> Create a new task for implementing user authentication
```

### Check Project Status

```bash
/project:status
```

### Report a Bug

```bash
/project:report-bug Login button not working on mobile
```

---

## 🎯 Features

### Task Management
- ✅ Create, update, and track tasks
- ✅ Task status management (Pending, In Progress, Completed)
- ✅ Priority levels (Critical, High, Medium, Low)
- ✅ Task dependencies and sub-tasks
- ✅ Automatic task expansion for complex work
- ✅ Windows-safe emojis: `[ ]`, `[🔄]`, `[✅]`, `[❌]`

### Project Planning
- ✅ Product Requirements Documents (PRD)
- ✅ Feature specifications
- ✅ User stories and acceptance criteria
- ✅ 27-question planning framework
- ✅ Scope validation and over-engineering prevention

### Bug Tracking
- ✅ Centralized bug tracking (BUGS.md)
- ✅ Severity classification (Critical, High, Medium, Low)
- ✅ Bug-to-task relationships
- ✅ Resolution tracking
- ✅ Quality metrics (bug discovery rate, resolution time)

### Cross-IDE Compatibility
- ✅ Works in Claude Code and Cursor
- ✅ Git-friendly markdown files
- ✅ Team collaboration support
- ✅ Seamless IDE switching

---

## 📁 File Structure

When installed as template, creates:

```
your-project/
├── .fstrent_spec_tasks/
│   ├── PLAN.md              # Product Requirements Document
│   ├── TASKS.md             # Master task checklist
│   ├── BUGS.md              # Bug tracking
│   ├── PROJECT_CONTEXT.md   # Project mission
│   ├── SUBSYSTEMS.md        # Component registry
│   ├── FILE_REGISTRY.md     # File documentation
│   ├── tasks/               # Individual task files
│   └── features/            # Feature specifications
└── .claude/
    ├── skills/
    │   ├── fstrent-task-management/
    │   ├── fstrent-planning/
    │   ├── fstrent-qa/
    │   └── fstrent-code-reviewer/
    ├── agents/
    │   └── task-expander.md
    └── commands/
        ├── new-task.md
        ├── update-task.md
        └── ...
```

---

## 📚 Documentation

- [Main Repository](https://github.com/wrm3/ai_project_template)
- [Task Management Guide](https://github.com/wrm3/ai_project_template/blob/main/docs/TASK_MANAGEMENT_GUIDE.md)
- [Planning Framework](https://github.com/wrm3/ai_project_template/blob/main/docs/PLANNING_FRAMEWORK.md)
- [Quality Metrics](https://github.com/wrm3/ai_project_template/blob/main/docs/QUALITY_METRICS.md)

---

## 🤝 Compatibility

**IDEs Supported**:
- ✅ Claude Code
- ✅ Cursor
- ✅ Windsurf (via rules)
- ✅ Roo-Code (via rules)
- ✅ Cline (via rules)

**Works With**:
- Task management across teams
- Mixed IDE environments
- Git-based workflows
- Remote/async collaboration

---

## 📄 License

MIT License - See [LICENSE](../../LICENSE) for details

---

## 🙏 Credits

Part of the [ai_project_template](https://github.com/wrm3/ai_project_template) marketplace.

**Author**: wrm3  
**Repository**: https://github.com/wrm3/ai_project_template  
**Issues**: https://github.com/wrm3/ai_project_template/issues

