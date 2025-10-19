# fstrent_tasks_v2 - AI IDE Agent Rules System

## Overview

The **fstrent_tasks_v2** system is a comprehensive set of AI IDE Agent rules designed for Cursor that provides a **spec-driven task management system** with intelligent workflow automation. This system transforms AI agents from simple code generators into sophisticated project management partners that understand context, maintain project history, and follow structured development methodologies.

## Purpose & Intent

### Primary Goals
- **Spec-Driven Development**: Transform requirements into structured, trackable tasks
- **Context Awareness**: Maintain project context across sessions and team members
- **Intelligent Automation**: Automate routine development workflows and decision-making
- **Quality Assurance**: Ensure consistent coding standards and project organization
- **Knowledge Preservation**: Archive completed work for future reference and learning

### Target Technologies
This rule system is specifically designed for teams working with:
- **Python** - Backend development and automation
- **JavaScript/React** - Frontend web development
- **Oracle Database (23ai)** - Database development and management
- **Oracle Apex** - Rapid application development

## System Architecture

### Core Philosophy
The system follows a **progressive disclosure** approach with three levels:
- **BASIC**: Essential functionality for immediate use
- **STANDARD**: Complete features for regular development
- **ADVANCED**: Sophisticated capabilities for complex projects

### File Organization
```
.cursor/rules/fstrent_tasks_v2/
├── core/                    # Essential system rules (10 files)
├── coding_specs/           # Language-specific standards (5 files)
├── scope_management/       # Requirements & scope control (3 files)
├── workflow/               # Development methodologies (3 files)
├── quality/                # QA and documentation (3 files)
├── advanced/               # Advanced system features (5 files)
└── [System Files]          # Overview and documentation (2 files)
```

## Core Components

### 1. Task Management System (`core/tasks.mdc`)
- **File-based task tracking** with YAML frontmatter
- **Automatic complexity assessment** and task expansion
- **Dependency management** and workflow orchestration
- **Status tracking** (pending → in-progress → completed)
- **Sub-task creation** for complex work breakdown

### 2. Memory System (`core/memory.mdc`)
- **Historical context preservation** across sessions
- **Automatic archival** of completed work
- **Knowledge retrieval** for similar past projects
- **Pattern recognition** for improved decision-making

### 3. Planning System (`core/plans.mdc`)
- **Product Requirements Document (PRD)** generation
- **Structured planning questionnaires** for requirements gathering
- **Scope validation** and over-engineering prevention
- **Feature prioritization** and milestone tracking

### 4. Context Management (`core/context_management.mdc`)
- **Project awareness** maintenance across all interactions
- **Goal alignment** validation for every task
- **Scope boundary** enforcement
- **Success criteria** tracking

### 5. Tool Integration (`core/tool_awareness.mdc`)
- **MCP (Model Context Protocol)** tool integration
- **Tool-first approach** to automation
- **Intelligent tool selection** based on task requirements
- **Workflow optimization** through tool orchestration

## Coding Standards

### Language-Specific Rules
Each technology stack has dedicated coding standards:

#### Python (`coding_specs/python_coding_spec.mdc`)
- PEP 8 compliance (relaxed enforcement)
- Type hints and comprehensive docstrings
- Error handling and testing standards
- Performance optimization guidelines

#### JavaScript/React (`coding_specs/javascript_react_coding_spec.mdc`)
- ESLint/Prettier configuration
- React hooks and component patterns
- TypeScript integration
- Testing with Jest and React Testing Library

#### Oracle PL/SQL (`coding_specs/oracle_plsql_coding_spec.mdc`)
- Business area prefixing (AA_, AC_, MG_, etc.)
- Package-oriented design
- Security and performance best practices
- utPLSQL testing framework

#### Oracle Apex (`coding_specs/oracle_apex_coding_spec.mdc`)
- Application design standards
- Security implementation
- Performance optimization
- JavaScript integration patterns

## Workflow Management

### Scope Control (`scope_management/`)
- **Anti-scope-creep validation** prevents over-engineering
- **Scope clarification** ensures clear requirements
- **Planning questionnaires** capture comprehensive project needs

### Development Methodologies (`workflow/`)
- **Sprint planning** with story point estimation
- **Modern methodology integration** (Kanban, DevOps)
- **Workflow diagram generation** for process visualization

### Quality Assurance (`quality/`)
- **Bug tracking** with structured workflows
- **Design fix documentation** for retroactive improvements
- **Standardized documentation** templates

