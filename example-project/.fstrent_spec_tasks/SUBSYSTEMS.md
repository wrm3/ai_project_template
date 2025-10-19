# TaskFlow - Subsystems Registry

## Overview

This document provides a registry of all major subsystems in the TaskFlow application, their responsibilities, and relationships.

## Subsystem Categories

### 1. Application Layer
Core application components that handle business logic and user interactions.

### 2. Data Layer
Database models, schemas, and data access logic.

### 3. Presentation Layer
UI components, templates, and frontend logic.

### 4. Infrastructure Layer
Configuration, deployment, and supporting utilities.

---

## Subsystem Definitions

### APP-001: Flask Application Core
**Category**: Application Layer  
**Status**: Implemented  
**Owner**: Development Team

**Responsibilities**:
- Application initialization and configuration
- Request/response handling
- Session management
- Error handling
- Middleware integration

**Key Files**:
- `src/app.py` (main application)
- `config.py` (configuration)

**Dependencies**:
- Flask framework
- Flask-SQLAlchemy
- Flask-WTF

**Interfaces**:
- HTTP endpoints (REST-like)
- Template rendering
- Database connection

---

### APP-002: Task Management Routes
**Category**: Application Layer  
**Status**: Implemented  
**Owner**: Development Team

**Responsibilities**:
- Handle task CRUD operations
- Process task status updates
- Manage task filtering and sorting
- Handle task search requests

**Key Files**:
- `src/app.py` (routes section)

**Endpoints**:
- `GET /` - List tasks
- `GET /task/<id>` - View task
- `POST /task/create` - Create task
- `POST /task/<id>/update` - Update task
- `POST /task/<id>/delete` - Delete task
- `POST /task/<id>/status` - Update status
- `GET /search` - Search tasks

**Dependencies**:
- APP-001 (Flask Core)
- DATA-001 (Task Model)
- UI-001 (Templates)

---

### DATA-001: Task Model
**Category**: Data Layer  
**Status**: Implemented  
**Owner**: Development Team

**Responsibilities**:
- Define task data structure
- Provide data validation
- Handle database operations
- Serialize task data (to_dict)

**Key Files**:
- `src/app.py` (Task class)

**Schema**:
```python
class Task:
    id: Integer (primary key)
    title: String(200) (required)
    description: Text (optional)
    status: String(20) (default: 'pending')
    priority: String(20) (default: 'medium')
    due_date: DateTime (optional)
    created_at: DateTime (auto)
    updated_at: DateTime (auto)
```

**Valid Values**:
- Status: pending, in_progress, completed, cancelled
- Priority: critical, high, medium, low

**Dependencies**:
- SQLAlchemy ORM
- SQLite database

---

### DATA-002: Database Management
**Category**: Data Layer  
**Status**: Implemented  
**Owner**: Development Team

**Responsibilities**:
- Database initialization
- Schema migrations (manual for now)
- Sample data creation
- Database connection management

**Key Files**:
- `src/app.py` (database setup)
- `taskflow.db` (SQLite database file)

**Dependencies**:
- Flask-SQLAlchemy
- SQLite

**Configuration**:
- Database URI: `sqlite:///taskflow.db`
- Track modifications: False

---

### UI-001: Template System
**Category**: Presentation Layer  
**Status**: Implemented  
**Owner**: Development Team

**Responsibilities**:
- Render HTML pages
- Display task data
- Handle user input forms
- Show flash messages
- Provide responsive layout

**Key Files**:
- `src/templates/base.html` (base template)
- `src/templates/index.html` (task list)
- `src/templates/task_detail.html` (task details)
- `src/templates/create_task.html` (task form)
- `src/templates/update_task.html` (edit form)

**Dependencies**:
- Jinja2 template engine
- Bootstrap 5.3 CSS framework

**Features**:
- Responsive design
- Priority color coding
- Status indicators
- Modal dialogs
- Flash messages

---

### UI-002: Frontend Styling
**Category**: Presentation Layer  
**Status**: Implemented  
**Owner**: Development Team

**Responsibilities**:
- Visual design and styling
- Priority color scheme
- Status indicators
- Responsive layout
- Hover effects

**Key Files**:
- `src/templates/base.html` (embedded CSS)

**CSS Classes**:
- `.priority-critical` - Red background
- `.priority-high` - Orange background
- `.priority-medium` - Yellow background
- `.priority-low` - Green background
- `.status-*` - Status color coding
- `.task-card` - Task card styling

**Dependencies**:
- Bootstrap 5.3
- Custom CSS

---

### UI-003: JavaScript Interactions
**Category**: Presentation Layer  
**Status**: Planned  
**Owner**: Development Team

