# IDE Template Adaptation Guide

**Version:** 1.0
**Last Updated:** November 2025

## Purpose

This template framework allows rapid adaptation of the fstrent_spec_tasks system to ANY AI coding IDE in 2-4 hours.

## Supported IDEs (Current)

✅ Claude Code (.claude/)
✅ Cursor (.cursor/)
✅ Windsurf (.windsurf/)
✅ Roo-Code (.roo-code/)
✅ Cline (.cline/)

## Future IDEs (Template Ready)

📋 Gemini CLI
📋 Google Jules
📋 Factory
📋 Pieces
📋 Tabnine
📋 Any future AI IDE

## Quick Adaptation Process

### Step 1: Research IDE (30-60 minutes)

**Questions to Answer:**
1. What is the IDE's configuration directory structure?
   - Examples: `.claude/`, `.cursor/rules/`, `.windsurf/`

2. What file formats does it use?
   - Markdown (.md), MDC (.mdc), JSON, YAML, etc.

3. Does it support custom commands/slash commands?
   - How are they defined?
   - What syntax does it use?

4. Does it support rules/instructions/context files?
   - Where are they located?
   - How are they loaded?

5. Does it support the agents.md standard?
   - Full support, partial support, or none?

6. What AI models does it support?
   - Claude, GPT-4, Gemini, etc.

**Resources to Check:**
- Official IDE documentation
- GitHub repository
- Community forums/Discord
- Example projects

### Step 2: Create Directory Structure (15-30 minutes)

**Copy template:**
```bash
cp -r .ide-template/ .{IDE_NAME}/
```

**Rename files:**
```bash
# Example for hypothetical "CodeAI" IDE
mv .ide-template/ .codeai/
```

**Update README_TEMPLATE.md:**
- Replace `{IDE_NAME}` with actual IDE name
- Replace `{IDE_URL}` with official website
- Replace `{IDE_DESCRIPTION}` with brief description
- Update configuration examples

### Step 3: Adapt Settings (15-30 minutes)

**Edit settings_TEMPLATE.json:**

1. Check IDE's actual settings format
2. Update field names to match IDE conventions
3. Set appropriate default values
4. Remove unsupported options
5. Add IDE-specific settings

**Example transformations:**
```json
// Template
{
  "{IDE_NAME}.taskSystem": "fstrent_spec_tasks"
}

// For CodeAI IDE
{
  "codeai.taskSystem": "fstrent_spec_tasks"
}
```

### Step 4: Convert Rules (60-90 minutes)

**For Each Rule File:**

1. Check IDE's rule file format:
   - Plain markdown (.md)
   - MDC format (.mdc)
   - JSON configuration
   - YAML format

2. Convert from template:
   ```bash
   cp .ide-template/rules/TEMPLATE_always.md .codeai/rules/always.md
   ```

3. Adapt syntax if needed:
   - Some IDEs use YAML frontmatter
   - Some use special syntax markers
   - Some use plain text

4. Update file references:
   - Replace template paths
   - Update command syntax
   - Fix IDE-specific examples

**Rule Files to Adapt:**
- always.md (core rules)
- task_management.md
- planning_workflow.md
- qa_bug_tracking.md
- git_workflow.md
- documentation.md
- python_env.md (if needed)
- parallel_workflow.md (if supported)

### Step 5: Create Commands (60-90 minutes)

**For Each Command:**

1. Determine IDE's command format:
   - Slash commands (/new-task)
   - Natural language (Cline style)
   - Command palette entries
   - Custom syntax

2. Convert from template:
   ```bash
   cp .ide-template/commands/TEMPLATE_new-task.md .codeai/commands/new-task.md
   ```

3. Adapt to IDE syntax:
   - Update trigger mechanism
   - Adjust parameter passing
   - Modify response format
   - Add IDE-specific features

**Commands to Create:**
- new-task
- update-task
- status
- start-planning
- quality-report
- review
- add-feature
- report-bug
- fix-github-issue

### Step 6: Test Integration (30-60 minutes)

**Testing Checklist:**

1. **Load Configuration:**
   - [ ] Open project in IDE
   - [ ] Verify IDE detects configuration
   - [ ] Check rules are loaded
   - [ ] Confirm commands available

2. **Test Task Creation:**
   - [ ] Create new task via command
   - [ ] Verify YAML frontmatter correct
   - [ ] Check TASKS.md updated
   - [ ] Confirm file naming correct

