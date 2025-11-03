---
name: hanx-database-tools
description: MySQL and Oracle database interaction tools with connection management, query execution, and result processing. Provides context managers, parameterized queries, connection pooling, metadata extraction, and comprehensive error handling for enterprise database operations.
---

# Hanx Database Tools Skill

Enterprise-grade database interaction tools for MySQL and Oracle databases with comprehensive connection management, query execution, result processing, and metadata extraction capabilities.

## Overview

This skill provides robust database interaction capabilities based on proven production implementations from MCP servers and enterprise tools. It includes:

- **MySQL Support**: Full connection management with pooling, parameterized queries, transaction control
- **Oracle Support**: Service name connections, PL/SQL execution, LOB handling, metadata extraction
- **Security**: Parameterized queries for SQL injection prevention, connection validation
- **Context Managers**: Safe resource cleanup with Python context manager protocol
- **Error Handling**: Comprehensive error categorization and user-friendly messages
- **Data Conversion**: Automatic conversion of database types to JSON-compatible formats

## When to Use This Skill

**Activate this skill when:**
- Setting up database connections for MySQL or Oracle
- Executing database queries (SELECT, INSERT, UPDATE, DELETE)
- Performing database schema operations (CREATE, ALTER, DROP)
- Extracting database metadata (tables, columns, constraints)
- Implementing database migration scripts
- Building data processing pipelines
- Handling database transactions
- Working with enterprise database systems

## Core Capabilities

### MySQL Database Operations

#### Connection Management
- Environment-based configuration (.env file support)
- Connection pooling for performance
- Automatic connection lifecycle management
- Context manager support for safe cleanup
- Parameterized connection parameters

#### Query Execution
- **Read Operations**: SELECT, SHOW, DESCRIBE, EXPLAIN
- **Write Operations**: INSERT, UPDATE, DELETE, REPLACE
- **DDL Operations**: CREATE, ALTER, DROP, TRUNCATE
- **Parameterized Queries**: SQL injection prevention with ? placeholders
- **Batch Operations**: executemany for bulk inserts/updates
- **Transaction Control**: Commit/rollback support

#### Result Processing
- Dictionary-based results (column_name: value)
- Automatic data type conversion (datetime, Decimal, bytes)
- JSON-compatible output format
- Row count information
- Column metadata

### Oracle Database Operations

#### Connection Management
- Service name-based connections
- TNS-style DSN support
- Schema specification
- Source/target database distinction
- Thick/thin mode support

#### Advanced Features
- **PL/SQL Support**: Execute stored procedures and functions
- **LOB Handling**: CLOB, BLOB, NCLOB with automatic conversion
- **Metadata Extraction**:
  - Table definitions
  - Column information with data types
  - Constraints (primary keys, foreign keys, unique, check)
  - Indexes
  - Sequences
  - Views
- **Oracle-Specific Types**:
  - TIMESTAMP WITH TIME ZONE
  - INTERVAL DAY TO SECOND
  - NUMBER with precision/scale preservation
  - ROWID
  - RAW binary data

#### Data Type Conversion
- Enhanced type metadata in results
- Precision and scale information for NUMBER types
- Timezone preservation for timestamps
- Base64 encoding for binary data
- LOB content extraction

## Usage Patterns

### MySQL Usage

#### Basic Query Execution
```python
from scripts.mysql_db import MySQLDB

# Simple query with context manager
with MySQLDB(source_db=True) as db:
    results = db.execute_query("SELECT * FROM users WHERE active = 1")
    for row in results:
        print(f"User: {row['username']}, Email: {row['email']}")
```

#### Parameterized Queries (Security Best Practice)
```python
# Prevent SQL injection with parameterized queries
with MySQLDB(source_db=True) as db:
    # Safe query - parameters are escaped automatically
    query = "SELECT * FROM users WHERE username = %(username)s AND status = %(status)s"
    params = {'username': user_input, 'status': 'active'}
    results = db.execute_query(query, params)
```

