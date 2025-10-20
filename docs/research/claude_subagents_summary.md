# Claude Code Sub-Agents: Implementation Guide

**Research Date**: 2025-10-20
**Topic**: Claude Code Sub-Agents Implementation and Integration
**Researcher**: Claude Code (Manual Research)
**Project**: ai_project_template

---

## Executive Summary

Claude Code sub-agents are **specialized autonomous agents** that handle specific, complex tasks independently. They are defined as markdown files in `.claude/agents/` with YAML frontmatter and detailed instructions. This project already has **3 working sub-agents** (task-expander, code-reviewer, test-runner), demonstrating production-ready patterns for integration.

**Key Finding**: Sub-agents enable Claude to break complex tasks into manageable pieces, with each agent having specialized knowledge, specific tool access, and autonomous decision-making capabilities.

## What Are Claude Code Sub-Agents?

### Definition
Sub-agents are **specialized, autonomous AI agents** that:
- **Run independently** with their own context and instructions
- **Have specific tool access** (Read, Edit, Write, Grep, Glob, Bash)
- **Make autonomous decisions** within their domain
- **Report results** back to the main conversation
- **Are stateless** (each invocation is independent)

### How They Differ from Regular Skills
| Feature | Skills | Sub-Agents |
|---------|--------|------------|
| **Activation** | Manual (user types `/skill-name`) | Automatic (Claude launches when needed) |
| **Context** | Runs in main conversation | Runs in isolated context |
| **Autonomy** | Guided by user | Fully autonomous execution |
| **Tools** | All tools available | Specific tools defined in YAML |
| **Use Case** | User-initiated workflows | Complex background tasks |

## File Structure

### Location
```
.claude/agents/
├── agent-name.md       # Each agent is a markdown file
├── task-expander.md    # Example: task complexity analyzer
├── code-reviewer.md    # Example: code quality reviewer
└── test-runner.md      # Example: automated testing
```

### File Format

Every sub-agent file has two parts:

#### 1. YAML Frontmatter (Required)
```yaml
---
name: agent-name                    # Unique identifier (kebab-case)
description: When to use this agent # Concise description for Claude
tools: Read, Edit, Write, Grep      # Allowed tools (comma-separated)
---
```

**Available Tools**:
- `Read` - Read files
- `Write` - Create new files
- `Edit` - Modify existing files
- `Grep` - Search code
- `Glob` - Find files by pattern
- `Bash` - Execute commands
- `WebSearch` - Search the web
- `WebFetch` - Fetch web content

#### 2. Agent Instructions (Markdown)
Detailed instructions for the agent including:
- **Purpose**: What the agent does
- **When to Activate**: Trigger conditions
- **Process/Workflow**: Step-by-step procedures
- **Best Practices**: Do's and don'ts
- **Examples**: Real-world scenarios
- **Error Handling**: Edge cases

## Existing Sub-Agents in This Project

### 1. task-expander Agent

**Purpose**: Automatically assess task complexity and break down complex tasks into manageable sub-tasks.

**Key Features**:
- **Complexity scoring system** (1-10+ scale based on 8 criteria)
- **Automatic activation** when tasks mention multiple subsystems or >2 days work
- **Sub-task file creation** with proper YAML frontmatter
- **TASKS.md updates** with indented sub-task entries
- **Dependency management** between sub-tasks

**When It Activates** (Proactive):
- User creates task with multiple subsystems
- Task description mentions >2-3 days of work
- Lists multiple distinct outcomes
- Mentions >5 story points

**Complexity Criteria**:
1. Estimated Effort (4 points) - >2-3 days
2. Cross-Subsystem Impact (3 points) - affects 3+ subsystems
3. Multiple Components (3 points) - 3+ distinct components
4. High Uncertainty (2 points) - unclear requirements
5. Multiple Outcomes (2 points) - 4+ acceptance criteria
6. Dependency Blocking (2 points) - blocks multiple tasks
7. Numerous Criteria (1 point) - >10 acceptance criteria
8. Story Points (1 point) - >5 points

**Complexity Matrix**:
- 0-3 points: Simple (no expansion)
- 4-6 points: Moderate (ask user)
- 7-10 points: Complex (expansion required)
- 11+ points: High Complex (mandatory expansion)

**Sub-Task Naming**: `task{parent_id}.{sub_id}_descriptive_name.md`
- Example: `task42.1_setup_database.md`, `task42.2_implement_api.md`

