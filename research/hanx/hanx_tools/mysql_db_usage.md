# MySQL Database Tool

The `mysql_db.py` provides a convenient way to interact with MySQL databases in this project.

## Usage

```python
from tools.mysql_db import MySQLDB

# Connect to the database
with MySQLDB() as db:
    # Execute a query and get results as a list of dictionaries
    results = db.execute_query("SELECT * FROM tables LIMIT 10")
    
    # Execute a parameterized query
    results = db.execute_query(
        "SELECT * FROM tables WHERE original_name = %(name)s", 
        {"name": "example_table"}
    )
    
    # Execute batch operations
    db.execute_many(
        "INSERT INTO translations (esp, eng) VALUES (%(esp)s, %(eng)s)",
        [{"esp": "tabla", "eng": "table"}, {"esp": "columna", "eng": "column"}]
    )
```

## Key Features

- Connection management with context manager support
- Environment variable configuration
- Parameterized queries for SQL injection prevention
- Batch operations for efficient data manipulation
- Results returned as dictionaries for easy access

## Environment Variables

The tool uses these environment variables:
- `src_mysql_host`: Source database hostname
- `src_mysql_port`: Source database port
- `src_mysql_db`: Source database name
- `src_mysql_user`: Source database username
- `src_mysql_pw`: Source database password

For target database, use the `tgt_` prefix instead of `src_`.

## Example: Checking Untranslated Tables

```python
from tools.mysql_db import MySQLDB

def check_untranslated_tables():
    """Check tables with untranslated names."""
    print("Checking tables with untranslated names...")
    
    with MySQLDB() as db:
        results = db.execute_query("""
            SELECT id, original_name 
            FROM tables 
            WHERE translated_name IS NULL OR translated_name = ''
        """)
        
        if results:
            print(f"\nTables with untranslated names ({len(results)} total):")
            for row in results[:10]:  # Show first 10
                print(f"  - ID: {row['id']}, Name: {row['original_name']}")
        else:
            print("\nAll tables have been translated.")

if __name__ == "__main__":
    check_untranslated_tables()
```

## Example: Batch Translation Update

```python
from tools.mysql_db import MySQLDB

def update_translations(translation_pairs):
    """Update translations in the database.
    
    Args:
        translation_pairs: List of (esp, eng) tuples
    """
    with MySQLDB() as db:
        # Convert to list of dictionaries
        params = [{"esp": esp, "eng": eng} for esp, eng in translation_pairs]
        
        # Execute batch update
        db.execute_many("""
            INSERT INTO translations (esp, eng)
            VALUES (%(esp)s, %(eng)s)
            ON DUPLICATE KEY UPDATE eng = VALUES(eng)
        """, params)
        
        print(f"Updated {len(params)} translations")

# Example usage
if __name__ == "__main__":
    translations = [
        ("tabla", "table"),
        ("columna", "column"),
        ("indice", "index"),
        ("vista", "view")
    ]
    update_translations(translations)
``` 