**Responsibilities**:
- Real-time search
- Dynamic filtering
- Modal interactions
- AJAX requests
- Form validation

**Key Files**:
- (To be created)

**Features** (Planned):
- Debounced search
- Filter state management
- Smooth transitions
- Keyboard shortcuts

**Dependencies**:
- Vanilla JavaScript (no framework)
- Fetch API

---

### INFRA-001: Configuration Management
**Category**: Infrastructure Layer  
**Status**: Implemented  
**Owner**: Development Team

**Responsibilities**:
- Application configuration
- Environment variables
- Secret key management
- Database configuration

**Key Files**:
- `src/app.py` (config section)
- `.env` (environment variables, not in repo)

**Configuration**:
- `SECRET_KEY` - Session encryption
- `SQLALCHEMY_DATABASE_URI` - Database connection
- `DEBUG` - Debug mode flag

---

### INFRA-002: Dependency Management
**Category**: Infrastructure Layer  
**Status**: Implemented  
**Owner**: Development Team

**Responsibilities**:
- Python package management
- Version pinning
- Dependency documentation

**Key Files**:
- `requirements.txt`

**Dependencies**:
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-WTF==1.2.1
- python-dotenv==1.0.0

---

### INFRA-003: Task Management System
**Category**: Infrastructure Layer  
**Status**: Implemented  
**Owner**: Development Team

**Responsibilities**:
- Project planning (PRD)
- Task tracking
- Bug management
- Feature documentation
- Cross-IDE compatibility

**Key Files**:
- `.fstrent_spec_tasks/` (all files)
- `.cursor/` (Cursor interface)
- `.claude/` (Claude Code interface)

**Features**:
- Product Requirements Document
- Task lifecycle management
- Bug tracking workflow
- Feature specifications
- Works with both Cursor and Claude Code

---

## Subsystem Relationships

### Dependency Graph

```
┌─────────────────────────────────────────────────────────┐
│                   Flask Application Core                 │
│                      (APP-001)                           │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼──────────┐    ┌──────▼──────────┐
│ Task Management  │    │  Configuration  │
│     Routes       │    │   Management    │
│   (APP-002)      │    │   (INFRA-001)   │
└───────┬──────────┘    └─────────────────┘
        │
    ┌───┴───┐
    │       │
┌───▼───┐ ┌─▼──────┐
│ Task  │ │Template│
│ Model │ │ System │
│(DATA  │ │ (UI-   │
│-001)  │ │  001)  │
└───┬───┘ └────────┘
    │
┌───▼────────┐
│  Database  │
│ Management │
│ (DATA-002) │
└────────────┘
```

### Integration Points

**APP-001 ↔ APP-002**:
- APP-001 provides Flask app instance
- APP-002 registers routes with APP-001

**APP-002 ↔ DATA-001**:
- APP-002 queries Task model
- DATA-001 provides data to APP-002

**APP-002 ↔ UI-001**:
- APP-002 renders templates from UI-001
- UI-001 receives data from APP-002

**DATA-001 ↔ DATA-002**:
- DATA-001 uses database connection from DATA-002
- DATA-002 manages Task model schema

**UI-001 ↔ UI-002**:
- UI-001 uses styles from UI-002
- UI-002 provides visual design for UI-001

---

## Subsystem Status Summary

| Subsystem | Category | Status | Priority |
|-----------|----------|--------|----------|
| APP-001 | Application | ✅ Implemented | Critical |
| APP-002 | Application | ✅ Implemented | Critical |
| DATA-001 | Data | ✅ Implemented | Critical |
| DATA-002 | Data | ✅ Implemented | Critical |
| UI-001 | Presentation | ✅ Implemented | High |
| UI-002 | Presentation | ✅ Implemented | High |
| UI-003 | Presentation | ⏳ Planned | Medium |
| INFRA-001 | Infrastructure | ✅ Implemented | High |
| INFRA-002 | Infrastructure | ✅ Implemented | High |
| INFRA-003 | Infrastructure | ✅ Implemented | High |

**Legend**:
- ✅ Implemented
- 🔄 In Progress
- ⏳ Planned
- ❌ Deprecated

---

## Change History

- **2025-10-01**: Initial subsystem definitions
- **2025-10-08**: Added UI subsystems
- **2025-10-15**: Added infrastructure subsystems
- **2025-10-19**: Documented for example project

---

## Notes

This subsystem registry helps understand the architecture of TaskFlow and how different components interact. Use this as a reference when:

- Planning new features
- Investigating bugs
- Onboarding new developers
- Making architectural decisions