3. **Test Task Updates:**
   - [ ] Update task status
   - [ ] Verify both files updated
   - [ ] Check emoji status correct
   - [ ] Confirm sync maintained

4. **Test Planning:**
   - [ ] Start planning workflow
   - [ ] Create PRD entry
   - [ ] Generate feature file
   - [ ] Verify task breakdown

5. **Cross-IDE Compatibility:**
   - [ ] Open same project in different IDE
   - [ ] Verify tasks visible
   - [ ] Make changes in new IDE
   - [ ] Confirm changes in original IDE

### Step 7: Document (30-60 minutes)

**Complete Documentation:**

1. **README:**
   - Quick start guide
   - Command reference
   - Configuration details
   - Troubleshooting section

2. **Integration Notes:**
   - IDE-specific quirks
   - Known limitations
   - Workarounds
   - Best practices

3. **Examples:**
   - Sample workflows
   - Command usage
   - Common patterns

4. **Update Main README:**
   - Add IDE to supported list
   - Update IDE comparison table
   - Link to IDE-specific docs

## Template Variables

Replace these throughout all template files:

| Variable | Description | Example |
|----------|-------------|---------|
| `{IDE_NAME}` | IDE name (lowercase) | `codeai` |
| `{IDE_DISPLAY_NAME}` | IDE name (display) | `CodeAI` |
| `{IDE_URL}` | Official website | `https://codeai.dev` |
| `{IDE_DESCRIPTION}` | Brief description | `AI coding assistant` |
| `{CONFIG_DIR}` | Config directory | `.codeai/` |
| `{RULES_DIR}` | Rules directory | `.codeai/rules/` |
| `{COMMANDS_DIR}` | Commands directory | `.codeai/commands/` |
| `{SETTINGS_FILE}` | Settings filename | `settings.json` |
| `{COMMAND_PREFIX}` | Command prefix | `/` or `@` |

## IDE Architecture Patterns

### Pattern 1: Rich Structure (Claude Code, Roo-Code)

```
.{ide}/
├── README.md
├── settings.json
├── rules/
│   ├── always.md
│   ├── task_management.md
│   ├── planning_workflow.md
│   ├── qa_bug_tracking.md
│   ├── git_workflow.md
│   ├── documentation.md
│   ├── python_env.md
│   └── parallel_workflow.md
└── commands/
    ├── new-task.md
    ├── update-task.md
    ├── status.md
    ├── start-planning.md
    ├── quality-report.md
    ├── review.md
    ├── add-feature.md
    ├── report-bug.md
    └── fix-github-issue.md
```

**Use when:** IDE supports complex configuration, separate rules and commands

### Pattern 2: Simple Structure (Cline)

```
.{ide}/
├── README.md
├── settings.json
└── rules/
    └── fstrent_spec_tasks.md  # All rules in one file
```

**Use when:** IDE prefers consolidated configuration, natural language commands

### Pattern 3: Cursor-Style (.mdc format)

```
.{ide}/rules/
├── always.mdc  # YAML frontmatter + markdown
├── task_management.mdc
└── commands/
    └── commands.md
```

**Use when:** IDE uses MDC format with YAML frontmatter

## Common Adaptations Needed

### Command Syntax Differences

**Slash Commands (Cursor, Roo-Code):**
```
/new-task Implement user authentication
```

**Natural Language (Cline):**
```
Create a new task for implementing user authentication
```

**At-Mentions (some IDEs):**
```
@assistant new-task Implement user authentication
```

**Command Palette (VS Code extensions):**
```
Cmd+Shift+P → "IDE: New Task"
```

### Rule File Formats

**Plain Markdown:**
```markdown
# Task Management Rules

All tasks must have YAML frontmatter...
```

**MDC Format (Cursor):**
```yaml
---
description: Task management rules
globs: ["**/*.md"]
alwaysApply: true
---

# Task Management Rules

All tasks must have YAML frontmatter...
```

**JSON Configuration:**
```json
{
  "rules": {
    "taskManagement": {
      "yamlRequired": true,
      "statusSync": true
    }
  }
}
```

### Settings Variations

**Standard JSON:**
```json
{
  "ide.taskSystem": "fstrent_spec_tasks"
}
```

**YAML Settings:**
```yaml
taskSystem: fstrent_spec_tasks
taskDirectory: .fstrent_spec_tasks
```