#### Batch Operations
```python
# Efficient bulk inserts
with MySQLDB(source_db=False) as db:
    insert_query = "INSERT INTO logs (message, level, timestamp) VALUES (%(msg)s, %(lvl)s, NOW())"
    batch_data = [
        {'msg': 'User login', 'lvl': 'INFO'},
        {'msg': 'Data processed', 'lvl': 'DEBUG'},
        {'msg': 'Error occurred', 'lvl': 'ERROR'}
    ]
    db.execute_many(insert_query, batch_data)
```

#### Transaction Management
```python
# Manual transaction control
db = MySQLDB(source_db=True)
db.connect()
try:
    db.execute_query("START TRANSACTION")
    db.execute_query("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    db.execute_query("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    db.execute_query("COMMIT")
except Exception as e:
    db.execute_query("ROLLBACK")
    raise
finally:
    db.disconnect()
```

### Oracle Usage

#### Basic Connection and Query
```python
from scripts.oracle_db import OracleDB

# Connect to source Oracle database
with OracleDB(source_db=True) as db:
    results = db.execute_query("SELECT * FROM employees WHERE department_id = :dept_id",
                               params={'dept_id': 10})
```

#### Metadata Extraction
```python
from scripts.oracle_utils import extract_table_metadata, extract_constraints

# Get complete table schema
with OracleDB(source_db=True) as db:
    # Extract table structure
    table_metadata = extract_table_metadata(db, 'EMPLOYEES')

    # Extract constraints
    constraints = extract_constraints(db, 'EMPLOYEES')

    # Extract indexes
    indexes = db.execute_query("""
        SELECT index_name, column_name, column_position
        FROM user_ind_columns
        WHERE table_name = :table_name
        ORDER BY index_name, column_position
    """, params={'table_name': 'EMPLOYEES'})
```

#### Working with LOBs
```python
# Reading CLOB data
with OracleDB(source_db=True) as db:
    results = db.execute_query("SELECT id, document_text FROM documents WHERE id = :doc_id",
                               params={'doc_id': 12345})

    # CLOB data is automatically converted to dictionary format
    if results:
        doc = results[0]
        if doc['document_text']['type'] == 'CLOB':
            text_content = doc['document_text']['data']
            print(f"Document size: {doc['document_text']['size']} characters")
```

#### PL/SQL Execution
```python
# Execute stored procedure
with OracleDB(source_db=True) as db:
    # Call procedure with parameters
    db.execute_query("""
        BEGIN
            update_employee_salary(:emp_id, :new_salary);
        END;
    """, params={'emp_id': 100, 'new_salary': 75000})
```

### Connection Manager Usage

#### Connection Pooling
```python
from scripts.connection_manager import ConnectionPool

# Create connection pool for high-throughput applications
pool = ConnectionPool(
    db_type='mysql',
    host='localhost',
    port=3306,
    database='production',
    user='app_user',
    password='secure_password',
    pool_size=10,
    max_overflow=5
)

# Get connection from pool
with pool.get_connection() as conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE status = 'pending'")
    orders = cursor.fetchall()
```

#### Connection Health Checks
```python
from scripts.connection_manager import test_connection

# Validate connection before use
is_valid, error_msg = test_connection(
    db_type='mysql',
    host='database-server',
    port=3306,
    username='app_user',
    password='password',
    database='production'
)

if is_valid:
    print("Connection successful!")
else:
    print(f"Connection failed: {error_msg}")
```

### Query Builder Utilities

#### Safe Query Construction
```python
from scripts.query_builder import build_select, build_insert, build_update

# Build SELECT query safely
query, params = build_select(
    table='users',
    columns=['id', 'username', 'email'],
    where={'status': 'active', 'role': 'admin'},
    order_by='created_at DESC',
    limit=10
)
# Result: "SELECT id, username, email FROM users WHERE status = ? AND role = ? ORDER BY created_at DESC LIMIT 10"
# Params: ['active', 'admin']

# Build INSERT query
query, params = build_insert(
    table='audit_log',
    data={'user_id': 123, 'action': 'login', 'ip_address': '192.168.1.1'}
)

# Build UPDATE query
query, params = build_update(
    table='users',
    data={'last_login': 'NOW()', 'login_count': 'login_count + 1'},
    where={'id': 123}
)
```

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# MySQL Source Database
src_mysql_host=localhost
src_mysql_port=3306
src_mysql_db=source_database
src_mysql_user=source_user
src_mysql_pw=source_password

