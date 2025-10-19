#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MySQL Database Access Utilities

This module provides functions for accessing MySQL databases configured in the
.env file. It can be imported and used in Python code for database operations.

Example:
    from tools.mysql_utils import query, execute, describe_table
    
    # Get data from the main database
    results = query("SELECT * FROM your_table LIMIT 10")
    
    # Update data in the OHLCV database
    affected_rows = execute("UPDATE your_table SET column='value' WHERE id=1", db_type='ohlcv')
    
    # Get table structure
    columns = describe_table("your_table")
"""

import os
import sys
from typing import List, Dict, Any, Union, Optional, Tuple
from pathlib import Path

# Add the parent directory to the path so we can import from libs
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the MySQL class from the project
from libs.cls_db_mysql import db_mysql

# Try to import dotenv for environment variables
try:
    from dotenv import load_dotenv
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection(db_type: str = 'main') -> db_mysql:
    """
    Get a database connection based on the specified type.
    
    Args:
        db_type: Either 'main' or 'ohlcv'
        
    Returns:
        A db_mysql instance
    """
    if db_type.lower() == 'main':
        return db_mysql(
            db_host=os.getenv('DB_HOST', 'localhost'),
            db_port=int(os.getenv('DB_PORT', 3306)),
            db_name=os.getenv('DB_NAME', 'cbtrade'),
            db_user=os.getenv('DB_USER', 'cbtrade'),
            db_pw=os.getenv('DB_PW', 'cbtrade')
        )
    elif db_type.lower() == 'ohlcv':
        return db_mysql(
            db_host=os.getenv('DB_OHLCV_HOST', 'localhost'),
            db_port=int(os.getenv('DB_OHLCV_PORT', 3306)),
            db_name=os.getenv('DB_OHLCV_NAME', 'ohlcv'),
            db_user=os.getenv('DB_OHLCV_USER', 'ohlcv'),
            db_pw=os.getenv('DB_OHLCV_PW', 'ohlcv')
        )
    else:
        raise ValueError(f"Unknown database type: {db_type}. Use 'main' or 'ohlcv'.")

def query(sql: str, db_type: str = 'main', pretty_print: bool = False) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query and return the results as a list of dictionaries.
    
    Args:
        sql: The SQL query to execute
        db_type: The database to use ('main' or 'ohlcv')
        pretty_print: Whether to pretty print the SQL before executing
        
    Returns:
        A list of dictionaries representing the result rows
    """
    db = get_db_connection(db_type)
    if pretty_print:
        db.pretty_print_sql(sql)
    return db.seld(sql)

def execute(sql: str, db_type: str = 'main', pretty_print: bool = False) -> int:
    """
    Execute an UPDATE, INSERT, or DELETE statement and return the number of affected rows.
    
    Args:
        sql: The SQL statement to execute
        db_type: The database to use ('main' or 'ohlcv')
        pretty_print: Whether to pretty print the SQL before executing
        
    Returns:
        The number of affected rows
    """
    db = get_db_connection(db_type)
    if pretty_print:
        db.pretty_print_sql(sql)
    return db.execute(sql)

def describe_table(table_name: str, db_type: str = 'main') -> List[Dict[str, Any]]:
    """
    Get the structure of a table.
    
    Args:
        table_name: The name of the table to describe
        db_type: The database to use ('main' or 'ohlcv')
        
    Returns:
        A list of dictionaries describing the table columns
    """
    db = get_db_connection(db_type)
    return db.table_cols(table_name)

def get_tables(db_type: str = 'main') -> List[str]:
    """
    Get a list of all tables in the database.
    
    Args:
        db_type: The database to use ('main' or 'ohlcv')
        
    Returns:
        A list of table names
    """
    db = get_db_connection(db_type)
    database_name = os.getenv('DB_NAME') if db_type == 'main' else os.getenv('DB_OHLCV_NAME')
    results = db.seld(f"SHOW TABLES FROM {database_name}")
    return [list(table.values())[0] for table in results]

def insert(table: str, data: Dict[str, Any], db_type: str = 'main') -> int:
    """
    Insert a record into a table.
    
    Args:
        table: The table to insert into
        data: A dictionary of column:value pairs
        db_type: The database to use ('main' or 'ohlcv')
        
    Returns:
        The ID of the inserted record
    """
    db = get_db_connection(db_type)
    database_name = os.getenv('DB_NAME') if db_type == 'main' else os.getenv('DB_OHLCV_NAME')
    return db.ins_ez(database_name, table, data)

def update(table: str, data: Dict[str, Any], where: Dict[str, Any], db_type: str = 'main') -> int:
    """
    Update records in a table.
    
    Args:
        table: The table to update
        data: A dictionary of column:value pairs to update
        where: A dictionary of column:value pairs for the WHERE clause
        db_type: The database to use ('main' or 'ohlcv')
        
    Returns:
        The number of affected rows
    """
    db = get_db_connection(db_type)
    database_name = os.getenv('DB_NAME') if db_type == 'main' else os.getenv('DB_OHLCV_NAME')
    return db.upd_ez(database_name, table, data, where)

def delete(table: str, where: Dict[str, Any], db_type: str = 'main') -> int:
    """
    Delete records from a table.
    
    Args:
        table: The table to delete from
        where: A dictionary of column:value pairs for the WHERE clause
        db_type: The database to use ('main' or 'ohlcv')
        
    Returns:
        The number of affected rows
    """
    db = get_db_connection(db_type)
    database_name = os.getenv('DB_NAME') if db_type == 'main' else os.getenv('DB_OHLCV_NAME')
    return db.del_ez(database_name, table, where)

# Example usage
if __name__ == "__main__":
    print("This module is intended to be imported, not run directly.")
    print("Example usage:")
    print("  from tools.mysql_utils import query, execute, describe_table")
    print("  results = query(\"SELECT * FROM your_table LIMIT 10\")") 