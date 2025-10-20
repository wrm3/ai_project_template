# Documentation Standards

## Documentation File Placement

**CRITICAL:** All documentation files MUST be created in the `docs/` folder, NOT in the project root.

### Naming Convention

**Format:** `YYYYMMDD_HHMMSS_IDE_TOPIC_NAME.md`

**Components:**
- `YYYYMMDD` - Date (e.g., 20251019)
- `HHMMSS` - Time in 24-hour format (e.g., 173402)
- `IDE` - Which IDE created it (Claude, Cursor, Windsurf, Roo, Cline)
- `TOPIC_NAME` - Descriptive name in UPPERCASE_WITH_UNDERSCORES

**Examples:**
```
✅ docs/20251019_173402_Claude_SETUP_COMPLETE_SUMMARY.md
✅ docs/20251019_173407_Cursor_CODE_REVIEW_ANALYSIS.md
✅ docs/20251020_094523_Claude_API_INTEGRATION_GUIDE.md
✅ docs/20251020_143011_Windsurf_DEPLOYMENT_CHECKLIST.md

❌ SETUP_COMPLETE_SUMMARY.md  (wrong location)
❌ docs/setup-guide.md  (missing timestamp and IDE)
❌ docs/20251019_guide.md  (missing time and IDE)
```

### Why This Convention?

**Benefits:**
1. ✅ **Automatic chronological sorting** - Files sort by creation date/time
2. ✅ **IDE attribution** - Know which tool created each doc
3. ✅ **Clean root directory** - All docs organized in one place
4. ✅ **Easy to find latest** - Most recent files appear last
5. ✅ **Cross-IDE compatibility** - Works in all IDEs

### Timestamp Format

**Use PowerShell command for Windows:**
```powershell
powershell -Command "(Get-Date).ToString('yyyyMMdd_HHmmss')"
```

**Or in code:**
```python
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"docs/{timestamp}_Claude_TOPIC_NAME.md"
```

```javascript
const timestamp = new Date().toISOString().replace(/[-:]/g, '').slice(0, 15);
const filename = `docs/${timestamp}_Claude_TOPIC_NAME.md`;
```

---

## Exceptions

**The ONLY files allowed in project root:**
- `README.md` - Main project README
- `LICENSE` - License file
- `CLAUDE.md` - Claude Code instructions (if used)
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines

**Everything else goes in `docs/`**

---

## Workflow

### When Creating Documentation

1. **Generate timestamp:**
   ```powershell
   $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
   ```

2. **Construct filename:**
   ```
   docs/${timestamp}_Claude_YOUR_TOPIC.md
   ```

3. **Create file in docs/ folder**

4. **Add to docs index if needed**

### Example Creation

**User asks:** "Document the API integration approach"

**You create:**
```
docs/20251019_173402_Claude_API_INTEGRATION_APPROACH.md
```

**NOT:**
```
❌ API_INTEGRATION_APPROACH.md
❌ docs/api-integration.md
❌ integration-docs.md
```

---

## File Organization

```
project/
├── README.md                           ✅ Root (main readme only)
├── LICENSE                             ✅ Root (standard)
├── CLAUDE.md                          ✅ Root (IDE instructions)
├── CHANGELOG.md                       ✅ Root (version history)
│
└── docs/                              ✅ All other docs here!
    ├── 20251019_101234_Claude_SETUP_GUIDE.md
    ├── 20251019_143022_Cursor_FEATURE_ANALYSIS.md
    ├── 20251019_173402_Claude_API_INTEGRATION.md
    ├── 20251020_094523_Claude_DATABASE_SCHEMA.md
    └── 20251020_114455_Windsurf_DEPLOYMENT_NOTES.md
```

---

## When to Create Documentation

**DO create docs for:**
- ✅ Architecture decisions
- ✅ Setup guides
- ✅ Analysis results
- ✅ Integration guides
- ✅ Deployment procedures
- ✅ Troubleshooting guides
- ✅ API documentation
- ✅ Testing strategies

**DON'T create docs for:**
- ❌ Temporary notes (use comments instead)
- ❌ Work-in-progress drafts (use temp/ folder)
- ❌ Auto-generated content (use appropriate folders)

---

## Enforcement

**Before creating any .md file:**
1. Check if it's an allowed root file (README, LICENSE, etc.)
2. If not, MUST go in `docs/` with timestamp and IDE prefix
3. Verify format: `YYYYMMDD_HHMMSS_IDE_TOPIC.md`

**If user asks you to create doc in root:**
1. Politely explain the convention
2. Suggest proper location in `docs/`
3. Use timestamped, IDE-prefixed filename

---

**Remember:** Clean root directory = better project organization!