**Tools**: Read, Edit, Write, Grep, Glob

---

### 2. code-reviewer Agent

**Purpose**: Perform comprehensive code reviews focusing on quality, security, and best practices.

**Review Checklist**:
- **Code Quality**: conventions, DRY, naming, comments
- **Security**: no hardcoded credentials, input validation, SQL injection prevention, XSS prevention
- **Performance**: no bottlenecks, efficient algorithms, optimized queries
- **Testing**: critical path coverage, edge cases
- **Documentation**: API docs, complex logic comments

**Severity Levels**:
- **Critical**: Security issues, data loss risks
- **High**: Bugs, major performance issues
- **Medium**: Code quality, maintainability
- **Low**: Style, minor optimizations

**When to Use**:
- Before merging pull requests
- Explicitly asked to review code
- After major feature implementations
- Code quality concerns raised

**Tools**: Read, Grep, Glob

---

### 3. test-runner Agent

**Purpose**: Run test suites, diagnose failures, and fix them automatically.

**Features**:
- Executes test commands
- Analyzes test failures
- Attempts fixes for common issues
- Re-runs tests to verify fixes
- Reports results

**When to Use**:
- After code changes (PROACTIVE)
- When tests are failing
- Before committing code
- During CI/CD pipeline

**Tools**: Read, Edit, Write, Grep, Glob, Bash

---

## How Claude Uses Sub-Agents

### Invocation Pattern

Claude invokes sub-agents using the `Task` tool:

```markdown
I'll use the task-expander agent to analyze this task's complexity...
```

**Behind the scenes**:
1. Claude calls `Task` tool with agent name
2. Agent runs in isolated context
3. Agent has access only to specified tools
4. Agent returns final report
5. Claude receives results
6. Claude communicates findings to user

### Stateless Nature
- Each invocation is **independent**
- No memory between runs
- Must include all context in prompt
- Results returned in single message

### Parallel Execution
Multiple agents can run concurrently:
```
I'll launch the code-reviewer and test-runner in parallel...
```

## Creating New Sub-Agents

### Step 1: Define the Agent's Purpose
Ask yourself:
- What specific task does this automate?
- When should it activate?
- What tools does it need?
- What output does it produce?

### Step 2: Create the Agent File
```bash
.claude/agents/my-agent-name.md
```

### Step 3: Write YAML Frontmatter
```yaml
---
name: my-agent-name
description: Brief description of when to use this agent (shown to Claude)
tools: Read, Edit, Write, Grep, Glob, Bash
---
```

### Step 4: Write Agent Instructions

**Required Sections**:
1. **Purpose**: Clear statement of what the agent does
2. **When to Activate**: Specific trigger conditions
3. **Process/Workflow**: Step-by-step instructions
4. **Best Practices**: Do's and don'ts
5. **Examples**: Demonstration scenarios

**Optional but Recommended**:
- Error handling
- Integration with other systems
- Success indicators
- Common pitfalls

### Step 5: Test the Agent
1. Create a scenario that should trigger the agent
2. Check if Claude launches it correctly
3. Verify the agent produces expected results
4. Refine instructions based on results

## Agent Design Best Practices

### Clarity
- ✅ **Do**: Write clear, unambiguous instructions
- ✅ **Do**: Provide specific examples
- ✅ **Do**: Define trigger conditions precisely
- ❌ **Don't**: Leave room for interpretation
- ❌ **Don't**: Use vague language

### Autonomy
- ✅ **Do**: Make agents self-sufficient
- ✅ **Do**: Include all necessary decision logic
- ✅ **Do**: Handle edge cases explicitly
- ❌ **Don't**: Require human intervention mid-process
- ❌ **Don't**: Leave critical decisions undefined

### Tool Selection
- ✅ **Do**: Grant only necessary tools
- ✅ **Do**: Consider tool combinations needed
- ❌ **Don't**: Grant all tools by default
- ❌ **Don't**: Restrict tools too much

### Scope
- ✅ **Do**: Keep agents focused on one task
- ✅ **Do**: Make agents composable
- ❌ **Don't**: Create do-everything agents
- ❌ **Don't**: Overlap responsibilities

## Integration Patterns

### 1. Sequential Agent Chain
```
task-expander → code-reviewer → test-runner
```
One agent completes, triggers next

