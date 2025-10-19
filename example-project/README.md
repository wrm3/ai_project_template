# TaskFlow - Example Project

## Overview

This is a **complete example project** demonstrating how to use the `fstrent_spec_tasks` system with both **Claude Code** and **Cursor**. It shows a real-world task management web application with proper planning, task tracking, and bug management.

## What This Example Demonstrates

### 1. Cross-IDE Compatibility ✅
- **Both IDE interfaces included**: `.cursor/` and `.claude/`
- **Shared data**: `.fstrent_spec_tasks/` works with both IDEs
- **Zero duplication**: Same tasks, plans, and bugs in both IDEs

### 2. Complete Project Planning 📋
- **PRD (Product Requirements Document)**: `PLAN.md` with full project specification
- **Feature Documents**: Individual feature specs in `features/` folder
- **Project Context**: Clear mission, goals, and scope boundaries

### 3. Realistic Task Management 📝
- **16 sample tasks** showing various states:
  - ✅ Completed tasks (foundation work)
  - 🔄 In-progress tasks (current work)
  - ⏳ Pending tasks (upcoming work)
- **Task files** with detailed requirements and acceptance criteria
- **Task dependencies** and relationships

### 4. Bug Tracking 🐛
- **Sample bugs** with different severity levels
- **Bug-to-task relationships**
- **Bug workflow** from discovery to resolution

### 5. Working Application 💻
- **Simple Flask web app** (200 lines)
- **Task CRUD operations**
- **Priority and status management**
- **Responsive UI with Bootstrap**

## Quick Start

### Prerequisites
- Python 3.11+
- Git
- Either Cursor or Claude Code (or both!)

### Installation

```bash
# Clone this example
git clone <repository-url>
cd example-project

# Install Python dependencies
pip install -r requirements.txt

# Run the Flask app
python src/app.py

# Open browser to http://localhost:5000
```

### Exploring the Example

#### In Claude Code

1. Open this directory in Claude Code
2. Skills are automatically available:
   - `fstrent-task-management`
   - `fstrent-planning`
   - `fstrent-qa`
3. Try commands:
   - `/project:status` - See project overview
   - `/project:new-task` - Create a new task
   - `/project:report-bug` - Report a bug

#### In Cursor

1. Open this directory in Cursor
2. Rules are automatically loaded from `.cursor/rules/`
3. Try commands:
   - `/fstrent_spec_tasks_setup` - Verify setup
   - Use Cursor's AI to create/update tasks
   - Ask about project status

### What to Explore

1. **`.fstrent_spec_tasks/`** - The shared data directory
   - `PLAN.md` - Complete PRD for TaskFlow app
   - `TASKS.md` - Master task list
   - `BUGS.md` - Bug tracking
   - `tasks/` - Individual task files
   - `features/` - Feature specifications

2. **`.cursor/` and `.claude/`** - IDE-specific interfaces
   - Both read/write the same `.fstrent_spec_tasks/` files
   - Different UI, same data

3. **`src/`** - The actual Flask application
   - `app.py` - Main application (200 lines)
   - `templates/` - HTML templates
   - Shows how code relates to tasks

4. **`docs/`** - Project documentation
   - Setup guides
   - Compatibility guide
   - Troubleshooting

## Project Structure

