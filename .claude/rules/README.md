# .claude/rules/ - Generic Rules Directory

**Purpose:** Rules in this folder are loaded for EVERY Claude Code conversation, regardless of context.

**Use Cases:** Critical requirements, always-applicable guidelines, frequently-needed reminders.

**Warning:** Every file here uses context tokens. Keep minimal!

---

## What Goes Here vs What Goes in Skills

### `.claude/rules/` - Always-Loaded Generic Rules

**Loaded:** Every single conversation
**Cost:** Uses context tokens always
**Size:** Keep under 100 lines per file
**Content:** Critical requirements, format reminders, skill invocation hints

**Examples:**
- `always.md` - Universal guidelines (file size limits, available tools)
- `documentation.md` - Doc file placement rules
- `task_management.md` - Critical YAML format requirement for tasks
- `git_workflow.md` - Git commit conventions

### `.claude/skills/{skill-name}/rules.md` - Lazy-Loaded Skill Rules

**Loaded:** Only when skill is invoked
**Cost:** Zero context cost when not used
**Size:** Can be 500+ lines
**Content:** Complete implementation details, all edge cases, full specifications

**Examples:**
- `.claude/skills/fstrent-task-management/rules.md` - Complete task system rules
- `.claude/skills/fstrent-planning/rules.md` - Full planning workflow
- `.claude/skills/web-tools/rules.md` - Detailed web scraping procedures

---

## Decision Tree: Should I Create a Rule File?

```
Is this requirement CRITICAL to project success?
│
├─ YES → Does it have strict format requirements?
│         │
│         ├─ YES → Will AI likely forget or do wrong?
│         │         │
│         │         ├─ YES → CREATE RULE FILE ✅
│         │         │         (75-100 lines max)
│         │         │
│         │         └─ NO → Skill description might be enough
│         │
│         └─ NO → Is it used in 80%+ of projects?
│                  │
│                  ├─ YES → CREATE BRIEF POINTER ✅
│                  │         (20-30 lines)
│                  │
│                  └─ NO → SKIP, let skill handle it ❌
│
└─ NO → Is it used frequently?
          │
          ├─ YES → CREATE MINIMAL POINTER ✅
          │         (10-20 lines)
          │
          └─ NO → SKIP, let skill handle it ❌
```

---

## Current Rule Files

### always.md (Universal)
**Size:** ~60 lines
**Purpose:** Guidelines that apply to ALL conversations
**Content:**
- File size management (refactoring at 800/900/1000 lines)
- Available MCP tools reminder
**Justification:** Core workflow principles, always relevant

### documentation.md (Universal)
**Size:** ~160 lines
**Purpose:** Where to put documentation files
**Content:**
- Doc files go in `docs/` with timestamps
- Naming convention: `YYYYMMDD_HHMMSS_IDE_TOPIC.md`
- Root exceptions (README, LICENSE, etc.)
**Justification:** Prevents root clutter, always applicable

### git_workflow.md (Universal)
**Size:** ~200 lines
**Purpose:** Git commit conventions and workflow
**Content:**
- Commit message format
- Branch naming
- PR conventions
**Justification:** Every git operation should follow these

### powershell.md (Context-Specific)
**Size:** ~100 lines
**Purpose:** Windows PowerShell helpers
**Content:**
- Common PowerShell commands
- Path handling on Windows
**Justification:** Windows-specific, helpful for Windows users

### virtual_environments_python.md (Context-Specific)
**Size:** ~100 lines
**Purpose:** Python virtual environment guidelines
**Content:**
- venv creation and activation
- Dependency management
**Justification:** Python projects need this

### task_management.md (CRITICAL)
**Size:** ~500 lines
**Purpose:** **MISSION CRITICAL** - YAML format requirement for tasks
**Content:**
- YAML frontmatter REQUIRED warning
- Complete format specification
- Wrong vs correct examples
- Validation checklists
**Justification:**
- Most critical aspect of template
- Breaking format breaks entire system
- Cross-IDE compatibility depends on it
- 61 tasks created wrong without this
- Context cost justified by enforcement need

**Note:** A minimal 75-line version exists at:
`.claude/skills/fstrent-task-management/task_management_rules_minimal.md.txt`
This can be tested in future to see if shorter version is sufficient.

---

## File Size Guidelines

### Mission-Critical (75-500 lines)
**When:** Absolutely must be enforced, breaking consequences
**Example:** task_management.md
**Tradeoff:** High context cost, but justified by criticality

### Important (30-75 lines)
**When:** Frequently needed, has format preferences
**Example:** Hypothetical "planning_format.md"
**Tradeoff:** Moderate context cost, high value

### Helpful (10-30 lines)
**When:** Nice reminder, points to skill
**Example:** Hypothetical "web_tools_hint.md"
**Tradeoff:** Low context cost, occasional value

### Maximum Limit
**Hard limit:** 500 lines per file
**Soft limit:** 100 lines per file
**Total limit:** Try to keep entire `.claude/rules/` folder under 1500 lines

---

## Pattern: Pointer + Details

**Good Pattern:**

`.claude/rules/skill_name.md` (50 lines):
```markdown
# Skill Name - Brief Purpose

## Critical Requirement
[Minimal example of required format]

## Common Mistakes
❌ WRONG: [brief example]
✅ CORRECT: [brief example]

## Full Details
See: .claude/skills/skill-name/rules.md
```

`.claude/skills/skill-name/rules.md` (500 lines):
```markdown
[Complete implementation details]
[All edge cases]
[Full specifications]
```

**Bad Pattern:**

`.claude/rules/skill_name.md` (500 lines):
```markdown
[Entire skill rules copied here]
```

