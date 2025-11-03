# fstrent_spec_tasks System for Windsurf

The fstrent_spec_tasks system is a consolidated, practical task management framework optimized for daily coding work with minimal context overhead.

## Core Rules (5 Consolidated Files)

### 1. **`core.md`** - Core System Management
- **Task Management**: YAML-based task lifecycle with Windows-safe emojis
- **File Organization**: Template vs working directory management
- **Tool Integration**: MCP tool-first approach and automation
- **Context Management**: Project awareness and goal alignment
- **Scope Control**: Anti-scope-creep validation and over-engineering prevention
- **Coding Standards**: Python, JavaScript/React, Oracle PL/SQL standards

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
- **Security Guidelines**: Security checklist and vulnerability checks
- **Quality Standards**: Code quality metrics and standards
- **Review Process**: Systematic code review approach
- **Best Practices**: Language-specific best practices

## Directory Structure

```
.fstrent_spec_tasks/
├── tasks/                # Active task files
├── features/             # Feature documentation
├── memory/               # Historical archives
├── TASKS.md              # Master task checklist
├── BUGS.md               # Bug tracking
├── PROJECT_CONTEXT.md    # Project mission
├── PLAN.md               # Product Requirements Document
├── SUBSYSTEMS.md         # Component registry
└── FILE_REGISTRY.md      # File documentation

docs/                     # Project documentation
temp_scripts/             # Test and utility scripts
```

## Key Features

### Context Optimization
- **85% Reduction**: From 26+ rules to 5 consolidated rules
- **Windsurf Integration**: Native command integration
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

## How Windsurf Rules Work

Windsurf loads markdown-based rules from the `.windsurf/rules/` directory. These rules guide the AI assistant's behavior and provide context for your project.

### Rule Loading
- Rules are automatically loaded when you open the project
- Rules can reference project files and documentation
- Rules support standard markdown formatting

### Using Commands
Commands are invoked with the `/windsurf:` prefix:

```
/windsurf:setup           # Initialize the system
/windsurf:new-task        # Create a new task
/windsurf:status          # Check project status
```

## Cross-IDE Compatibility

The `.fstrent_spec_tasks/` directory is shared across all IDEs:

```
┌─────────────────────────────────────────────┐
│     .fstrent_spec_tasks/ (Shared Data)     │
│  ├── PLAN.md        (Product Requirements) │
│  ├── TASKS.md       (Master task list)     │
│  ├── BUGS.md        (Bug tracking)         │
│  └── tasks/         (Individual tasks)     │
└─────────────────────────────────────────────┘
                      ▲
                      │
          ┌───────────┴───────────────────┐
          │           │           │       │
    ┌─────▼────┐ ┌────▼────┐ ┌───▼────┐ ┌▼─────┐
    │ Windsurf │ │ Cursor  │ │ Claude │ │agents│
    │          │ │         │ │  Code  │ │ .md  │
    │.windsurf/│ │.cursor/ │ │.claude/│ │      │
    │  rules/  │ │ rules/  │ │skills/ │ │      │
    └──────────┘ └─────────┘ └────────┘ └──────┘
```

All IDEs read and write the same files. No conflicts. No translation.

## Getting Started

1. **Initialize**: Run `/windsurf:setup` to create the directory structure
2. **Set Context**: Update `PROJECT_CONTEXT.md` with your project details
3. **Plan**: Run `/windsurf:planning` to create your PRD
4. **Create Tasks**: Run `/windsurf:new-task` to start working
5. **Track Progress**: Check `/windsurf:status` regularly

## Documentation

- **Setup Guide**: [docs/WINDSURF_ADAPTATION_GUIDE.md](../../../docs/WINDSURF_ADAPTATION_GUIDE.md)
- **Main README**: [README.md](../../../README.md)
- **agents.md**: [agents.md](../../../agents.md)

---

*This consolidated system provides a solid, practical workhorse optimized for daily coding work with minimal context overhead while preserving 95% of original functionality.*
