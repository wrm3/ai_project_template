"""
Oracle database query tool for direct database access.
"""
import os
import cx_Oracle
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
import json

# Load environment variables
load_dotenv()

class OracleDB:
    def __init__(self, source_db: bool = True):
        """Initialize Oracle connection using environment variables.
        Args:
            source_db: If True, connects to source database, otherwise target database
        """
        prefix = "src" if source_db else "tgt"
        self.host = os.getenv(f"{prefix}_db_host")
        self.port = os.getenv(f"{prefix}_db_port")
        self.service = os.getenv(f"{prefix}_db_service")
        self.user = os.getenv(f"{prefix}_db_user")
        self.password = os.getenv(f"{prefix}_db_pw")
        self.schema = os.getenv(f"{prefix}_db_schema")
        
        if not all([self.host, self.port, self.service, self.user, self.password, self.schema]):
            raise ValueError("Missing required Oracle connection details in .env file")
        
        # Construct DSN
        self.dsn = f"{self.host}:{self.port}/{self.service}"
        self._connection = None

    def connect(self) -> None:
        """Establish connection to Oracle database."""
        try:
            self._connection = cx_Oracle.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn
            )
            print(f"Connected to Oracle database as {self.user}")
        except cx_Oracle.Error as e:
            print(f"Error connecting to Oracle database: {str(e)}")
            raise

    def disconnect(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Disconnected from Oracle database")

    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results as a list of dictionaries.
        
        Args:
            query: SQL query to execute
            params: Optional dictionary of query parameters
            
        Returns:
            List of dictionaries containing query results
        """
        if not self._connection:
            self.connect()
            
        cursor = self._connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # Get column names
            columns = [col[0] for col in cursor.description]
            
            # Fetch results and convert to list of dictionaries
            results = []
            for row in cursor:
                results.append(dict(zip(columns, row)))
                
            return results
            
        except cx_Oracle.Error as e:
            print(f"Error executing query: {str(e)}")
            raise
        finally:
            cursor.close()

    def execute_many(self, query: str, params: List[Dict]) -> None:
        """Execute a query multiple times with different parameters.
        
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
        except cx_Oracle.Error as e:
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

def main():
    """Test the Oracle database connection and query execution."""
    # Test source database connection
    with OracleDB(source_db=True) as db:
        # Test a simple query
        results = db.execute_query("SELECT * FROM user_tables")
        print("\nSource Database Tables:")
        print(json.dumps(results, indent=2, default=str))

if __name__ == "__main__":
    main() 