### 2. Parallel Agent Execution
```
code-reviewer (in parallel) test-runner
```
Run multiple agents simultaneously

### 3. Conditional Agent Use
```
IF task_complexity > 7 THEN task-expander
```
Agents activate based on conditions

### 4. Proactive Agent Activation
```
After code changes → AUTOMATICALLY launch test-runner
```
Agents run without explicit user request

## Real-World Examples

### Example 1: Task Expansion Flow

**User Input**:
"Create a task to implement complete user authentication with email/password, OAuth, 2FA, and password reset"

**Agent Activation**:
```
🔍 Analyzing task complexity...
Complexity Score: 12/10 (High Complexity)
⚠️ This task MUST be expanded into sub-tasks

Proposed Sub-Tasks:
1. Setup Authentication Infrastructure
2. Implement Email/Password Authentication
3. Add OAuth Integration
4. Implement Two-Factor Authentication
5. Add Password Reset Flow
6. Create Frontend Authentication Components

Shall I create these sub-tasks?
```

**Agent Creates**:
- 6 sub-task files in `.fstrent_spec_tasks/tasks/`
- Updates TASKS.md with indented entries
- Updates parent task with sub-task references
- Sets up dependency chains

---

### Example 2: Code Review Flow

**User Input**:
"Review this authentication code"

**Agent Activation**:
```
I'll conduct a comprehensive code review...

🔍 Security Review:
✅ No hardcoded credentials
⚠️  Missing input validation on email field
❌ Password is not hashed before storage (CRITICAL)

🔍 Code Quality:
⚠️  Function is 150 lines (should be <100)
✅ Good naming conventions
⚠️  Missing error handling

🔍 Performance:
✅ No obvious bottlenecks
✅ Efficient database queries

Recommendations:
1. CRITICAL: Hash passwords using bcrypt before storage
2. Add email format validation
3. Refactor into smaller functions
4. Add try-catch blocks
```

---

### Example 3: Test Runner Flow

**User Input**: (Makes code changes)

**Agent Activation** (Proactive):
```
🧪 Running tests after code changes...

❌ Tests failed: 3/45 failed
  - test_login: AssertionError
  - test_register: TypeError
  - test_password_reset: NoneType error

🔧 Diagnosing failures...
🔧 Fixing common issues...
✅ Fixed TypeError in registration
✅ Fixed NoneType in password reset
⚠️  Login test still failing - requires manual review

Re-running tests...
✅ Tests passed: 44/45

Remaining issue: test_login
Needs attention: JWT token generation logic
```

## Common Use Cases for New Sub-Agents

### 1. Documentation Generator
**Purpose**: Auto-generate API docs, README sections, or code comments
**Tools**: Read, Write, Grep, Glob
**Activation**: After significant code changes, before releases

### 2. Dependency Updater
**Purpose**: Check for outdated dependencies and update them
**Tools**: Read, Edit, Bash
**Activation**: Weekly/monthly schedule or on-demand

### 3. Performance Analyzer
**Purpose**: Profile code, identify bottlenecks, suggest optimizations
**Tools**: Read, Bash, Grep, Glob
**Activation**: Before production deploys, during performance reviews

### 4. Security Auditor
**Purpose**: Scan for security vulnerabilities, check configurations
**Tools**: Read, Grep, Glob
**Activation**: Before releases, after security-related changes

### 5. Migration Assistant
**Purpose**: Help migrate code between frameworks, versions, or patterns
**Tools**: Read, Edit, Write, Grep, Glob
**Activation**: During major refactoring or upgrades

### 6. API Consistency Checker
**Purpose**: Ensure API endpoints follow conventions and standards
**Tools**: Read, Grep, Glob
**Activation**: Before API releases, during reviews

### 7. Database Schema Validator
**Purpose**: Verify database schemas match models, check migrations
**Tools**: Read, Bash, Grep
**Activation**: Before deploying migrations

### 8. Internationalization (i18n) Manager
**Purpose**: Extract strings, manage translations, verify coverage
**Tools**: Read, Edit, Write, Grep, Glob
**Activation**: Before adding new features with UI

## Advanced Patterns

### Agent Composition
Agents can trigger other agents:
```markdown
# Inside an agent's instructions
If code review identifies test gaps:
  Recommend launching test-coverage-analyzer agent
```

