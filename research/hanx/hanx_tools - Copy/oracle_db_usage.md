# Oracle Database Tool

The `oracle_db.py` provides a convenient way to interact with Oracle databases in this project.

## Usage

```python
from tools.oracle_db import OracleDB

# Connect to the database using context manager (recommended)
with OracleDB(source_db=True) as db:
    # Execute a query and get results as a list of dictionaries
    results = db.execute_query(
        "SELECT * FROM employees WHERE department_id = :dept_id",
        {"dept_id": 10}
    )
    
    # Process results
    for row in results:
        print(f"Employee: {row['EMPLOYEE_NAME']}, Salary: {row['SALARY']}")

# Manual connection management
db = OracleDB(source_db=False)  # Connect to target database
try:
    db.connect()
    results = db.execute_query("SELECT * FROM departments")
    print(results)
finally:
    db.disconnect()
```

## Key Features

- Connection management with context manager support
- Environment variable configuration
- Parameterized queries for SQL injection prevention
- Results returned as dictionaries for easy access
- Support for both source and target database connections

## Environment Variables

The tool uses these environment variables:

### Source Database
```
src_db_host=hostname
src_db_port=1521
src_db_service=service_name
src_db_user=username
src_db_pw=password
src_db_schema=schema_name
```

### Target Database
```
tgt_db_host=hostname
tgt_db_port=1521
tgt_db_service=service_name
tgt_db_user=username
tgt_db_pw=password
tgt_db_schema=schema_name
```

## Example: Extracting Table Metadata

```python
from tools.oracle_db import OracleDB

def extract_table_metadata(schema_name):
    """Extract table metadata from Oracle database.
    
    Args:
        schema_name: The schema to extract tables from
    
    Returns:
        List of dictionaries containing table metadata
    """
    with OracleDB(source_db=True) as db:
        query = """
            SELECT 
                table_name,
                tablespace_name,
                status,
                num_rows,
                blocks,
                last_analyzed
            FROM 
                all_tables
            WHERE 
                owner = :schema_name
            ORDER BY 
                table_name
        """
        
        results = db.execute_query(query, {"schema_name": schema_name})
        return results

# Example usage
if __name__ == "__main__":
    tables = extract_table_metadata("HR")
    for table in tables:
        print(f"Table: {table['TABLE_NAME']}, Rows: {table['NUM_ROWS']}")
```

## Example: Extracting Column Metadata

```python
from tools.oracle_db import OracleDB

def extract_column_metadata(schema_name, table_name):
    """Extract column metadata for a specific table.
    
    Args:
        schema_name: The schema name
        table_name: The table name
    
    Returns:
        List of dictionaries containing column metadata
    """
    with OracleDB(source_db=True) as db:
        query = """
            SELECT 
                column_name,
                data_type,
                data_length,
                data_precision,
                data_scale,
                nullable,
                column_id
            FROM 
                all_tab_columns
            WHERE 
                owner = :schema_name
                AND table_name = :table_name
            ORDER BY 
                column_id
        """
        
        params = {
            "schema_name": schema_name,
            "table_name": table_name
        }
        
        results = db.execute_query(query, params)
        return results

# Example usage
if __name__ == "__main__":
    columns = extract_column_metadata("HR", "EMPLOYEES")
    for column in columns:
        print(f"Column: {column['COLUMN_NAME']}, Type: {column['DATA_TYPE']}")
``` 