# agents.md - AI Project Template

> **Unified instructions for AI coding agents across all IDEs**  
> This file follows the industry-standard agents.md format (August 2025)  
> Replaces IDE-specific configs: CLAUDE.md, cursor rules, Gemini.md, etc.

**Standard**: [agents.md](https://agents.md) - Adopted by OpenAI, Cursor, Google Jules, Gemini CLI, Factory, Roo-Code

---

## 📋 Project Overview

**AI Project Template** - Multi-IDE development framework for AI-powered coding

**Purpose**: Provide one system that works seamlessly across multiple AI IDEs with:
- **fstrent_spec_tasks**: Task management system (PLAN.md, TASKS.md, tasks/)
- **Cross-IDE compatibility**: Claude Code, Cursor, Windsurf, Roo-Code, Gemini CLI
- **MCP tool integration**: MySQL, Oracle, Browser automation, FTP, Computer Use, Deep Research
- **Comprehensive documentation**: 47,500+ words, 50+ files, example project

**Primary Goal**: Enable teams to collaborate using different AI coding tools without workflow conflicts.

**Repository**: https://github.com/wrm3/ai_project_template

---

## 🚀 Environment Setup

```bash
# Clone repository
git clone https://github.com/wrm3/ai_project_template.git
cd ai_project_template

# No installation required for template usage
# Just copy the IDE configs you need to your project

# For Claude Code users:
cp -r .claude/ your-project/
cp -r .claude-plugin/ your-project/

# For Cursor users:
cp -r .cursor/ your-project/

# For both IDEs (recommended for teams):
cp -r .claude/ .cursor/ .fstrent_spec_tasks/ your-project/
```

### Example Project Setup

```bash
# Run the included Flask example
cd example-project
pip install -r requirements.txt
python src/app.py
# Open http://localhost:5000
```

---

## 📁 Project Structure - Navigation Guide

**IMPORTANT**: Know where things are to avoid exploring the codebase on every chat.

### Core Directories

```
.fstrent_spec_tasks/           # Task management system (READ THIS FIRST)
├── PLAN.md                    # Product Requirements Document
├── TASKS.md                   # Master task checklist with status
├── PROJECT_CONTEXT.md         # Project mission and goals
├── SUBSYSTEMS.md              # Component registry
├── FILE_REGISTRY.md           # File organization documentation
├── MCP_TOOLS_INVENTORY.md     # Available MCP tools
├── tasks/                     # Individual task files (task{id}_name.md)
└── features/                  # Feature specifications

.claude/                       # Claude Code configuration
├── skills/                    # Skills (task-management, planning, qa, youtube-analysis, etc.)
├── agents/                    # Sub-agents (task-expander)
└── commands/                  # Custom commands (/project:* commands)

.cursor/                       # Cursor IDE configuration
└── rules/                     # Rule files (core, planning, qa, workflow)

docs/                          # ALL project documentation
├── 20251020_*_Cursor_*.md    # Timestamped documentation (YYYYMMDD_HHMMSS_IDE_TOPIC.md)
└── research/                  # Research summaries

temp_scripts/                  # Test scripts and utilities

example-project/               # Complete working example
├── src/                       # Flask application code
├── .fstrent_spec_tasks/      # Example task files
└── README.md                  # Example documentation
```

### Quick Navigation

**Want to understand the project?** → Read `.fstrent_spec_tasks/PROJECT_CONTEXT.md`  
**Want to see current tasks?** → Read `.fstrent_spec_tasks/TASKS.md`  
**Want to see the plan?** → Read `.fstrent_spec_tasks/PLAN.md`  
**Want examples?** → Look in `example-project/`  
**Want skills?** → Check `.claude/skills/`  
**Want rules?** → Check `.cursor/rules/`

---

## 🔧 Build & Test Commands

### File-Specific Commands (Preferred - Faster)

**IMPORTANT**: Agents know what file they just modified. Use targeted checks instead of full builds.

```bash
# Python file checks
python -m py_compile path/to/file.py
black --check path/to/file.py
mypy path/to/file.py

# Run specific test
pytest path/to/test_file.py -v

# JavaScript/TypeScript checks
prettier --check path/to/file.tsx
eslint path/to/file.tsx
tsc --noEmit path/to/file.tsx
```

### Full Project Commands (Only When Needed)

```bash
# Example project
cd example-project
pip install -r requirements.txt
python src/app.py

# Full test suite (slower)
pytest tests/ -v

# Full type checking (slower)
mypy src/
```

### PowerShell Commands (Windows)

```powershell
# Get timestamp for documentation
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# Check git status
git status

# Use Invoke-WebRequest instead of curl
Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing
```

---

## 📝 Code Style Guidelines

### Python (PEP 8 - Relaxed Enforcement)

**✅ Do**:
- Use black formatter (88-100 character line length)
- Add type hints where possible
- Write comprehensive docstrings
- Follow PEP 8 naming conventions
- Use pathlib for file operations

**❌ Don't**:
- Use wildcard imports (`from module import *`)
- Ignore type hints in function signatures
- Write functions >50 lines without refactoring
- Use mutable default arguments

**Good Example**: See `example-project/src/app.py` for Flask patterns

### JavaScript/React

**✅ Do**:
- Use ESLint + Prettier configuration
- Use functional components with hooks
- Use React.memo, useCallback, useMemo for performance
- Use TypeScript when available
- Follow component composition patterns

**❌ Don't**:
- Use class-based components (use functional + hooks)
- Ignore prop-types or TypeScript types
- Create deep component hierarchies
- Use inline styles (use CSS-in-JS or modules)

**Good Example**: See `.claude/skills/` for React patterns

### Oracle PL/SQL

**✅ Do**:
- Use business area prefixes (AA\_, AC\_, MG\_, etc.)
- Prefer package APIs over standalone procedures
- Always use bind variables (prevent SQL injection)
- Use bulk operations for large datasets (FORALL, BULK COLLECT)
- Document complex queries

**❌ Don't**:
- Concatenate strings into SQL (SQL injection risk)
- Use SELECT * in production code
- Forget exception handling
- Use autonomous transactions without understanding implications

---

## ✅ Do's and Don'ts

### Project Management Do's

- ✅ **Always check PROJECT_CONTEXT.md** before starting work
- ✅ **Create task files** in `.fstrent_spec_tasks/tasks/` for complex work
- ✅ **Update TASKS.md** when task status changes
- ✅ **Use Windows-safe emojis**: `[ ]` pending, `[🔄]` in-progress, `[✅]` completed, `[❌]` failed
- ✅ **Put documentation** in `docs/` folder with timestamp naming (YYYYMMDD_HHMMSS_IDE_TOPIC.md)
- ✅ **Use MCP tools first** before implementing manually
- ✅ **Test file-specific** commands before running full builds
- ✅ **Follow existing patterns** in codebase

### Project Management Don'ts

- ❌ **Don't put task files in wrong locations** (.fstrent_spec_tasks/ is for core docs only)
- ❌ **Don't create .md files in project root** (use docs/ except README, LICENSE, CLAUDE, CHANGELOG, CONTRIBUTING)
- ❌ **Don't over-engineer** solutions (no auth unless requested, no complex DB unless needed)
- ❌ **Don't ignore .gitignore** (respects research/, secrets/, large files)
- ❌ **Don't skip task documentation** for complex work (>15 minutes)
- ❌ **Don't assume patterns** - check existing code first
- ❌ **Don't commit without testing** relevant file-specific checks

### MCP Tool Usage Do's

- ✅ **Use tool-first principle**: Check available MCP tools before manual implementation
- ✅ **Combine tools in workflows**: Database Read → Web Interaction → Verify
- ✅ **Use browser tools** for web testing and automation
- ✅ **Use database tools** for MySQL and Oracle operations
- ✅ **Use research tools** for deep investigation and web scraping
- ✅ **Use computer use tools** for desktop automation and screenshots

---

## 📚 Good/Bad File Examples

### ✅ GOOD Examples (Follow These Patterns)

**Task Files**:
- `.fstrent_spec_tasks/tasks/task033_implement_agents_md_standard.md` - Proper YAML frontmatter, comprehensive details
- `.fstrent_spec_tasks/tasks/task028_create_computer_use_skill.md` - Clear objectives, acceptance criteria

**Documentation**:
- `docs/20251020_111731_Cursor_PROJECT_RENAME_SUMMARY.md` - Timestamp naming convention
- `docs/20251020_113947_Cursor_AGENTS_MD_RESEARCH_SUMMARY.md` - Comprehensive research summary

**Skills**:
- `.claude/skills/youtube-video-analysis/skill.md` - Complete skill structure with YAML, examples, reference
- `.claude/skills/deep-research/skill.md` - Progressive disclosure pattern

**Code**:
- `example-project/src/app.py` - Clean Flask application structure
- `.claude/agents/task-expander.md` - Well-documented agent with clear activation

### ❌ BAD Examples (Avoid These Patterns)

**File Placement**:
- Putting .md files in root instead of `docs/` (except allowed files)
- Task files without proper YAML metadata
- Documentation without timestamp naming
- Research files outside `docs/research/`

**Code Patterns**:
- Functions >100 lines without refactoring
- Missing error handling
- Hard-coded values instead of environment variables
- SQL string concatenation (use parameterized queries)

---

## 🧪 Testing Instructions

### Before Committing Changes

1. **Run file-specific checks** for files you modified:
   ```bash
   # Python
   python -m py_compile path/to/modified.py
   black --check path/to/modified.py
   
   # JavaScript/TypeScript
   prettier --check path/to/modified.tsx
   eslint path/to/modified.tsx
   ```

2. **Run relevant tests** for affected functionality:
   ```bash
   pytest path/to/test_module.py -v
   ```

3. **Update task status** in TASKS.md if completing tasks

4. **Update documentation** if behavior changed

### Integration Testing

- Test Claude Code skills load correctly
- Test Cursor rules activate properly
- Verify MCP tools connect successfully (check .mcp.json or claude_desktop_config.json)
- Check cross-IDE file compatibility

### Manual Testing Checklist

- [ ] Modified code runs without errors
- [ ] Tests pass for affected functionality
- [ ] Documentation updated if needed
- [ ] Task status updated in TASKS.md
- [ ] No linter errors introduced
- [ ] No security vulnerabilities introduced

---

## 🔒 Security Considerations

### Critical Security Rules

**🚨 NEVER commit sensitive data**:
- API keys, tokens, passwords
- Database credentials
- FTP credentials (use encrypted ftp_sites.json)
- Private keys (.key, .pem, .p12, .pfx files)
- Secrets of any kind

**✅ Use environment variables**:
```bash
# .env (gitignored)
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
DATABASE_URL=your_connection_string
```

**✅ Always use parameterized queries**:
```python
# GOOD - Parameterized (safe)
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# BAD - String concatenation (SQL injection!)
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

**✅ Validate all user input**:
- Sanitize file paths
- Validate URLs before fetching
- Check file sizes before processing
- Verify file types before accepting uploads

**✅ Check .gitignore coverage**:
- `research/` folder (may contain sensitive data)
- `*.log` files
- `*.sqlite`, `*.db` files
- `ftp_sites.json` (encrypted credentials)
- `.env*` files

### MCP FTP Security

For FTP operations, use the encrypted credential system:
- FTP credentials stored in encrypted `ftp_sites.json` (never committed)
- Use `mcp_fstrent_mcp_ftp` tools for secure credential management
- Site profiles keep credentials out of code

---

## 🔗 MCP Tool Integration

### Available MCP Tools

**Task Management & Utilities**:
- `fstrent_mcp_tasks` - Task management, datetime utilities, system setup

**Database Operations**:
- `fstrent_mcp_mysql` - MySQL query/update operations
- `fstrent_mcp_oracle` - Oracle query/execute operations (supports parameterized queries)

**Web & Browser Automation**:
- `fstrent_mcp_browser_use` - Browser automation, web scraping, screenshots
- `mcp_fstrent_mcp_computer_use` - Desktop automation, GUI interaction, local screenshots

**File Transfer**:
- `fstrent_mcp_ftp` - FTP operations with encrypted credential storage (25 tools)

**Research & Analysis**:
- Deep research capabilities with iterative workflows
- Web search and content extraction

### Tool-First Principle

**Before implementing any solution manually, check if an MCP tool exists.**

### Common Tool Workflow Patterns

**Web Testing Workflow**:
1. Database Read → Get expected data
2. Web Interaction → Navigate, click, fill forms
3. Visual Tools → Take screenshots for verification
4. Database Verification → Confirm data changes

**Database Operations Workflow**:
1. Read Current State → Query existing data
2. Make Changes → Execute updates/inserts
3. Verify Changes → Query to confirm

**Research Workflow**:
1. Search → Use web search to find resources
2. Extract → Scrape content from found pages
3. Process → Analyze and synthesize information
4. Document → Save findings to docs/

### MCP Tool Configuration

**Claude Code**: Tools configured in `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

**Cursor**: MCP support varies by version - check Cursor documentation

---

## 📋 Task Management (fstrent_spec_tasks)

### Standard Workflow

1. **Check project context**: Read `.fstrent_spec_tasks/PROJECT_CONTEXT.md`
2. **Review current tasks**: Check `.fstrent_spec_tasks/TASKS.md`
3. **Create task file**: `.fstrent_spec_tasks/tasks/task{id}_descriptive_name.md`
4. **Update master list**: Add entry to TASKS.md
5. **Start work**: Update status to `in-progress`, TASKS.md to `[🔄]`
6. **Complete work**: Update status to `completed`, TASKS.md to `[✅]`

### Task File Format

```yaml
---
id: {number}
title: 'Task Title'
type: feature|bug_fix|refactor|documentation
status: pending|in_progress|completed|failed
priority: critical|high|medium|low
feature: Related Feature Name
subsystems: [affected_components]
project_context: How this task relates to project goals
dependencies: [other_task_ids]
estimated_effort: '2-4 hours'
---

# Task: {title}

## Objective
[Clear, actionable goal]

## Acceptance Criteria
- [ ] Specific outcome 1
- [ ] Specific outcome 2
- [ ] Verification requirement

## Implementation Notes
[Technical details, constraints, approach]
```

### Task Status Emojis (Windows-Safe)

- `[ ]` - Pending
- `[🔄]` - In Progress
- `[✅]` - Completed
- `[❌]` - Failed/Cancelled

### When to Create Tasks

**✅ Create task files for**:
- Work requiring >15 minutes
- Changes affecting multiple files or subsystems
- Features requiring planning or design
- Bug fixes requiring investigation
- Work needing documentation for future reference

**❌ Skip task files for**:
- Simple typo corrections
- Minor formatting adjustments
- Quick documentation updates
- Trivial refactoring

---

## 📄 Documentation Standards

### File Location Rules

**✅ docs/ folder** (ALL documentation except core planning):
- API documentation
- Architecture documents
- User guides
- Technical specifications
- Research summaries
- Setup summaries
- Migration reports
- Troubleshooting guides

**✅ Project root** (ONLY these files):
- README.md
- LICENSE
- CLAUDE.md (symlink to agents.md)
- CHANGELOG.md
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md

**✅ .fstrent_spec_tasks/** (ONLY core planning docs):
- PLAN.md (Product Requirements)
- TASKS.md (Master task list)
- BUGS.md (Bug tracking)
- PROJECT_CONTEXT.md (Project mission)
- SUBSYSTEMS.md (Component registry)
- FILE_REGISTRY.md (File documentation)
- MCP_TOOLS_INVENTORY.md (Tool inventory)

### Naming Convention

**Format**: `YYYYMMDD_HHMMSS_IDE_TOPIC_NAME.md`

**Examples**:
- `docs/20251020_111731_Cursor_PROJECT_RENAME_SUMMARY.md`
- `docs/20251020_113947_Cursor_AGENTS_MD_RESEARCH_SUMMARY.md`
- `docs/20251019_173629_Claude_SETUP_COMPLETE_SUMMARY.md`

**Get timestamp** (PowerShell):
```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
# Creates: 20251020_113947
```

### Auto-Creation Rules

- **Always auto-create** missing folders (docs/, temp_scripts/, etc.)
- **Never ask for confirmation** before creating files
- **Create with proper templates** if file doesn't exist
- **Report what was created** but don't block on it

---

## 🎯 Commit & PR Guidelines

### Commit Message Format

```
type: brief description (50 chars or less)

- Detailed point 1
- Detailed point 2  
- Detailed point 3

Closes #issue_number
```

### Commit Types

- `feat:` - New feature
- `fix:` - Bug fix
- `chore:` - Maintenance tasks (updates, cleanup)
- `docs:` - Documentation changes
- `refactor:` - Code restructuring without behavior change
- `test:` - Adding or updating tests
- `style:` - Code formatting, no logic change
- `perf:` - Performance improvements

### PR Requirements

- [ ] Code follows style guidelines
- [ ] Tests added/updated for changes
- [ ] Documentation updated if needed
- [ ] TASKS.md updated if completing tasks
- [ ] No merge conflicts
- [ ] Cross-IDE compatibility tested (if touching configs)
- [ ] Security considerations addressed

### Example Commit Messages

```
feat: add agents.md standard support

- Created comprehensive agents.md with all best practices
- Added symbolic link from CLAUDE.md for backward compatibility
- Updated documentation to mention agents.md standard
- Tested cross-IDE compatibility with Claude Code and Cursor

Closes #33
```

```
fix: correct file placement in task creation

- Task files now go to .fstrent_spec_tasks/tasks/ correctly
- Documentation files placed in docs/ folder
- Updated task creation validation

Fixes #12
```

---

## 🌐 External Resources

### Project Links

- **GitHub**: https://github.com/wrm3/ai_project_template
- **Issues**: https://github.com/wrm3/ai_project_template/issues
- **Discussions**: https://github.com/wrm3/ai_project_template/discussions

### Standards & Protocols

- **agents.md Standard**: https://agents.md (OpenAI initiative, August 2025)
- **Model Context Protocol (MCP)**: https://modelcontextprotocol.io
- **llms.txt**: LLM web crawling standard (similar to robots.txt)

### IDE Documentation

- **Claude Code**: https://docs.anthropic.com/claude/docs
- **Claude Code Skills**: https://docs.anthropic.com/claude/docs/skills
- **Cursor**: https://cursor.sh/docs
- **Cursor Rules**: https://cursor.sh/docs/rules

### Learning Resources

- **Python**: https://docs.python.org/3/
- **Flask**: https://flask.palletsprojects.com/
- **React**: https://react.dev/
- **Oracle PL/SQL**: https://docs.oracle.com/en/database/

### Design Systems & APIs

- [Add your API documentation links here]
- [Add design system references here]
- [Add team-specific resources here]

---

## 🎨 IDE-Specific Features

### Claude Code

**Skills** (`.claude/skills/`):
- `fstrent-task-management` - Task lifecycle management
- `fstrent-planning` - Project planning and PRD creation
- `fstrent-qa` - Bug tracking and quality assurance
- `youtube-video-analysis` - Extract knowledge from videos
- `deep-research` - Comprehensive AI research
- `research-methodology` - Research workflows

**Commands**:
- `/project:new-task` - Create new task
- `/project:update-task` - Update task status
- `/project:report-bug` - Report a bug
- `/project:start-planning` - Initialize planning
- `/project:status` - Project overview

**Agents** (`.claude/agents/`):
- `task-expander` - Automatically break down complex tasks

### Cursor

**Rules** (`.cursor/rules/fstrent_spec_tasks/`):
- Core task management rules
- Planning system rules
- QA and bug tracking rules
- Workflow management rules
- Code review guidelines

**Commands**:
- `/fstrent_spec_tasks_setup` - Initialize system
- `/fstrent_spec_tasks_plan` - Activate planning
- `/fstrent_spec_tasks_qa` - Activate QA
- `/fstrent_spec_tasks_workflow` - Workflow management

---

## 🚧 Common Pitfalls & Solutions

### File Size Management

**Problem**: Files exceeding 800 lines become harder to maintain

**Solution**:
- Refactor into smaller, focused modules
- Extract reusable functions into utilities
- Split large classes into multiple files
- Use composition over inheritance

**Alert Levels**:
- 800 lines: Consider refactoring
- 900 lines: Should refactor soon
- 1000+ lines: Refactor immediately

### PowerShell Command Issues

**Problem**: `curl` doesn't work in PowerShell (it's an alias)

**Solution**:
```powershell
# Use Invoke-WebRequest instead
Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing

# Or use curl.exe explicitly
curl.exe -s http://localhost:5000

# && doesn't work in PowerShell - use ; instead
cd mydir ; python script.py
```

### Git Large File Issues

**Problem**: ffmpeg binaries (141MB each) exceed GitHub's 100MB limit

**Solution**:
- Already handled by .gitignore (*.exe blocked)
- Local copies remain for your use
- Users cloning should use imageio-ffmpeg or download manually

### MCP Tool Connection Issues

**Problem**: MCP tools not connecting

**Solution**:
1. Check configuration file location (varies by IDE)
2. Verify server names match exactly
3. Ensure Python/Node servers are in PATH
4. Check error logs for specific issues
5. Try restarting the IDE

---

## 🔄 Migration Guide

### From CLAUDE.md

```bash
# This file IS the migration! CLAUDE.md is now a symlink to agents.md
# The symlink was created during Task 033 implementation

# If you need to recreate it:
# Windows
mklink CLAUDE.md agents.md

# Linux/Mac
ln -s agents.md CLAUDE.md
```

### From Cursor Rules

Cursor rules still work alongside agents.md:
- Keep `.cursor/rules/` for Cursor-specific functionality
- agents.md provides shared context across all IDEs
- Rules can reference information in agents.md
- No migration needed - both coexist

### From Multiple Config Files

If you have multiple IDE-specific files:
1. Identify common instructions across all files
2. Merge common content into agents.md
3. Keep IDE-specific details in original locations
4. Create symlinks for backward compatibility
5. Test each tool still works

---

## 📊 Success Metrics

### Agent Performance Indicators

**✅ Good Agent Behavior**:
- Checks PROJECT_CONTEXT.md before starting work
- Uses file-specific commands instead of full builds
- References existing code patterns
- Updates task status proactively
- Creates documentation with proper naming
- Uses MCP tools when available

**❌ Poor Agent Behavior**:
- Explores codebase from scratch every time
- Runs full builds to check single files
- Reinvents patterns instead of following existing
- Forgets to update TASKS.md
- Creates files in wrong locations
- Implements manually when tools exist

### Quality Metrics

- **Task Completion Rate**: % of tasks completed successfully
- **Documentation Coverage**: % of work properly documented
- **Test Coverage**: % of code with tests
- **Code Review Pass Rate**: % passing first review
- **Bug Discovery Rate**: Bugs found per development cycle
- **Velocity**: Story points completed per sprint

---

## 🎯 Future Enhancements

### Planned Features

- [ ] Validation tool to check agents.md completeness
- [ ] Template generator for new projects
- [ ] Sync automation for symlinks
- [ ] Enhanced IDE integration
- [ ] Community example library
- [ ] Monorepo management tools

### Community Contributions

Want to improve this template?
- See CONTRIBUTING.md for guidelines
- Check open issues for opportunities
- Submit PRs with improvements
- Share your agents.md examples

---

**Version**: 1.0  
**Standard**: agents.md (OpenAI Initiative - August 2025)  
**Last Updated**: 2025-10-20  
**Maintained By**: Project Team  
**License**: MIT

**Adopted By**: OpenAI Codex, Cursor, Google Jules, Gemini CLI, Factory, Roo-Code, AmpCode  
**Backward Compatible With**: Claude Code (via CLAUDE.md symlink)

---

*This file provides comprehensive context for AI coding agents, eliminating the need for IDE-specific configuration files. For IDE-specific features, see `.claude/` or `.cursor/` directories.*

