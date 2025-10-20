# Python Virtual Environment Management

## UV Package Manager

**CRITICAL**: This project uses UV as the standard Python package manager and virtual environment tool.

### Core Requirements

1. **Virtual Environment Creation**
   - Always use `uv venv` to create virtual environments
   - Never use `python -m venv` or `virtualenv` directly
   - UV provides faster, more reliable environment management

2. **Package Installation**
   - Use `uv pip install <package>` for installing packages
   - Use `uv pip install -r requirements.txt` for bulk installations
   - Use `uv run python <script>` to run Python scripts in the UV environment

3. **Dependency Management**
   - **ALWAYS** keep both `requirements.txt` AND `pyproject.toml` synchronized
   - When adding a new package, update BOTH files immediately
   - When removing a package, remove from BOTH files
   - Never let these files get out of sync

### File Synchronization Rules

#### requirements.txt
```txt
# Format: package==version
numpy==1.24.0
pandas==2.0.0
requests==2.31.0
```

#### pyproject.toml
```toml
[project]
name = "project-name"
version = "0.1.0"
dependencies = [
    "numpy==1.24.0",
    "pandas==2.0.0",
    "requests==2.31.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Workflow for Adding Dependencies

1. **Install the package**:
   ```bash
   uv pip install <package>
   ```

2. **Update requirements.txt**:
   ```bash
   uv pip freeze > requirements.txt
   ```

3. **Update pyproject.toml**:
   - Manually add the package with version to the `dependencies` array
   - Ensure version matches what's in requirements.txt

4. **Verify synchronization**:
   - Check that both files contain the same package versions
   - Commit both files together

### Common UV Commands

```bash
# Create virtual environment
uv venv

# Activate environment (Windows)
.venv\Scripts\activate

# Activate environment (Unix/Mac)
source .venv/bin/activate

# Install package
uv pip install <package>

# Install from requirements
uv pip install -r requirements.txt

# Run script in UV environment
uv run python script.py

# Update all packages
uv pip install --upgrade -r requirements.txt

# List installed packages
uv pip list

# Show package info
uv pip show <package>
```

### Benefits of UV

- **Speed**: 10-100x faster than pip for package resolution
- **Reliability**: Better dependency conflict resolution
- **Compatibility**: Drop-in replacement for pip
- **Modern**: Built with Rust for performance and safety

### Migration from pip/venv

If converting an existing project:

1. Install UV: `pip install uv`
2. Create UV environment: `uv venv`
3. Install existing requirements: `uv pip install -r requirements.txt`
4. Update pyproject.toml with all dependencies
5. Verify both files are synchronized
6. Document UV usage in project README

### Enforcement

- **Code Reviews**: Check that both requirements.txt and pyproject.toml are updated
- **CI/CD**: Add validation to ensure file synchronization
- **Documentation**: Always mention UV in setup instructions
- **Consistency**: Never mix pip and UV in the same project

---

**Remember**: UV is the standard. Both requirements.txt and pyproject.toml must always be in sync.