### Dynamic Tool Access
Some agents need more tools than others:
- **Read-Only Agents**: code-reviewer, security-auditor
- **Safe Writers**: documentation-generator, i18n-manager
- **Power Agents**: test-runner, migration-assistant (Read, Edit, Write, Bash)

### Agent Chains
Define workflows where agents run in sequence:
```
feature-planner → task-expander → code-generator → test-runner → code-reviewer
```

## Limitations and Considerations

### Statelessness
- Agents don't remember previous invocations
- Must pass all context in initial prompt
- Can't build knowledge over time

### Context Window
- Each agent gets its own context
- Limited by model's context window
- Must be self-contained

### Tool Restrictions
- Agents only have tools defined in YAML
- Can't request additional tools mid-execution
- Must be granted upfront

### No User Interaction
- Agents can't ask user questions
- Must make autonomous decisions
- Clarifications must be in instructions

### Execution Time
- Complex agents can take minutes
- User should be informed of progress
- Long-running tasks need timeout handling

## Troubleshooting

### Agent Not Activating
**Problem**: Claude doesn't launch your agent
**Solutions**:
- Check description is clear about when to use
- Ensure trigger conditions are obvious
- Make proactive activation explicit in description
- Test with explicit request: "Use the X agent..."

### Agent Produces Wrong Results
**Problem**: Agent completes but output is incorrect
**Solutions**:
- Refine instructions with more examples
- Add error handling sections
- Include edge cases explicitly
- Test with various scenarios

### Agent Fails Mid-Execution
**Problem**: Agent errors out during execution
**Solutions**:
- Check tool access (does it have needed tools?)
- Add error handling instructions
- Test tools individually first
- Review logs for specific errors

### Agent Takes Too Long
**Problem**: Agent runs but takes excessive time
**Solutions**:
- Narrow scope of agent's task
- Optimize instructions for efficiency
- Consider splitting into multiple agents
- Add timeout instructions

## Future Enhancements

### Potential Improvements to This Project

1. **Research Agent** - Autonomous deep research (once dependencies installed!)
2. **Deployment Agent** - Handle deployments, rollbacks, monitoring
3. **Changelog Generator** - Auto-generate changelogs from commits
4. **PR Description Writer** - Create comprehensive PR descriptions
5. **Codebase Analyzer** - Analyze code metrics, generate reports
6. **Dependency Graph Builder** - Visualize project dependencies
7. **Configuration Validator** - Check configs across environments
8. **Accessibility Checker** - Verify WCAG compliance

### Agent Marketplace
Consider creating reusable agents that can be:
- Shared across projects
- Imported from agent libraries
- Customized per project

### Agent Analytics
Track agent performance:
- Success rates
- Execution times
- User satisfaction
- Improvement areas

## Conclusion

Claude Code sub-agents are a powerful way to automate complex, specialized tasks. This project demonstrates production-ready patterns with 3 working agents:

1. **task-expander** - Complexity analysis and task breakdown
2. **code-reviewer** - Comprehensive code quality reviews
3. **test-runner** - Automated testing and fixes

**Key Takeaways**:
- Agents are **markdown files** with YAML frontmatter
- They run **autonomously** with specific tool access
- They're **stateless** and return single reports
- They can be **proactive** (auto-activate) or **manual**
- They excel at **specialized, complex tasks**

**Next Steps**:
1. Study the existing 3 agents in `.claude/agents/`
2. Identify repetitive complex tasks in your workflow
3. Create custom agents for your specific needs
4. Test and refine based on results
5. Build an agent library over time

---

## References

**Project Files**:
- `.claude/agents/task-expander.md` - Task complexity analyzer (369 lines)
- `.claude/agents/code-reviewer.md` - Code quality reviewer (62 lines)
- `.claude/agents/test-runner.md` - Test automation (est. 100 lines)

**Related Skills**:
- `.claude/skills/fstrent-task-management/` - Task file management
- `.claude/skills/fstrent-planning/` - Planning and PRDs
- `.claude/skills/fstrent-qa/` - QA and bug tracking

**Documentation**:
- `CLAUDE.md` - Project overview and structure
- `.fstrent_spec_tasks/` - Task management system

---

**Research Methodology**: Manual analysis of existing project files, pattern extraction, and synthesis of implementation best practices.

**Date**: 2025-10-20
**Researcher**: Claude Code
**Status**: Complete