# MySQL Target Database
tgt_mysql_host=localhost
tgt_mysql_port=3306
tgt_mysql_db=target_database
tgt_mysql_user=target_user
tgt_mysql_pw=target_password

# Oracle Source Database
src_db_host=oracle-server
src_db_port=1521
src_db_service=ORCL
src_db_user=source_user
src_db_pw=source_password
src_db_schema=SOURCE_SCHEMA

# Oracle Target Database
tgt_db_host=oracle-server
tgt_db_port=1521
tgt_db_service=ORCL_TARGET
tgt_db_user=target_user
tgt_db_pw=target_password
tgt_db_schema=TARGET_SCHEMA
```

### Python Dependencies

Add to your `requirements.txt`:

```
# MySQL Support
mysql-connector-python>=8.0.0

# Oracle Support
oracledb>=1.0.0  # Oracle's new python-oracledb (thin mode)
# OR
cx_Oracle>=8.0.0  # Legacy driver (requires Oracle Instant Client)

# Utilities
python-dotenv>=1.0.0
sqlparse>=0.4.0  # SQL parsing and validation
```

## Security Best Practices

### 1. Always Use Parameterized Queries

```python
# BAD - SQL Injection Vulnerable
user_input = request.args.get('username')
query = f"SELECT * FROM users WHERE username = '{user_input}'"  # UNSAFE!

# GOOD - Protected Against SQL Injection
query = "SELECT * FROM users WHERE username = %s"
params = (user_input,)
results = db.execute_query(query, params)
```

### 2. Environment-Based Configuration

```python
# GOOD - Credentials from environment
from dotenv import load_dotenv
import os

load_dotenv()
db = MySQLDB(source_db=True)  # Uses .env variables

# BAD - Hardcoded credentials
db = mysql.connector.connect(
    host="production-server",
    user="admin",
    password="hardcoded_password"  # NEVER DO THIS!
)
```

### 3. Connection Validation

```python
from scripts.connection_manager import validate_connection_parameters

# Validate before connecting
error_msg = validate_connection_parameters(
    host=host,
    port=port,
    username=username,
    password=password,
    database=database
)

if error_msg:
    raise ValueError(f"Invalid connection parameters: {error_msg}")
```

### 4. Safe Error Handling

```python
# Provide user-friendly errors without exposing internals
try:
    results = db.execute_query(query, params)
except DatabaseError as e:
    # Log detailed error internally
    logger.error(f"Database error: {str(e)}", exc_info=True)

    # Return sanitized error to user
    raise RuntimeError("Database query failed. Please contact support.")
```

## Error Handling

### MySQL Error Categories

The skill provides categorized error handling:

- **CONNECTION**: Server unreachable, network issues, timeout
- **AUTHENTICATION**: Invalid credentials, access denied
- **SYNTAX**: SQL syntax errors
- **SCHEMA**: Table/column not found, database doesn't exist
- **DATA**: Constraint violations, data too long, foreign key errors
- **SERVER**: Internal server errors
- **TIMEOUT**: Operation timeout
- **UNKNOWN**: Unexpected errors

### Oracle Error Handling

Similar categorization with Oracle-specific errors:

- **ORA-00001**: Unique constraint violation
- **ORA-01017**: Invalid username/password
- **ORA-12154**: TNS could not resolve service name
- **ORA-12541**: No listener
- **ORA-01031**: Insufficient privileges

### Example Error Handling

```python
from scripts.mysql_db import MySQLDB
from mysql.connector import Error

try:
    with MySQLDB(source_db=True) as db:
        results = db.execute_query("SELECT * FROM users")
