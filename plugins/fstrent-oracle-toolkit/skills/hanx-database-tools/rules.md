# Hanx Database Tools - Skill Rules

## Activation Rules

This skill activates when the user's request involves:

### Direct Triggers
- Database connection setup or configuration
- SQL query execution (SELECT, INSERT, UPDATE, DELETE)
- Database schema operations (CREATE, ALTER, DROP)
- Database metadata extraction
- Database migration tasks
- Mentions of "database", "MySQL", "Oracle", "SQL"

### Context Triggers
- Working with `.env` database configuration
- Files in `scripts/` related to database operations
- Error messages mentioning database connectivity
- Discussion of data persistence or storage

### Workflow Triggers
- Setting up new database connections
- Debugging database connection issues
- Implementing data migration workflows
- Extracting database schemas
- Optimizing database queries

## When This Skill is Active

### Primary Responsibilities

1. **Connection Management**
   - Guide proper database connection configuration
   - Recommend environment variable usage
   - Suggest connection pooling for performance
   - Validate connection parameters

2. **Query Construction**
   - Ensure parameterized queries are used (prevent SQL injection)
   - Review SQL syntax for correctness
   - Suggest query optimizations
   - Classify SQL commands (read vs. write)

3. **Error Handling**
   - Categorize database errors appropriately
   - Provide user-friendly error messages
   - Suggest troubleshooting steps
   - Log errors for debugging

4. **Security**
   - Enforce parameterized query usage
   - Prevent credential exposure
   - Validate dangerous SQL patterns
   - Recommend security best practices

5. **Data Processing**
   - Convert database types to JSON-compatible formats
   - Handle special data types (LOBs, timestamps, Decimals)
   - Process result sets efficiently
   - Support batch operations

## Implementation Standards

### Code Quality Rules

1. **Always Use Context Managers**
   ```python
   # CORRECT
   with MySQLDB(source_db=True) as db:
       results = db.execute_query(query)

   # INCORRECT - Resource leak risk
   db = MySQLDB(source_db=True)
   db.connect()
   results = db.execute_query(query)
   # Missing db.disconnect()
   ```

2. **Always Use Parameterized Queries**
   ```python
   # CORRECT - Safe from SQL injection
   query = "SELECT * FROM users WHERE username = %s"
   results = db.execute_query(query, (username,))

   # INCORRECT - SQL injection vulnerable
   query = f"SELECT * FROM users WHERE username = '{username}'"
   results = db.execute_query(query)
   ```

3. **Environment-Based Configuration**
   ```python
   # CORRECT - Configuration from environment
   from dotenv import load_dotenv
   load_dotenv()
   db = MySQLDB(source_db=True)  # Uses .env variables

   # INCORRECT - Hardcoded credentials
   db = MySQLDB(host='prod-server', user='admin', password='secret123')
   ```

4. **Comprehensive Error Handling**
   ```python
   # CORRECT - Categorized, user-friendly errors
   try:
       results = db.execute_query(query, params)
   except Error as e:
       category, message = categorize_error(e)
       logger.error(f"Database error [{category}]: {str(e)}")
       raise RuntimeError(message)  # User-friendly message

   # INCORRECT - Exposing internal errors
   try:
       results = db.execute_query(query, params)
   except Error as e:
       raise  # Exposes stack trace to user
   ```

5. **Proper Type Conversion**
   ```python
   # CORRECT - Convert to JSON-compatible types
   results = db.execute_query(query)
   converted_results = [convert_mysql_row(row) for row in results]
   return json.dumps(converted_results, default=str)

   # INCORRECT - May fail with datetime/Decimal types
   results = db.execute_query(query)
   return json.dumps(results)  # Fails on non-JSON types
   ```

### Database-Specific Rules

#### MySQL Rules

1. **Connection Validation**
   - Validate host, port, username before connecting
   - Check port is in range 1-65535
   - Validate database name format (alphanumeric + underscores)
   - Set connection timeout (default: 30 seconds)

