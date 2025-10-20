# AI Project Template

## Multi-IDE Development Framework for AI-Powered Coding

**One system. Multiple IDEs. Zero duplication.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/wrm3/ai_project_template)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> A comprehensive project template that works seamlessly across multiple AI-powered IDEs (**Claude Code**, **Cursor**, **Windsurf**, **Roo-Code**, and more), enabling teams to collaborate regardless of IDE preference.

---

## 🎯 What Makes This Unique

### The Problem

You love Claude Code's Skills and Agents. Your teammate prefers Cursor's rules-based approach. Your project planning system is stuck in one IDE or the other.

### The Solution

**fstrent_spec_tasks** provides:
- ✅ **100% cross-IDE compatibility** - Same tasks, plans, and bugs in both IDEs
- ✅ **Zero duplication** - One source of truth, two interfaces
- ✅ **Team-ready** - Everyone uses their preferred IDE
- ✅ **Git-friendly** - Standard markdown files, easy merging
- ✅ **Future-proof** - Add more IDE support anytime

### How It Works

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
          ┌───────────┴───────────┐
          │                       │
    ┌─────▼─────┐          ┌─────▼─────┐
    │  Cursor   │          │Claude Code│
    │           │          │           │
    │ .cursor/  │          │ .claude/  │
    │  rules/   │          │  skills/  │
    │           │          │  agents/  │
    │           │          │ commands/ │
    └───────────┘          └───────────┘
```

**Both IDEs read and write the same files. No conflicts. No translation. Just works.**

---

## ⚡ Quick Start

### 5-Minute Setup

#### For Claude Code Users

```bash
# Clone the repository
git clone https://github.com/wrm3/ai_project_template.git
cd ai_project_template

# Copy Claude Code interface to your project
cp -r .claude your-project/
cp -r .claude-plugin your-project/

# Open your project in Claude Code
# Skills are automatically available!
```

Try it:
```
/project:status
```

#### For Cursor Users

```bash
# Clone the repository
git clone https://github.com/wrm3/ai_project_template.git
cd ai_project_template

# Copy Cursor interface to your project
cp -r .cursor your-project/

# Open your project in Cursor
# Rules are automatically loaded!
```

Try it:
```
Ask Cursor's AI: "What's the current project status?"
```

#### For Both IDEs (Recommended for Teams)

```bash
# Copy both interfaces
cp -r .claude your-project/
cp -r .claude-plugin your-project/
cp -r .cursor your-project/

