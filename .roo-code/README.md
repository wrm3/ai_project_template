# Roo-Code Configuration for fstrent_spec_tasks

**Version:** 1.0
**Last Updated:** November 2025
**Status:** Production Ready

## Overview

This directory contains Roo-Code-specific configuration for the **fstrent_spec_tasks** system - a comprehensive, file-based task management and workflow system that works across all AI coding IDEs.

Roo-Code is an open-source AI coding assistant that supports the [agents.md](https://agents.md) standard, making it ideal for cross-IDE development workflows.

## What is Roo-Code?

**Roo-Code** is a VS Code extension and standalone IDE that provides:
- Full agents.md standard support
- Advanced context management
- Multi-model AI support (Claude, GPT-4, etc.)
- Git integration and team collaboration features
- Extensible rule and command system

**Official Site:** https://roo.code (example - verify actual URL)

## Directory Structure

```
.roo-code/
├── README.md                    # This file
├── settings.json               # Roo-Code configuration
├── rules/                      # Core behavior rules
│   ├── always.md              # Always-active rules
│   ├── task_management.md     # Task system rules
│   ├── planning_workflow.md   # Planning process rules
│   ├── qa_bug_tracking.md     # QA and bug tracking
│   ├── git_workflow.md        # Git conventions
│   ├── documentation.md       # Documentation standards
│   ├── python_env.md          # Python virtual environments
│   └── parallel_workflow.md   # Parallel task execution
└── commands/                   # Custom Roo-Code commands
    ├── new-task.md            # Create new task
    ├── update-task.md         # Update existing task
    ├── status.md              # Project status report
    ├── start-planning.md      # Begin planning session
    ├── quality-report.md      # Generate QA report
    ├── review.md              # Code review workflow
    ├── add-feature.md         # Add new feature
    ├── report-bug.md          # Report and track bug
    └── fix-github-issue.md    # Fix GitHub issue
```

## Quick Start

### 1. Prerequisites

- Roo-Code IDE or VS Code with Roo-Code extension installed
- Git repository initialized
- Basic understanding of fstrent_spec_tasks (see `agents.md`)

### 2. First Time Setup

The fstrent_spec_tasks system should already be initialized if you cloned this project. If not:

```bash
# Roo-Code will automatically detect the configuration
# Just open the project and you're ready to go!
```

### 3. Using Commands

Roo-Code supports custom commands via the command palette or inline:

**Via Command Palette:**
```
Cmd/Ctrl + Shift + P → "Roo: new-task"
```

**Via Inline Mention:**
```
@roo new-task: Implement user authentication
```

**Via Chat:**
```
/new-task Implement user authentication
```

## Available Commands

### Task Management

**`/new-task`** - Create a new task
```
/new-task Implement user authentication with JWT
```

**`/update-task`** - Update task status
```
/update-task 042 status=completed
```

**`/status`** - Get project status overview
```
/status
```

### Planning & Design

**`/start-planning`** - Begin feature planning
```
/start-planning User authentication system
```

**`/add-feature`** - Add new feature to project
```
/add-feature Real-time notifications
```

### Quality Assurance

**`/quality-report`** - Generate quality metrics
```
/quality-report
```

**`/report-bug`** - Report and track a bug
```
/report-bug Login fails with special characters in password
```

**`/review`** - Perform code review
```
/review src/auth/
```

### GitHub Integration

**`/fix-github-issue`** - Link task to GitHub issue
```
/fix-github-issue #123
```

## Core Rules

### Always-Active Rules

The `.roo-code/rules/always.md` file contains rules that apply to EVERY interaction:

1. **YAML Frontmatter Required** - All task files must have YAML metadata
2. **Task ID Management** - Sequential IDs, zero-padded to 3 digits
3. **Cross-IDE Compatibility** - Changes work in Claude Code, Cursor, Windsurf
4. **Status Synchronization** - Task file YAML and TASKS.md must always match

### Task Management Rules

Located in `.roo-code/rules/task_management.md`:

- File-based task tracking in `.fstrent_spec_tasks/`
- YAML frontmatter for structured metadata
- Status management with emojis ([ ], [🔄], [✅], [❌])
- Dependency tracking and validation
- Sub-task support for complex work

### Planning Workflow Rules

Located in `.roo-code/rules/planning_workflow.md`:

- Product Requirements Document (PRD) creation
- Feature planning questionnaires
- Scope validation to prevent over-engineering
- Acceptance criteria definition
- Subsystem mapping

## Configuration

### settings.json

The `.roo-code/settings.json` file contains:

```json
{
  "roo.taskSystem": "fstrent_spec_tasks",
  "roo.taskDirectory": ".fstrent_spec_tasks",
  "roo.rules.autoLoad": true,
  "roo.commands.customPath": ".roo-code/commands"
}
```

**Key Settings:**
- `taskSystem` - Identifies the task management system in use
- `taskDirectory` - Location of task files
- `rules.autoLoad` - Automatically load all rules on startup
- `commands.customPath` - Location of custom commands

## Integration with Other IDEs

### Shared Data Layer

All IDEs share the same data in `.fstrent_spec_tasks/`:

```
.fstrent_spec_tasks/
├── TASKS.md              # Master task list (shared)
├── PLAN.md              # Project plan (shared)
├── PROJECT_CONTEXT.md   # Project context (shared)
├── BUGS.md              # Bug tracking (shared)
├── tasks/               # Individual task files (shared)
└── features/            # Feature documentation (shared)
```

### IDE-Specific Directories

Each IDE has its own configuration:

- `.claude/` - Claude Code configuration
- `.cursor/` - Cursor IDE rules (.mdc format)
- `.roo-code/` - **Roo-Code configuration** (you are here)
- `.cline/` - Cline extension configuration
- `.windsurf/` - Windsurf IDE configuration

### Cross-IDE Workflow

**Scenario:** Team uses multiple IDEs

1. **Developer A** (Roo-Code) creates task:
   - Uses `/new-task` command
   - Task file created in `.fstrent_spec_tasks/tasks/`
   - TASKS.md updated

2. **Developer B** (Cursor) sees the task:
   - Opens same repository
   - Cursor reads `.fstrent_spec_tasks/TASKS.md`
   - Can update task using Cursor commands

3. **Developer C** (Claude Code) completes task:
   - Updates task status to completed
   - Both task file YAML and TASKS.md updated
   - All other developers see completion

**Result:** Seamless collaboration regardless of IDE choice!

## File Locations Reference

### Task Files
**Location:** `.fstrent_spec_tasks/tasks/`
**Naming:** `task{id}_descriptive_name.md`
**Example:** `task042_implement_authentication.md`

### Master Task List
**Location:** `.fstrent_spec_tasks/TASKS.md`
**Purpose:** Central checklist with status for all tasks

### Project Documentation
- **Context:** `.fstrent_spec_tasks/PROJECT_CONTEXT.md`
- **Plan:** `.fstrent_spec_tasks/PLAN.md`
- **Bugs:** `.fstrent_spec_tasks/BUGS.md`
- **Features:** `.fstrent_spec_tasks/features/`

## Best Practices

### For Roo-Code Users

1. **Use Commands Consistently**
   - Always use `/new-task` instead of manually creating files
   - Let Roo-Code handle YAML frontmatter and task IDs

2. **Check Status Regularly**
   - Run `/status` to see current project state
   - Review TASKS.md before starting new work

3. **Follow Planning Process**
   - Use `/start-planning` for new features
   - Create PRDs for complex functionality
   - Validate scope before implementation

4. **Maintain Quality**
   - Run `/quality-report` regularly
   - Use `/review` before committing code
   - Track bugs with `/report-bug`

5. **Sync with Team**
   - Commit `.fstrent_spec_tasks/` changes frequently
   - Pull latest before creating tasks
   - Communicate task assignments

## Troubleshooting

### Commands Not Working

**Problem:** Custom commands not recognized

**Solutions:**
1. Check that `.roo-code/commands/` exists
2. Verify `settings.json` has correct `commands.customPath`
3. Restart Roo-Code to reload commands
4. Check command file format (markdown with proper structure)

### Rules Not Applying

**Problem:** Roo-Code not following fstrent_spec_tasks rules

**Solutions:**
1. Verify `settings.json` has `rules.autoLoad: true`
2. Check that rule files exist in `.roo-code/rules/`
3. Review rule file format (must be valid markdown)
4. Mention rules explicitly: "Follow the task management rules"

### Task Files Not Recognized

**Problem:** Tasks not appearing in system

**Solutions:**
1. Check YAML frontmatter is present and valid
2. Verify task file is in `.fstrent_spec_tasks/tasks/`
3. Ensure task entry exists in TASKS.md
4. Validate task ID is unique and properly formatted

### Cross-IDE Sync Issues

**Problem:** Changes in Roo-Code not visible in other IDEs

**Solutions:**
1. Commit and push changes to git
2. Other developers pull latest
3. Check that task files follow standard format
4. Verify no file conflicts in `.fstrent_spec_tasks/`

## Advanced Features

### Custom Rule Extension

You can add your own rules to `.roo-code/rules/`:

```markdown
# my_custom_rule.md

When working with API endpoints:
- Always validate input parameters
- Return proper HTTP status codes
- Log all errors with context
- Include request/response examples in docs
```

Roo-Code will automatically load and apply this rule.

### Command Customization

Create custom commands in `.roo-code/commands/`:

```markdown
# deploy.md

Deploy the application to staging:

1. Run all tests
2. Build production bundle
3. Create deployment package
4. Upload to staging server
5. Run smoke tests
6. Notify team in Slack
```

### Model Selection

Roo-Code supports multiple AI models. Configure in settings:

```json
{
  "roo.model.default": "claude-sonnet-4",
  "roo.model.fallback": "gpt-4-turbo"
}
```

### Team Collaboration

For team workflows, add to settings:

```json
{
  "roo.team.assignmentTracking": true,
  "roo.team.notifyOnTaskChange": true,
  "roo.team.slackWebhook": "https://hooks.slack.com/..."
}
```

## Resources

### Documentation
- **Main Documentation:** `agents.md` in project root
- **Task System Guide:** `.claude/skills/fstrent-task-management/SKILL.md`
- **Planning Guide:** `.claude/skills/fstrent-planning/SKILL.md`
- **QA Guide:** `.claude/skills/fstrent-qa/SKILL.md`

### Examples
- **Example Tasks:** `.fstrent_spec_tasks/tasks/`
- **Example Project:** `example-project/`
- **Command Examples:** Each command file contains usage examples

### External Links
- **agents.md Standard:** https://agents.md
- **Roo-Code Docs:** https://roo.code/docs (verify URL)
- **fstrent_spec_tasks GitHub:** (your repository URL)

## Migration from Other IDEs

### From Cursor

Cursor uses `.mdc` rule files, but the underlying task system is identical:

1. Open project in Roo-Code
2. All `.fstrent_spec_tasks/` files work immediately
3. Use Roo-Code commands instead of Cursor commands
4. Everything else stays the same!

### From Claude Code

Claude Code uses skills system, Roo-Code uses rules:

1. Task files work identically
2. Commands have same functionality, different syntax
3. Both follow agents.md standard
4. No data migration needed

### From VS Code + Cline

Cline configuration in `.cline/` won't interfere:

1. Install Roo-Code extension
2. Roo-Code reads `.roo-code/` configuration
3. Can use both simultaneously
4. Shared `.fstrent_spec_tasks/` data

## Support

### Getting Help

1. **Check Documentation:** Start with `agents.md` and this README
2. **Review Examples:** Look at existing task files and commands
3. **Check Troubleshooting:** See section above
4. **Ask in Chat:** Mention the specific issue you're facing

### Reporting Issues

If you find bugs in the Roo-Code configuration:

1. Use `/report-bug` command to create bug task
2. Include Roo-Code version and system info
3. Provide steps to reproduce
4. Attach relevant files or screenshots

### Contributing

To improve the Roo-Code configuration:

1. Test changes thoroughly
2. Update documentation
3. Ensure cross-IDE compatibility
4. Submit pull request with clear description

---

**Happy Coding with Roo-Code!** 🦘

The fstrent_spec_tasks system makes your AI assistant a true development partner, and Roo-Code's flexibility makes it even more powerful.

**Questions?** Ask your AI assistant - it knows these rules!
