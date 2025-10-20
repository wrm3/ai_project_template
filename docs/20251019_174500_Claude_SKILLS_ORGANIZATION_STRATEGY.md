# Skills Organization and GitHub Strategy

**Date:** 2025-10-19 17:45:00
**Created By:** Claude Code

---

## Current Situation

### Skills in Your Project (12 Total)

**Your Custom Skills (4):**
1. `fstrent-task-management` - Your task management system ⭐
2. `fstrent-planning` - Your project planning system ⭐
3. `fstrent-qa` - Your QA/bug tracking system ⭐
4. `fstrent-code-reviewer` - Your code review system ⭐ NEW

**Anthropic Example Skills (7):**
5. `artifacts-builder` - From anthropics/skills repo
6. `document-skills` - From anthropics/skills repo
7. `internal-comms` - From anthropics/skills repo
8. `mcp-builder` - From anthropics/skills repo
9. `skill-creator` - From anthropics/skills repo
10. `template-skill` - From anthropics/skills repo

**Other Skills (2):**
11. `project-setup` - Generic project setup
12. `youtube-video-analysis` - Your enhanced YouTube analyzer ⭐

---

## Understanding `.claude-plugin/`

### What `.claude-plugin/` IS

**Purpose:** Plugin **distribution manifest**, NOT storage

Think of it like:
- `package.json` for npm
- `setup.py` for Python packages
- `Cargo.toml` for Rust crates

**What it contains:**
```json
{
  "name": "fstrent-spec-tasks",
  "version": "1.0.0",
  "description": "...",
  "repository": "https://github.com/fstrent/fstrent-spec-tasks"
}
```

**What it does:**
- Tells Claude Code plugin system what to install
- Provides metadata for marketplace (when available)
- Specifies version, author, dependencies

---

### What `.claude-plugin/` IS NOT

**❌ NOT a storage location for skills**
- Skills don't go IN `.claude-plugin/`
- Skills stay in `.claude/skills/`
- `.claude-plugin/` just describes what to package

**❌ NOT for "inactive" skills**
- Can't store skills there until needed
- Skills are either installed (in `.claude/skills/`) or not

**❌ NOT for reducing context usage**
- Skills already use progressive disclosure
- Only ~150 tokens each initially
- Having 12 skills vs 4 skills = minimal difference

---

## Context Impact: How Many Skills is Too Many?

### Current Context Usage

**12 Skills (Current):**
```
Initial context (metadata only):
- 12 skills × 150 tokens = 1,800 tokens (~7.2 KB)

This is MINIMAL - only 0.9% of 200K context window!
```

**For Comparison:**
- Your `.claude/rules/` files: ~10 KB (always loaded)
- One activated skill: ~5-10 KB additional
- Total with one skill active: ~17-27 KB

**Verdict:** 12 skills is NOT too many! The metadata is negligible.

---

### When Skills Actually Use Context

**Skills only expand when activated:**
```
Initial State:
✓ All 12 skills loaded (metadata): 1,800 tokens

User says: "Create a new task"
→ fstrent-task-management activates
→ Loads rules.md: +5,000 tokens
→ Total: 6,800 tokens (still only 3.4% of context!)

Other 11 skills remain as metadata only
```

**This is the power of progressive disclosure!**

---

## GitHub Strategy Options

### Option 1: Keep Everything in This Template (Recommended for Now)

**Structure:**
```
ai_project_template/
├── .claude/
│   ├── skills/
│   │   ├── fstrent-task-management/    ⭐ Yours
│   │   ├── fstrent-planning/           ⭐ Yours
│   │   ├── fstrent-qa/                 ⭐ Yours
│   │   ├── fstrent-code-reviewer/      ⭐ Yours
│   │   ├── youtube-video-analysis/     ⭐ Yours
│   │   ├── artifacts-builder/          📦 Anthropic
│   │   ├── document-skills/            📦 Anthropic
│   │   └── [other examples]
│   └── rules/
├── .claude-plugin/
│   └── plugin.json  (describes fstrent-spec-tasks bundle)
└── .fstrent_spec_tasks/
```

