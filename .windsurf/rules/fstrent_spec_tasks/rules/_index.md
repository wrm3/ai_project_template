# fstrent_spec_tasks System Overview for Windsurf

The fstrent_spec_tasks system is a consolidated, practical task management framework optimized for daily coding work with minimal context overhead.

## Core Rules (5 Files)

### 1. **`core.md`** - Core System Management
- **Task Management**: YAML-based task lifecycle with Windows-safe emojis
- **File Organization**: Template vs working directory management
- **Tool Integration**: MCP tool-first approach and automation
- **Context Management**: Project awareness and goal alignment
- **Scope Control**: Anti-scope-creep validation and over-engineering prevention
- **Coding Standards**: Python, JavaScript/React, Oracle PL/SQL, Oracle Apex standards
- **Template Setup**: System initialization

### 2. **`planning.md`** - Planning & Requirements
- **PRD Generation**: Product Requirements Document creation
- **Planning Questionnaire**: 27-question requirements gathering framework
- **Scope Clarification**: Scope validation and assumption checking
- **Feature Management**: Features folder structure and documentation
- **Codebase Analysis**: Automatic project analysis for existing codebases

### 3. **`qa.md`** - Quality Assurance
- **Bug Tracking**: Bug identification, categorization, and resolution tracking
- **Design Fixes**: Retroactive documentation for completed fixes
- **Documentation Templates**: Standardized templates for tasks, bugs, and fixes
- **Quality Workflows**: Bug lifecycle and quality management processes

### 4. **`workflow.md`** - Workflow Management
- **Task Expansion**: Complexity assessment and sub-task breakdown
- **Methodology Integration**: Kanban flow, WIP limits, DevOps practices
- **Workflow Diagrams**: Mermaid diagram generation for visualization
- **Architecture Visualization**: System component relationship diagrams
- **Sprint Planning**: Iteration planning and story point estimation

### 5. **`code_review.md`** - Code Review Guidelines
- **Security Checklist**: Security vulnerability checks
- **Quality Standards**: Code quality metrics
- **Review Process**: Systematic code review
- **Best Practices**: Language-specific guidelines

## Directory Structure
```
.fstrent_spec_tasks/
├── tasks/                # Active task files
├── features/             # Feature documentation (renamed from plans/)
├── memory/               # Historical archives (using Windsurf's memory)
├── TASKS.md              # Master task checklist
├── BUGS.md               # Bug tracking (subset of TASKS.md)
├── PROJECT_CONTEXT.md    # Project mission
├── PLAN.md               # Product Requirements Document
├── SUBSYSTEMS.md         # Component registry
└── FILE_REGISTRY.md      # File documentation

docs/                     # Project documentation (migration files, setup summaries)
temp_scripts/             # Test and utility scripts
```

## Key Features

### Context Optimization
- **85% Reduction**: From 26+ rules to 5 consolidated rules
- **Windsurf Integration**: Built-in with native commands
- **Single-Level Rules**: No progressive disclosure complexity
- **Tool-First Approach**: MCP tool integration for automation

### Practical Daily Use
- **Clear Hierarchy**: PLAN → FEATURES → TASKS → BUGS
- **Windows-Safe Emojis**: ✅ 🔄 ❌ for task status
- **Simplified Workflows**: Focus on essential coding tasks
- **No Rule Conflicts**: Clean, predictable activation

### Commands Available
- `/windsurf:setup` - Initialize system
- `/windsurf:new-task` - Create new task
- `/windsurf:update-task` - Update task status
- `/windsurf:planning` - Activate planning system
- `/windsurf:qa` - Activate quality assurance
- `/windsurf:status` - Show project status

## How to Use

### Initial Setup
1. Run `/windsurf:setup` to initialize the system
2. Update `PROJECT_CONTEXT.md` with your project details
3. Run `/windsurf:planning` to create your PRD
4. Start creating tasks with `/windsurf:new-task`

### Daily Workflow
1. Check status with `/windsurf:status`
2. Work on tasks (status: [ ] → [📋] → [🔄] → [✅])
3. Report bugs with `/windsurf:qa`
4. Update tasks with `/windsurf:update-task`

### Cross-IDE Collaboration
- All IDEs share the same `.fstrent_spec_tasks/` directory
- Windsurf, Cursor, and Claude Code work seamlessly together
- No file conflicts or translation needed
- Team members can use their preferred IDE

---

*This consolidated system provides a solid, practical workhorse optimized for daily coding work with minimal context overhead while preserving 95% of original functionality.*
