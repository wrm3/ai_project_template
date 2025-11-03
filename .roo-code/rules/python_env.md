# Python Virtual Environment Rules (Roo-Code)

For complete Python environment documentation, see: `.claude/rules/virtual_environments_python.md`

## Quick Reference

### Use UV for Virtual Environments

**Check for existing environment:**
```bash
ls -la .venv/
```

**Create new environment with UV:**
```bash
uv venv
```

**Activate environment:**
```bash
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Install Dependencies
```bash
# With UV (faster)
uv pip install -r requirements.txt

# Standard pip (fallback)
pip install -r requirements.txt
```

### Before Running Python Commands
1. Check if venv exists
2. Activate venv if exists
3. Install dependencies if needed
4. Then run commands

### Requirements Files
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies
- `requirements-test.txt` - Testing dependencies

### Best Practices
- **Always use virtual environments** - Never install globally
- **UV preferred** - Much faster than pip
- **Keep requirements updated** - Use `uv pip freeze > requirements.txt`
- **Gitignore venv** - Don't commit virtual environment

### Common Issues
**Problem:** "Module not found"
**Solution:** Ensure venv is activated and dependencies installed

**Problem:** "Permission denied"
**Solution:** Use virtual environment, don't use sudo with pip

For complete Python environment rules, see `.claude/rules/virtual_environments_python.md`
