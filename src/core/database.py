"""
Database utilities and connection management
"""

import re
import sqlite3
from typing import List, Dict, Any, Optional
from pathlib import Path
from contextlib import contextmanager

from src.utils.config import Config
from src.utils.logger import setup_logger
from src.utils.exceptions import DatabaseError

logger = setup_logger(__name__)


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to database file. Uses config default if None.
        """
        self.db_path = db_path or Config.get_db_path()
        logger.debug(f"DatabaseManager initialized with path: {self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections
        
        Yields:
            sqlite3.Connection: Database connection
        """
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result rows as dictionaries with intelligently rounded numbers
        """
        logger.debug(f"Executing query (pre-check): {query[:200]}...")

        # Enforce server-side result limits to protect DB and frontend
        # Only apply LIMIT to SELECT queries (not PRAGMA, EXPLAIN, etc.)
        query_upper = query.strip().upper()
        is_select_query = query_upper.startswith('SELECT') or query_upper.startswith('WITH')
        
        if is_select_query:
            try:
                max_allowed = Config.MAX_QUERY_RESULTS
                default_limit = Config.DEFAULT_RESULT_LIMIT

                # Regex to find a LIMIT <number> (allow optional OFFSET after)
                limit_pattern = re.compile(r"\bLIMIT\s+(\d+)(?:\s+OFFSET\s+\d+)?\b", re.IGNORECASE)
                m = limit_pattern.search(query)

                if m:
                    requested = int(m.group(1))
                    if requested > max_allowed:
                        logger.warning(
                            f"Requested LIMIT {requested} exceeds MAX_QUERY_RESULTS {max_allowed}; capping to {max_allowed}"
                        )
                        # Replace the requested limit with the max_allowed
                        query = limit_pattern.sub(f"LIMIT {max_allowed}", query)
                    else:
                        logger.debug(f"Found LIMIT {requested} within allowed max {max_allowed}")
                else:
                    # No LIMIT found — append a safe default
                    logger.debug(f"No LIMIT found in query; appending default LIMIT {default_limit}")
                    # Ensure we don't break trailing semicolon
                    if query.rstrip().endswith(';'):
                        query = query.rstrip().rstrip(';')
                    query = f"{query} LIMIT {default_limit}"

            except Exception as e:
                # In the unlikely event of failure in limit enforcement, log and proceed with original query
                logger.exception(f"Failed to enforce query limits: {e}")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            results = cursor.fetchall()

            # Convert to dictionaries with intelligent number rounding
            processed_results = []
            for row in results:
                row_dict = {}
                for col, value in zip(columns, row):
                    # Apply smart rounding to numeric values
                    if isinstance(value, float):
                        # Round based on magnitude
                        if abs(value) >= 1000:
                            # Large numbers: 2 decimal places (e.g., 225235190.5599999 → 225235190.56)
                            row_dict[col] = round(value, 2)
                        elif abs(value) >= 0.01:
                            # Medium numbers: 2 decimal places (e.g., 12.3456 → 12.35)
                            row_dict[col] = round(value, 2)
                        elif value != 0:
                            # Small decimals: 4 decimal places (e.g., 0.001234 → 0.0012)
                            row_dict[col] = round(value, 4)
                        else:
                            # Zero stays zero
                            row_dict[col] = 0
                    else:
                        # Non-numeric values pass through unchanged
                        row_dict[col] = value
                
                processed_results.append(row_dict)

            return processed_results
    
    def execute_many(self, query: str, data: List[tuple]) -> int:
        """
        Execute a query with multiple parameter sets
        
        Args:
            query: SQL query string
            data: List of parameter tuples
            
        Returns:
            Number of affected rows
        """
        logger.debug(f"Executing batch query with {len(data)} rows")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, data)
            return cursor.rowcount
    
    def get_tables(self) -> List[str]:
        """
        Get list of all tables in database
        
        Returns:
            List of table names
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        results = self.execute_query(query)
        return [row['name'] for row in results]
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get column information for a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information dictionaries
        """
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def get_row_count(self, table_name: str) -> int:
        """
        Get number of rows in a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            Row count
        """
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if table exists, False otherwise
        """
        return table_name in self.get_tables()
    
    def database_exists(self) -> bool:
        """
        Check if database file exists
        
        Returns:
            True if database exists, False otherwise
        """
        return self.db_path.exists()
    
    def get_schema(self) -> List[Dict[str, Any]]:
        """
        Get database schema as list of tables
        
        Returns:
            List of tables with their schema information
        """
        if not self.database_exists():
            raise DatabaseError("Database does not exist")
        
        tables = self.get_tables()
        schema = []
        
        for table in tables:
            columns = self.get_table_info(table)
            row_count = self.get_row_count(table)
            
            schema.append({
                'name': table,
                'columns': [
                    {
                        'name': col['name'],
                        'type': col['type'],
                        'notnull': bool(col['notnull']),
                        'pk': bool(col['pk'])
                    }
                    for col in columns
                ],
                'row_count': row_count
            })
        
        return schema
    
    def get_schema_summary(self) -> Dict[str, Any]:
        """
        Get complete database schema summary
        
        Returns:
            Dictionary with schema information
        """
        if not self.database_exists():
            raise DatabaseError("Database does not exist")
        
        tables = self.get_tables()
        schema = {}
        
        for table in tables:
            columns = self.get_table_info(table)
            row_count = self.get_row_count(table)
            
            schema[table] = {
                'columns': [
                    {
                        'name': col['name'],
                        'type': col['type'],
                        'notnull': bool(col['notnull']),
                        'pk': bool(col['pk'])
                    }
                    for col in columns
                ],
                'row_count': row_count
            }
        
        return schema
