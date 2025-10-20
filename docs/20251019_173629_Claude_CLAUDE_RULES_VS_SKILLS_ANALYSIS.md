# Claude Code: Rules vs Skills Analysis

**Date:** 2025-10-19
**Questions:**
1. Are you capable of using rules files in `.claude/rules/`, and is that the correct way?
2. Will Skills (fstrent-planning, fstrent-qa, fstrent-task-management) work correctly enough to approximate the Cursor rules?

---

## Quick Answers

### Question 1: Can Claude Code Use Rules Files?

**Answer: ⚠️ YES, but Rules ≠ Skills (Different Purposes)**

| Feature | `.claude/rules/` | `.claude/skills/` |
|---------|------------------|-------------------|
| **Purpose** | General coding guidelines | Specialized workflows with context management |
| **When Loaded** | Always (like Cursor .mdc files) | Only when relevant (progressive disclosure) |
| **Context Impact** | Uses context constantly | Minimal until activated |
| **Best For** | Project-wide conventions | Specific repeatable tasks |
| **Similar To** | Cursor's `.mdc` files | Custom Anthropic Skills system |

---

### Question 2: Will Skills Approximate Cursor Rules?

**Answer: ⚠️ PARTIALLY - Skills are Better for Some Things, Rules for Others**

**Skills Advantages:**
- ✅ Progressive disclosure (doesn't bloat context)
- ✅ Automatic activation based on user intent
- ✅ Can include tools, scripts, examples
- ✅ Hierarchical reference materials

**Rules Advantages:**
- ✅ Always active (no need to "trigger")
- ✅ Enforce project-wide conventions
- ✅ Simpler mental model
- ✅ Direct Cursor compatibility

**Recommendation: Use BOTH!** (See strategy below)

---

## Deep Dive: Rules vs Skills

### What Are .claude/rules/ Files?

**Purpose:** Project-wide coding guidelines that are ALWAYS active

**Think of them as:**
- Cursor's `.mdc` files
- Windsurf's rules
- Roo-Code's conventions
- Global coding standards

**Example (Your virtual_environments_python.md):**
```markdown
# Python Virtual Environment Management

## UV Package Manager

**CRITICAL**: This project uses UV...

1. Always use `uv venv`
2. Never use `python -m venv`
3. Keep requirements.txt and pyproject.toml in sync
```

**When Active:** ALWAYS (every chat/task)

**Context Cost:** Full file loaded into every conversation

---

### What Are .claude/skills/ ?

**Purpose:** Specialized workflows activated ONLY when relevant

**Think of them as:**
- Domain-specific agents
- Task-specific toolkits
- Modular instruction sets

**Example (Your fstrent-task-management):**
```
SKILL.md (metadata: ~500 words)
↓ When activated
rules.md (detailed implementation: ~8,500 words)
↓ When needed
reference/ (examples, schemas, etc.)
```

**When Active:** Only when user mentions tasks/planning/QA

**Context Cost:**
- Initially: ~150 tokens (just metadata)
- When activated: ~5,000 tokens (rules.md)
- When needed: Access reference materials

---

## Your Current Setup: Analysis

### Cursor Rules Structure

```
.cursor/rules/
├── always.mdc (562 bytes)
├── powershell.mdc (2.3 KB)
├── silicon_valley_personality.mdc (11 KB)
├── virtual_environments_python.md (3.4 KB)
└── fstrent_spec_tasks/
    └── rules/
        ├── _index.mdc
        ├── plans.mdc (10.4 KB)
        ├── qa.mdc (8.3 KB)
        ├── rules.mdc (8.1 KB)
        └── workflow.mdc (7.8 KB)
```

**Total:** ~51 KB of rules loaded ALWAYS in Cursor

---

### Claude Code Setup (Current)

**Rules:**
```
.claude/rules/
└── virtual_environments_python.md (3.4 KB)
```

**Skills:**
```
.claude/skills/
├── fstrent-task-management/
│   ├── SKILL.md (~500 words)
│   ├── rules.md (~8,500 words)
│   ├── reference/
│   └── examples/
├── fstrent-planning/
│   ├── SKILL.md
│   ├── rules.md (~9,000 words)
│   ├── reference/
│   └── examples/
└── fstrent-qa/
    ├── SKILL.md
    ├── rules.md (~8,000 words)
    ├── reference/
    └── examples/
```

**Skills Total:** ~25,500 words (~68,000 characters)

---

## Context Management Comparison

### Cursor Approach (All Rules Always Loaded)

**Every conversation starts with:**
```
Context Window Used:
✓ always.mdc (562 bytes)
✓ powershell.mdc (2.3 KB)
✓ silicon_valley_personality.mdc (11 KB)
✓ virtual_environments_python.md (3.4 KB)
✓ plans.mdc (10.4 KB)
✓ qa.mdc (8.3 KB)
✓ rules.mdc (8.1 KB)
✓ workflow.mdc (7.8 KB)

Total: ~51 KB always loaded
```

**Pros:**
- ✅ Always enforced
- ✅ No activation needed

**Cons:**
- ❌ Context bloat
- ❌ Slower responses
- ❌ Less room for actual work

---

### Claude Code Skills Approach (Progressive Disclosure)

**Every conversation starts with:**
```
Context Window Used:
✓ fstrent-task-management metadata (~150 tokens)
✓ fstrent-planning metadata (~150 tokens)
✓ fstrent-qa metadata (~150 tokens)

Total: ~450 tokens initially
```

**When user says "create a new task":**
```
Additional Context Loaded:
✓ fstrent-task-management/rules.md (~5,000 tokens)
↓ If needed
✓ fstrent-task-management/reference/ (on-demand)
```

**Pros:**
- ✅ Minimal initial context
- ✅ Loads only what's needed
- ✅ More room for complex tasks

**Cons:**
- ⚠️ Must be "triggered" by relevant request
- ⚠️ Not "always enforced" like rules

---

## Answering Your Questions in Detail

### Question 1: Can Claude Code Use Rules Files?

**YES - Here's How:**

**1. Rules Files ARE Supported**
```
.claude/rules/
├── coding_standards.md
├── git_workflow.md
├── testing_requirements.md
└── deployment_process.md
```

**How They Work:**
- Loaded into conversation context
- Applied to all responses
- Similar to Cursor's .mdc files

**2. Rules vs Skills - When to Use Which**

**Use `.claude/rules/` for:**
```markdown
✅ Coding standards (always apply)
✅ Naming conventions
✅ Git commit message format
✅ Testing requirements
✅ Deployment procedures
✅ Security guidelines
✅ Technology stack (UV, Python, etc.)
```

**Use `.claude/skills/` for:**
```markdown
✅ Task management workflows
✅ Project planning processes
✅ QA/bug tracking procedures
✅ Code review checklists
✅ Specific domain knowledge
✅ Repeatable multi-step processes
```

---

### Question 2: Will Skills Work Like Cursor Rules?

**PARTIAL YES - Different But Effective**

**What Skills DO Well (Better than Rules):**

**1. Context Efficiency**
```
Cursor Rules: 51 KB always loaded
Skills: 450 tokens initially → expand when needed
```

**2. Automatic Activation**
```
User: "Create a new task for bug tracking"
Claude: [Activates fstrent-task-management skill automatically]
        [Loads rules.md with task creation workflow]
        [Follows detailed procedures]
```

**3. Hierarchical Information**
```
SKILL.md: "I handle task management"
  ↓
rules.md: "Here's HOW to create tasks"
  ↓
reference/: "Here are examples and schemas"
```

**What Skills DON'T Do (Compared to Rules):**

**1. Always-On Enforcement**
```
❌ Not automatically applied to every response
⚠️ Must be relevant to user's request
⚠️ Won't enforce if not triggered
```

**2. Cross-Cutting Concerns**
```
❌ Can't enforce "always use UV" globally
❌ Can't enforce "always format code this way"
⚠️ Better handled by rules files
```

---

## Recommended Hybrid Strategy

### Best of Both Worlds

**Use `.claude/rules/` for Always-On Guidelines:**

```markdown
.claude/rules/
├── coding_standards.md
│   - Always use TypeScript for new files
│   - Always add JSDoc comments
│   - Always handle errors explicitly
│
├── python_standards.md
│   - CRITICAL: Use UV for package management
│   - Always sync requirements.txt and pyproject.toml
│   - Always use type hints
│
├── git_workflow.md
│   - Commit messages: type(scope): description
│   - Always create feature branches
│   - Always run tests before committing
│
└── project_conventions.md
    - File naming: kebab-case
    - Folder structure standards
    - Import organization rules
```

**Use `.claude/skills/` for Workflow-Specific Processes:**

```markdown
.claude/skills/
├── fstrent-task-management/
│   When: User wants to create/update/manage tasks
│   Loads: Detailed task management workflows
│
├── fstrent-planning/
│   When: User starts project planning or creates PRD
│   Loads: Planning templates, scope validation
│
├── fstrent-qa/
│   When: User reports bugs or does quality checks
│   Loads: Bug tracking procedures, QA workflows
│
└── code-review/
    When: User asks for code review
    Loads: Review checklists, security checks
```

---

## Migration Guide: Cursor Rules → Claude Setup

### Your Cursor Rules Breakdown

**From `.cursor/rules/fstrent_spec_tasks/rules/`:**

| File | Size | Best Claude Location | Reason |
|------|------|---------------------|--------|
| `_index.mdc` | 3.9 KB | → `.claude/rules/` | Always-on index |
| `plans.mdc` | 10.4 KB | → `.claude/skills/fstrent-planning/rules.md` | ✅ Already done! |
| `qa.mdc` | 8.3 KB | → `.claude/skills/fstrent-qa/rules.md` | ✅ Already done! |
| `rules.mdc` | 8.1 KB | → `.claude/skills/fstrent-task-management/rules.md` | ✅ Already done! |
| `workflow.mdc` | 7.8 KB | → `.claude/skills/fstrent-task-management/rules.md` | ✅ Merged in! |

**From `.cursor/rules/`:**

| File | Size | Best Claude Location | Reason |
|------|------|---------------------|--------|
| `always.mdc` | 562 B | → `.claude/rules/always.md` | Always-on guidelines |
| `powershell.mdc` | 2.3 KB | → `.claude/rules/powershell.md` | Always-on for Windows |
| `silicon_valley_personality.mdc` | 11 KB | → `.claude/rules/personality.md` | ⚠️ Fun but expensive |
| `virtual_environments_python.md` | 3.4 KB | → `.claude/rules/python_env.md` | ✅ Already there! |

---

## Your Current Status: Assessment

### ✅ What You Did Right

**1. Created Skills for Workflow-Specific Processes**
```
✅ fstrent-task-management (was rules.mdc + workflow.mdc)
✅ fstrent-planning (was plans.mdc)
✅ fstrent-qa (was qa.mdc)
```

**This is CORRECT!** These are perfect candidates for Skills because:
- They're activated by specific user intents
- They contain multi-step workflows
- They benefit from progressive disclosure
- They're task-specific, not always-on

**2. Used Progressive Disclosure Pattern**
```
SKILL.md: Metadata (~500 words)
rules.md: Detailed implementation (~8,500 words)
reference/: Examples and schemas
examples/: Working examples
```

**This is EXCELLENT!** Matches Anthropic's recommended pattern.

---

### ⚠️ What Could Be Improved

**1. Missing Always-On Rules**

**Current `.claude/rules/`:**
```
.claude/rules/
└── virtual_environments_python.md  (good!)
```

**Should Add:**
```
.claude/rules/
├── virtual_environments_python.md  ✅ (already have)
├── always.md  ⬅️ ADD (from Cursor's always.mdc)
├── powershell.md  ⬅️ ADD (from Cursor's powershell.mdc)
├── coding_standards.md  ⬅️ ADD (general standards)
└── git_workflow.md  ⬅️ ADD (commit message format, etc.)
```

**2. Silicon Valley Personality**

**Current:** 11 KB in Cursor's rules (expensive!)

**Recommendation:**
```
Option A: Skip it (saves 11 KB context)
Option B: Add to .claude/rules/ but be aware of cost
Option C: Make it a Skill activated by "/personality" command
```

**My Recommendation:** Option C - Make it an optional Skill

---

## Will Your Skills Work? (Detailed Answer)

### Comparison Test

**Scenario:** User says "Create a new task for implementing dark mode"

**In Cursor (with rules):**
```
1. rules.mdc loaded (8.1 KB)
2. workflow.mdc loaded (7.8 KB)
3. Cursor follows task creation workflow
4. Creates task file in .fstrent_spec_tasks/tasks/
5. Updates TASKS.md
```

**In Claude Code (with Skills):**
```
1. Metadata: "fstrent-task-management handles tasks" (150 tokens)
2. User intent matches → Skill activated
3. rules.md loaded (~5,000 tokens)
4. Claude follows task creation workflow
5. Creates task file in .fstrent_spec_tasks/tasks/
6. Updates TASKS.md
```

**Result:** ✅ SAME OUTCOME, but Claude uses less context initially

---

### Effectiveness Assessment

| Aspect | Cursor Rules | Claude Skills | Winner |
|--------|-------------|---------------|---------|
| **Task Creation** | ✅ Always knows how | ✅ Knows when activated | Tie |
| **Quality** | ✅ Detailed procedures | ✅ Same procedures | Tie |
| **Activation** | ✅ Always ready | ⚠️ Must trigger | Cursor |
| **Context Usage** | ❌ 51 KB always | ✅ ~450 tokens → 5K when needed | Skills |
| **Complex Tasks** | ❌ Less room for work | ✅ More context available | Skills |
| **Cross-IDE** | ❌ Cursor only | ✅ Claude apps, API, Code | Skills |

**Overall:** Skills are MORE EFFICIENT but require activation

---

## How to Test If Skills Work

### Test 1: Task Creation

**User Says:**
```
"Create a new task for implementing user authentication"
```

**Expected Behavior:**
1. ✅ Claude activates fstrent-task-management skill
2. ✅ Loads rules.md with task creation workflow
3. ✅ Asks for required information (title, priority, etc.)
4. ✅ Creates task file in .fstrent_spec_tasks/tasks/
5. ✅ Updates TASKS.md with new task
6. ✅ Follows Windows-safe emoji conventions

**How to Check:**
- Task file created with proper YAML frontmatter
- TASKS.md updated correctly
- Follows your conventions (emojis, structure, etc.)

---

### Test 2: Project Planning

**User Says:**
```
"I want to start planning a new feature for video streaming"
```

**Expected Behavior:**
1. ✅ Claude activates fstrent-planning skill
2. ✅ Loads planning workflow from rules.md
3. ✅ Guides through PRD creation process
4. ✅ Creates PLAN.md or feature documentation
5. ✅ Follows scope validation procedures

**How to Check:**
- PRD structure matches your templates
- Scope validation questions asked
- Feature documentation created properly

---

### Test 3: Bug Reporting

**User Says:**
```
"I found a bug where the login button doesn't work on mobile"
```

**Expected Behavior:**
1. ✅ Claude activates fstrent-qa skill
2. ✅ Loads QA workflow from rules.md
3. ✅ Guides through bug reporting process
4. ✅ Creates bug task file
5. ✅ Updates quality metrics

**How to Check:**
- Bug task created with proper severity
- Reproduction steps documented
- QA procedures followed

---

## Recommendations

### Immediate Actions

**1. Add Missing Rules Files**
```bash
# Copy Cursor's always.mdc → Claude's rules/
cp .cursor/rules/always.mdc .claude/rules/always.md

# Copy powershell.mdc
cp .cursor/rules/powershell.mdc .claude/rules/powershell.md
```

**2. Test Your Skills**
```
Test task creation: "Create a new task for..."
Test planning: "Start planning a new feature..."
Test QA: "Report a bug where..."
```

**3. Create Index Rule**
```markdown
# .claude/rules/README.md

## Always-On Guidelines

These rules apply to ALL conversations:

1. Python: Use UV (see python_env.md)
2. Git: Follow commit format (see git_workflow.md)
3. PowerShell: Follow conventions (see powershell.md)
4. Testing: Always run before committing

## Skills Available

When you need specialized workflows, Skills activate automatically:

- fstrent-task-management: Task creation, updates, tracking
- fstrent-planning: Project planning, PRDs, features
- fstrent-qa: Bug tracking, quality assurance
```

---

### Long-Term Strategy

**Month 1: Rules for Standards**
```
.claude/rules/
├── always.md (core guidelines)
├── python_env.md (UV requirements) ✅
├── powershell.md (PowerShell conventions)
├── git_workflow.md (commit format, branching)
└── coding_standards.md (general coding rules)
```

**Month 2: Skills for Workflows**
```
.claude/skills/
├── fstrent-task-management/ ✅ (already done)
├── fstrent-planning/ ✅ (already done)
├── fstrent-qa/ ✅ (already done)
├── code-review/ (code review checklist)
└── deployment/ (deployment procedures)
```

**Month 3: Optimization**
```
- Measure context usage
- Identify frequently used skills
- Move ultra-common ones to rules if needed
- Refine skill activation triggers
```

---

## Final Answers

### Question 1: Can Claude Code Use Rules Files?

**✅ YES**

**How:**
- Place `.md` files in `.claude/rules/`
- They're loaded into every conversation
- Similar to Cursor's `.mdc` files
- Use for always-on guidelines

**Currently Using:**
- ✅ `virtual_environments_python.md` (good!)

**Should Add:**
- `always.md` (general guidelines)
- `powershell.md` (PowerShell conventions)
- `git_workflow.md` (git standards)

---

### Question 2: Will Skills Work Like Cursor Rules?

**✅ YES, But Different Approach**

**Skills Work Well For:**
- ✅ Task management (fstrent-task-management)
- ✅ Project planning (fstrent-planning)
- ✅ QA workflows (fstrent-qa)
- ✅ Any workflow-specific process

**Skills Work Differently:**
- ⚠️ Activate based on user intent (not always-on)
- ✅ More context-efficient (progressive disclosure)
- ✅ Same quality once activated

**Recommendation:**
```
✅ Keep Skills for workflows (task, planning, QA)
✅ Add Rules for always-on standards (Python, git, etc.)
✅ Use BOTH together for best results
```

---

## Context Efficiency: Real Numbers

### Cursor Setup

**Every Conversation:**
```
Context Used:
- rules.mdc: 8,100 bytes
- workflow.mdc: 7,800 bytes
- plans.mdc: 10,400 bytes
- qa.mdc: 8,300 bytes
- Other rules: ~16,000 bytes

Total: ~51,000 bytes (51 KB)
Always loaded, whether needed or not
```

---

### Claude Skills Setup

**Every Conversation:**
```
Initial Context:
- fstrent-task-management metadata: ~150 tokens
- fstrent-planning metadata: ~150 tokens
- fstrent-qa metadata: ~150 tokens

Total: ~450 tokens (~1,800 bytes)
```

**When Task Management Needed:**
```
Additional Context:
- rules.md: ~5,000 tokens (~20,000 bytes)

Total: ~5,450 tokens (~21,800 bytes)
Still less than Cursor's always-on 51 KB!
```

**Savings:** ~60% context reduction even when activated!

---

## Bottom Line

**Your Skills Setup is GOOD!** ✅

**What Works:**
- ✅ Converted workflow rules → Skills (correct)
- ✅ Used progressive disclosure (excellent)
- ✅ Proper SKILL.md + rules.md structure

**What to Add:**
- Add always-on rules to `.claude/rules/`
- Copy `always.mdc`, `powershell.mdc` from Cursor
- Create `git_workflow.md` for commit standards

**Will It Work Like Cursor?**
- ✅ YES for workflow-specific tasks
- ✅ MORE EFFICIENT context usage
- ⚠️ Need rules files for always-on guidelines

**Action Plan:**
1. Test your Skills (task creation, planning, QA)
2. Add missing rules files from Cursor
3. Use hybrid approach: Rules + Skills together

**You're 90% there - just need to add the always-on rules!** 🎯
