#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MySQL Database Tool

This module provides comprehensive functionality for working with MySQL databases:
1. Low-level database connection and query execution
2. High-level utility functions for common operations
3. Command-line interface for direct database access

The tool supports both synchronous and asynchronous operations, and can be used
with environment variables for configuration.

Examples:
    # As an imported module
    from hanx_tools.tool_mysql import MySQLDB, query, execute, describe_table
    
    # Connect using context manager
    with MySQLDB() as db:
        results = db.execute_query("SELECT * FROM your_table LIMIT 10")
    
    # Use high-level functions
    results = query("SELECT * FROM your_table LIMIT 10")
    affected_rows = execute("UPDATE your_table SET column='value' WHERE id=1")
    columns = describe_table("your_table")
    
    # Command-line usage
    python hanx_tools/tool_mysql.py --query "SELECT * FROM your_table LIMIT 10"
    python hanx_tools/tool_mysql.py --execute "UPDATE your_table SET column='value' WHERE id=1"
    python hanx_tools/tool_mysql.py --describe "your_table"
"""

import os
import sys
import json
import argparse
import datetime
import traceback
from pathlib import Path
from typing import List, Dict, Any, Union, Optional, Tuple

# Try to import required libraries
try:
    import pymysql
    import aiomysql
    import sqlparse
    from dotenv import load_dotenv
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymysql", "aiomysql", "sqlparse", "python-dotenv"])
    import pymysql
    import aiomysql
    import sqlparse
    from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#
# PART 1: Core MySQL Database Class (from cls_db_mysql.py)
#

class MySQLConnection:
    """
    Core MySQL database connection class with comprehensive functionality.
    Supports both synchronous and asynchronous operations.
    """
    
    def __init__(self, db_host, db_port, db_name, db_user, db_pw):
        """
        Initialize MySQL connection with connection parameters.
        
        Args:
            db_host: Database host
            db_port: Database port
            db_name: Database name
            db_user: Database username
            db_pw: Database password
        """
        self.db_host = db_host
        self.db_port = int(db_port) if isinstance(db_port, str) else db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_pw = db_pw
        self.conn = None
        self.__connection = None
        self.__session = None
    
    def __open(self):
        """Open a standard database connection."""
        try:
            self.conn = pymysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw
            )
            self.__connection = self.conn
            self.__session = self.conn.cursor()
            # Set the session time zone to UTC
            self.__session.execute("SET time_zone = '+00:00';")
            self.__session.execute("SET GLOBAL log_bin_trust_function_creators = 1;")
        except (pymysql.Error, pymysql.Warning) as err:
            print(f"Error connecting to MySQL: {err}")
            raise
    
    def __opend(self):
        """Open a database connection with dictionary cursor."""
        try:
            self.conn = pymysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw
            )
            self.__connection = self.conn
            self.__session = self.conn.cursor(pymysql.cursors.DictCursor)
            self.__session.execute("SET time_zone = '+00:00';")
            self.__session.execute("SET GLOBAL log_bin_trust_function_creators = 1;")
        except (pymysql.Error, pymysql.Warning) as err:
            print(f"Error connecting to MySQL: {err}")
            raise
    
    def __close(self):
        """Close the database connection."""
        if self.__session:
            self.__session.close()
        if self.__connection:
            self.__connection.close()
    
    def pretty_print_sql(self, sql: str) -> None:
        """
        Format and print SQL query for better readability.
        
        Args:
            sql: SQL query string
        """
        formatted_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
        print(formatted_sql)
    
    def curs(self, sql):
        """
        Execute a SQL query and return a cursor.
        
        Args:
            sql: SQL query string
            
        Returns:
            Cursor object
        """
        self.__open()
        self.__session.execute(sql)
        return self.__session
    
    def cursd(self, sql):
        """
        Execute a SQL query and return a dictionary cursor.
        
        Args:
            sql: SQL query string
            
        Returns:
            Dictionary cursor object
        """
        self.__opend()
        self.__session.execute(sql)
        return self.__session
    
    def query(self, sql, args=None):
        """
        Execute a SQL query and return all results.
        
        Args:
            sql: SQL query string
            args: Query parameters
            
        Returns:
            Query results as a list of tuples
        """
        self.__open()
        self.__session.execute(sql, args)
        result = self.__session.fetchall()
        self.__close()
        return result
    
    def queryd(self, sql, args=None):
        """
        Execute a SQL query and return all results as dictionaries.
        
        Args:
            sql: SQL query string
            args: Query parameters
            
        Returns:
            Query results as a list of dictionaries
        """
        self.__opend()
        self.__session.execute(sql, args)
        result = self.__session.fetchall()
        self.__close()
        return result
    
    def execute(self, sql, args=None):
        """
        Execute a SQL statement (INSERT, UPDATE, DELETE).
        
        Args:
            sql: SQL statement
            args: Statement parameters
            
        Returns:
            Number of affected rows
        """
        self.__open()
        affected_rows = self.__session.execute(sql, args)
        self.__connection.commit()
        self.__close()
        return affected_rows
    
    def executemany(self, sql, args_list):
        """
        Execute a SQL statement with multiple parameter sets.
        
        Args:
            sql: SQL statement
            args_list: List of parameter sets
            
        Returns:
            Number of affected rows
        """
        self.__open()
        affected_rows = self.__session.executemany(sql, args_list)
        self.__connection.commit()
        self.__close()
        return affected_rows
    
    async def async_query(self, sql, args=None):
        """
        Execute a SQL query asynchronously.
        
        Args:
            sql: SQL query string
            args: Query parameters
            
        Returns:
            Query results as a list of dictionaries
        """
        conn = await aiomysql.connect(
            host=self.db_host, 
            port=self.db_port, 
            db=self.db_name, 
            user=self.db_user, 
            password=self.db_pw
        )
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql, args)
            result = await cur.fetchall()
        conn.close()
        return result
    
    async def async_execute(self, sql, args=None):
        """
        Execute a SQL statement asynchronously.
        
        Args:
            sql: SQL statement
            args: Statement parameters
            
        Returns:
            Number of affected rows
        """
        conn = await aiomysql.connect(
            host=self.db_host, 
            port=self.db_port, 
            db=self.db_name, 
            user=self.db_user, 
            password=self.db_pw
        )
        async with conn.cursor() as cur:
            affected_rows = await cur.execute(sql, args)
            await conn.commit()
        conn.close()
        return affected_rows

#
# PART 2: Context Manager MySQL Class (from tool_mysql_db.py)
#

class MySQLDB:
    """
    MySQL database class with context manager support.
    Uses environment variables for configuration.
    """
    
    def __init__(self, source_db: bool = True):
        """
        Initialize MySQL connection using environment variables.
        
        Args:
            source_db: If True, connects to source database, otherwise target database
        """
        prefix = "src" if source_db else "tgt"
        self.host = os.getenv(f"{prefix}_mysql_host")
        self.port = os.getenv(f"{prefix}_mysql_port")
        self.database = os.getenv(f"{prefix}_mysql_db")
        self.user = os.getenv(f"{prefix}_mysql_user")
        self.password = os.getenv(f"{prefix}_mysql_pw")
        
        if not all([self.host, self.port, self.database, self.user, self.password]):
            raise ValueError("Missing required MySQL connection details in .env file")
        
        self._connection = None
    
    def connect(self) -> None:
        """Establish connection to MySQL database."""
        try:
            self._connection = pymysql.connect(
                host=self.host,
                port=int(self.port),
                database=self.database,
                user=self.user,
                password=self.password
            )
            print(f"Connected to MySQL database {self.database} as {self.user}")
        except pymysql.Error as e:
            print(f"Error connecting to MySQL database: {str(e)}")
            raise
    
    def disconnect(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Disconnected from MySQL database")
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Execute a query and return results as a list of dictionaries.
        
        Args:
            query: SQL query to execute
            params: Optional dictionary of query parameters
            
        Returns:
            List of dictionaries containing query results
        """
        if not self._connection:
            self.connect()
            
        cursor = self._connection.cursor(pymysql.cursors.DictCursor)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            results = cursor.fetchall()
            return results
            
        except pymysql.Error as e:
            print(f"Error executing query: {str(e)}")
            raise
        finally:
            cursor.close()
    
    def execute_many(self, query: str, params: List[Dict]) -> None:
        """
        Execute a query multiple times with different parameters.
        
        Args:
            query: SQL query to execute
            params: List of parameter dictionaries
        """
        if not self._connection:
            self.connect()
            
        cursor = self._connection.cursor()
        try:
            cursor.executemany(query, params)
            self._connection.commit()
        except pymysql.Error as e:
            print(f"Error executing batch query: {str(e)}")
            self._connection.rollback()
            raise
        finally:
            cursor.close()
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

