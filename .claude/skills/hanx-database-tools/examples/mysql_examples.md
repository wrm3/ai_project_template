# MySQL Database Tools - Usage Examples

This document provides comprehensive examples for using the MySQL database tools.

## Table of Contents

1. [Basic Connection](#basic-connection)
2. [Parameterized Queries](#parameterized-queries)
3. [Batch Operations](#batch-operations)
4. [Transaction Management](#transaction-management)
5. [Metadata Extraction](#metadata-extraction)
6. [Common Patterns](#common-patterns)
7. [Error Handling](#error-handling)

## Basic Connection

### Using Context Manager (Recommended)

```python
from scripts.mysql_db import MySQLDB

# Connect and execute query
with MySQLDB(source_db=True) as db:
    results = db.execute_query("SELECT * FROM users WHERE active = 1")

    for row in results:
        print(f"User ID: {row['id']}, Username: {row['username']}")
```

### Manual Connection Management

```python
from scripts.mysql_db import MySQLDB

db = MySQLDB(source_db=True)
db.connect()

try:
    results = db.execute_query("SELECT * FROM users")
    print(f"Found {len(results)} users")
finally:
    db.disconnect()
```

### Explicit Connection Parameters

```python
from scripts.mysql_db import MySQLDB

# Override environment variables
db = MySQLDB(
    host='localhost',
    port=3306,
    database='myapp',
    user='app_user',
    password='secure_password'
)

with db:
    results = db.execute_query("SELECT COUNT(*) as user_count FROM users")
    print(f"Total users: {results[0]['user_count']}")
```

## Parameterized Queries

### SELECT with Parameters

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=True) as db:
    # Single parameter
    results = db.execute_query(
        "SELECT * FROM users WHERE id = %(user_id)s",
        params={'user_id': 123}
    )

    # Multiple parameters
    results = db.execute_query(
        """
        SELECT * FROM orders
        WHERE status = %(status)s
          AND created_at >= %(start_date)s
          AND total_amount > %(min_amount)s
        ORDER BY created_at DESC
        """,
        params={
            'status': 'pending',
            'start_date': '2024-01-01',
            'min_amount': 100.00
        }
    )
```

### INSERT with Parameters

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=False) as db:
    # Insert single record
    db.execute_query(
        """
        INSERT INTO users (username, email, created_at)
        VALUES (%(username)s, %(email)s, NOW())
        """,
        params={
            'username': 'john_doe',
            'email': 'john@example.com'
        }
    )
```

### UPDATE with Parameters

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=False) as db:
    # Update specific record
    db.execute_query(
        """
        UPDATE users
        SET last_login = NOW(),
            login_count = login_count + 1
        WHERE id = %(user_id)s
        """,
        params={'user_id': 123}
    )

    # Update with multiple conditions
    db.execute_query(
        """
        UPDATE orders
        SET status = %(new_status)s,
            updated_at = NOW()
        WHERE status = %(old_status)s
          AND created_at < %(cutoff_date)s
        """,
        params={
            'new_status': 'cancelled',
            'old_status': 'pending',
            'cutoff_date': '2024-01-01'
        }
    )
```

### DELETE with Parameters

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=False) as db:
    # Delete specific records
    db.execute_query(
        "DELETE FROM logs WHERE created_at < %(cutoff_date)s",
        params={'cutoff_date': '2023-01-01'}
    )
```

## Batch Operations

### Bulk Insert

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=False) as db:
    # Prepare batch data
    batch_data = [
        {'username': 'user1', 'email': 'user1@example.com'},
        {'username': 'user2', 'email': 'user2@example.com'},
        {'username': 'user3', 'email': 'user3@example.com'},
    ]

    # Execute batch insert
    insert_query = """
        INSERT INTO users (username, email, created_at)
        VALUES (%(username)s, %(email)s, NOW())
    """

    rows_affected = db.execute_many(insert_query, batch_data)
    print(f"Inserted {rows_affected} records")
```

### Bulk Update

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=False) as db:
    # Prepare batch update data
    updates = [
        {'user_id': 1, 'new_email': 'user1_new@example.com'},
        {'user_id': 2, 'new_email': 'user2_new@example.com'},
        {'user_id': 3, 'new_email': 'user3_new@example.com'},
    ]

    # Execute batch update
    update_query = """
        UPDATE users
        SET email = %(new_email)s, updated_at = NOW()
        WHERE id = %(user_id)s
    """

    rows_affected = db.execute_many(update_query, updates)
    print(f"Updated {rows_affected} records")
```

### Processing Large Datasets

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=True) as source_db, MySQLDB(source_db=False) as target_db:
    # Read in batches
    offset = 0
    batch_size = 1000

    while True:
        # Fetch batch
        batch = source_db.execute_query(
            """
            SELECT * FROM large_table
            ORDER BY id
            LIMIT %(limit)s OFFSET %(offset)s
            """,
            params={'limit': batch_size, 'offset': offset}
        )

        if not batch:
            break  # No more data

        # Process batch
        processed_data = [
            {
                'id': row['id'],
                'data': process_data(row['data'])
            }
            for row in batch
        ]

        # Insert batch into target
        target_db.execute_many(
            "INSERT INTO processed_table (id, data) VALUES (%(id)s, %(data)s)",
            processed_data
        )

        offset += batch_size
        print(f"Processed {offset} records...")
```

## Transaction Management

### Basic Transaction

```python
from scripts.mysql_db import MySQLDB

db = MySQLDB(source_db=False, autocommit=False)  # Disable autocommit
db.connect()

try:
    # Start transaction (implicit with autocommit=False)
    db.execute_query(
        "UPDATE accounts SET balance = balance - %(amount)s WHERE id = %(from_id)s",
        params={'amount': 100.00, 'from_id': 1}
    )

    db.execute_query(
        "UPDATE accounts SET balance = balance + %(amount)s WHERE id = %(to_id)s",
        params={'amount': 100.00, 'to_id': 2}
    )

    # Commit transaction
    db._connection.commit()
    print("Transaction committed successfully")

except Exception as e:
    # Rollback on error
    db._connection.rollback()
    print(f"Transaction rolled back: {str(e)}")
    raise

finally:
    db.disconnect()
```

### Savepoint Usage

```python
from scripts.mysql_db import MySQLDB

db = MySQLDB(source_db=False, autocommit=False)
db.connect()

try:
    # First set of changes
    db.execute_query("INSERT INTO logs (message) VALUES ('Started')")

    # Create savepoint
    cursor = db._connection.cursor()
    cursor.execute("SAVEPOINT sp1")
    cursor.close()

    try:
        # Risky operation
        db.execute_query("INSERT INTO orders (product_id) VALUES (999999)")
    except:
        # Rollback to savepoint
        cursor = db._connection.cursor()
        cursor.execute("ROLLBACK TO SAVEPOINT sp1")
        cursor.close()
        print("Rolled back to savepoint")

    # Final changes
    db.execute_query("INSERT INTO logs (message) VALUES ('Completed')")

    # Commit everything
    db._connection.commit()

finally:
    db.disconnect()
```

## Metadata Extraction

### List All Tables

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=True) as db:
    tables = db.get_tables()

    print(f"Database has {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
```

### Describe Table Structure

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=True) as db:
    # Get table structure
    columns = db.describe_table('users')

    print("Table: users")
    print("-" * 80)
    for col in columns:
        field = col['Field']
        col_type = col['Type']
        null = col['Null']
        key = col['Key']
        default = col['Default']

        print(f"{field:20} {col_type:20} {null:5} {key:5} {default}")
```

### Get Table Row Count

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=True) as db:
    tables = db.get_tables()

    print("Table row counts:")
    for table in tables:
        result = db.execute_query(f"SELECT COUNT(*) as cnt FROM {table}")
        count = result[0]['cnt']
        print(f"  {table:30} {count:>10,} rows")
```

### Extract Table Indexes

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=True) as db:
    indexes = db.execute_query(
        "SHOW INDEX FROM %(table)s",
        params={'table': 'users'}
    )

    print("Indexes on 'users' table:")
    for idx in indexes:
        print(f"  Index: {idx['Key_name']}, Column: {idx['Column_name']}, "
              f"Unique: {idx['Non_unique'] == 0}")
```

## Common Patterns

### Check if Record Exists

```python
from scripts.mysql_db import MySQLDB

def user_exists(username):
    with MySQLDB(source_db=True) as db:
        results = db.execute_query(
            "SELECT COUNT(*) as cnt FROM users WHERE username = %(username)s",
            params={'username': username}
        )
        return results[0]['cnt'] > 0

if user_exists('john_doe'):
    print("User exists")
else:
    print("User not found")
```

### Get or Create Pattern

```python
from scripts.mysql_db import MySQLDB

def get_or_create_user(username, email):
    with MySQLDB(source_db=False) as db:
        # Try to get existing user
        users = db.execute_query(
            "SELECT * FROM users WHERE username = %(username)s",
            params={'username': username}
        )

        if users:
            return users[0]  # User exists

        # Create new user
        db.execute_query(
            "INSERT INTO users (username, email) VALUES (%(username)s, %(email)s)",
            params={'username': username, 'email': email}
        )

        # Fetch the newly created user
        users = db.execute_query(
            "SELECT * FROM users WHERE username = %(username)s",
            params={'username': username}
        )
        return users[0]
```

### Pagination

```python
from scripts.mysql_db import MySQLDB

def get_users_page(page=1, page_size=10):
    offset = (page - 1) * page_size

    with MySQLDB(source_db=True) as db:
        # Get total count
        total_result = db.execute_query("SELECT COUNT(*) as total FROM users")
        total = total_result[0]['total']

        # Get page of results
        users = db.execute_query(
            """
            SELECT * FROM users
            ORDER BY id
            LIMIT %(limit)s OFFSET %(offset)s
            """,
            params={'limit': page_size, 'offset': offset}
        )

        return {
            'data': users,
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }

# Usage
page1 = get_users_page(page=1, page_size=20)
print(f"Showing page {page1['page']} of {page1['total_pages']}")
print(f"Total records: {page1['total']}")
```

### Upsert (Insert or Update)

```python
from scripts.mysql_db import MySQLDB

with MySQLDB(source_db=False) as db:
    # MySQL-specific ON DUPLICATE KEY UPDATE syntax
    db.execute_query(
        """
        INSERT INTO user_stats (user_id, login_count, last_login)
        VALUES (%(user_id)s, 1, NOW())
        ON DUPLICATE KEY UPDATE
            login_count = login_count + 1,
            last_login = NOW()
        """,
        params={'user_id': 123}
    )
```

## Error Handling

### Basic Error Handling

```python
from scripts.mysql_db import MySQLDB
from mysql.connector import Error

try:
    with MySQLDB(source_db=True) as db:
        results = db.execute_query("SELECT * FROM non_existent_table")
except Error as e:
    print(f"Database error: {e.errno} - {e.msg}")
except ValueError as e:
    print(f"Configuration error: {str(e)}")
```

### Specific Error Handling

```python
from scripts.mysql_db import MySQLDB
from mysql.connector import Error, IntegrityError

with MySQLDB(source_db=False) as db:
    try:
        db.execute_query(
            "INSERT INTO users (id, username) VALUES (%(id)s, %(username)s)",
            params={'id': 1, 'username': 'john_doe'}
        )
    except IntegrityError as e:
        if e.errno == 1062:  # Duplicate entry
            print("User already exists")
        elif e.errno == 1452:  # Foreign key constraint
            print("Foreign key constraint violation")
        else:
            raise
```

### Retry Logic

```python
import time
from scripts.mysql_db import MySQLDB
from mysql.connector import OperationalError

def execute_with_retry(query, params=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            with MySQLDB(source_db=True) as db:
                return db.execute_query(query, params)
        except OperationalError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Connection failed, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise

# Usage
results = execute_with_retry("SELECT * FROM users WHERE id = %(id)s", params={'id': 123})
```

---

For more examples, see:
- `oracle_examples.md` - Oracle-specific examples
- `connection_pooling.md` - Connection pool examples
- `migration_workflow.md` - Database migration examples