except Error as e:
    error_code = e.errno
    error_msg = str(e)

    if error_code == 1045:
        print("Authentication failed. Check username/password.")
    elif error_code == 2003:
        print("Cannot connect to database server.")
    elif error_code == 1146:
        print("Table does not exist.")
    else:
        print(f"Database error: {error_msg}")
```

## Performance Optimization

### 1. Connection Pooling

Use connection pools for high-throughput applications:

```python
# Reuse connections instead of creating new ones
pool = ConnectionPool(pool_size=10)

# Process 1000s of requests efficiently
for request in requests:
    with pool.get_connection() as conn:
        process_request(conn, request)
```

### 2. Batch Operations

Use `executemany` for bulk operations:

```python
# SLOW - Individual inserts
for record in records:
    db.execute_query("INSERT INTO table VALUES (%s, %s)", (record.a, record.b))

# FAST - Batch insert
data = [(r.a, r.b) for r in records]
db.execute_many("INSERT INTO table VALUES (%s, %s)", data)
```

### 3. Query Optimization

```python
# Use query builder to add proper indexes awareness
from scripts.query_builder import should_add_index

# Check if query would benefit from index
query = "SELECT * FROM large_table WHERE uncommon_column = 'value'"
if should_add_index(query, db):
    print("Consider adding index on uncommon_column for better performance")
```

## Common Workflows

### Database Migration

```python
from scripts.mysql_db import MySQLDB
from scripts.oracle_db import OracleDB

# Extract from Oracle, load to MySQL
with OracleDB(source_db=True) as oracle_db:
    # Extract data
    data = oracle_db.execute_query("SELECT * FROM employees")

with MySQLDB(source_db=False) as mysql_db:
    # Transform and load
    for row in data:
        mysql_db.execute_query(
            "INSERT INTO employees (id, name, salary) VALUES (%s, %s, %s)",
            (row['id'], row['name'], row['salary'])
        )
```

### Schema Comparison

```python
from scripts.oracle_utils import extract_table_metadata

# Compare schemas between environments
with OracleDB(source_db=True) as source_db:
    source_schema = extract_table_metadata(source_db, 'EMPLOYEES')

with OracleDB(source_db=False) as target_db:
    target_schema = extract_table_metadata(target_db, 'EMPLOYEES')

# Find differences
differences = compare_schemas(source_schema, target_schema)
```

### Data Validation

```python
from scripts.connection_manager import validate_data_consistency

# Ensure data integrity between source and target
inconsistencies = validate_data_consistency(
    source_db=MySQLDB(source_db=True),
    target_db=MySQLDB(source_db=False),
    table='orders',
    key_column='order_id'
)

if inconsistencies:
    print(f"Found {len(inconsistencies)} inconsistencies")
```

## Troubleshooting

### MySQL Connection Issues

**Problem**: "Can't connect to MySQL server"
```python
# Solution: Check server status and network
from scripts.connection_manager import diagnose_connection

diagnosis = diagnose_connection(host='localhost', port=3306)
print(diagnosis)  # Provides detailed connection diagnostics
```

**Problem**: "Access denied for user"
```python
# Solution: Verify credentials in .env file
import os
from dotenv import load_dotenv

load_dotenv()
print(f"Connecting as: {os.getenv('src_mysql_user')}")
print(f"To database: {os.getenv('src_mysql_db')}")
```

### Oracle Connection Issues

**Problem**: "ORA-12154: TNS could not resolve service name"
```python
# Solution: Verify service name and tnsnames.ora
with OracleDB(source_db=True) as db:
    print(f"Connecting to DSN: {db.dsn}")
    # Check: oracle-server:1521/ORCL
```

**Problem**: "Oracle thick mode initialization failed"
```python
# Solution: Install Oracle Instant Client or use thin mode
# Thin mode (no client needed):
import oracledb
# Automatically uses thin mode if thick client not available