2. **Query Classification**
   - Classify SQL commands before execution
   - Separate read-only from modification operations
   - Block genuinely dangerous operations (DROP DATABASE, SHUTDOWN)
   - Use sqlparse for accurate SQL parsing

3. **Data Type Handling**
   - Convert datetime/date to ISO format strings
   - Convert Decimal to string for precision preservation
   - Handle TINYINT(1) as boolean indicators
   - Base64 encode binary data

4. **Performance Optimization**
   - Use dictionary cursor for named column access
   - Enable autocommit for read-only queries
   - Use executemany for batch operations
   - Close cursors and connections in finally blocks

#### Oracle Rules

1. **Connection Strategies**
   - Support both thick and thin mode
   - Use service name for connections (not SID)
   - Include schema in connection parameters
   - Handle TNS configuration gracefully

2. **LOB Handling**
   - Read LOB content with .read() method
   - Check LOB size before reading
   - Convert CLOB to text, BLOB to base64
   - Include type metadata in results

3. **PL/SQL Support**
   - Support BEGIN...END blocks
   - Handle stored procedure calls
   - Manage bind variables correctly
   - Process procedure output parameters

4. **Metadata Extraction**
   - Query user_tables for table list
   - Use user_tab_columns for column info
   - Extract constraints from user_constraints
   - Include data type precision/scale information

5. **Oracle-Specific Types**
   - Preserve NUMBER precision and scale
   - Convert TIMESTAMP WITH TIME ZONE properly
   - Handle INTERVAL types
   - Process ROWID as string
   - Decode RAW data appropriately

### Security Rules

1. **SQL Injection Prevention**
   - NEVER use string formatting for SQL queries
   - ALWAYS use parameterized queries with placeholders
   - Validate and sanitize user input
   - Use prepared statements when available

2. **Credential Management**
   - Store credentials in .env file (never in code)
   - Add .env to .gitignore
   - Use environment variables for configuration
   - Mask passwords in logs and error messages

3. **Access Control**
   - Use principle of least privilege for database users
   - Separate read-only and write users when possible
   - Implement connection parameter validation
   - Audit database operations in logs

4. **Dangerous Operations**
   - Block DROP DATABASE/SCHEMA operations
   - Warn before TRUNCATE operations
   - Require confirmation for bulk DELETE
   - Prevent SHUTDOWN commands
   - Validate GRANT/REVOKE operations

### Error Handling Rules

1. **Error Categorization**
   - CONNECTION: Network, timeout, server unreachable
   - AUTHENTICATION: Invalid credentials, access denied
   - SYNTAX: SQL syntax errors
   - SCHEMA: Table/column not found
   - DATA: Constraint violations, data errors
   - SERVER: Internal server errors
   - TIMEOUT: Operation timeout
   - UNKNOWN: Unexpected errors

2. **User-Friendly Messages**
   - Provide actionable error messages
   - Hide internal implementation details
   - Suggest troubleshooting steps
   - Include error category in response

3. **Logging Strategy**
   - Log detailed errors internally (with stack trace)
   - Return sanitized errors to users
   - Use date-based log files
   - Include timestamp, category, and operation in logs

### Performance Rules

1. **Connection Pooling**
   - Use connection pools for high-throughput apps
   - Configure appropriate pool size (10-20 connections)
   - Set max_overflow for burst capacity
   - Implement connection health checks

2. **Query Optimization**
   - Use LIMIT clauses for large result sets
   - Select only needed columns (avoid SELECT *)
   - Use indexes on WHERE clause columns
   - Analyze slow queries with EXPLAIN

3. **Batch Operations**
   - Use executemany for bulk inserts (100-1000 rows)
   - Batch updates instead of individual operations
   - Commit in batches for large transactions
   - Use LOAD DATA INFILE for very large datasets (MySQL)