**Pros:**
- ✅ All-in-one template
- ✅ Easy to clone and start new projects
- ✅ Examples included for reference
- ✅ Single repo to maintain

**Cons:**
- ⚠️ Large repo with all skills
- ⚠️ Includes Anthropic skills you may not use
- ⚠️ Harder to share individual skills

**Best for:**
- Personal project template
- Starting new projects
- Learning/experimentation

---

### Option 2: Separate Repos for Each Skill Bundle (Recommended for Sharing)

**Create Multiple Repos:**

**1. fstrent-spec-tasks (Core)**
```
github.com/fstrent/fstrent-spec-tasks

Contains:
- fstrent-task-management
- fstrent-planning
- fstrent-qa
- fstrent-code-reviewer
- .fstrent_spec_tasks/ system

Purpose: Complete task management system
```

**2. youtube-video-analyzer**
```
github.com/fstrent/youtube-video-analyzer

Contains:
- youtube-video-analysis skill
- Enhanced Python script
- FFmpeg binaries
- Documentation

Purpose: YouTube video analysis with dual-analysis
```

**3. claude-code-project-template**
```
github.com/fstrent/claude-code-project-template

Contains:
- Basic project structure
- Rules files
- Installation instructions
- Links to install skills separately

Purpose: Clean starting template
```

**Pros:**
- ✅ Each skill can be shared independently
- ✅ Clear separation of concerns
- ✅ Easier to maintain versions
- ✅ Users install only what they need
- ✅ Better for street cred (separate stars per repo)

**Cons:**
- ⚠️ More repos to maintain
- ⚠️ Setup requires multiple installs

**Best for:**
- Public sharing
- Building a portfolio
- Getting street cred (GitHub stars)

---

### Option 3: Hybrid Approach (BEST OF BOTH WORLDS)

**Structure:**

**Main Template (Minimal):**
```
github.com/fstrent/claude-code-project-template

Contains:
- .claude/rules/ (always-on guidelines)
- .cursor/rules/ (Cursor compatibility)
- .fstrent_spec_tasks/ (empty structure)
- README with installation instructions
- Links to install skills separately

Does NOT contain skills (except maybe skill-creator)
```

**Separate Skill Repos:**
```
github.com/fstrent/fstrent-spec-tasks
  → fstrent-task-management
  → fstrent-planning
  → fstrent-qa
  → fstrent-code-reviewer
  → Complete .fstrent_spec_tasks/ system

github.com/fstrent/youtube-video-analyzer
  → youtube-video-analysis skill
  → Python scripts
  → Documentation
```

**Installation:**
```bash
# Clone template
git clone https://github.com/fstrent/claude-code-project-template my-project
cd my-project

# Install skills separately
git clone https://github.com/fstrent/fstrent-spec-tasks
cp -r fstrent-spec-tasks/.claude/skills/* .claude/skills/
cp -r fstrent-spec-tasks/.fstrent_spec_tasks .

# Or (when marketplace available):
/plugin install fstrent-spec-tasks@fstrent
```

**Pros:**
- ✅ Clean template for new projects
- ✅ Skills separately shareable
- ✅ Each repo gets its own stars
- ✅ Users pick what they want
- ✅ Best for street cred

**Cons:**
- ⚠️ Multi-step installation
- ⚠️ More complex to explain

**Best for:**
- Public portfolio
- Maximum flexibility
- Street cred opportunities

---

## Recommended Strategy

### Phase 1: Current (Development Phase)

**Keep everything in `ai_project_template`:**
- Develop and test all skills together
- Iterate quickly
- No overhead of multiple repos

### Phase 2: Public Sharing (When Ready)

**Split into separate repos:**

