"""
MySQL Database Connection and Query Execution Module

Provides a robust MySQLDB class with connection management, parameterized queries,
context manager support, and comprehensive error handling.

Usage:
    from mysql_db import MySQLDB

    # Using context manager (recommended)
    with MySQLDB(source_db=True) as db:
        results = db.execute_query("SELECT * FROM users WHERE active = %(active)s",
                                   params={'active': 1})

    # Manual connection management
    db = MySQLDB(source_db=True)
    db.connect()
    try:
        results = db.execute_query("SELECT * FROM users")
    finally:
        db.disconnect()
"""

import os
import mysql.connector
from mysql.connector import Error, DatabaseError, InterfaceError, ProgrammingError
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Tuple
import json
from datetime import datetime, date
from decimal import Decimal
import logging

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class MySQLDB:
    """
    MySQL database connection and query execution class.

    Manages MySQL database connections with support for parameterized queries,
    context manager protocol, and comprehensive error handling.

    Attributes:
        host (str): Database server hostname
        port (int): Database server port
        database (str): Database name
        user (str): Database username
        password (str): Database password
        _connection: MySQL connection object

    Example:
        >>> with MySQLDB(source_db=True) as db:
        ...     results = db.execute_query("SELECT * FROM users LIMIT 10")
        ...     print(f"Found {len(results)} users")
    """

    def __init__(
        self,
        source_db: bool = True,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize MySQL connection parameters.

        Args:
            source_db: If True, connects to source database using src_* env vars,
                      otherwise uses tgt_* env vars
            host: Database server hostname (overrides environment variable)
            port: Database server port (overrides environment variable)
            database: Database name (overrides environment variable)
            user: Database username (overrides environment variable)
            password: Database password (overrides environment variable)
            **kwargs: Additional connection parameters passed to mysql.connector.connect()

        Raises:
            ValueError: If required connection parameters are missing

        Example:
            >>> # From environment variables
            >>> db = MySQLDB(source_db=True)
            >>>
            >>> # With explicit parameters
            >>> db = MySQLDB(host='localhost', port=3306, database='mydb',
            ...              user='myuser', password='mypass')
        """
        prefix = "src" if source_db else "tgt"

        # Use explicit parameters if provided, otherwise use environment variables
        self.host = host or os.getenv(f"{prefix}_mysql_host")
        self.port = port or (int(os.getenv(f"{prefix}_mysql_port")) if os.getenv(f"{prefix}_mysql_port") else None)
        self.database = database or os.getenv(f"{prefix}_mysql_db")
        self.user = user or os.getenv(f"{prefix}_mysql_user")
        self.password = password or os.getenv(f"{prefix}_mysql_pw")

        # Store additional connection parameters
        self.connection_params = kwargs

        # Validate required parameters
        if not all([self.host, self.port, self.user, self.password]):
            missing = []
            if not self.host:
                missing.append(f"{prefix}_mysql_host")
            if not self.port:
                missing.append(f"{prefix}_mysql_port")
            if not self.user:
                missing.append(f"{prefix}_mysql_user")
            if not self.password:
                missing.append(f"{prefix}_mysql_pw")

            raise ValueError(
                f"Missing required MySQL connection parameters: {', '.join(missing)}. "
                f"Please set these in your .env file or pass them explicitly."
            )

        self._connection = None
        logger.info(f"MySQLDB initialized for {self.host}:{self.port}/{self.database or '(no database)'}")

    def connect(self) -> None:
        """
        Establish connection to MySQL database.

        Raises:
            mysql.connector.Error: If connection fails

        Example:
            >>> db = MySQLDB(source_db=True)
            >>> db.connect()
            >>> # Use db...
            >>> db.disconnect()
        """
        try:
            connection_config = {
                'host': self.host,
                'port': self.port,
                'user': self.user,
                'password': self.password,
                'connection_timeout': self.connection_params.get('connection_timeout', 30),
                'autocommit': self.connection_params.get('autocommit', True)
            }

            # Only include database if specified
            if self.database:
                connection_config['database'] = self.database

            # Add any additional connection parameters
            for key, value in self.connection_params.items():
                if key not in connection_config:
                    connection_config[key] = value

            self._connection = mysql.connector.connect(**connection_config)

            logger.info(
                f"Connected to MySQL database {self.database or '(no database)'} "
                f"at {self.host}:{self.port} as {self.user}"
            )

        except Error as e:
            logger.error(f"Error connecting to MySQL database: {str(e)}")
            raise

    def disconnect(self) -> None:
        """
        Close the database connection.

        Safe to call multiple times - only disconnects if currently connected.

        Example:
            >>> db = MySQLDB(source_db=True)
            >>> db.connect()
            >>> db.disconnect()  # Closes connection
            >>> db.disconnect()  # Safe to call again (no-op)
        """
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None
            logger.info("Disconnected from MySQL database")

    def is_connected(self) -> bool:
        """
        Check if database connection is active.

        Returns:
            bool: True if connected, False otherwise

        Example:
            >>> db = MySQLDB(source_db=True)
            >>> db.is_connected()
            False
            >>> db.connect()
            >>> db.is_connected()
            True
        """
        return self._connection is not None and self._connection.is_connected()

    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results as a list of dictionaries.

        This method handles both SELECT queries (returning results) and
        modification queries (INSERT, UPDATE, DELETE).

        Args:
            query: SQL query to execute with %(name)s placeholders
            params: Optional dictionary of query parameters

        Returns:
            List of dictionaries containing query results (for SELECT queries)
            or empty list (for modification queries)

        Raises:
            mysql.connector.Error: If query execution fails
            ValueError: If parameters are invalid

        Example:
            >>> db = MySQLDB(source_db=True)
            >>> # SELECT query
            >>> results = db.execute_query(
            ...     "SELECT * FROM users WHERE status = %(status)s AND age > %(age)s",
            ...     params={'status': 'active', 'age': 18}
            ... )
            >>> for row in results:
            ...     print(f"User: {row['username']}, Email: {row['email']}")
            >>>
            >>> # INSERT query
            >>> db.execute_query(
            ...     "INSERT INTO users (username, email) VALUES (%(name)s, %(email)s)",
            ...     params={'name': 'john_doe', 'email': 'john@example.com'}
            ... )

        Security:
            - Uses parameterized queries to prevent SQL injection
            - Parameters are automatically escaped by mysql-connector-python
            - NEVER use string formatting (f-strings, %) for SQL queries
        """
        if not self._connection or not self._connection.is_connected():
            self.connect()

        cursor = self._connection.cursor(dictionary=True)
        try:
            # Log query (with masked sensitive data)
            logger.debug(f"Executing query: {query[:100]}...")

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Check if this is a SELECT query (returns results)
            if cursor.description:
                results = cursor.fetchall()
                # Convert MySQL types to JSON-compatible types
                converted_results = [self._convert_row(row) for row in results]
                logger.debug(f"Query returned {len(converted_results)} rows")
                return converted_results
            else:
                # For INSERT/UPDATE/DELETE, commit and return empty list
                self._connection.commit()
                logger.debug(f"Query affected {cursor.rowcount} rows")
                return []

        except Error as e:
            logger.error(f"Error executing query: {str(e)}")
            if self._connection:
                self._connection.rollback()
            raise
        finally:
            cursor.close()

    def execute_many(
        self,
        query: str,
        params: List[Dict[str, Any]]
    ) -> int:
        """
        Execute a query multiple times with different parameters (batch operation).

        Efficient for bulk INSERT, UPDATE, or DELETE operations.

        Args:
            query: SQL query to execute with %(name)s placeholders
            params: List of parameter dictionaries

        Returns:
            int: Total number of rows affected

        Raises:
            mysql.connector.Error: If query execution fails

        Example:
            >>> db = MySQLDB(source_db=True)
            >>> insert_query = "INSERT INTO logs (message, level) VALUES (%(msg)s, %(lvl)s)"
            >>> batch_data = [
            ...     {'msg': 'User login', 'lvl': 'INFO'},
            ...     {'msg': 'Data processed', 'lvl': 'DEBUG'},
            ...     {'msg': 'Error occurred', 'lvl': 'ERROR'}
            ... ]
            >>> rows_affected = db.execute_many(insert_query, batch_data)
            >>> print(f"Inserted {rows_affected} records")

        Performance:
            - Much faster than executing individual queries in a loop
            - Recommended for batches of 100-1000 records
            - For very large datasets (>10000 records), consider LOAD DATA INFILE
        """
        if not self._connection or not self._connection.is_connected():
            self.connect()

        cursor = self._connection.cursor()
        try:
            logger.debug(f"Executing batch query with {len(params)} parameter sets")

            cursor.executemany(query, params)
            self._connection.commit()

            rows_affected = cursor.rowcount
            logger.info(f"Batch query affected {rows_affected} rows")
            return rows_affected

        except Error as e:
            logger.error(f"Error executing batch query: {str(e)}")
            if self._connection:
                self._connection.rollback()
            raise
        finally:
            cursor.close()

    def _convert_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert MySQL data types to JSON-compatible types.

        Args:
            row: Dictionary from MySQL cursor

        Returns:
            Dictionary with converted values

        Conversion Rules:
            - datetime/date -> ISO format string
            - Decimal -> string (preserves precision)
            - bytes -> UTF-8 string or base64
            - None -> None (preserved)
            - int/float/str -> unchanged
        """
        if not row:
            return row

        converted = {}
        for column, value in row.items():
            converted[column] = self._convert_value(value)

        return converted

    def _convert_value(self, value: Any) -> Any:
        """
        Convert a single MySQL value to JSON-compatible type.

        Args:
            value: Raw value from MySQL cursor

        Returns:
            JSON-compatible value
        """
        if value is None:
            return None

        # Handle date/time types - convert to ISO format strings
        if isinstance(value, (datetime, date)):
            return value.isoformat()

        # Handle Decimal types - convert to string to preserve precision
        if isinstance(value, Decimal):
            return str(value)

        # Handle bytes (BINARY, VARBINARY, BLOB types)
        if isinstance(value, bytes):
            try:
                # Try to decode as UTF-8 text
                return value.decode('utf-8')
            except UnicodeDecodeError:
                # If not text, return as base64 encoded string
                import base64
                return base64.b64encode(value).decode('ascii')

        # For all other types (int, float, str, bool), return as-is
        return value

    def get_tables(self) -> List[str]:
        """
        Get list of all tables in the current database.

        Returns:
            List of table names

        Raises:
            ValueError: If no database is selected

        Example:
            >>> db = MySQLDB(source_db=True)
            >>> tables = db.get_tables()
            >>> print(f"Database has {len(tables)} tables: {', '.join(tables)}")
        """
        if not self.database:
            raise ValueError("No database selected. Cannot list tables.")

        results = self.execute_query(f"SHOW TABLES FROM {self.database}")
        # SHOW TABLES returns a dict with a single key (the database name)
        return [list(row.values())[0] for row in results]

    def describe_table(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get the structure of a table.

        Args:
            table_name: Name of the table to describe

        Returns:
            List of dictionaries describing table columns

        Example:
            >>> db = MySQLDB(source_db=True)
            >>> columns = db.describe_table('users')
            >>> for col in columns:
            ...     print(f"{col['Field']}: {col['Type']} {col['Null']} {col['Key']}")
        """
        return self.execute_query(f"DESCRIBE {table_name}")

    def __enter__(self):
        """
        Context manager entry - establishes database connection.

        Returns:
            self: The MySQLDB instance

        Example:
            >>> with MySQLDB(source_db=True) as db:
            ...     results = db.execute_query("SELECT * FROM users")
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit - closes database connection.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)

        Returns:
            False: Allows exceptions to propagate
        """
        self.disconnect()
        return False

    def __repr__(self) -> str:
        """
        String representation of MySQLDB instance.

        Returns:
            str: Representation showing connection details
        """
        status = "connected" if self.is_connected() else "disconnected"
        return (
            f"MySQLDB(host='{self.host}', port={self.port}, "
            f"database='{self.database or '(none)'}', user='{self.user}', "
            f"status='{status}')"
        )


def main():
    """
    Test the MySQL database connection and query execution.

    This function demonstrates basic usage of the MySQLDB class.
    """
    print("Testing MySQL Database Connection...")
    print()

    try:
        # Test source database connection
        print("Connecting to source database...")
        with MySQLDB(source_db=True) as db:
            print(f"Connected: {db}")
            print()

            # Test table listing
            print("Available tables:")
            try:
                tables = db.get_tables()
                for table in tables:
                    print(f"  - {table}")
            except ValueError as e:
                print(f"  {e}")
            print()

            # Test simple query
            print("Executing test query (SHOW STATUS LIKE 'Threads_connected'):")
            results = db.execute_query("SHOW STATUS LIKE 'Threads_connected'")
            print(json.dumps(results, indent=2, default=str))

        print()
        print("MySQL database test completed successfully!")

    except Error as e:
        print(f"MySQL Error: {str(e)}")
    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
        print()
        print("Please ensure your .env file contains:")
        print("  src_mysql_host=...")
        print("  src_mysql_port=...")
        print("  src_mysql_db=...")
        print("  src_mysql_user=...")
        print("  src_mysql_pw=...")


if __name__ == "__main__":
    main()