`.claude/skills/skill-name/rules.md` (500 lines):
```markdown
[Duplicate of above]
```

---

## When to Create New Rule Files

### ✅ Create rule file if:
1. **Critical format** that AI often gets wrong
2. **Used in 80%+ of projects** in template
3. **Breaking consequences** if done incorrectly
4. **Can't rely on skill auto-triggering**
5. **Short enough** to not waste too much context (<100 lines ideal)

### ❌ Don't create rule file if:
1. **Optional/niche** - only some projects need it
2. **Skill description sufficient** - clear from skill name/description
3. **User explicitly invokes** - they know when they need it
4. **No format requirements** - flexible usage
5. **Would be too long** (>500 lines) - keep in skill

---

## Testing Impact

### To Test Context Usage

**Before adding rule file:**
1. Start new conversation
2. Check context usage (Claude shows token count)
3. Note baseline

**After adding rule file:**
1. Start new conversation
2. Check context usage
3. Calculate difference

**Decision:**
- <100 tokens added? ✅ Acceptable
- 100-500 tokens added? ⚠️ Justify the value
- >500 tokens added? ❌ Too expensive, move to skill

### To Test Enforcement

**Without rule file:**
1. Create fresh project from template
2. Ask AI to complete task/feature
3. Check if AI follows format correctly

**With rule file:**
1. Create fresh project from template
2. Ask AI to complete task/feature
3. Check if AI follows format correctly

**Compare:** Does rule file improve compliance significantly?

---

## Maintenance

### Regular Audits
- **Quarterly:** Review each rule file
- **Ask:** Is this still needed?
- **Ask:** Can this be shorter?
- **Ask:** Should this move to skill?

### Signs a Rule File Should Be Removed
- ❌ Rarely relevant to conversations
- ❌ Duplicates skill content
- ❌ Too long (>500 lines)
- ❌ Not improving AI behavior
- ❌ Context cost > value

### Signs a Rule File Should Be Added
- ✅ AI consistently makes same mistake
- ✅ Critical format often wrong
- ✅ Skill not auto-triggering reliably
- ✅ Can be kept brief (<100 lines)
- ✅ Used in most projects

---

## For Template Users (AI Agents)

**As an AI agent using this template:**

1. **Read all files in `.claude/rules/`** - They apply to you
2. **Follow the guidelines** - They're mandatory, not optional
3. **Check for skill hints** - Some rules point to skills
4. **Invoke skills when needed** - Skills have complete details
5. **Don't duplicate content** - Rules and skills work together

**If you see a requirement in rules:**
- Follow it exactly
- Check if skill mentioned
- Invoke skill for complete workflow

---

## For Template Developers

**When adding new skill to template:**

1. **Create skill in `.claude/skills/{skill-name}/`**
2. **Add SKILL.md** with description and triggers
3. **Add rules.md** with complete implementation
4. **Decide:** Does this need a rule pointer?
   - Check decision tree above
   - Consider criticality and frequency
   - Evaluate context cost vs value
5. **If yes:** Create minimal pointer in `.claude/rules/`
   - Keep under 100 lines
   - Critical requirements only
   - Link to full skill rules
6. **If no:** Skill description is sufficient

**Template for deciding:**
- Critical + strict format? → Yes, create rule
- Important + frequent? → Maybe, test both ways
- Optional + flexible? → No, skill is enough

---

## Example Workflow: Adding Planning Rule

**Scenario:** fstrent-planning skill exists, considering rule pointer.

**Analysis:**
- **Critical?** Somewhat - PRDs are important
- **Strict format?** Yes - preferred structure for PRDs
- **Frequent?** Yes - most projects start with planning
- **Breaking if wrong?** No - annoying but not broken
- **Can be brief?** Yes - ~40 lines

**Decision:** Create brief pointer

**File:** `.claude/rules/planning_prd_format.md` (~40 lines)
```markdown
# Planning - PRD Format Reminder

## When to Use
Starting new project or feature? Create PRD first.

**Invoke:** fstrent-planning skill

## Preferred Format
`.fstrent_spec_tasks/PLAN.md`:
- Vision & Goals
- Features (high-level)
- Success Metrics
- Out of Scope

## Common Mistake
❌ Don't start coding before PRD
✅ Do create PRD, get feedback, then code

**Full workflow:** `.claude/skills/fstrent-planning/SKILL.md`
```

---

## Context Budget

**Total context available:** ~200K tokens per conversation
**Rule files should use:** <2% (~4K tokens max)

**Current usage (estimated):**
- always.md: ~300 tokens
- documentation.md: ~800 tokens
- git_workflow.md: ~1000 tokens
- task_management.md: ~2500 tokens
- Other files: ~400 tokens
- **Total:** ~5000 tokens (~2.5% of context)

**Status:** Within budget, but monitor additions carefully

**If adding new rule file:**
- Estimate tokens (roughly 2 tokens per word)
- Check if total stays under 4-5K tokens
- Remove or shrink existing rules if needed

---

## Summary

**Rules Folder Purpose:**
- Always-loaded reminders for critical requirements
- Minimal pointers to skills
- Universal guidelines

**Keep It Lean:**
- Only truly critical content
- Brief format examples
- Link to skills for details

**Balance:**
- Enforcement (rules always visible)
- vs
- Context efficiency (skills loaded on-demand)

**Mission Critical Exception:**
- task_management.md is 500 lines
- Justified by absolute criticality
- Minimal version available for future testing

---

**For questions about whether to add a rule file, see:**
`_TEMPLATE_skill_pointer.md` - Template and decision guide