4. **Resource Cleanup**
   - Always close cursors after use
   - Close connections when done
   - Use context managers for automatic cleanup
   - Avoid connection leaks

## Integration Guidelines

### With Other Skills

1. **Task Management Skill**
   - Create tasks for database schema changes
   - Track database migration tasks
   - Document database-related issues

2. **QA Skill**
   - Report database connection bugs
   - Document query performance issues
   - Track data integrity problems

3. **Planning Skill**
   - Include database schema in technical planning
   - Plan database migrations
   - Design data models

4. **Security Auditor Agent**
   - Review database security configurations
   - Audit SQL injection vulnerabilities
   - Validate credential management

### With MCP Servers

1. **Claude Code Integration**
   - Provide read-only query tool for safe operations
   - Require user approval for modification operations
   - Classify SQL commands for security
   - Log all database operations

2. **Tool Separation**
   - query_sql: Read-only operations (SELECT, SHOW, DESCRIBE)
   - execute_updating_sql: Modification operations (INSERT, UPDATE, DELETE)
   - Validate SQL classification before execution

## Response Patterns

### When Guiding Database Operations

1. **Setup Phase**
   - Ask about database type (MySQL or Oracle)
   - Request connection details (or .env setup)
   - Validate configuration
   - Test connection before proceeding

2. **Query Phase**
   - Review SQL syntax
   - Suggest parameterization
   - Classify operation type
   - Execute with proper error handling

3. **Result Processing**
   - Convert data types appropriately
   - Format results for display
   - Handle empty result sets
   - Report row counts and performance

4. **Error Resolution**
   - Categorize error type
   - Provide specific troubleshooting steps
   - Suggest configuration changes if needed
   - Log error details for debugging

### Code Examples to Provide

Always provide:
- Complete, runnable code examples
- Error handling and validation
- Context manager usage
- Parameterized query examples
- Type conversion for results
- Comments explaining security considerations

### Common Recommendations

1. **For New Projects**
   - Set up .env file first
   - Use connection pooling from the start
   - Implement proper error handling
   - Add logging for all database operations

2. **For Database Migrations**
   - Extract source schema completely
   - Validate data type compatibility
   - Test with small dataset first
   - Implement rollback strategy

3. **For Performance Issues**
   - Add appropriate indexes
   - Use connection pooling
   - Implement query result caching
   - Batch operations where possible

4. **For Security Concerns**
   - Audit all SQL queries for injection risks
   - Implement parameterization everywhere
   - Rotate database credentials regularly
   - Monitor database access logs

## Anti-Patterns to Avoid

### Never Do This

1. **String Formatting in SQL**
   ```python
   # NEVER DO THIS - SQL injection risk
   query = f"SELECT * FROM users WHERE id = {user_id}"
   query = "SELECT * FROM users WHERE name = '" + username + "'"
   ```

2. **Hardcoded Credentials**
   ```python
   # NEVER DO THIS - Security risk
   conn = mysql.connector.connect(
       host="production-db.company.com",
       user="admin",
       password="super_secret_123"
   )
   ```

3. **Missing Resource Cleanup**
   ```python
   # NEVER DO THIS - Resource leak
   db = MySQLDB()
   db.connect()
   results = db.execute_query(query)
   # Missing: db.disconnect()
   ```

4. **Exposing Internal Errors**
   ```python
   # NEVER DO THIS - Exposes system details
   try:
       db.execute_query(query)
   except Exception as e:
       print(f"Error: {e}")  # Shows stack trace, paths, etc.
   ```

5. **Ignoring SQL Classification**
   ```python
   # NEVER DO THIS - Security risk
   def execute_any_sql(sql):
       # Accepts DROP DATABASE, SHUTDOWN, etc.
       return db.execute_query(sql)
   ```

## Testing Requirements

### Unit Tests Required