# Now anyone can use either IDE!
```

### Your First Task

**In Claude Code**:
```
/project:new-task
```

**In Cursor**:
Ask the AI: "Create a new task for implementing user authentication"

**Result**: Task file created in `.fstrent_spec_tasks/tasks/`, visible in both IDEs!

---

## 🚀 Features

### Task Management
- ✅ Create, update, and track tasks
- ✅ Task status management (Pending, In Progress, Completed)
- ✅ Priority levels (Critical, High, Medium, Low)
- ✅ Task dependencies and sub-tasks
- ✅ Automatic task expansion for complex work

### Project Planning
- ✅ Product Requirements Documents (PRD)
- ✅ Feature specifications
- ✅ User stories and acceptance criteria
- ✅ Project context and scope management
- ✅ 27-question planning framework

### Bug Tracking
- ✅ Centralized bug tracking
- ✅ Severity classification
- ✅ Bug-to-task relationships
- ✅ Resolution tracking
- ✅ Quality metrics

### Cross-IDE Compatibility
- ✅ Works in both Claude Code and Cursor
- ✅ Same data, different interfaces
- ✅ No file conflicts
- ✅ Git-based collaboration
- ✅ Seamless IDE switching

### Team Collaboration
- ✅ Mixed IDE teams supported
- ✅ Git-friendly file formats
- ✅ Clear merge conflict resolution
- ✅ Shared vocabulary and processes
- ✅ Coordinated workflows

---

## 📦 What's Included

### For Claude Code

**Skills** (`.claude/skills/`):
- `fstrent-task-management` - Complete task lifecycle management
- `fstrent-planning` - Project planning and PRD creation
- `fstrent-qa` - Bug tracking and quality assurance

**Agents** (`.claude/agents/`):
- `task-expander` - Automatically break down complex tasks

**Commands** (`.claude/commands/`):
- `/project:new-task` - Create a new task
- `/project:update-task` - Update task status
- `/project:report-bug` - Report a bug
- `/project:start-planning` - Initialize project planning
- `/project:add-feature` - Add a feature document
- `/project:quality-report` - Generate quality metrics
- `/project:status` - Get project overview

### For Cursor

**Rules** (`.cursor/rules/fstrent_spec_tasks/`):
- Core task management rules
- Planning system rules
- QA and bug tracking rules
- Workflow management rules

**Commands**:
- `/fstrent_spec_tasks_setup` - Initialize system
- `/fstrent_spec_tasks_plan` - Activate planning
- `/fstrent_spec_tasks_qa` - Activate QA
- `/fstrent_spec_tasks_workflow` - Activate workflow management

### Shared Data (`.fstrent_spec_tasks/`)

**Core Files**:
- `PLAN.md` - Product Requirements Document
- `TASKS.md` - Master task checklist
- `BUGS.md` - Bug tracking
- `PROJECT_CONTEXT.md` - Project mission and goals
- `SUBSYSTEMS.md` - Component registry
- `FILE_REGISTRY.md` - File documentation
- `MCP_TOOLS_INVENTORY.md` - Available tools

**Directories**:
- `tasks/` - Individual task files
- `features/` - Feature specifications

---

## 📚 Documentation

### Getting Started
- **[Claude Code Setup Guide](docs/CLAUDE_CODE_SETUP_GUIDE.md)** - Complete setup for Claude Code (4,200 words)
- **[Cursor Compatibility Guide](docs/CURSOR_COMPATIBILITY_GUIDE.md)** - Cross-IDE collaboration (8,200 words)
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Solve common issues (11,500 words)

### Examples
- **[Example Project](example-project/)** - Complete working example with TaskFlow web app (30+ files)
- **[Sample Tasks](example-project/.fstrent_spec_tasks/tasks/)** - Real task examples
- **[Sample PRD](example-project/.fstrent_spec_tasks/PLAN.md)** - Complete product requirements

### Reference
- **[Task Templates](docs/TASK_TEMPLATES.md)** - Task file formats and examples
- **[Planning Framework](docs/PLANNING_FRAMEWORK.md)** - 27-question planning guide
- **[Quality Metrics](docs/QUALITY_METRICS.md)** - Bug tracking and QA metrics

---

## 💡 Use Cases

### Solo Developer
**Scenario**: You work on multiple projects and want consistent task management.

**Solution**: Install in all projects. Switch between IDEs based on task type. All your planning stays consistent.

**Benefits**:
- Consistent workflow across projects
- Learn new IDE without abandoning your system
- Future-proof your workflow

### Small Team (2-10 People)
**Scenario**: Your team uses different IDEs but needs to coordinate work.

**Solution**: Everyone installs their preferred interface. All work tracked in shared `.fstrent_spec_tasks/` files.

**Benefits**:
- No IDE conflicts
- Everyone sees the same tasks
- Git-based collaboration works perfectly

### Mixed IDE Team
**Scenario**: Half your team uses Cursor, half uses Claude Code.

**Solution**: Commit both interfaces to Git. Everyone clones and uses their preferred IDE.

**Benefits**:
- Zero friction for team members
- No "translation" between systems
- Seamless code reviews

### Learning & Teaching
**Scenario**: Teaching students or onboarding new developers.

**Solution**: Use example project as learning resource. Students can use either IDE.

**Benefits**:
- Lower barrier to entry
- Students choose comfortable IDE
- Focus on concepts, not tools

---

## 🎓 Example Project

We've included a **complete working example** to help you get started:

**TaskFlow** - A simple task management web app built with Flask

```bash
cd example-project
pip install -r requirements.txt
python src/app.py
# Open http://localhost:5000
```

**What's Included**:
- ✅ Complete PRD (4,800 words)
- ✅ 16 sample tasks (various states)
- ✅ 4 sample bugs
- ✅ 3 feature specifications
- ✅ Working Flask application (200 lines)
- ✅ Both IDE interfaces configured
- ✅ Comprehensive README

**Learn From**:
- How to structure a PRD
- How to write effective tasks
- How to track bugs
- How code relates to tasks
- How both IDEs work together

[Explore the Example →](example-project/)

---

## 🔧 Installation

### Prerequisites
- Git
- Python 3.11+ (for example project)
- Either Cursor or Claude Code (or both!)

### Option 1: Use Example as Template

```bash
# Clone this repository
git clone https://github.com/wrm3/ai_project_template.git

# Copy example to your project
cp -r ai_project_template/example-project my-project
cd my-project

# Customize for your project
# Edit .fstrent_spec_tasks/PROJECT_CONTEXT.md
# Edit .fstrent_spec_tasks/PLAN.md
# Start creating tasks!
```

### Option 2: Add to Existing Project

```bash
# Navigate to your project
cd my-existing-project

