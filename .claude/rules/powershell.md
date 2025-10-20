# PowerShell Guidelines for Windows Development

**Platform:** Windows 10/11
**Shell:** PowerShell (not bash)

---

## Critical PowerShell Behavior

### 1. Command Separators

**❌ AVOID: `&&` doesn't work reliably**
```powershell
cd myproject && npm start  # May not work as expected
```

**✅ USE: `;` as command separator**
```powershell
cd myproject; npm start  # Works correctly
```

### 2. Curl Issues (CRITICAL)

**Problem:** In PowerShell, `curl` is an alias for `Invoke-WebRequest`, causing interactive prompts.

**❌ AVOID - Gets stuck on Uri prompt:**
```powershell
curl -s http://localhost:5000/api/status
# This will prompt: "Uri:" and hang
```

**✅ USE INSTEAD:**

**Option 1: Use Invoke-WebRequest properly**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/status" -UseBasicParsing
```

**Option 2: Use shorthand 'iwr'**
```powershell
iwr "http://localhost:5000/api/status" -UseBasicParsing
```

**Option 3: Force actual curl executable**
```powershell
curl.exe -s http://localhost:5000/api/status
```

**Option 4: For JSON responses**
```powershell
(Invoke-WebRequest -Uri "http://localhost:5000/api/status").Content | ConvertFrom-Json
```

### 3. DateTime Commands

**✅ Get current timestamp (UTC):**
```powershell
powershell -Command "(Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')"
```

**Local time:**
```powershell
Get-Date -Format "yyyy-MM-dd HH:mm:ss"
```

---

## Common PowerShell Patterns

### Directory Operations

**Create multiple directories:**
```powershell
New-Item -ItemType Directory -Path "app\templates", "app\static" -Force
```

**Navigate and run command:**
```powershell
cd flask-vpn-manager; uv run python main.py
```

### Flask/Web Server Development

**IMPORTANT:** Flask servers block the terminal. Use background execution.

**❌ AVOID - Blocks terminal:**
```powershell
uv run python main.py  # Terminal hangs
```

**✅ USE - Run in background:**
```powershell
Start-Process powershell -ArgumentList "-Command", "cd $PWD; uv run python main.py"
```

**Test endpoints:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -UseBasicParsing
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/status" -UseBasicParsing
```

---

## Important Flags

### -UseBasicParsing

**Always use with Invoke-WebRequest** to avoid DOM parsing issues:
```powershell
Invoke-WebRequest -Uri "http://example.com" -UseBasicParsing
```

Without it, PowerShell tries to parse HTML/DOM which can cause errors.

---

## Common Gotchas

### 1. Aliases Override Expected Behavior
- `curl` → `Invoke-WebRequest`
- `wget` → `Invoke-WebRequest`
- `ls` → `Get-ChildItem`
- `cat` → `Get-Content`

**Solution:** Use `.exe` suffix to force actual executable
```powershell
curl.exe instead of curl
```

### 2. Quote URLs with Special Characters
```powershell
# Good
Invoke-WebRequest -Uri "http://api.example.com/data?key=value&other=123"

# Bad (may fail)
Invoke-WebRequest -Uri http://api.example.com/data?key=value&other=123
```

### 3. Background Processes
When running servers or long-running processes:
- Use `Start-Process` for background execution
- Use `&` at end of command (limited support)
- Consider separate terminal for servers

---

## Quick Reference

| Task | PowerShell Command |
|------|-------------------|
| HTTP GET | `iwr "http://url" -UseBasicParsing` |
| HTTP GET (actual curl) | `curl.exe -s http://url` |
| Create directory | `New-Item -ItemType Directory -Path "path" -Force` |
| Run in background | `Start-Process powershell -ArgumentList "-Command", "cmd"` |
| Get UTC time | `(Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')` |
| Command separator | `;` (not `&&`) |

---

**Remember:** PowerShell is not bash. Always account for Windows-specific behavior.