#
# PART 3: High-level Utility Functions (from tool_mysql_utils.py)
#

def get_db_connection(db_type: str = 'main') -> MySQLConnection:
    """
    Get a database connection based on the specified type.
    
    Args:
        db_type: Either 'main' or 'ohlcv'
        
    Returns:
        A MySQLConnection instance
    """
    if db_type.lower() == 'main':
        return MySQLConnection(
            db_host=os.getenv('DB_HOST', 'localhost'),
            db_port=int(os.getenv('DB_PORT', 3306)),
            db_name=os.getenv('DB_NAME', 'database'),
            db_user=os.getenv('DB_USER', 'user'),
            db_pw=os.getenv('DB_PW', 'password')
        )
    elif db_type.lower() == 'ohlcv':
        return MySQLConnection(
            db_host=os.getenv('DB_OHLCV_HOST', 'localhost'),
            db_port=int(os.getenv('DB_OHLCV_PORT', 3306)),
            db_name=os.getenv('DB_OHLCV_NAME', 'ohlcv'),
            db_user=os.getenv('DB_OHLCV_USER', 'user'),
            db_pw=os.getenv('DB_OHLCV_PW', 'password')
        )
    else:
        raise ValueError(f"Unknown database type: {db_type}. Use 'main' or 'ohlcv'.")