# Copy interfaces
cp -r /path/to/ai_project_template/.claude .
cp -r /path/to/ai_project_template/.claude-plugin .
cp -r /path/to/ai_project_template/.cursor .

# Initialize task system
mkdir -p .fstrent_spec_tasks/tasks
mkdir -p .fstrent_spec_tasks/features

# Copy template files
cp /path/to/ai_project_template/example-project/.fstrent_spec_tasks/*.md .fstrent_spec_tasks/

# Customize for your project
```

### Option 3: Install as Plugin (Claude Code)

```bash
# Coming soon!
# /plugin marketplace add your-username/ai_project_template
# /plugin install ai_project_template
```

---

## 🤝 Team Collaboration

### Git Workflow

**Step 1: Initial Setup**
```bash
# Team lead sets up project
git init
# Copy both IDE interfaces
cp -r .claude .cursor .fstrent_spec_tasks my-project/
cd my-project
git add .
git commit -m "Add fstrent_spec_tasks system"
git push
```

**Step 2: Team Members Clone**
```bash
# Each team member clones
git clone <repository-url>
cd project

# Open in preferred IDE
# Cursor users: Open in Cursor
# Claude Code users: Open in Claude Code
```

**Step 3: Daily Workflow**
```bash
# Pull latest changes
git pull

# Create/update tasks in your IDE
# (Changes go to .fstrent_spec_tasks/)

# Commit and push
git add .fstrent_spec_tasks/
git commit -m "Update tasks"
git push
```

**Step 4: Switching IDEs**
```bash
# Just close one IDE and open the other
# All your tasks are there!
```

### Handling Merge Conflicts

**Common Conflict: TASKS.md**
```bash
# Two people added tasks simultaneously
git pull
# CONFLICT in .fstrent_spec_tasks/TASKS.md

# Open TASKS.md, find:
<<<<<<< HEAD
- [ ] Task 042: Feature A
=======
- [ ] Task 042: Feature B
>>>>>>> origin/main

# Resolve by merging both:
- [ ] Task 042: Feature A
- [ ] Task 043: Feature B

# Commit resolution
git add .fstrent_spec_tasks/TASKS.md
git commit -m "Resolve task list conflict"
```

[See Full Collaboration Guide →](docs/CURSOR_COMPATIBILITY_GUIDE.md#team-collaboration)

---

## 🎯 Comparison with Other Systems

| Feature | fstrent_spec_tasks | Jira | GitHub Issues | Notion |
|---------|-------------------|------|---------------|--------|
| **Works in Multiple IDEs** | ✅ Cursor + Claude Code | ❌ Web only | ❌ Web/GitHub | ❌ Web only |
| **Offline Access** | ✅ Full | ❌ Limited | ❌ No | ❌ Limited |
| **Git-Friendly** | ✅ Markdown files | ❌ Database | ✅ Yes | ❌ No |
| **No Account Required** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Free & Open Source** | ✅ Yes | ❌ Paid | ✅ Yes | ❌ Freemium |
| **AI Integration** | ✅ Native | ❌ No | ❌ Limited | ❌ Limited |
| **Team Collaboration** | ✅ Git-based | ✅ Built-in | ✅ Built-in | ✅ Built-in |
| **Customizable** | ✅ Fully | ❌ Limited | ❌ Limited | ✅ Yes |

**Best For**:
- ✅ Developers who live in their IDE
- ✅ Teams with mixed IDE preferences
- ✅ Projects that need Git-based workflows
- ✅ Teams that value simplicity and control

**Not For**:
- ❌ Non-technical teams
- ❌ Large enterprises needing complex workflows
- ❌ Teams requiring real-time collaboration
- ❌ Projects needing advanced reporting

---

## 🛠️ Advanced Features

### Task Expansion Agent

The `task-expander` agent automatically breaks down complex tasks:

```
# In Claude Code
# Agent detects complex task (>7 complexity points)
# Automatically proposes sub-tasks

Task 042: Implement User Authentication
  ├── Task 042.1: Set up database schema
  ├── Task 042.2: Create authentication routes
  ├── Task 042.3: Implement session management
  └── Task 042.4: Add password hashing
```

[Learn More →](docs/TASK_EXPANDER_AGENT_GUIDE.md)

### Planning Framework

27-question framework for comprehensive project planning:

**Phase 1: Project Context** (Q1-Q7)
- Problem definition
- Success criteria
- User identification

**Phase 2: Technical Requirements** (Q8-Q16)
- Deployment strategy
- Security needs
- Performance expectations

**Phase 3: Feature Scope** (Q17-Q22)
- Essential features
- Nice-to-haves
- Features to avoid

**Phase 4: Timeline & Resources** (Q23-Q27)
- Timeline drivers
- Delivery preferences
- Trade-offs

[See Full Framework →](docs/PLANNING_FRAMEWORK.md)

### Quality Metrics

Track project health with built-in metrics:

- **Task Completion Rate**: % of tasks completed on time
- **Bug Discovery Rate**: Bugs found per development cycle
- **Bug Resolution Time**: Average time to fix bugs
- **Feature Impact**: Which features have most bugs
- **Velocity**: Tasks completed per sprint

[See All Metrics →](docs/QUALITY_METRICS.md)

---

## 📊 Project Stats

**Documentation**: 47,500+ words
- Setup guides: 12,400 words
- Example project: 23,600 words
- Troubleshooting: 11,500 words

**Code**: 200+ lines (example Flask app)

**Files**: 50+ files across all components

**Skills**: 3 Claude Code Skills with progressive disclosure

**Commands**: 7 Claude Code commands + 4 Cursor commands

**Agents**: 1 intelligent task expansion agent

---

## 🤔 FAQ

### Q: Can I use only one IDE?

**A**: Yes! Both interfaces are included, but you can use just one. The `.fstrent_spec_tasks/` files work with either IDE.

### Q: How do I switch between IDEs?

**A**: Just close one IDE and open the other in the same directory. All your tasks, plans, and bugs are there.

### Q: What if my team uses different IDEs?

**A**: Perfect! That's exactly what this system is designed for. Commit both `.cursor/` and `.claude/` to Git. Everyone uses their preferred IDE.

### Q: Do I need to install anything?

**A**: Just copy the interface files (`.cursor/` or `.claude/`) to your project. No npm packages, no pip installs (except for the example Flask app).

### Q: Can I customize the system?

**A**: Absolutely! All files are markdown and YAML. Edit templates, add custom fields, modify workflows. It's your system.

### Q: What about merge conflicts?

**A**: Rare, but possible. Most conflicts are in TASKS.md and are easy to resolve. See the [Compatibility Guide](docs/CURSOR_COMPATIBILITY_GUIDE.md#troubleshooting) for details.

### Q: Is this production-ready?

**A**: Yes! We use it daily for real projects. The example project demonstrates production-quality setup.

### Q: How do I contribute?

**A**: We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🗺️ Roadmap

### v0.1.0 (Current)
- ✅ Core task management
- ✅ Project planning (PRD)
- ✅ Bug tracking
- ✅ Cross-IDE compatibility (Cursor + Claude Code)
- ✅ Example project
- ✅ Comprehensive documentation

### v0.2.0 (Next)
- ⏳ Plugin marketplace distribution
- ⏳ Additional IDE support (Windsurf, Roo-Code)
- ⏳ Enhanced task templates
- ⏳ Time tracking integration
- ⏳ Gantt chart visualization

### v1.0.0 (Future)
- ⏳ Web dashboard (optional)
- ⏳ API for external integrations
- ⏳ Advanced reporting
- ⏳ Team analytics
- ⏳ Mobile app (view-only)

[See Full Roadmap →](ROADMAP.md)

---

## 🙏 Acknowledgments

**Inspired By**:
- Cursor's innovative rules-based AI assistance
- Claude Code's Skills and Agents architecture
- The need for IDE-agnostic development tools

**Built With**:
- Markdown for universal compatibility
- YAML for structured data
- Git for version control
- Python for example application

**Special Thanks**:
- The Cursor team for their amazing IDE
- Anthropic for Claude Code and Claude AI
- The open-source community

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

**TL;DR**: Free to use, modify, and distribute. Just keep the license notice.

---

## 🚀 Get Started Now

```bash
# Clone the repository
git clone https://github.com/wrm3/ai_project_template.git

# Explore the example
cd ai_project_template/example-project
pip install -r requirements.txt
python src/app.py

# Copy to your project
cp -r .claude .cursor .fstrent_spec_tasks ../my-project/

# Start planning!
```

**Questions?** Check the [documentation](docs/) or [open an issue](https://github.com/wrm3/ai_project_template/issues).

**Ready to collaborate across IDEs?** Give it a try! ⭐

---

<div align="center">

**Made with ❤️ for developers who value flexibility**

[Documentation](docs/) • [Example Project](example-project/) • [Issues](https://github.com/wrm3/ai_project_template/issues) • [Discussions](https://github.com/wrm3/ai_project_template/discussions)

</div>