```
example-project/
├── .fstrent_spec_tasks/        # Shared task management data
│   ├── PLAN.md                 # Product Requirements Document
│   ├── TASKS.md                # Master task list
│   ├── BUGS.md                 # Bug tracking
│   ├── PROJECT_CONTEXT.md      # Project context
│   ├── tasks/                  # Individual task files
│   │   ├── task001_setup_flask_project.md
│   │   ├── task006_add_priority_system.md
│   │   ├── task009_implement_search.md
│   │   └── task015_fix_deletion_bug.md
│   └── features/               # Feature specifications
│       ├── task-management.md
│       ├── priority-management.md
│       └── search.md
├── .cursor/                    # Cursor IDE interface
│   └── rules/
│       └── fstrent_spec_tasks/
├── .claude/                    # Claude Code interface
│   ├── skills/
│   ├── agents/
│   └── commands/
├── .claude-plugin/             # Plugin manifest
├── src/                        # Flask application
│   ├── app.py                  # Main app (200 lines)
│   └── templates/              # HTML templates
│       ├── base.html
│       └── index.html
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Learning Objectives

### 1. Understanding Cross-IDE Compatibility

**Key Insight**: Both IDEs use the same `.fstrent_spec_tasks/` files.

**Try This**:
1. Open project in Cursor
2. Create a new task using Cursor's AI
3. Close Cursor, open Claude Code
4. See the same task in Claude Code!

### 2. Task Management Workflow

**See Examples**:
- **Completed Task**: `task001_setup_flask_project.md` - Shows completed task with notes
- **In-Progress Task**: `task006_add_priority_system.md` - Shows work in progress
- **Pending Task**: `task009_implement_search.md` - Shows detailed planning
- **Bug Fix Task**: `task015_fix_deletion_bug.md` - Shows bug investigation

### 3. Project Planning

**See Examples**:
- **PRD**: `PLAN.md` - Complete product requirements
- **Features**: `features/` - Individual feature specs
- **Context**: `PROJECT_CONTEXT.md` - Project mission and scope

### 4. Bug Tracking

**See Examples**:
- **BUGS.md**: Centralized bug tracking
- **Bug Task**: Task 015 links to BUG-001
- **Severity Levels**: Critical, High, Medium, Low

## Common Tasks

### Create a New Task

**In Claude Code**:
```
/project:new-task
```

**In Cursor**:
Ask Cursor's AI: "Create a new task for implementing user authentication"

### Update Task Status

**In Claude Code**:
```
/project:update-task
```

**In Cursor**:
Ask Cursor's AI: "Mark task 006 as completed"

### Report a Bug

**In Claude Code**:
```
/project:report-bug
```

**In Cursor**:
Ask Cursor's AI: "Report a bug: Search not working on mobile"

### Get Project Status

**In Claude Code**:
```
/project:status
```

**In Cursor**:
Ask Cursor's AI: "What's the current project status?"

## Testing the Application

### Run the Flask App

```bash
python src/app.py
```

### Test Features

1. **View Tasks**: http://localhost:5000
2. **Create Task**: Click "New Task" button
3. **Filter Tasks**: Use status and priority filters
4. **Update Task**: Click "Edit" on any task
5. **Delete Task**: Click "Delete" (note: confirmation modal works!)

### Verify Cross-IDE Compatibility

1. **Make changes in Cursor**:
   - Create a new task
   - Update TASKS.md
   - Commit to Git

2. **Switch to Claude Code**:
   - Pull latest changes
   - See the same tasks
   - Continue working

## Key Files to Review

### For Task Management
- `.fstrent_spec_tasks/TASKS.md` - Master task list
- `.fstrent_spec_tasks/tasks/task006_add_priority_system.md` - In-progress task example

### For Planning
- `.fstrent_spec_tasks/PLAN.md` - Complete PRD
- `.fstrent_spec_tasks/features/task-management.md` - Feature spec

### For Bug Tracking
- `.fstrent_spec_tasks/BUGS.md` - Bug list
- `.fstrent_spec_tasks/tasks/task015_fix_deletion_bug.md` - Bug fix task

### For Cross-IDE Setup
- `.cursor/rules/` - Cursor interface
- `.claude/skills/` - Claude Code interface

## Next Steps

### 1. Adapt for Your Project

Use this as a template:
```bash
# Copy the structure
cp -r example-project my-project
cd my-project

# Update PROJECT_CONTEXT.md with your project info
# Update PLAN.md with your requirements
# Start creating tasks!
```

### 2. Learn More

- **Claude Code Setup**: `docs/CLAUDE_CODE_SETUP_GUIDE.md`
- **Cursor Compatibility**: `docs/CURSOR_COMPATIBILITY_GUIDE.md`
- **Troubleshooting**: `docs/TROUBLESHOOTING.md`

### 3. Contribute

Found this helpful? Consider:
- Sharing with your team
- Contributing improvements
- Creating your own examples

## FAQ

### Q: Can I use only one IDE?

**A**: Yes! Both interfaces are included, but you can use just one. The `.fstrent_spec_tasks/` files work with either IDE.

### Q: How do I switch between IDEs?

**A**: Just close one IDE and open the other in the same directory. All your tasks, plans, and bugs are there.

### Q: What if I don't need the Flask app?

**A**: The Flask app is just an example. You can delete `src/` and use the task management system for any project.

### Q: Can I modify the task structure?

**A**: Yes! The system is flexible. Add custom fields, change priorities, adapt to your workflow.

### Q: How do I collaborate with a team?

**A**: Use Git! Commit `.fstrent_spec_tasks/`, `.cursor/`, and `.claude/` to your repository. Team members can use either IDE.

## Troubleshooting

### Flask app won't start

```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+

# Run with verbose output
python src/app.py
```

### Tasks not appearing in IDE

**Cursor**: Restart Cursor to reload rules

**Claude Code**: Restart Claude Code to reload skills

### Git merge conflicts

See the [Cursor Compatibility Guide](docs/CURSOR_COMPATIBILITY_GUIDE.md#troubleshooting) for resolving conflicts in TASKS.md.

## Support

- **Documentation**: See `docs/` folder
- **Issues**: Open an issue on GitHub
- **Questions**: Check the compatibility guide

## License

MIT License - Feel free to use this example for learning and adaptation.

---

**Happy Task Managing!** 🚀

Whether you use Cursor, Claude Code, or both, this example shows how the `fstrent_spec_tasks` system provides a solid foundation for project planning and task management.