1. **Connection Tests**
   - Valid connection parameters
   - Invalid host/port/credentials
   - Connection timeout handling
   - Context manager functionality

2. **Query Tests**
   - Parameterized query execution
   - SQL injection prevention
   - Query classification accuracy
   - Error categorization

3. **Data Conversion Tests**
   - MySQL datetime/Decimal conversion
   - Oracle LOB handling
   - JSON serialization
   - Type metadata preservation

4. **Security Tests**
   - SQL injection attempts
   - Dangerous operation blocking
   - Credential masking in logs
   - Parameter validation

### Integration Tests Required

1. **Real Database Tests**
   - Connect to test MySQL instance
   - Connect to test Oracle instance
   - Execute CRUD operations
   - Validate result accuracy

2. **Error Handling Tests**
   - Server unreachable scenarios
   - Authentication failures
   - Invalid SQL syntax
   - Constraint violations

3. **Performance Tests**
   - Connection pool efficiency
   - Batch operation speed
   - Large result set handling
   - Query timeout behavior

## Documentation Requirements

### Every Database Function Must Include

1. **Docstring with**:
   - Purpose and functionality
   - Parameters with types
   - Return value description
   - Raises (exceptions)
   - Usage example

2. **Type Hints**:
   - Use typing module
   - Specify parameter types
   - Define return types
   - Use Optional for nullable values

3. **Error Handling**:
   - Try/except blocks
   - Error categorization
   - User-friendly messages
   - Logging of errors

### Example Documentation

```python
def execute_query(
    self,
    query: str,
    params: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Execute a SQL query and return results as a list of dictionaries.

    Args:
        query: SQL query to execute with %(name)s placeholders
        params: Optional dictionary of query parameters

    Returns:
        List of dictionaries containing query results with column names as keys

    Raises:
        mysql.connector.Error: If query execution fails
        ValueError: If query contains invalid parameters

    Example:
        >>> db = MySQLDB(source_db=True)
        >>> results = db.execute_query(
        ...     "SELECT * FROM users WHERE status = %(status)s",
        ...     params={'status': 'active'}
        ... )
        >>> for row in results:
        ...     print(f"User: {row['username']}")

    Security:
        - Uses parameterized queries to prevent SQL injection
        - Parameters are automatically escaped by mysql-connector-python
    """
    # Implementation...
```

## Success Metrics

A well-implemented database operation should demonstrate:

- No SQL injection vulnerabilities
- Proper resource cleanup (no leaks)
- Comprehensive error handling
- User-friendly error messages
- Efficient query execution
- Correct data type conversion
- Appropriate logging
- Security best practices
- Performance optimization
- Complete documentation

## Quick Reference

### MySQL Common Patterns

```python
# Read-only query
with MySQLDB(source_db=True) as db:
    results = db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))

# Write operation
with MySQLDB(source_db=False) as db:
    db.execute_query(
        "INSERT INTO logs (message, level) VALUES (%s, %s)",
        ('User login', 'INFO')
    )

# Batch operation
with MySQLDB(source_db=False) as db:
    data = [('msg1', 'INFO'), ('msg2', 'DEBUG')]
    db.execute_many("INSERT INTO logs (message, level) VALUES (%s, %s)", data)
```

### Oracle Common Patterns

```python
# Basic query
with OracleDB(source_db=True) as db:
    results = db.execute_query(
        "SELECT * FROM employees WHERE department_id = :dept_id",
        params={'dept_id': 10}
    )

# Metadata extraction
with OracleDB(source_db=True) as db:
    tables = db.execute_query("SELECT table_name FROM user_tables")

# PL/SQL block
with OracleDB(source_db=True) as db:
    db.execute_query("""
        BEGIN
            update_employee_salary(:emp_id, :new_salary);
        END;
    """, params={'emp_id': 100, 'new_salary': 75000})
```

---

**These rules ensure safe, secure, and efficient database operations across all use cases.**
