# TaskFlow - File Registry

## Overview

This document provides a comprehensive registry of all files in the TaskFlow project, their purposes, and relationships.

---

## Directory Structure

```
example-project/
├── .fstrent_spec_tasks/        # Task management system (shared)
├── .cursor/                    # Cursor IDE interface
├── .claude/                    # Claude Code interface
├── .claude-plugin/             # Plugin manifest
├── src/                        # Application source code
├── docs/                       # Project documentation
├── tests/                      # Test files
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## File Categories

### Category 1: Task Management System
IDE-agnostic task and project management files.

### Category 2: IDE Interfaces
IDE-specific configuration for Cursor and Claude Code.

### Category 3: Application Code
Flask web application source code.

### Category 4: Documentation
Project documentation and guides.

### Category 5: Configuration
Project configuration and dependency files.

---

## File Definitions

### Task Management System (.fstrent_spec_tasks/)

#### PLAN.md
**Purpose**: Product Requirements Document (PRD) for TaskFlow  
**Type**: Markdown  
**Category**: Planning  
**Owner**: Product/Development Team

**Contents**:
- Product overview and summary
- Business and user goals
- User personas
- Feature specifications
- Technical considerations
- Milestones and user stories

**Usage**: Reference for project requirements and planning

---

#### TASKS.md
**Purpose**: Master task checklist  
**Type**: Markdown  
**Category**: Task Management  
**Owner**: Development Team

**Contents**:
- Active tasks by phase
- Task status indicators (✅ 🔄 ⏳)
- Completed tasks archive
- Task statistics

**Usage**: Quick overview of all project tasks

---

#### BUGS.md
**Purpose**: Bug tracking and management  
**Type**: Markdown  
**Category**: Quality Assurance  
**Owner**: Development Team

**Contents**:
- Active bugs by severity
- Bug details and status
- Resolved bugs
- Bug statistics
- Bug reporting guidelines

**Usage**: Track and manage bugs throughout development

---

#### PROJECT_CONTEXT.md
**Purpose**: Project mission, goals, and context  
**Type**: Markdown  
**Category**: Planning  
**Owner**: Product/Development Team

**Contents**:
- Mission statement
- Project goals and success criteria
- Current phase and progress
- Scope boundaries
- Technology stack
- Team and resources
- Risks and mitigation

**Usage**: Understand project context and constraints

---

#### SUBSYSTEMS.md
**Purpose**: Component registry and architecture  
**Type**: Markdown  
**Category**: Architecture  
**Owner**: Development Team

**Contents**:
- Subsystem definitions
- Responsibilities and interfaces
- Dependency relationships
- Integration points

**Usage**: Understand system architecture and component relationships

---

#### FILE_REGISTRY.md
**Purpose**: This file - comprehensive file documentation  
**Type**: Markdown  
**Category**: Documentation  
**Owner**: Development Team

**Contents**:
- File purposes and descriptions
- Directory structure
- File relationships
- Usage guidelines

**Usage**: Reference for understanding project file organization

---

#### tasks/ Directory
**Purpose**: Individual task files  
**Type**: Markdown with YAML frontmatter  
**Category**: Task Management  
**Owner**: Development Team

**Files**:
- `task001_setup_flask_project.md` - Completed setup task
- `task006_add_priority_system.md` - In-progress feature task
- `task009_implement_search.md` - Pending feature task
- `task015_fix_deletion_bug.md` - Bug fix task

**Format**:
```yaml
---
id: {number}
title: 'Task title'
type: {setup|feature|bug_fix|documentation}
status: {pending|in-progress|completed|cancelled}
priority: {critical|high|medium|low}
---
# Task content
```

**Usage**: Detailed task specifications and tracking

---

#### features/ Directory
**Purpose**: Feature specification documents  
**Type**: Markdown  
**Category**: Planning  
**Owner**: Product/Development Team

**Files**:
- `task-management.md` - Core CRUD operations
- `priority-management.md` - Priority system
- `search.md` - Search functionality

**Contents**:
- Feature overview
- Requirements
- User stories
- Technical considerations
- Acceptance criteria

**Usage**: Detailed feature specifications and requirements

---

### IDE Interfaces

#### .cursor/ Directory
**Purpose**: Cursor IDE configuration  
**Type**: Directory with rules and commands  
**Category**: IDE Configuration  
**Owner**: Development Team

**Structure**:
```
.cursor/
└── rules/
    └── fstrent_spec_tasks/
        ├── commands/
        └── rules/
```

**Usage**: Enables Cursor to work with `.fstrent_spec_tasks/` files

---

#### .claude/ Directory
**Purpose**: Claude Code configuration  
**Type**: Directory with skills, agents, commands  
**Category**: IDE Configuration  
**Owner**: Development Team

**Structure**:
```
.claude/
├── skills/
│   ├── fstrent-task-management/
│   ├── fstrent-planning/
│   └── fstrent-qa/
├── agents/
│   └── task-expander.md
└── commands/
    ├── new-task.md
    ├── update-task.md
    └── ...