**1. Clean Template Repo**
```
fstrent/claude-code-project-template
- Minimal structure
- Rules files
- Documentation
- Installation guide
```

**2. fstrent-spec-tasks Bundle**
```
fstrent/fstrent-spec-tasks
- 4 task management skills
- .fstrent_spec_tasks system
- Cross-IDE compatible
- 68K words of docs
```

**3. YouTube Video Analyzer**
```
fstrent/youtube-video-analyzer
- youtube-video-analysis skill
- Dual-analysis system
- Cursor + Claude hybrid
- Production-ready
```

**4. (Future) Individual Skills**
```
fstrent/claude-code-reviewer
fstrent/project-setup-skill
fstrent/[other-skills]
```

---

## What to Do with Anthropic Example Skills

### Current Anthropic Skills in Your Template

You have these from `anthropics/skills`:
- `artifacts-builder`
- `document-skills`
- `internal-comms`
- `mcp-builder`
- `skill-creator`
- `template-skill`

### Recommendation: Remove from Public Repo

**Why:**
- These are examples from Anthropic's repo
- Users can clone them directly from `anthropics/skills`
- Reduces your repo size
- Avoids duplication/confusion

**Keep in Local Template:**
- Useful for reference during development
- Can use `skill-creator` to build new skills
- Remove before publishing to GitHub

**Command:**
```bash
# When ready to publish
rm -rf .claude/skills/artifacts-builder
rm -rf .claude/skills/document-skills
rm -rf .claude/skills/internal-comms
rm -rf .claude/skills/mcp-builder
rm -rf .claude/skills/template-skill
# Keep skill-creator if useful, or remove it too
```

---

## Organizing Your Skills

### Your Core Skills (Keep Together)

**fstrent-spec-tasks bundle:**
```
These work as a system:
- fstrent-task-management
- fstrent-planning
- fstrent-qa
- fstrent-code-reviewer

Bundle them in one repo: fstrent-spec-tasks
```

### Standalone Skills (Separate Repos)

**youtube-video-analyzer:**
- Independent functionality
- Not related to task management
- Shareable on its own
- Deserves its own repo and stars

**project-setup:**
- Generic project initialization
- Could be separate or part of template
- Decide based on how often you update it

---

## `.claude-plugin/` Usage

### Current `plugin.json`

Your current `.claude-plugin/plugin.json`:
```json
{
  "name": "fstrent-spec-tasks",
  "version": "1.0.0",
  "description": "Comprehensive task management...",
  ...
}
```

This describes the **fstrent-spec-tasks bundle** only.

### If You Split into Multiple Repos

**fstrent-spec-tasks repo:**
```
.claude-plugin/
└── plugin.json  (describes task management bundle)
```

**youtube-video-analyzer repo:**
```
.claude-plugin/
└── plugin.json  (describes YouTube analyzer)
```

Each repo gets its own `.claude-plugin/` manifest.

### Template Repo (No Plugin)

The clean template repo doesn't need `.claude-plugin/` - it's not a plugin itself, just a starting structure.

---

## File Size Considerations

### Current Repo Size

Let me check your current size:
```bash
# Skills folder
du -sh .claude/skills/

# Total repo
du -sh .
```

**If large:** Mostly due to:
- YouTube skill with FFmpeg binaries (~100 MB)
- All 12 skills combined

**Solution:** Separate repos reduces size per repo.

---

## Recommended Action Plan

### Now (Keep Developing)

```
✅ Keep everything in ai_project_template
✅ Continue development and testing
✅ Iterate on skills together
✅ Don't worry about context usage (12 skills is fine!)
```

### When Ready to Share (Split Repos)

**Step 1: Create fstrent-spec-tasks repo**
```bash
# New repo with:
- fstrent-task-management/
- fstrent-planning/
- fstrent-qa/
- fstrent-code-reviewer/
- .fstrent_spec_tasks/
- .claude-plugin/
- README.md
```