# Thick mode (better encryption support):
oracledb.init_oracle_client(lib_dir="/path/to/instantclient")
```

## Integration with MCP Servers

This skill is compatible with MCP (Model Context Protocol) servers for AI assistant integration:

### Claude Code Integration

```json
{
  "mcpServers": {
    "mysql": {
      "command": "uv",
      "args": ["run", "python", "scripts/mcp_mysql_server.py"],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306"
      }
    }
  }
}
```

### Query Classification

The skill includes SQL command classification for security:

```python
from scripts.query_classifier import classify_sql_command

classification = classify_sql_command("SELECT * FROM users")
# Returns: {'command_type': 'READ', 'is_read_only': True, 'is_modification': False}

classification = classify_sql_command("DELETE FROM logs WHERE old = 1")
# Returns: {'command_type': 'WRITE', 'is_read_only': False, 'is_modification': True}
```

## File Reference

### Core Scripts

- `scripts/mysql_db.py` - MySQL connection and query execution class
- `scripts/mysql_utils.py` - MySQL utility functions (query, execute, describe_table)
- `scripts/oracle_db.py` - Oracle connection and query execution class
- `scripts/oracle_utils.py` - Oracle utility functions and metadata extraction
- `scripts/connection_manager.py` - Connection pooling and validation
- `scripts/query_builder.py` - Safe query construction utilities
- `scripts/data_converter.py` - Database type to JSON conversion

### Templates

- `templates/.env.database.example` - Environment configuration template

### Examples

- `examples/mysql_examples.md` - Comprehensive MySQL usage examples
- `examples/oracle_examples.md` - Comprehensive Oracle usage examples
- `examples/metadata_extraction.md` - Database schema extraction workflows
- `examples/connection_pooling.md` - Connection pool implementation examples
- `examples/migration_workflow.md` - Database migration patterns

### Reference

- `reference/mysql_datatypes.md` - MySQL data type reference and conversion
- `reference/oracle_datatypes.md` - Oracle data type reference and conversion
- `reference/security_checklist.md` - Security best practices checklist
- `reference/performance_tuning.md` - Database performance optimization guide

## Advanced Topics

### Custom Connection Pools

```python
from scripts.connection_manager import BaseConnectionPool

class CustomMySQLPool(BaseConnectionPool):
    def __init__(self, **kwargs):
        super().__init__(db_type='mysql', **kwargs)

    def get_connection_with_retry(self, max_retries=3):
        for attempt in range(max_retries):
            try:
                return self.get_connection()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
```

### Query Result Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_user_by_id(user_id):
    with MySQLDB() as db:
        results = db.execute_query(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )
        return results[0] if results else None
```

### Async Database Operations

```python
import asyncio
from scripts.async_mysql_db import AsyncMySQLDB

async def process_records_concurrently():
    async with AsyncMySQLDB() as db:
        tasks = []
        for record_id in range(1000):
            task = db.execute_query_async(
                "SELECT * FROM records WHERE id = %s",
                (record_id,)
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return results
```

## Success Criteria

A successful implementation should demonstrate:

- Secure database connections using environment variables
- Parameterized queries preventing SQL injection
- Proper error handling with user-friendly messages
- Context manager usage for resource cleanup
- Efficient batch operations for bulk data
- Metadata extraction capabilities
- Cross-database compatibility (source/target)
- Connection pooling for performance
- Comprehensive logging for debugging
- Type conversion for JSON compatibility

## Support and Resources

### Documentation
- MySQL Connector/Python: https://dev.mysql.com/doc/connector-python/en/
- Oracle python-oracledb: https://python-oracledb.readthedocs.io/
- SQL Injection Prevention: https://owasp.org/www-community/attacks/SQL_Injection

### Common Issues
- See `examples/troubleshooting.md` for detailed issue resolution
- Check logs in `logs/` directory for error details
- Review `.env.database.example` for configuration format

### Testing
- Unit tests in `tests/test_mysql_db.py`
- Integration tests in `tests/test_oracle_db.py`
- Security tests in `tests/test_sql_injection.py`

---

**Last Updated**: 2025-11-01
**Version**: 1.0.0
**Skill Type**: Database Integration
**Compatibility**: Claude Code, Cursor IDE, VS Code