```

**Usage**: Enables Claude Code to work with `.fstrent_spec_tasks/` files

---

#### .claude-plugin/ Directory
**Purpose**: Plugin manifest for distribution  
**Type**: Directory with plugin.json  
**Category**: Plugin Configuration  
**Owner**: Development Team

**Files**:
- `plugin.json` - Plugin metadata
- `README.md` - Plugin documentation

**Usage**: Package Claude Code components as installable plugin

---

### Application Code (src/)

#### src/app.py
**Purpose**: Main Flask application  
**Type**: Python  
**Category**: Application Code  
**Owner**: Development Team  
**Lines**: ~200

**Contents**:
- Flask app initialization
- Database configuration
- Task model definition
- Route handlers
- Sample data creation

**Key Components**:
- `Task` class (SQLAlchemy model)
- Routes: `/`, `/task/<id>`, `/task/create`, etc.
- Search endpoint: `/search`

**Dependencies**:
- Flask
- Flask-SQLAlchemy
- datetime

**Usage**: Run with `python src/app.py`

---

#### src/templates/ Directory
**Purpose**: Jinja2 HTML templates  
**Type**: HTML with Jinja2 syntax  
**Category**: Presentation  
**Owner**: Development Team

**Files**:
- `base.html` - Base template with navigation and styling
- `index.html` - Task list dashboard
- `task_detail.html` - Task details view (not yet created)
- `create_task.html` - Task creation form (not yet created)
- `update_task.html` - Task edit form (not yet created)

**Features**:
- Bootstrap 5.3 styling
- Responsive design
- Priority color coding
- Status indicators
- Modal dialogs

**Usage**: Rendered by Flask routes

---

### Configuration Files

#### requirements.txt
**Purpose**: Python package dependencies  
**Type**: Text  
**Category**: Configuration  
**Owner**: Development Team

**Contents**:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
python-dotenv==1.0.0
```

**Usage**: `pip install -r requirements.txt`

---

#### .gitignore
**Purpose**: Git ignore rules  
**Type**: Text  
**Category**: Configuration  
**Owner**: Development Team

**Key Exclusions**:
- `__pycache__/` - Python bytecode
- `*.db` - SQLite databases
- `.env` - Environment variables
- IDE-specific files

**Important**: Does NOT ignore `.cursor/`, `.claude/`, `.fstrent_spec_tasks/`

**Usage**: Automatically used by Git

---

#### README.md
**Purpose**: Project documentation and guide  
**Type**: Markdown  
**Category**: Documentation  
**Owner**: Development Team

**Contents**:
- Project overview
- What the example demonstrates
- Quick start guide
- Installation instructions
- Learning objectives
- Common tasks
- FAQ
- Troubleshooting

**Usage**: Read first when exploring the project

---

## File Relationships

### Task System Files
```
PLAN.md
  ├── features/task-management.md
  ├── features/priority-management.md
  └── features/search.md

TASKS.md
  ├── tasks/task001_setup_flask_project.md
  ├── tasks/task006_add_priority_system.md
  ├── tasks/task009_implement_search.md
  └── tasks/task015_fix_deletion_bug.md

BUGS.md
  └── tasks/task015_fix_deletion_bug.md (references BUG-001)
```

### Application Files
```
src/app.py
  ├── src/templates/base.html
  └── src/templates/index.html

requirements.txt
  └── src/app.py (imports dependencies)
```

### IDE Configuration
```
.fstrent_spec_tasks/ (shared data)
  ├── .cursor/ (Cursor interface)
  └── .claude/ (Claude Code interface)
```

---

## File Statistics

### By Category
- **Task Management**: 10 files
- **IDE Interfaces**: 20+ files (Cursor + Claude)
- **Application Code**: 3 files
- **Documentation**: 2 files
- **Configuration**: 3 files

### By Type
- **Markdown**: 15+ files
- **Python**: 1 file
- **HTML**: 2 files
- **JSON**: 1 file
- **Text**: 2 files

### Total Size
- **Task Management**: ~50 KB
- **Application Code**: ~10 KB
- **Documentation**: ~30 KB
- **Total**: ~100 KB (excluding IDE interfaces)

---

## File Naming Conventions

### Task Files
Format: `task{id}_{descriptive_name}.md`
- Examples: `task001_setup_flask_project.md`, `task006_add_priority_system.md`
- ID is zero-padded to 3 digits
- Descriptive name uses underscores

### Feature Files
Format: `{feature-name}.md`
- Examples: `task-management.md`, `priority-management.md`
- Uses hyphens for multi-word names
- Lowercase

### Template Files
Format: `{page_name}.html`
- Examples: `index.html`, `task_detail.html`
- Uses underscores for multi-word names
- Lowercase

---

## Change History

- **2025-10-01**: Initial file structure created
- **2025-10-08**: Added task and feature files
- **2025-10-15**: Added IDE interfaces
- **2025-10-19**: Documented for example project

---

## Notes

### For New Developers

1. **Start with README.md** - Understand the project
2. **Read PROJECT_CONTEXT.md** - Understand the mission
3. **Review PLAN.md** - Understand requirements
4. **Check TASKS.md** - See current work
5. **Explore src/app.py** - Understand the code

### For Task Management

1. **TASKS.md** - Quick overview
2. **tasks/*.md** - Detailed specifications
3. **features/*.md** - Feature requirements
4. **BUGS.md** - Known issues

### For Architecture

1. **SUBSYSTEMS.md** - Component overview
2. **FILE_REGISTRY.md** - This file
3. **src/app.py** - Implementation

---

This file registry helps navigate the TaskFlow project and understand the purpose and relationships of all files.

