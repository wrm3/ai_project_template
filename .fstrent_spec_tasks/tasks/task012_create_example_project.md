---
id: 012
title: 'Create example project with both IDE configs'
type: documentation
status: completed
priority: high
feature: Documentation
subsystems: [documentation, examples, cross_ide_compatibility]
project_context: 'Create a working example project demonstrating cross-IDE setup and usage'
dependencies: [001, 002, 003, 007, 008, 010, 011]
---

# Task 012: Create Example Project with Both IDE Configs

## Objective
Create a complete, working example project that demonstrates how to use `fstrent_spec_tasks` with both Claude Code and Cursor, serving as a reference implementation for users.

## Background
Users need a concrete example to:
- See both IDE interfaces in action
- Understand the file structure
- Learn from sample tasks and plans
- Have a starting template for their own projects
- Verify their installation works correctly

## Example Project Structure

### Project Type
A simple **Task Management Web App** that:
- Has clear features to plan
- Requires multiple tasks
- Demonstrates bug tracking
- Shows quality metrics
- Is relatable and understandable

### Directory Structure
```
example-project/
├── .fstrent_spec_tasks/        # Shared data
│   ├── PLAN.md                 # Sample PRD
│   ├── TASKS.md                # Sample tasks
│   ├── BUGS.md                 # Sample bugs
│   ├── PROJECT_CONTEXT.md      # Project context
│   ├── SUBSYSTEMS.md           # Components
│   ├── FILE_REGISTRY.md        # File docs
│   ├── tasks/                  # Sample task files
│   └── features/               # Sample features
├── .cursor/                    # Cursor interface
│   └── rules/
│       └── fstrent_spec_tasks/
├── .claude/                    # Claude Code interface
│   ├── skills/
│   ├── agents/
│   └── commands/
├── .claude-plugin/             # Plugin manifest
├── docs/                       # Documentation
├── src/                        # Example source code
│   ├── app.py                  # Simple Flask app
│   ├── models.py               # Data models
│   └── templates/              # HTML templates
├── tests/                      # Example tests
├── README.md                   # Project README
├── requirements.txt            # Python dependencies
└── .gitignore                  # Git ignore rules
```

## Sample Content

### 1. Sample PRD (PLAN.md)
- Complete PRD for task management web app
- Features: User auth, task CRUD, filtering, search
- User stories and acceptance criteria
- Technical considerations

### 2. Sample Tasks (TASKS.md + task files)
- 10-15 sample tasks covering:
  - Setup tasks (completed)
  - In-progress tasks
  - Pending tasks
  - Tasks with dependencies
  - Tasks with sub-tasks

### 3. Sample Bugs (BUGS.md)
- 3-5 sample bugs showing:
  - Different severity levels
  - Bug lifecycle stages
  - Bug-to-task relationships

### 4. Sample Features
- 3-4 feature documents
- Show feature-to-task relationships
- Include acceptance criteria

### 5. Example Source Code
- Simple Flask web app (100-200 lines)
- Demonstrates the project being planned
- Shows how code relates to tasks

### 6. Documentation
- README explaining the example
- Setup instructions
- How to explore the example
- What to learn from it

## Acceptance Criteria

- [ ] Example project created in `example-project/` directory
- [ ] Both IDE interfaces installed and configured
- [ ] Sample PRD with realistic content
- [ ] 10-15 sample tasks with various states
- [ ] 3-5 sample bugs
- [ ] 3-4 sample feature documents
- [ ] Simple working Flask app
- [ ] Comprehensive README
- [ ] All files properly formatted
- [ ] Cross-IDE compatibility verified
- [ ] Git repository initialized
- [ ] .gitignore configured correctly

## Success Metrics

- Users can clone and run the example
- Example demonstrates all key features
- Both IDEs work with the example
- Clear learning path for users
- Serves as project template

## Implementation Steps

1. Create example-project directory structure
2. Write sample PRD for task management app
3. Create sample tasks (various states)
4. Create sample bugs
5. Create sample feature documents
6. Write simple Flask app
7. Create comprehensive README
8. Test in both Cursor and Claude Code
9. Verify all features work
10. Document learning objectives

## Notes

- Keep the example simple but realistic
- Show best practices in action
- Include comments explaining choices
- Make it easy to adapt for other projects
- Ensure it works out-of-the-box

