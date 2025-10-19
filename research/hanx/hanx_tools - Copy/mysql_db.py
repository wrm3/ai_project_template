"""
MySQL database query tool for direct database access.
"""
import os
import mysql.connector
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
import json

# Load environment variables
load_dotenv()

class MySQLDB:
    def __init__(self, source_db: bool = True):
        """Initialize MySQL connection using environment variables.
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
            self._connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print(f"Connected to MySQL database {self.database} as {self.user}")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL database: {str(e)}")
            raise

    def disconnect(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Disconnected from MySQL database")

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
            
        cursor = self._connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            results = cursor.fetchall()
            return results
            
        except mysql.connector.Error as e:
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
        except mysql.connector.Error as e:
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
    """Test the MySQL database connection and query execution."""
    # Test source database connection
    with MySQLDB(source_db=True) as db:
        # Test a simple query
        results = db.execute_query("SHOW TABLES")
        print("\nSource Database Tables:")
        print(json.dumps(results, indent=2, default=str))

if __name__ == "__main__":
    main() 