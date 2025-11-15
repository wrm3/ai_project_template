"""
Oracle Database Connection and Query Execution Module

Provides a robust OracleDB class with connection management, parameterized queries,
LOB handling, metadata extraction, and PL/SQL support.

Usage:
    from oracle_db import OracleDB

    # Using context manager (recommended)
    with OracleDB(source_db=True) as db:
        results = db.execute_query(
            "SELECT * FROM employees WHERE department_id = :dept_id",
            params={'dept_id': 10}
        )

    # Manual connection management
    db = OracleDB(source_db=True)
    db.connect()
    try:
        results = db.execute_query("SELECT * FROM user_tables")
    finally:
        db.disconnect()
"""

import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Tuple
import json
from datetime import datetime, date
from decimal import Decimal
import logging
import base64

# Try to import oracledb (new driver) first, fall back to cx_Oracle (legacy)
try:
    import oracledb as oracle_driver
    DRIVER_NAME = "oracledb"
except ImportError:
    try:
        import cx_Oracle as oracle_driver
        DRIVER_NAME = "cx_Oracle"
    except ImportError:
        raise ImportError(
            "No Oracle driver found. Install either:\n"
            "  pip install oracledb  (recommended, thin mode)\n"
            "  pip install cx_Oracle  (legacy, requires Oracle Client)"
        )

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class OracleDB:
    """
    Oracle database connection and query execution class.

    Manages Oracle database connections with support for parameterized queries,
    LOB handling, metadata extraction, PL/SQL execution, and context manager protocol.

    Attributes:
        host (str): Database server hostname
        port (int): Database server port
        service (str): Oracle service name
        user (str): Database username
        password (str): Database password
        schema (str): Default schema name
        dsn (str): Constructed DSN connection string
        _connection: Oracle connection object

    Example:
        >>> with OracleDB(source_db=True) as db:
        ...     results = db.execute_query(
        ...         "SELECT * FROM employees WHERE department_id = :dept_id",
        ...         params={'dept_id': 10}
        ...     )
        ...     print(f"Found {len(results)} employees")
    """

    def __init__(
        self,
        source_db: bool = True,
        host: Optional[str] = None,
        port: Optional[int] = None,
        service: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        schema: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Oracle connection parameters.

        Args:
            source_db: If True, connects to source database using src_* env vars,
                      otherwise uses tgt_* env vars
            host: Database server hostname (overrides environment variable)
            port: Database server port (overrides environment variable)
            service: Oracle service name (overrides environment variable)
            user: Database username (overrides environment variable)
            password: Database password (overrides environment variable)
            schema: Default schema name (overrides environment variable)
            **kwargs: Additional connection parameters

        Raises:
            ValueError: If required connection parameters are missing

        Example:
            >>> # From environment variables
            >>> db = OracleDB(source_db=True)
            >>>
            >>> # With explicit parameters
            >>> db = OracleDB(
            ...     host='oracle-server',
            ...     port=1521,
            ...     service='ORCL',
            ...     user='myuser',
            ...     password='mypass',
            ...     schema='MYSCHEMA'
            ... )
        """
        prefix = "src" if source_db else "tgt"

        # Use explicit parameters if provided, otherwise use environment variables
        self.host = host or os.getenv(f"{prefix}_db_host")
        self.port = port or (int(os.getenv(f"{prefix}_db_port")) if os.getenv(f"{prefix}_db_port") else None)
        self.service = service or os.getenv(f"{prefix}_db_service")
        self.user = user or os.getenv(f"{prefix}_db_user")
        self.password = password or os.getenv(f"{prefix}_db_pw")
        self.schema = schema or os.getenv(f"{prefix}_db_schema")

        # Store additional connection parameters
        self.connection_params = kwargs

        # Validate required parameters
        if not all([self.host, self.port, self.service, self.user, self.password]):
            missing = []
            if not self.host:
                missing.append(f"{prefix}_db_host")
            if not self.port:
                missing.append(f"{prefix}_db_port")
            if not self.service:
                missing.append(f"{prefix}_db_service")
            if not self.user:
                missing.append(f"{prefix}_db_user")
            if not self.password:
                missing.append(f"{prefix}_db_pw")

            raise ValueError(
                f"Missing required Oracle connection parameters: {', '.join(missing)}. "
                f"Please set these in your .env file or pass them explicitly."
            )

        # Construct DSN (Data Source Name)
        self.dsn = f"{self.host}:{self.port}/{self.service}"
        self._connection = None

        logger.info(
            f"OracleDB initialized for {self.dsn} (schema: {self.schema or '(default)'}), "
            f"using {DRIVER_NAME} driver"
        )

    def connect(self) -> None:
        """
        Establish connection to Oracle database.

        Raises:
            oracledb.Error or cx_Oracle.Error: If connection fails

        Example:
            >>> db = OracleDB(source_db=True)
            >>> db.connect()
            >>> # Use db...
            >>> db.disconnect()
        """
        try:
            self._connection = oracle_driver.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn,
                **self.connection_params
            )

            logger.info(
                f"Connected to Oracle database as {self.user} at {self.dsn} "
                f"(schema: {self.schema or '(default)'})"
            )

            # Set current schema if specified
            if self.schema:
                cursor = self._connection.cursor()
                try:
                    cursor.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {self.schema}")
                    logger.info(f"Set current schema to {self.schema}")
                finally:
                    cursor.close()

        except Exception as e:
            logger.error(f"Error connecting to Oracle database: {str(e)}")
            raise

    def disconnect(self) -> None:
        """
        Close the database connection.

        Safe to call multiple times - only disconnects if currently connected.

        Example:
            >>> db = OracleDB(source_db=True)
            >>> db.connect()
            >>> db.disconnect()  # Closes connection
            >>> db.disconnect()  # Safe to call again (no-op)
        """
        if self._connection:
            try:
                self._connection.close()
                self._connection = None
                logger.info("Disconnected from Oracle database")
            except Exception as e:
                logger.warning(f"Error during disconnect: {str(e)}")

    def is_connected(self) -> bool:
        """
        Check if database connection is active.

        Returns:
            bool: True if connected, False otherwise

        Example:
            >>> db = OracleDB(source_db=True)
            >>> db.is_connected()
            False
            >>> db.connect()
            >>> db.is_connected()
            True
        """
        if not self._connection:
            return False

        # Try to ping the connection
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            cursor.close()
            return True
        except:
            return False

    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results as a list of dictionaries.

        Supports both SELECT queries (returning results) and modification queries
        (INSERT, UPDATE, DELETE, PL/SQL blocks).

        Args:
            query: SQL query to execute with :name placeholders for Oracle
            params: Optional dictionary of query parameters

        Returns:
            List of dictionaries containing query results (for SELECT queries)
            or empty list (for modification queries)

        Raises:
            oracledb.Error or cx_Oracle.Error: If query execution fails

        Example:
            >>> db = OracleDB(source_db=True)
            >>> # SELECT query
            >>> results = db.execute_query(
            ...     "SELECT * FROM employees WHERE department_id = :dept_id AND salary > :min_sal",
            ...     params={'dept_id': 10, 'min_sal': 50000}
            ... )
            >>> for row in results:
            ...     print(f"Employee: {row['first_name']} {row['last_name']}")
            >>>
            >>> # PL/SQL block
            >>> db.execute_query("""
            ...     BEGIN
            ...         update_employee_salary(:emp_id, :new_salary);
            ...     END;
            ... """, params={'emp_id': 100, 'new_salary': 75000})

        Security:
            - Uses parameterized queries to prevent SQL injection
            - Parameters are automatically bound by the Oracle driver
            - NEVER use string formatting (f-strings, %) for SQL queries
        """
        if not self._connection:
            self.connect()

        cursor = self._connection.cursor()
        try:
            # Log query (with masked sensitive data)
            logger.debug(f"Executing query: {query[:100]}...")

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Check if this is a SELECT query (returns results)
            if cursor.description:
                # Get column names
                columns = [col[0] for col in cursor.description]

                # Fetch results and convert to list of dictionaries
                results = []
                for row in cursor:
                    row_dict = dict(zip(columns, row))
                    # Convert Oracle types to JSON-compatible types
                    converted_row = self._convert_row(row_dict)
                    results.append(converted_row)

                logger.debug(f"Query returned {len(results)} rows")
                return results
            else:
                # For INSERT/UPDATE/DELETE/PL-SQL, commit and return empty list
                self._connection.commit()
                logger.debug(f"Query affected {cursor.rowcount} rows")
                return []

        except Exception as e:
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
            query: SQL query to execute with :name placeholders
            params: List of parameter dictionaries

        Returns:
            int: Total number of rows affected

        Raises:
            oracledb.Error or cx_Oracle.Error: If query execution fails

        Example:
            >>> db = OracleDB(source_db=True)
            >>> insert_query = "INSERT INTO audit_log (message, level) VALUES (:msg, :lvl)"
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
            - Oracle automatically optimizes batch operations
        """
        if not self._connection:
            self.connect()

        cursor = self._connection.cursor()
        try:
            logger.debug(f"Executing batch query with {len(params)} parameter sets")

            cursor.executemany(query, params)
            self._connection.commit()

            rows_affected = cursor.rowcount
            logger.info(f"Batch query affected {rows_affected} rows")
            return rows_affected

        except Exception as e:
            logger.error(f"Error executing batch query: {str(e)}")
            if self._connection:
                self._connection.rollback()
            raise
        finally:
            cursor.close()

    def _convert_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Oracle data types to JSON-compatible types.

        Args:
            row: Dictionary from Oracle cursor

        Returns:
            Dictionary with converted values

        Conversion Rules:
            - LOBs (CLOB/BLOB) -> dict with type, data, size
            - datetime/date -> dict with type and ISO format
            - Decimal -> dict with type, value, precision, scale
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
        Convert a single Oracle value to JSON-compatible type.

        Args:
            value: Raw value from Oracle cursor

        Returns:
            JSON-compatible value or dict with metadata
        """
        if value is None:
            return None

        # Handle Oracle LOB types (CLOB, BLOB, NCLOB)
        if hasattr(value, 'read'):
            try:
                # Read LOB content
                lob_content = value.read()

                # Check if it's binary data (BLOB) or text data (CLOB/NCLOB)
                if isinstance(lob_content, bytes):
                    # BLOB: Convert to base64 for JSON compatibility
                    return {
                        "type": "BLOB",
                        "data": base64.b64encode(lob_content).decode('ascii'),
                        "size": len(lob_content)
                    }
                else:
                    # CLOB/NCLOB: Return as string with metadata
                    return {
                        "type": "CLOB",
                        "data": str(lob_content),
                        "size": len(str(lob_content))
                    }
            except Exception as e:
                return {
                    "type": "LOB_ERROR",
                    "error": f"Failed to read LOB: {str(e)}"
                }

        # Handle Oracle DATE and TIMESTAMP types
        if isinstance(value, datetime):
            # Check if it has timezone info
            if value.tzinfo is not None:
                return {
                    "type": "TIMESTAMP_TZ",
                    "value": value.isoformat(),
                    "timezone": str(value.tzinfo)
                }
            else:
                return {
                    "type": "TIMESTAMP",
                    "value": value.isoformat()
                }

        if isinstance(value, date):
            return {
                "type": "DATE",
                "value": value.isoformat()
            }

        # Handle Oracle NUMBER types with precision/scale metadata
        if isinstance(value, Decimal):
            sign, digits, exponent = value.as_tuple()
            return {
                "type": "NUMBER",
                "value": str(value),
                "precision": len(digits),
                "scale": -exponent if exponent < 0 else 0,
                "is_integer": exponent >= 0
            }

        # Handle Oracle INTERVAL types
        try:
            from datetime import timedelta
            if isinstance(value, timedelta):
                return {
                    "type": "INTERVAL_DS",
                    "days": value.days,
                    "seconds": value.seconds,
                    "microseconds": value.microseconds,
                    "total_seconds": value.total_seconds()
                }
        except:
            pass

        # Handle Oracle RAW type (binary data)
        if isinstance(value, bytes):
            try:
                # Try to decode as UTF-8 text
                decoded_text = value.decode('utf-8')
                return {
                    "type": "RAW_TEXT",
                    "value": decoded_text
                }
            except UnicodeDecodeError:
                # Binary data - return as base64
                return {
                    "type": "RAW_BINARY",
                    "data": base64.b64encode(value).decode('ascii'),
                    "size": len(value)
                }

        # For all other types (int, float, str, bool), return as-is
        return value

    def get_tables(self) -> List[str]:
        """
        Get list of all tables accessible to the current user.

        Returns:
            List of table names

        Example:
            >>> db = OracleDB(source_db=True)
            >>> tables = db.get_tables()
            >>> print(f"User has access to {len(tables)} tables")
            >>> print(tables[:10])  # Print first 10 tables
        """
        results = self.execute_query("SELECT table_name FROM user_tables ORDER BY table_name")
        return [row['table_name'] if isinstance(row['table_name'], str) else row['table_name']['value']
                for row in results]

    def describe_table(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get the structure of a table including columns and data types.

        Args:
            table_name: Name of the table to describe

        Returns:
            List of dictionaries describing table columns

        Example:
            >>> db = OracleDB(source_db=True)
            >>> columns = db.describe_table('EMPLOYEES')
            >>> for col in columns:
            ...     col_name = col['column_name']
            ...     col_type = col['data_type']
            ...     nullable = col['nullable']
            ...     print(f"{col_name}: {col_type} ({'NULL' if nullable == 'Y' else 'NOT NULL'})")
        """
        query = """
            SELECT
                column_name,
                data_type,
                data_length,
                data_precision,
                data_scale,
                nullable,
                column_id
            FROM user_tab_columns
            WHERE table_name = :table_name
            ORDER BY column_id
        """
        return self.execute_query(query, params={'table_name': table_name.upper()})

    def __enter__(self):
        """
        Context manager entry - establishes database connection.

        Returns:
            self: The OracleDB instance

        Example:
            >>> with OracleDB(source_db=True) as db:
            ...     results = db.execute_query("SELECT * FROM employees")
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
        String representation of OracleDB instance.

        Returns:
            str: Representation showing connection details
        """
        status = "connected" if self.is_connected() else "disconnected"
        return (
            f"OracleDB(dsn='{self.dsn}', user='{self.user}', "
            f"schema='{self.schema or '(default)'}', "
            f"driver='{DRIVER_NAME}', status='{status}')"
        )


def main():
    """
    Test the Oracle database connection and query execution.

    This function demonstrates basic usage of the OracleDB class.
    """
    print(f"Testing Oracle Database Connection (using {DRIVER_NAME} driver)...")
    print()

    try:
        # Test source database connection
        print("Connecting to source database...")
        with OracleDB(source_db=True) as db:
            print(f"Connected: {db}")
            print()

            # Test table listing
            print("Available tables (first 10):")
            tables = db.get_tables()
            for table in tables[:10]:
                print(f"  - {table}")
            print(f"  ... ({len(tables)} total tables)")
            print()

            # Test simple query
            print("Executing test query (SELECT * FROM DUAL):")
            results = db.execute_query("SELECT 'Hello from Oracle!' AS message FROM DUAL")
            print(json.dumps(results, indent=2, default=str))

        print()
        print("Oracle database test completed successfully!")

    except Exception as e:
        print(f"Oracle Error: {str(e)}")
        print()
        print("Please ensure your .env file contains:")
        print("  src_db_host=...")
        print("  src_db_port=...")
        print("  src_db_service=...")
        print("  src_db_user=...")
        print("  src_db_pw=...")
        print("  src_db_schema=... (optional)")
        print()
        print(f"Also ensure {DRIVER_NAME} is installed:")
        if DRIVER_NAME == "oracledb":
            print("  pip install oracledb")
        else:
            print("  pip install cx_Oracle")
            print("  (and Oracle Instant Client is configured)")


if __name__ == "__main__":
    main()