def query(sql: str, args=None, db_type: str = 'main') -> List[Dict[str, Any]]:
    """
    Execute a SQL query and return results as dictionaries.
    
    Args:
        sql: SQL query string
        args: Query parameters
        db_type: Database type ('main' or 'ohlcv')
        
    Returns:
        Query results as a list of dictionaries
    """
    db = get_db_connection(db_type)
    return db.queryd(sql, args)

def execute(sql: str, args=None, db_type: str = 'main') -> int:
    """
    Execute a SQL statement and return affected rows.
    
    Args:
        sql: SQL statement
        args: Statement parameters
        db_type: Database type ('main' or 'ohlcv')
        
    Returns:
        Number of affected rows
    """
    db = get_db_connection(db_type)
    return db.execute(sql, args)

def describe_table(table_name: str, db_type: str = 'main') -> List[Dict[str, Any]]:
    """
    Get table structure information.
    
    Args:
        table_name: Name of the table
        db_type: Database type ('main' or 'ohlcv')
        
    Returns:
        List of dictionaries with column information
    """
    sql = f"DESCRIBE {table_name}"
    return query(sql, db_type=db_type)

def list_tables(db_type: str = 'main') -> List[str]:
    """
    Get a list of tables in the database.
    
    Args:
        db_type: Database type ('main' or 'ohlcv')
        
    Returns:
        List of table names
    """
    results = query("SHOW TABLES", db_type=db_type)
    return [list(row.values())[0] for row in results]

def get_table_count(table_name: str, where_clause: str = None, db_type: str = 'main') -> int:
    """
    Get the number of rows in a table.
    
    Args:
        table_name: Name of the table
        where_clause: Optional WHERE clause
        db_type: Database type ('main' or 'ohlcv')
        
    Returns:
        Number of rows
    """
    sql = f"SELECT COUNT(*) as count FROM {table_name}"
    if where_clause:
        sql += f" WHERE {where_clause}"
    
    result = query(sql, db_type=db_type)
    return result[0]['count']

#
# PART 4: Command-line Interface (from tool_mysql_access.py)
#

def execute_query_cli(sql: str, db_type: str = 'main', pretty_print: bool = False) -> List[Dict[str, Any]]:
    """
    Execute a SQL query and format results for CLI output.
    
    Args:
        sql: SQL query string
        db_type: Database type ('main' or 'ohlcv')
        pretty_print: Whether to pretty-print the results
        
    Returns:
        Query results as a list of dictionaries
    """
    try:
        results = query(sql, db_type=db_type)
        
        if pretty_print:
            print(json.dumps(results, indent=2, default=str))
        
        return results
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return []

def execute_statement_cli(sql: str, db_type: str = 'main') -> int:
    """
    Execute a SQL statement and format results for CLI output.
    
    Args:
        sql: SQL statement
        db_type: Database type ('main' or 'ohlcv')
        
    Returns:
        Number of affected rows
    """
    try:
        affected_rows = execute(sql, db_type=db_type)
        print(f"Query executed successfully. Affected rows: {affected_rows}")
        return affected_rows
    except Exception as e:
        print(f"Error executing statement: {str(e)}")
        return 0

def describe_table_cli(table_name: str, db_type: str = 'main', pretty_print: bool = False) -> List[Dict[str, Any]]:
    """
    Describe a table and format results for CLI output.
    
    Args:
        table_name: Name of the table
        db_type: Database type ('main' or 'ohlcv')
        pretty_print: Whether to pretty-print the results
        
    Returns:
        List of dictionaries with column information
    """
    try:
        results = describe_table(table_name, db_type=db_type)
        
        if pretty_print:
            print(json.dumps(results, indent=2, default=str))
        else:
            print(f"\nTable structure for {table_name}:")
            for column in results:
                print(f"  {column['Field']} ({column['Type']})")
                if column['Key'] == 'PRI':
                    print("    Primary Key")
                if column['Null'] == 'NO':
                    print("    Not Null")
                if column['Default']:
                    print(f"    Default: {column['Default']}")
        
        return results
    except Exception as e:
        print(f"Error describing table: {str(e)}")
        return []

def main():
    """Command-line interface for MySQL database access."""
    parser = argparse.ArgumentParser(description='MySQL Database Access Tool')
    
    # Define command-line arguments
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--query', help='Execute a SELECT query')
    group.add_argument('--execute', help='Execute an INSERT, UPDATE, or DELETE statement')
    group.add_argument('--describe', help='Describe a table structure')
    group.add_argument('--list-tables', action='store_true', help='List all tables in the database')
    
    parser.add_argument('--db', choices=['main', 'ohlcv'], default='main',
                        help='Database to use (main or ohlcv)')
    parser.add_argument('--pretty', action='store_true', help='Pretty-print JSON output')
    
    args = parser.parse_args()
    
    try:
        if args.query:
            execute_query_cli(args.query, args.db, args.pretty)
        elif args.execute:
            execute_statement_cli(args.execute, args.db)
        elif args.describe:
            describe_table_cli(args.describe, args.db, args.pretty)
        elif args.list_tables:
            tables = list_tables(args.db)
            print(f"\nTables in {args.db} database:")
            for table in tables:
                print(f"  {table}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 