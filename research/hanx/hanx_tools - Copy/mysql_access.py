#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MySQL Database Access Tool

This tool provides a simple interface to access MySQL databases configured in the
.env file. It supports both the main database and the OHLCV database as defined
in the environment variables.

Usage:
    python tools/mysql_access.py --query "SELECT * FROM your_table LIMIT 10" [--db {main|ohlcv}]
    python tools/mysql_access.py --execute "UPDATE your_table SET column='value' WHERE id=1" [--db {main|ohlcv}]
    python tools/mysql_access.py --describe "your_table" [--db {main|ohlcv}]
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Any, Union, Optional
from pathlib import Path

# Add the parent directory to the path so we can import from libs
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import the MySQL class from the project
from libs.cls_db_mysql import db_mysql

# Try to import dotenv for environment variables
try:
    from dotenv import load_dotenv
except ImportError:
    print("Installing python-dotenv...")
    os.system("pip install python-dotenv")
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

def execute_query(sql: str, db_type: str = 'main', pretty_print: bool = False) -> List[Dict[str, Any]]:
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

def execute_update(sql: str, db_type: str = 'main', pretty_print: bool = False) -> int:
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

def format_output(data: Any) -> str:
    """
    Format the output data as JSON.
    
    Args:
        data: The data to format
        
    Returns:
        A JSON string representation of the data
    """
    return json.dumps(data, indent=2, default=str)

def main():
    parser = argparse.ArgumentParser(description='MySQL Database Access Tool')
    
    # Create a mutually exclusive group for the actions
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--query', help='Execute a SELECT query')
    action_group.add_argument('--execute', help='Execute an UPDATE, INSERT, or DELETE statement')
    action_group.add_argument('--describe', help='Describe a table')
    
    # Additional options
    parser.add_argument('--db', choices=['main', 'ohlcv'], default='main', 
                        help='Which database to use (default: main)')
    parser.add_argument('--pretty-print', action='store_true',
                        help='Pretty print the SQL before executing')
    parser.add_argument('--output', choices=['json', 'table'], default='json',
                        help='Output format (default: json)')
    
    args = parser.parse_args()
    
    try:
        if args.query:
            result = execute_query(args.query, args.db, args.pretty_print)
            print(format_output(result))
        
        elif args.execute:
            affected_rows = execute_update(args.execute, args.db, args.pretty_print)
            print(format_output({"affected_rows": affected_rows}))
        
        elif args.describe:
            columns = describe_table(args.describe, args.db)
            print(format_output(columns))
    
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 