**Step 2: Create youtube-video-analyzer repo**
```bash
# New repo with:
- youtube-video-analysis/
- .claude-plugin/
- README.md
```

**Step 3: Clean up template repo**
```bash
# Keep only:
- .claude/rules/
- .cursor/rules/
- Basic structure
- Installation guide
- Remove all skills (or keep skill-creator)
```

---

## Context Usage: The Real Numbers

### Current Setup (12 Skills)

**Initial Load:**
```
Rules (always): ~10 KB
Skills metadata (12): ~7.2 KB
Total: ~17.2 KB

Percentage of 200K context: 8.6%
```

**With One Skill Active:**
```
Rules: ~10 KB
Skills metadata: ~7.2 KB
One active skill: ~10 KB
Total: ~27.2 KB

Percentage: 13.6%
```

**This is EXCELLENT efficiency!**

### If You Removed Half the Skills (6 Skills)

**Initial Load:**
```
Rules: ~10 KB
Skills metadata (6): ~3.6 KB
Total: ~13.6 KB

Savings: 3.6 KB (negligible!)
```

**Verdict:** Removing skills for context reasons is NOT necessary.

---

## Decision Matrix

| Factor | Keep in Template | Split into Repos | Hybrid |
|--------|-----------------|------------------|--------|
| **Development Speed** | ✅ Fast | ❌ Slower | ⚠️ Medium |
| **Public Sharing** | ⚠️ All or nothing | ✅ Individual | ✅ Flexible |
| **Street Cred** | ⚠️ One repo | ✅ Multiple stars | ✅ Multiple stars |
| **Maintenance** | ✅ Easy (one repo) | ❌ Complex | ⚠️ Medium |
| **User Flexibility** | ❌ Take all | ✅ Pick what you want | ✅ Pick what you want |
| **Repo Size** | ❌ Large | ✅ Small each | ✅ Small each |
| **Installation** | ✅ One clone | ❌ Multiple steps | ⚠️ Multiple steps |

---

## My Recommendation

### For Now: Keep Everything Together

**Reasons:**
1. You're still developing and iterating
2. Context usage is NOT a problem (only 8.6%)
3. Easier to test interactions between skills
4. Faster to make changes

### When Ready to Share: Split into 3 Repos

**1. fstrent-spec-tasks** (Core product)
- 4 task management skills
- Complete system
- Main attraction

**2. youtube-video-analyzer** (Separate product)
- Independent skill
- Different use case
- Deserves own spotlight

**3. claude-code-project-template** (Clean starting point)
- Minimal structure
- Rules files
- Links to install skills

### Remove Anthropic Examples Before Publishing

Keep for development, remove for public repos.

---

## Bottom Line

### Your Questions Answered

**Q: Can I store skills in `.claude-plugin/` until needed?**
**A:** No - `.claude-plugin/` is metadata, not storage. Skills go in `.claude/skills/`.

**Q: Should I keep updating this template or create separate repos?**
**A:**
- **Now:** Keep in template (easier development)
- **Later:** Split into separate repos (better sharing)

**Q: Should I put less-used skills in plugins?**
**A:** No need! 12 skills only uses 8.6% context. Progressive disclosure makes this efficient.

**Q: Is 12 skills too many?**
**A:** NO! Only 1,800 tokens for all 12 skill metadata. This is negligible.

---

## Next Steps

### Immediate (No Action Needed)

✅ Current setup is fine for development
✅ 12 skills is NOT too many
✅ Context usage is excellent
✅ Continue building in current template

### When Ready to Share

1. Create `fstrent-spec-tasks` repo (task management bundle)
2. Create `youtube-video-analyzer` repo (standalone skill)
3. Clean up template repo (minimal structure)
4. Remove Anthropic example skills from public repos

---

**The key insight:** Progressive disclosure means you're NOT penalized for having many skills. Keep developing, split later when sharing! 🎯
