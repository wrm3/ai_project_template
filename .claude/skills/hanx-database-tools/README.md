# Hanx Database Tools Skill

Enterprise-grade MySQL and Oracle database interaction tools with comprehensive connection management, query execution, and result processing.

## Quick Start

### 1. Install Dependencies

```bash
# MySQL support
pip install mysql-connector-python python-dotenv sqlparse

# Oracle support (choose one)
pip install oracledb  # Recommended: thin mode, no client needed
# OR
pip install cx_Oracle  # Legacy: requires Oracle Instant Client
```

### 2. Configure Environment

Copy the template and fill in your credentials:

```bash
cp templates/.env.database.example .env
# Edit .env with your database credentials
```

### 3. Basic Usage

#### MySQL

```python
from scripts.mysql_db import MySQLDB

# Using context manager (recommended)
with MySQLDB(source_db=True) as db:
    results = db.execute_query(
        "SELECT * FROM users WHERE status = %(status)s",
        params={'status': 'active'}
    )
    for row in results:
        print(f"User: {row['username']}")
```

#### Oracle

```python
from scripts.oracle_db import OracleDB

# Using context manager (recommended)
with OracleDB(source_db=True) as db:
    results = db.execute_query(
        "SELECT * FROM employees WHERE department_id = :dept_id",
        params={'dept_id': 10}
    )
    for row in results:
        print(f"Employee: {row['first_name']} {row['last_name']}")
```

## Key Features

### Security
- Parameterized queries prevent SQL injection
- Environment-based configuration (no hardcoded credentials)
- Connection parameter validation
- Error message sanitization

### Performance
- Connection pooling support
- Batch operations (executemany)
- Automatic resource cleanup
- Efficient data type conversion

### Reliability
- Context manager protocol
- Comprehensive error handling
- Transaction support
- Connection health checks

### Data Types
- Automatic MySQL type conversion (datetime, Decimal, bytes)
- Oracle LOB handling (CLOB, BLOB)
- Oracle type metadata (precision, scale, timezone)
- JSON-compatible output

## File Structure

```
.claude/skills/hanx-database-tools/
├── SKILL.md                          # Main skill documentation
├── rules.md                          # Implementation rules and standards
├── README.md                         # This file
├── scripts/
│   ├── mysql_db.py                  # MySQL connection class
│   ├── oracle_db.py                 # Oracle connection class
│   ├── mysql_utils.py               # MySQL utility functions
│   ├── oracle_utils.py              # Oracle utility functions
│   ├── connection_manager.py        # Connection pooling
│   ├── query_builder.py             # Safe query construction
│   └── data_converter.py            # Type conversion utilities
├── templates/
│   └── .env.database.example        # Configuration template
├── examples/
│   ├── mysql_examples.md            # MySQL usage examples
│   ├── oracle_examples.md           # Oracle usage examples
│   ├── metadata_extraction.md       # Schema extraction
│   ├── connection_pooling.md        # Pool implementation
│   └── migration_workflow.md        # Data migration patterns
└── reference/
    ├── mysql_datatypes.md           # MySQL type reference
    ├── oracle_datatypes.md          # Oracle type reference
    ├── security_checklist.md        # Security guidelines
    └── performance_tuning.md        # Optimization guide
```

## Common Tasks

### Test Connection

```bash
# Test MySQL connection
python scripts/mysql_db.py

# Test Oracle connection
python scripts/oracle_db.py
```

### List Tables

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=True) as db:
    tables = db.get_tables()
    print(f"Found {len(tables)} tables")
```

### Describe Table

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=True) as db:
    columns = db.describe_table('users')
    for col in columns:
        print(f"{col['Field']}: {col['Type']}")
```

### Batch Insert

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=False) as db:
    data = [
        {'name': 'Alice', 'email': 'alice@example.com'},
        {'name': 'Bob', 'email': 'bob@example.com'},
    ]
    db.execute_many(
        "INSERT INTO users (name, email) VALUES (%(name)s, %(email)s)",
        data
    )
```

## Security Best Practices

### Always Use Parameterized Queries

```python
# GOOD - Safe from SQL injection
results = db.execute_query(
    "SELECT * FROM users WHERE username = %(username)s",
    params={'username': user_input}
)

# BAD - SQL injection vulnerable
results = db.execute_query(
    f"SELECT * FROM users WHERE username = '{user_input}'"
)
```

### Store Credentials in .env

```bash
# .env file (add to .gitignore!)
src_mysql_host=localhost
src_mysql_port=3306
src_mysql_user=myuser
src_mysql_pw=mypassword
```

```python
# GOOD - Credentials from environment
db = MySQLDB(source_db=True)

# BAD - Hardcoded credentials
db = MySQLDB(host='prod-server', user='admin', password='secret123')
```

## Troubleshooting

### MySQL Connection Issues

**Error**: "Can't connect to MySQL server"
- Check if MySQL server is running
- Verify host and port in .env file
- Check network connectivity/firewall

**Error**: "Access denied for user"
- Verify username and password in .env
- Check user has appropriate permissions
- Ensure user can connect from your host

### Oracle Connection Issues

**Error**: "ORA-12154: TNS could not resolve service name"
- Verify service name (not SID) in .env
- Check tnsnames.ora configuration (if using)
- Ensure Oracle listener is running

**Error**: "Oracle thick mode initialization failed"
- Install Oracle Instant Client for thick mode
- Or use thin mode (oracledb driver default)

## Documentation

- **SKILL.md** - Complete skill documentation with all features
- **rules.md** - Implementation standards and patterns
- **examples/** - Comprehensive usage examples
- **reference/** - Data type references and guides

## Support

### Test Scripts

```bash
# MySQL connection test
python scripts/mysql_db.py

# Oracle connection test
python scripts/oracle_db.py
```

### Logging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from scripts.mysql_db import MySQLDB
with MySQLDB(source_db=True) as db:
    # Debug output will show connection details and queries
    results = db.execute_query("SELECT * FROM users")
```

## Integration

### With MCP Servers

This skill is compatible with MCP servers for AI assistant integration. See the `research/mcps/` directory for MySQL and Oracle MCP server implementations.

### With Other Skills

- **fstrent-task-management**: Create database-related tasks
- **fstrent-qa**: Report database bugs and issues
- **fstrent-planning**: Include database schema in planning

## Version

**Version**: 1.0.0
**Last Updated**: 2025-11-01
**Compatibility**: Claude Code, Cursor IDE, VS Code

## License

This skill is part of the AI Project Template and follows the same license terms.
