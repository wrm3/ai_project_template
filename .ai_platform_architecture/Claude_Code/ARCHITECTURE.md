# Claude Code Architecture: Deep Dive

**Last Updated**: 2025-10-29
**Purpose**: Comprehensive research documentation covering all Claude Code components and their workflows
**Status**: ✅ Research Complete

---

## Table of Contents

1. [Overview](#overview)
2. [Core Components](#core-components)
3. [Skills System](#skills-system)
4. [SubAgents](#subagents)
5. [Rules vs Skills](#rules-vs-skills)
6. [Plugins & Extensions](#plugins--extensions)
7. [Workflow Patterns](#workflow-patterns)
8. [Component Interactions](#component-interactions)
9. [Best Practices](#best-practices)
10. [Advanced Use Cases](#advanced-use-cases)

---

## Overview

Claude Code is Anthropic's official AI coding assistant as a VSCode extension. It features a unique multi-component architecture that goes beyond simple rule-based systems.

### Key Architectural Principles

1. **Component Isolation** - Skills, SubAgents, and Commands operate independently
2. **Progressive Disclosure** - Load only what's needed when it's needed
3. **Context Preservation** - Each SubAgent maintains isolated context
4. **Tool Scoping** - Granular control over what each component can access
5. **Hierarchical Organization** - Logical grouping of related functionality

### Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (VSCode Extension UI)                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Command Layer                           │
│         /command-name → Command Expansion                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Orchestration Layer                     │
│   Main Claude + Skills Activation + SubAgent Dispatch   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Execution Layer                         │
│    Tool Access (Read, Edit, Write, Bash, Grep, Glob)   │
│              + MCP Tool Integration                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  File System / Project                   │
│           (Source Code, Tests, Documentation)            │
└─────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Main Claude Instance

**Purpose**: Primary AI assistant that orchestrates all other components

**Capabilities**:
- Full tool access (Read, Edit, Write, Bash, Grep, Glob)
- MCP tool integration
- Skills activation
- SubAgent invocation
- Command processing
- Context management

**Workflow**:
```
User Request → Main Claude → Analyze → Decide:
  ├─> Handle directly (simple requests)
  ├─> Activate Skill (domain-specific knowledge)
  ├─> Invoke SubAgent (specialized task)
  └─> Execute Command (pre-defined workflow)
```

### 2. Skills

**Purpose**: Reusable knowledge modules that enhance Claude's capabilities in specific domains

**Location**: `.claude/skills/[skill-name]/SKILL.md`

**Components**:
- `SKILL.md` (required) - Main skill definition
- `rules.md` (optional) - Additional rules
- `scripts/` (optional) - Helper scripts
- `reference/` (optional) - Reference documentation
- `templates/` (optional) - File templates
- `examples/` (optional) - Usage examples

**Activation**:
- **Automatic**: Via `triggers` in YAML frontmatter
- **Manual**: User explicitly mentions skill
- **Proactive**: Claude determines skill is relevant

### 3. SubAgents

**Purpose**: Specialized AI agents with isolated context and scoped tool access

**Location**: `.claude/agents/[agent-name].md`

**Key Characteristics**:
- **Independent Context**: Each agent maintains separate conversation history
- **Tool Scoping**: Can restrict tool access for security
- **Model Selection**: Choose sonnet (balanced), opus (complex), haiku (fast)
- **Proactive Activation**: Use "PROACTIVELY" in description for auto-triggering

**Types**:
1. **Read-Only Agents**: `tools: Read, Grep, Glob`
2. **Full-Access Agents**: `tools: Read, Edit, Write, Bash, Grep, Glob`
3. **MCP-Enabled Agents**: Omit tools field to inherit all MCP tools

### 4. Commands

**Purpose**: Pre-defined workflows that expand into prompts for Claude

**Location**: `.claude/commands/[command-name].md`

**Invocation**: `/command-name [arguments]`

**Processing Flow**:
```
User: /command-name arg1 arg2
  ↓
Command file content + arguments → Main Claude as prompt
  ↓
Claude processes as normal request (can activate Skills/SubAgents)
```

### 5. MCP Tools

**Purpose**: External tool integration via Model Context Protocol

**Configuration**: `.claude/settings.local.json` or VSCode settings

**Access**:
- Main Claude: Automatic access to all MCP tools
- SubAgents: Omit `tools` field to inherit MCP tools
- Skills: Can reference MCP tools in documentation

---

## Skills System

### Skill Anatomy

```yaml
---
name: skill-name              # Unique identifier
description: What skill does  # Used for activation decisions
triggers:                     # Optional keywords for auto-activation
  - keyword1
  - keyword2
  - phrase with spaces
---

# Skill Name

## Overview
[Description of what this skill provides]

## When to Use This Skill
[Conditions that should trigger this skill]

## Capabilities
[What the skill can do]

## Methodology
[Step-by-step approach]

## Examples
[Code examples and usage patterns]

## Reference Materials
[Links to additional resources]

## Tools & Scripts
[If using scripts/ folder, document them here]
```

### Skill Activation Logic

```
User Request
  ↓
Main Claude analyzes:
  1. Check trigger keywords → Match?
     ├─ Yes → Load skill
     └─ No → Continue
  2. Semantic analysis → Relevant domain?
     ├─ Yes → Load skill
     └─ No → Continue
  3. User explicit mention? → Named in request?
     ├─ Yes → Load skill
     └─ No → Process without skill
```

### Skill Types & Examples

#### 1. Domain Knowledge Skills
**Purpose**: Provide expertise in specific domains

**Example**: `document-skills`
- Spreadsheet analysis
- Presentation creation
- Form processing
- Document conversion

#### 2. Methodology Skills
**Purpose**: Guide Claude through specific workflows

**Example**: `fstrent-task-management`
- Task creation workflow
- Status update procedures
- File organization rules
- Naming conventions

#### 3. Integration Skills
**Purpose**: Connect with external systems

**Example**: `youtube-video-analysis`
- Video download procedures
- Transcription processing
- Analysis frameworks
- Output formatting

#### 4. Tool-Enhanced Skills
**Purpose**: Combine knowledge with executable scripts

**Example**: Custom skill with scripts/
```
.claude/skills/data-processing/
├── SKILL.md              # Instructions
├── scripts/
│   ├── extract.py        # Data extraction
│   ├── transform.py      # Data transformation
│   └── requirements.txt  # Dependencies
└── reference/
    └── api_docs.md       # API documentation
```

### Skill Organization Strategies

#### 1. Flat Structure (Simple Projects)
```
.claude/skills/
├── code-review/
├── testing/
├── documentation/
└── deployment/
```

#### 2. Categorized Structure (Medium Projects)
```
.claude/skills/
├── development/
│   ├── code-review/
│   ├── testing/
│   └── refactoring/
├── operations/
│   ├── deployment/
│   ├── monitoring/
│   └── troubleshooting/
└── documentation/
    ├── api-docs/
    └── user-guides/
```

#### 3. Domain Structure (Large Projects)
```
.claude/skills/
├── frontend/
│   ├── react-patterns/
│   ├── component-testing/
│   └── accessibility/
├── backend/
│   ├── api-design/
│   ├── database-optimization/
│   └── security/
└── infrastructure/
    ├── kubernetes/
    ├── ci-cd/
    └── monitoring/
```

---

## SubAgents

### SubAgent Anatomy

```yaml
---
name: agent-name                    # Unique identifier
description: Specialized in X. Use PROACTIVELY for auto-trigger.
tools: Read, Edit, Write, Bash, Grep, Glob  # Or omit for MCP access
model: sonnet                       # sonnet (default), opus, haiku
---

# Agent Name

## Specialization
[What this agent is expert in]

## When to Use
[Situations where this agent should be invoked]

## Tool Access
[Which tools this agent uses and why]

## Approach
[How this agent solves problems]

## Examples
[Usage scenarios]
```

### Model Selection Strategy

| Model | Use Case | Speed | Cost | Capability |
|-------|----------|-------|------|------------|
| **haiku** | Simple tasks, quick responses | Fastest | Lowest | Basic |
| **sonnet** | Most development tasks | Balanced | Medium | Strong |
| **opus** | Complex architecture, difficult problems | Slowest | Highest | Exceptional |

**Guidelines**:
- **haiku**: Code formatting, simple refactoring, documentation updates
- **sonnet** (default): Feature implementation, bug fixing, testing, reviews
- **opus**: System design, complex debugging, architectural decisions

### Tool Scoping Patterns

#### Pattern 1: Read-Only Reviewer
```yaml
---
name: code-reviewer
description: Reviews code for quality and security. Use PROACTIVELY on PRs.
tools: Read, Grep, Glob
model: sonnet
---
```

**Use Case**: Security-sensitive operations where modifications should be prevented

#### Pattern 2: Full-Access Implementer
```yaml
---
name: feature-developer
description: Implements new features end-to-end.
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
---
```

**Use Case**: Complete feature development requiring full file system access

#### Pattern 3: MCP-Enhanced Specialist
```yaml
---
name: database-specialist
description: Database operations and optimization. Use PROACTIVELY for SQL.
# Omit tools field to inherit all MCP tools (MySQL, Oracle, etc.)
model: sonnet
---
```

**Use Case**: Leveraging MCP tools for specialized operations

#### Pattern 4: Script Runner
```yaml
---
name: test-runner
description: Executes tests and analyzes results.
tools: Read, Bash, Grep
model: haiku
---
```

**Use Case**: Fast execution of predefined scripts and result analysis

### SubAgent Lifecycle

```
1. Definition Phase
   - Create agent file in .claude/agents/
   - Define specialization and tools
   - Set model and activation criteria
   
2. Discovery Phase
   - Claude Code loads agent definitions
   - Indexes by specialization
   - Prepares for invocation
   
3. Activation Phase
   - User request matches specialization
   OR
   - Main Claude determines agent is needed
   OR
   - "PROACTIVELY" triggers automatic invocation
   
4. Execution Phase
   - Agent receives isolated context
   - Operates within tool scope
   - Returns results to main Claude
   
5. Completion Phase
   - Agent context released
   - Results integrated
   - Ready for next invocation
```

### SubAgent Communication Patterns

#### Pattern 1: Sequential Delegation
```
Main Claude → SubAgent A → Complete
          ↓
        SubAgent B → Complete
          ↓
    Aggregate Results
```

**Example**: Backend agent implements API, Frontend agent implements UI

#### Pattern 2: Parallel Execution
```
            ┌─> SubAgent A → Complete ─┐
Main Claude ├─> SubAgent B → Complete ─┼─> Aggregate
            └─> SubAgent C → Complete ─┘
```

**Example**: Multiple file reviews happening simultaneously

#### Pattern 3: Hierarchical Delegation
```
Main Claude
    ↓
SubAgent A (Architect)
    ↓
    ├─> SubAgent B (Backend)
    └─> SubAgent C (Frontend)
```

**Example**: Solution architect coordinates backend and frontend developers

---

## Rules vs Skills

### Conceptual Difference

**Rules** (in other platforms):
- Static instructions
- Always active
- No conditional loading
- Simple text files

**Skills** (Claude Code):
- Dynamic knowledge modules
- Conditionally activated
- Can include scripts and resources
- Structured with YAML metadata

### Migration Path

**From Cursor Rules → Claude Code Skills**:

```yaml
# Cursor Rule (.cursor/rules/api-design.mdc)
---
description: API design guidelines
alwaysApply: true
---
# API Design
[Content...]
```

**Becomes**:

```yaml
# Claude Code Skill (.claude/skills/api-design/SKILL.md)
---
name: api-design
description: API design guidelines and best practices
triggers:
  - "api"
  - "endpoint"
  - "REST"
  - "GraphQL"
---
# API Design Skill
[Enhanced content with examples, scripts, reference materials...]
```

### When to Use Each

**Use Rules** (in Cursor/other platforms):
- Project-wide standards
- Simple instructions
- No conditional logic needed
- Static reference material

**Use Skills** (in Claude Code):
- Domain-specific knowledge
- Conditional activation preferred
- Include helper scripts
- Complex workflows
- Multiple related resources

---

## Plugins & Extensions

### Claude Code Plugin System

**Status**: ⚠️ Limited public information

**Known Capabilities**:
- VSCode extension architecture
- MCP tool integration
- Custom tool development
- Settings customization

### MCP as Plugin System

**Model Context Protocol serves as Claude Code's plugin architecture:**

```json
{
  "mcpServers": {
    "custom-plugin": {
      "command": "node",
      "args": ["/path/to/plugin/server.js"],
      "env": {
        "PLUGIN_CONFIG": "value"
      }
    }
  }
}
```

**MCP Plugin Types**:

1. **Tool Plugins**: Add new capabilities (database, browser, FTP)
2. **Resource Plugins**: Provide external data sources
3. **Prompt Plugins**: Add templated workflows
4. **Integration Plugins**: Connect to external services

### Creating Custom MCP Plugins

**Node.js MCP Server Example**:

```javascript
// server.js
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "custom-plugin",
  version: "1.0.0"
});

server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "my_custom_tool",
      description: "What this tool does",
      inputSchema: {
        type: "object",
        properties: {
          param1: { type: "string" }
        }
      }
    }
  ]
}));

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "my_custom_tool") {
    // Tool implementation
    return { result: "Tool output" };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

**Python FastMCP Plugin Example**:

```python
# server.py
from fastmcp import FastMCP

mcp = FastMCP("custom-plugin")

@mcp.tool()
def my_custom_tool(param1: str) -> str:
    """What this tool does"""
    # Tool implementation
    return f"Result for {param1}"

if __name__ == "__main__":
    mcp.run()
```

---

## Workflow Patterns

### Pattern 1: Simple Request → Direct Response

```
User: "Fix this bug in app.py"
  ↓
Main Claude
  ├─ Read app.py
  ├─ Identify issue
  ├─ Edit fix
  └─ Response
```

**When**: Simple, straightforward tasks

### Pattern 2: Skill-Enhanced Workflow

```
User: "Analyze this YouTube video"
  ↓
Main Claude detects "YouTube" trigger
  ↓
Load youtube-video-analysis Skill
  ↓
Main Claude follows Skill methodology:
  ├─ Download video
  ├─ Extract transcript
  ├─ Analyze content
  └─ Generate summary
```

**When**: Domain-specific expertise required

### Pattern 3: SubAgent Delegation

```
User: "Review this pull request"
  ↓
Main Claude
  ↓
Invoke code-reviewer SubAgent
  ├─ Read changed files
  ├─ Check standards
  ├─ Identify issues
  └─ Generate report
  ↓
Main Claude presents formatted results
```

**When**: Specialized task with isolated context

### Pattern 4: Multi-Agent Collaboration

```
User: "Implement user authentication"
  ↓
Main Claude (Orchestrator)
  ↓
  ├─> Backend SubAgent
  │     ├─ Create API endpoints
  │     ├─ Database schema
  │     └─ Auth middleware
  │
  ├─> Frontend SubAgent
  │     ├─ Login component
  │     ├─ Auth state management
  │     └─ Protected routes
  │
  └─> Security SubAgent (Review)
        ├─ Check vulnerabilities
        ├─ Validate crypto
        └─ Test auth flow
```

**When**: Complex feature requiring multiple specializations

### Pattern 5: MCP Tool Integration

```
User: "Check database for inconsistencies"
  ↓
Main Claude
  ↓
Use MCP MySQL Tool
  ├─ Query database
  ├─ Analyze results
  ├─ Identify issues
  └─ Generate report
```

**When**: External system interaction required

### Pattern 6: Command-Initiated Workflow

```
User: "/project:new-task Create auth feature"
  ↓
Command file expands to prompt
  ↓
Main Claude
  ├─ Load fstrent-task-management Skill
  ├─ Create task file
  ├─ Update TASKS.md
  └─ Confirmation
```

**When**: Repeatable workflows benefit from standardization

---

## Component Interactions

### Interaction Matrix

| Initiator | Can Activate | Can Use | Communication |
|-----------|-------------|---------|---------------|
| **Main Claude** | Skills, SubAgents, Commands | All tools + MCP | Direct |
| **Skill** | N/A (passive) | Referenced by Claude | Via Main Claude |
| **SubAgent** | Can invoke other SubAgents | Scoped tools | Via Main Claude |
| **Command** | Skills, SubAgents | N/A (expands to prompt) | Via Main Claude |
| **MCP Tool** | N/A (tool only) | N/A | Called by Claude/SubAgents |

### Communication Flow Examples

#### Example 1: Skill → SubAgent → MCP Tool

```
User requests complex database migration
  ↓
Main Claude loads "database-migration" Skill
  ↓
Skill methodology suggests using SubAgent
  ↓
Main Claude invokes "database-specialist" SubAgent
  ↓
SubAgent uses MCP Oracle Tool
  ↓
SubAgent returns results to Main Claude
  ↓
Main Claude follows Skill's next steps
```

#### Example 2: Command → Multiple Skills → Multiple SubAgents

```
User: "/project:implement-feature Add search functionality"
  ↓
Command expands: "Implement search following best practices..."
  ↓
Main Claude activates:
  ├─ "feature-planning" Skill (planning phase)
  ├─ "backend-developer" SubAgent (API implementation)
  ├─ "frontend-developer" SubAgent (UI implementation)
  └─ "code-reviewer" SubAgent (review phase)
```

---

## Best Practices

### Skill Design Best Practices

1. **Single Responsibility**: Each skill should focus on one domain
2. **Clear Triggers**: Use specific keywords that uniquely identify the skill's domain
3. **Comprehensive Examples**: Include code examples for all major use cases
4. **Progressive Disclosure**: Start simple, add complexity in separate sections
5. **Script Integration**: Package helper scripts with skills when beneficial
6. **Reference Materials**: Link to official docs and standards
7. **Version Documentation**: Note which versions of tools/frameworks are covered

### SubAgent Design Best Practices

1. **Specific Specialization**: Clearly define what makes this agent unique
2. **Appropriate Model**: Match model to task complexity
3. **Minimal Tool Access**: Grant only necessary tools for security
4. **Proactive Triggers**: Use "PROACTIVELY" judiciously for auto-activation
5. **Clear Success Criteria**: Define what constitutes successful completion
6. **Error Handling**: Document how agent should handle failures
7. **Context Management**: Keep agent context focused and relevant

### Command Design Best Practices

1. **Descriptive Names**: Use kebab-case names that clearly indicate purpose
2. **Argument Documentation**: Explain each argument and its purpose
3. **Step-by-Step Process**: Outline exact steps Claude should follow
4. **Expected Outcomes**: Describe what results should look like
5. **Error Scenarios**: Include handling for common failure cases
6. **Example Usage**: Provide several examples with different arguments

### MCP Integration Best Practices

1. **Server Reliability**: Ensure MCP servers handle errors gracefully
2. **Tool Documentation**: Document tool parameters and return values clearly
3. **Security Considerations**: Validate inputs, protect credentials
4. **Performance**: Design tools to be responsive, use async where appropriate
5. **Version Management**: Keep MCP servers updated and compatible
6. **Testing**: Test MCP tools independently before Claude integration

### Organizational Best Practices

1. **Consistent Structure**: Follow same folder patterns across all components
2. **Naming Conventions**: Use kebab-case for files and folders
3. **Documentation Standards**: Keep YAML frontmatter complete and accurate
4. **Version Control**: Track all configuration in git (except settings.local.json)
5. **Team Sharing**: Use relative paths, avoid hardcoded absolute paths
6. **Regular Review**: Audit skills and agents quarterly for relevance

---

## Advanced Use Cases

### Use Case 1: Multi-Stage Development Pipeline

**Scenario**: Implement feature from planning to deployment

**Architecture**:
```
Command: /project:new-feature "Feature Name"
  ↓
Skill: feature-planning (methodology)
  ↓
SubAgent: solution-architect (design)
  ↓
SubAgent: backend-developer (API implementation)
  ↓
SubAgent: frontend-developer (UI implementation)
  ↓
SubAgent: test-engineer (test creation)
  ↓
SubAgent: code-reviewer (review)
  ↓
Skill: deployment-process (deployment steps)
```

### Use Case 2: Cross-Platform Development

**Scenario**: Build feature for web, iOS, and Android

**Architecture**:
```
Main Claude (orchestrator)
  ↓
  ├─> web-developer SubAgent
  │     └─> Uses react-patterns Skill
  │
  ├─> ios-developer SubAgent
  │     └─> Uses swift-patterns Skill
  │
  └─> android-developer SubAgent
        └─> Uses kotlin-patterns Skill

All agents report to main Claude for consistency checks
```

### Use Case 3: Automated Code Quality Pipeline

**Scenario**: Comprehensive code review and improvement

**Architecture**:
```
Commit detected
  ↓
Command: /project:code-review
  ↓
SubAgent: security-scanner (Read, Grep)
  ├─ Checks for vulnerabilities
  └─ Reports security issues
  ↓
SubAgent: performance-analyzer (Read, Grep)
  ├─ Analyzes performance patterns
  └─ Suggests optimizations
  ↓
SubAgent: code-reviewer (Read)
  ├─ Reviews style and standards
  └─ Suggests improvements
  ↓
Main Claude aggregates all findings
  ↓
SubAgent: auto-fixer (Read, Edit, Write)
  └─ Implements simple fixes automatically
```

### Use Case 4: Documentation Generation System

**Scenario**: Generate comprehensive project documentation

**Architecture**:
```
Command: /project:generate-docs
  ↓
Skill: documentation-standards
  ↓
SubAgent: code-analyzer (Read, Grep)
  ├─ Scans codebase
  ├─ Extracts functions, classes
  └─ Identifies patterns
  ↓
SubAgent: doc-writer (Read, Write)
  ├─ Generates API docs
  ├─ Creates usage examples
  └─ Writes README sections
  ↓
SubAgent: diagram-creator (Read, Write)
  ├─ Generates architecture diagrams
  └─> Uses MCP tool for diagram rendering
  ↓
Main Claude assembles final documentation
```

### Use Case 5: Intelligent Debugging Assistant

**Scenario**: Debug complex production issue

**Architecture**:
```
User reports bug
  ↓
Skill: debugging-methodology
  ↓
SubAgent: log-analyzer (Read, Grep, Bash)
  ├─ Parses log files
  ├─> Uses MCP tool for log aggregation
  └─ Identifies error patterns
  ↓
SubAgent: database-inspector (Read)
  └─> Uses MCP MySQL/Oracle tools
      └─ Checks data integrity
  ↓
SubAgent: code-tracer (Read, Grep)
  ├─ Traces execution path
  └─ Identifies root cause
  ↓
SubAgent: fix-implementer (Read, Edit, Write)
  ├─ Implements fix
  └─ Adds error handling
  ↓
SubAgent: test-creator (Read, Write)
  └─ Creates regression test
```

---

## Conclusion

Claude Code's architecture provides unprecedented flexibility for AI-assisted development through its multi-component system. Understanding when and how to use Skills, SubAgents, Commands, and MCP tools enables developers to build sophisticated workflows that adapt to project needs.

**Key Takeaways**:

1. **Skills** provide domain knowledge that enhances Claude's capabilities
2. **SubAgents** offer specialized expertise with isolated context
3. **Commands** standardize repeatable workflows
4. **MCP Tools** integrate external systems seamlessly
5. **Main Claude** orchestrates all components intelligently

**Next Steps**:
- Review research topics in [RESEARCH_TOPICS.md](RESEARCH_TOPICS.md)
- Explore examples in `.claude/skills/` folder
- Experiment with SubAgent creation
- Build custom MCP tools for your project needs

---

**Document Maintenance**:
- Review quarterly for Claude Code updates
- Test examples with new Claude Code versions
- Document new patterns as they emerge
- Share findings with community

**Last Verified**: 2025-10-29
**Next Review**: 2026-01-29

