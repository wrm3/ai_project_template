# TEMPLATE: Skill Pointer Rule File

**Purpose:** This template shows how to create minimal rule files in `.claude/rules/` that point to skills.

**When to use:** When a skill needs to be invoked more reliably, or has critical format requirements.

**Delete this file in your project** - it's just a template!

---

## Decision Tree: Does This Skill Need a Rule Pointer?

### ✅ YES - Create a rule pointer if:

- **Critical format required** (e.g., YAML frontmatter, specific file structure)
- **Used frequently** in most projects (e.g., task management, planning)
- **Easy to do wrong** (many common mistakes possible)
- **Breaking consequences** (wrong format breaks cross-IDE compatibility)
- **Core to template workflow** (essential part of development process)

**Examples:** fstrent-task-management, fstrent-planning, fstrent-qa

### ❌ NO - Skip rule pointer if:

- **Optional/niche use** (only some projects need it)
- **Self-explanatory** (skill description is enough)
- **No format requirements** (flexible usage)
- **User explicitly invokes** (user knows when they need it)
- **Low stakes** (mistakes are easily corrected)

**Examples:** youtube-video-analysis, internal-comms, artifacts-builder

---

## Template Structure

```markdown
# [Skill Name] - [One-Line Purpose]

## When to Use This Skill

**Invoke when:** [Specific scenarios]

**Triggers automatically on:** [Keywords that should invoke skill]

## Critical Requirements (if any)

[If skill has specific format/structure requirements, show minimal example here]

### ⚠️ Common Mistakes

❌ **WRONG:** [Show incorrect approach]

✅ **CORRECT:** [Show correct approach]

## Quick Reference

[30-second checklist or key points]

## Full Documentation

For complete details:
- `.claude/skills/[skill-name]/SKILL.md`
- `.claude/skills/[skill-name]/rules.md`
```

---

## Example 1: Critical Skill (Task Management)

**Characteristics:**
- Used in every project
- Has strict format requirements (YAML)
- Breaking = cross-IDE incompatibility
- Many common mistakes

**Rule file size:** 75-100 lines
**Includes:**
- Critical requirement warning
- Format example
- Wrong vs correct examples
- Validation checklist
- Link to full skill rules

**See:** `.claude/skills/fstrent-task-management/task_management_rules_minimal.md.txt`

---

## Example 2: Medium Criticality Skill (Planning)

**Characteristics:**
- Used frequently
- Has some format preferences
- Mistakes are annoying but not breaking

**Rule file size:** 30-50 lines
**Includes:**
- When to use skill
- Preferred format (brief example)
- Link to full skill rules

```markdown
# Planning - Product Requirements

## When to Use

**Invoke when:**
- Starting new project
- Defining new feature
- Creating PRD document

**Triggers:** "create PRD", "plan feature", "start planning"

## Preferred Format

Planning docs go in `.fstrent_spec_tasks/PLAN.md`

Use structured sections:
- Vision
- Goals
- Features
- Success Metrics

## Full Documentation

`.claude/skills/fstrent-planning/SKILL.md`
```

---

## Example 3: Low Criticality Skill (Web Tools)

**Characteristics:**
- Optional/context-specific
- No format requirements
- User knows when they need it

**Rule file size:** 10-20 lines OR skip entirely

```markdown
# Web Tools - For Web Scraping and Screenshots

## When to Use

Need to scrape a website or take screenshots? Invoke the web-tools skill.

**Triggers:** "scrape", "web search", "screenshot", "browser automation"

**Full docs:** `.claude/skills/web-tools/SKILL.md`
```

**OR** - Don't create rule file at all, let skill description handle it.

---

## Sizing Guidelines

### Mission-Critical (75-100 lines)
- Show format requirement
- Include wrong vs correct examples
- Add validation checklist
- Critical warnings visible

**Examples:** fstrent-task-management

### Important (30-50 lines)
- Brief format preference
- When to invoke
- Key points only

**Examples:** fstrent-planning, fstrent-qa

### Nice-to-Have (10-20 lines)
- One-line purpose
- When to invoke
- Link to skill

**Examples:** web-tools, github-integration

### Optional (0 lines - skip it!)
- Skill description is sufficient
- User explicitly invokes
- No special requirements

**Examples:** youtube-video-analysis, internal-comms, artifacts-builder

---

## Testing Your Rule File

### Size Check
- Under 100 lines? ✅ Good
- 100-200 lines? ⚠️ Consider if all necessary
- Over 200 lines? ❌ Move details to skill rules

### Duplication Check
- Repeating skill rules? ❌ Remove duplicates, link instead
- Unique content? ✅ Good
- Just pointers? ✅ Perfect

### Value Check
- Would I want this loaded every conversation? ✅ Keep it
- Only useful sometimes? ❌ Move to skill
- Provides critical reminder? ✅ Keep it

---

## Activation/Deactivation

### To Deactivate (for testing):
```bash
mv .claude/rules/skill_name.md .claude/skills/skill-name/skill_name_rules.md.txt
```

### To Activate:
```bash
mv .claude/skills/skill-name/skill_name_rules.md.txt .claude/rules/skill_name.md
```

---

## Anti-Patterns (DON'T DO THIS)

### ❌ Copying Entire Skill Rules

**Don't:**
```
.claude/rules/skill_name.md (500 lines - copy of skill rules)
.claude/skills/skill-name/rules.md (500 lines - original)
```

**Do:**
```
.claude/rules/skill_name.md (50 lines - critical points + link)
.claude/skills/skill-name/rules.md (500 lines - full details)
```

### ❌ Too Many Rule Files

**Don't:** Create rules for every skill (15+ files in rules/)

**Do:** Only create rules for critical/frequently-used skills (3-5 files)

### ❌ Vague Pointers

**Don't:**
```markdown
# Planning

Use the planning skill when planning.

See: .claude/skills/fstrent-planning/
```

**Do:**
```markdown
# Planning - Product Requirements

## When to Use
Starting new feature? Create PRD first using planning skill.

**Triggers:** "create PRD", "plan feature"

## Format
PRDs go in .fstrent_spec_tasks/PLAN.md with:
- Vision statement
- Feature list
- Success metrics

**Full docs:** .claude/skills/fstrent-planning/SKILL.md
```

---

## Summary

**Create rule pointer when:**
1. Skill is critical to project workflow
2. Has strict format requirements
3. Easy to forget or do wrong
4. Used in most/all projects

**Keep it minimal:**
- Critical warnings only
- Brief examples
- Link to full skill docs
- Under 100 lines

**Let skills handle details:**
- Full implementation rules stay in skill folder
- Skill loaded only when needed
- Minimal context waste

---

**Delete this template file in your project!**

**Usage:** Reference when deciding if a new skill needs a rule pointer.