## Advanced Features

### Performance Analytics (`advanced/performance.mdc`)
- **System metrics collection** and analysis
- **Task completion tracking** and velocity measurement
- **Bottleneck identification** and optimization recommendations

### Continuous Improvement (`advanced/continuous_improvement.mdc`)
- **Rule effectiveness analysis** and optimization
- **System evolution** based on usage patterns
- **Feedback loop** implementation for ongoing enhancement

### Context Optimization (`advanced/context_optimization.mdc`)
- **Context window management** for optimal AI performance
- **Progressive disclosure** intelligence monitoring
- **Resource allocation** optimization

## Getting Started

### 1. Installation
Copy the entire `.cursor/rules/fstrent_tasks_v2/` folder to your project's `.cursor/rules/` directory.

### 2. Initial Setup
The system provides templates that you can customize for your project:
- Copy template files to your project directory
- Customize PROJECT_CONTEXT.md with your project details
- Initialize task management files from templates
- Set up memory archival systems

### 3. First Use
1. **Create a project plan** using the planning questionnaire
2. **Generate initial tasks** from your PRD
3. **Start development** with context awareness
4. **Track progress** through the task management system

## Key Benefits

### For Development Teams
- **Consistent workflows** across all team members
- **Automated quality checks** and standards enforcement
- **Historical context** for better decision-making
- **Reduced onboarding time** for new team members

### For Project Management
- **Clear task breakdown** and dependency tracking
- **Progress visibility** through structured reporting
- **Scope control** to prevent project creep
- **Knowledge preservation** for future projects

### For AI Agents
- **Context awareness** across all interactions
- **Intelligent automation** of routine tasks
- **Tool integration** for enhanced capabilities
- **Learning from history** for improved performance

## File Structure

### Working Directory: `.fstrent_tasks_v2/`
Contains all active project files:
- `TASKS.md` - Master task checklist
- `PLANS.md` - Product Requirements Document
- `PROJECT_CONTEXT.md` - Project mission and goals
- `SUBSYSTEMS.md` - Component registry
- `FILE_REGISTRY.md` - File structure documentation
- `tasks/` - Active task files
- `memory/` - Archived completed work
- `docs/` - Detailed coding standards documentation

### Template Directory: `templates/fstrent_tasks_v2/`
Contains system templates (rarely modified):
- Installation templates
- Blank project structures
- Deployment configuration files

## Best Practices

### Task Management
- **Break down complex tasks** using the expansion system
- **Maintain clear dependencies** between related work
- **Update status regularly** for accurate progress tracking
- **Archive completed work** to maintain clean workspace

### Planning
- **Use structured questionnaires** for comprehensive requirements
- **Validate scope boundaries** before starting development
- **Create detailed PRDs** for complex features
- **Regular scope reviews** to prevent creep

### Code Quality
- **Follow language-specific standards** for consistency
- **Use automated tools** for formatting and linting
- **Document deviations** from standards with justification
- **Regular code reviews** using established templates

### Memory Management
- **Consult historical context** before starting new work
- **Archive completed tasks** regularly
- **Maintain clean active workspace** for focus
- **Learn from past decisions** for improved outcomes

## Troubleshooting

### Common Issues
1. **Rules not activating**: Ensure all files have `alwaysApply: true` in YAML frontmatter
2. **Context loss**: Check that `PROJECT_CONTEXT.md` is properly maintained
3. **Task confusion**: Use the memory consultation system before creating new tasks
4. **Scope creep**: Regularly validate against scope boundaries

### Support
- **Documentation**: Refer to individual rule files for detailed guidance
- **Standards**: Consult `.fstrent_tasks_v2/docs/` for comprehensive coding standards
- **Workflows**: Use workflow diagrams for process visualization

## Future Evolution

This system is designed to evolve with your team's needs:
- **Rule improvements** based on usage patterns
- **New technology support** as requirements change
- **Enhanced automation** through MCP tool integration
- **Advanced analytics** for continuous optimization

## Contributing

When modifying or extending the system:
1. **Maintain progressive disclosure** structure (BASIC/STANDARD/ADVANCED)
2. **Update documentation** for any new features
3. **Test rule activation** to ensure proper functionality
4. **Preserve backward compatibility** when possible

---

**Version**: 2.0  
**Last Updated**: December 2024  
**Compatibility**: Cursor IDE with MCP tool support  
**Target Audience**: Python, JavaScript/React, Oracle development teams