**TOML Settings:**
```toml
[ide]
task_system = "fstrent_spec_tasks"
task_directory = ".fstrent_spec_tasks"
```

## Quality Checklist

Before considering adaptation complete:

### Functionality
- [ ] Tasks can be created with proper YAML
- [ ] Task status can be updated
- [ ] TASKS.md stays synchronized
- [ ] Planning workflow works
- [ ] Quality reporting functions
- [ ] Code review available
- [ ] Bug tracking operational

### Documentation
- [ ] README complete and accurate
- [ ] Commands documented with examples
- [ ] Rules clearly explained
- [ ] Troubleshooting section helpful
- [ ] Quick start guide works

### Cross-IDE Compatibility
- [ ] Same task files work in other IDEs
- [ ] No IDE-specific task data
- [ ] File formats compatible
- [ ] Status emojis consistent
- [ ] Dependencies tracked correctly

### Testing
- [ ] Tested with actual IDE
- [ ] All commands work
- [ ] Rules apply correctly
- [ ] No errors or warnings
- [ ] Edge cases handled

## Tips for Success

### 1. Start with Documentation

Read the IDE's official docs thoroughly before starting. Understanding the IDE's philosophy helps with adaptation.

### 2. Find Example Projects

Look for existing projects using that IDE. See how others structure their configurations.

### 3. Test Incrementally

Don't create everything at once. Test each component:
1. Basic rules → test
2. Add commands → test
3. Add advanced features → test

### 4. Join Community

Most IDEs have Discord servers or forums. Ask questions about configuration best practices.

### 5. Keep It Simple

Start with minimum viable configuration. Add complexity only if needed.

### 6. Maintain Compatibility

Always ensure changes work with other IDEs. Test cross-IDE workflows.

## Support

### Need Help?

1. Check existing IDE adaptations (Claude Code, Cursor, etc.)
2. Review this guide thoroughly
3. Test with example project
4. Ask in project Discord/forum
5. Open GitHub issue if stuck

### Contributing Adaptations

If you create an adaptation for a new IDE:

1. Test thoroughly
2. Document completely
3. Ensure cross-IDE compatibility
4. Submit pull request
5. Add to main README

## Example: Adapting for "CodeAI" IDE

Let's walk through a complete example:

### Research Phase

After researching CodeAI documentation:
- Configuration directory: `.codeai/`
- Format: Plain markdown for rules
- Commands: Slash syntax `/command`
- Supports: agents.md standard
- Models: GPT-4, Claude

### Directory Creation

```bash
mkdir -p .codeai/rules
mkdir -p .codeai/commands
```

### README Adaptation

```bash
cp .ide-template/README_TEMPLATE.md .codeai/README.md
# Edit file, replace all {IDE_NAME} with CodeAI
```

### Settings Creation

```bash
cp .ide-template/settings_TEMPLATE.json .codeai/settings.json
```

Edit to:
```json
{
  "codeai.taskSystem": "fstrent_spec_tasks",
  "codeai.taskDirectory": ".fstrent_spec_tasks",
  "codeai.rules.autoLoad": true,
  "codeai.commands.customPath": ".codeai/commands"
}
```

### Rules Conversion

For each template rule:
```bash
cp .ide-template/rules/TEMPLATE_always.md .codeai/rules/always.md
# Edit file to match CodeAI syntax
```

### Commands Conversion

For each template command:
```bash
cp .ide-template/commands/TEMPLATE_new-task.md .codeai/commands/new-task.md
# Adapt to CodeAI command syntax
```

### Testing

1. Open project in CodeAI
2. Try `/new-task Test task`
3. Verify YAML created correctly
4. Check TASKS.md updated
5. Test in Claude Code to verify compatibility

### Documentation

Update main `README.md`:
```markdown
## Supported IDEs

- Claude Code (.claude/)
- Cursor (.cursor/)
- Windsurf (.windsurf/)
- Roo-Code (.roo-code/)
- Cline (.cline/)
- **CodeAI (.codeai/)** ← NEW!
```

**Total Time:** 3 hours

## Conclusion

This template framework makes it possible to support ANY AI IDE with minimal effort. The key is maintaining the shared `.fstrent_spec_tasks/` data layer while adapting the interface to each IDE's unique style.

**Remember:** The goal is not to create perfect IDE-specific features, but to ensure the core fstrent_spec_tasks workflow functions consistently across all IDEs.

**Happy Adapting!** 🚀
