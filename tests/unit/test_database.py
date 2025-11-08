"""
Unit Tests for Core Database Manager
Tests database operations, schema introspection, and query execution
"""

import pytest
import sqlite3
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.database import DatabaseManager
from src.utils.exceptions import DatabaseError


class TestDatabaseManager:
    """Test DatabaseManager functionality"""
    
    @pytest.fixture
    def db_path(self, tmp_path):
        """Create a temporary test database"""
        db_file = tmp_path / "test.db"
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        
        # Create test tables
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                age INTEGER
            )
        """)
        
        cursor.execute("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount REAL,
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Insert test data
        cursor.execute("INSERT INTO users VALUES (1, 'Alice', 'alice@test.com', 25)")
        cursor.execute("INSERT INTO users VALUES (2, 'Bob', 'bob@test.com', 30)")
        cursor.execute("INSERT INTO orders VALUES (1, 1, 99.99, 'completed')")
        cursor.execute("INSERT INTO orders VALUES (2, 1, 149.50, 'pending')")
        cursor.execute("INSERT INTO orders VALUES (3, 2, 75.00, 'completed')")
        
        conn.commit()
        conn.close()
        
        return db_file
    
    def test_database_exists(self, db_path):
        """Test database_exists method"""
        db = DatabaseManager(db_path=db_path)
        assert db.database_exists() is True
        
        # Test non-existent database
        db_fake = DatabaseManager(db_path=Path("/fake/path.db"))
        assert db_fake.database_exists() is False
    
    def test_get_tables(self, db_path):
        """Test get_tables method"""
        db = DatabaseManager(db_path=db_path)
        tables = db.get_tables()
        
        assert 'users' in tables
        assert 'orders' in tables
        assert len(tables) == 2
    
    def test_get_table_info(self, db_path):
        """Test get_table_info method"""
        db = DatabaseManager(db_path=db_path)
        columns = db.get_table_info('users')
        
        assert len(columns) == 4
        column_names = [col['name'] for col in columns]
        assert 'id' in column_names
        assert 'name' in column_names
        assert 'email' in column_names
        assert 'age' in column_names
        
        # Check primary key
        id_col = next(col for col in columns if col['name'] == 'id')
        assert id_col['pk'] == 1
    
    def test_get_row_count(self, db_path):
        """Test get_row_count method"""
        db = DatabaseManager(db_path=db_path)
        
        assert db.get_row_count('users') == 2
        assert db.get_row_count('orders') == 3
    
    def test_execute_query_select(self, db_path):
        """Test execute_query with SELECT"""
        db = DatabaseManager(db_path=db_path)
        
        results = db.execute_query("SELECT * FROM users")
        assert len(results) == 2
        assert results[0]['name'] == 'Alice'
        assert results[1]['name'] == 'Bob'
    
    def test_execute_query_join(self, db_path):
        """Test execute_query with JOIN"""
        db = DatabaseManager(db_path=db_path)
        
        results = db.execute_query("""
            SELECT u.name, COUNT(o.id) as order_count
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.name
        """)
        
        assert len(results) == 2
        alice = next(r for r in results if r['name'] == 'Alice')
        assert alice['order_count'] == 2
    
    def test_execute_query_aggregation(self, db_path):
        """Test execute_query with aggregation"""
        db = DatabaseManager(db_path=db_path)
        
        results = db.execute_query("SELECT COUNT(*) as total FROM users")
        assert results[0]['total'] == 2
        
        results = db.execute_query("SELECT SUM(amount) as total FROM orders")
        assert results[0]['total'] == 324.49  # 99.99 + 149.50 + 75.00
    
    def test_execute_query_invalid_sql(self, db_path):
        """Test execute_query with invalid SQL"""
        db = DatabaseManager(db_path=db_path)
        
        with pytest.raises(DatabaseError):
            db.execute_query("INVALID SQL QUERY")
    
    def test_get_schema(self, db_path):
        """Test get_schema method"""
        db = DatabaseManager(db_path=db_path)
        schema = db.get_schema()
        
        assert len(schema) == 2
        
        users_schema = next(t for t in schema if t['name'] == 'users')
        assert users_schema['row_count'] == 2
        assert len(users_schema['columns']) == 4
        
        orders_schema = next(t for t in schema if t['name'] == 'orders')
        assert orders_schema['row_count'] == 3
    
    def test_get_schema_summary(self, db_path):
        """Test get_schema_summary method"""
        db = DatabaseManager(db_path=db_path)
        summary = db.get_schema_summary()
        
        assert 'users' in summary
        assert 'orders' in summary
        assert summary['users']['row_count'] == 2
        assert len(summary['users']['columns']) == 4
    
    def test_context_manager(self, db_path):
        """Test get_connection context manager"""
        db = DatabaseManager(db_path=db_path)
        
        with db.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM users")
            result = cursor.fetchone()
            assert result[0] == 2


class TestDatabaseIntegration:
    """Integration tests with real databases"""
    
    @pytest.fixture
    def electronics_db(self):
        """Use electronics database if it exists"""
        db_path = Path("data/database/electronics_company.db")
        if not db_path.exists():
            pytest.skip("Electronics database not found")
        return DatabaseManager(db_path=db_path)
    
    @pytest.fixture
    def airline_db(self):
        """Use airline database if it exists"""
        db_path = Path("data/database/airline_company.db")
        if not db_path.exists():
            pytest.skip("Airline database not found")
        return DatabaseManager(db_path=db_path)
    
    def test_electronics_database_structure(self, electronics_db):
        """Test electronics database has expected structure"""
        tables = electronics_db.get_tables()
        
        # Should have 12 tables
        assert len(tables) >= 10
        
        # Check for expected tables (case-insensitive)
        tables_lower = [t.lower() for t in tables]
        expected_tables = ['employees', 'sales_orders', 'products', 'customers']
        for table in expected_tables:
            assert table in tables_lower, f"Expected table {table} not found. Available: {tables}"
    
    def test_electronics_database_data(self, electronics_db):
        """Test electronics database has data"""
        # Check employee count (case-insensitive table name)
        tables = electronics_db.get_tables()
        emp_table = next((t for t in tables if t.lower() == 'employees'), None)
        if emp_table:
            employees = electronics_db.execute_query(f"SELECT COUNT(*) as count FROM {emp_table}")
            assert employees[0]['count'] > 0
        
        # Check sales orders
        sales_table = next((t for t in tables if 'sales' in t.lower() and 'order' in t.lower()), None)
        if sales_table:
            orders = electronics_db.execute_query(f"SELECT COUNT(*) as count FROM {sales_table}")
            assert orders[0]['count'] > 0
    
    def test_airline_database_structure(self, airline_db):
        """Test airline database has expected structure"""
        tables = airline_db.get_tables()
        
        # Should have 16 tables
        assert len(tables) >= 15
        
        # Check for expected tables (case-insensitive)
        tables_lower = [t.lower() for t in tables]
        expected_tables = ['aircraft', 'pilots', 'flights', 'passengers']
        for table in expected_tables:
            assert table in tables_lower, f"Expected table {table} not found. Available: {tables}"
    
    def test_airline_database_data(self, airline_db):
        """Test airline database has data"""
        # Check aircraft count
        aircraft = airline_db.execute_query("SELECT COUNT(*) as count FROM aircraft")
        assert aircraft[0]['count'] == 350
        
        # Check pilots
        pilots = airline_db.execute_query("SELECT COUNT(*) as count FROM Pilots")
        assert pilots[0]['count'] == 400
    
    def test_complex_query_electronics(self, electronics_db):
        """Test complex query on electronics database"""
        result = electronics_db.execute_query("""
            SELECT department, COUNT(*) as emp_count
            FROM Employees
            GROUP BY department
            ORDER BY emp_count DESC
            LIMIT 3
        """)
        
        assert len(result) > 0
        assert 'department' in result[0]
        assert 'emp_count' in result[0]
    
    def test_complex_query_airline(self, airline_db):
        """Test complex query on airline database"""
        result = airline_db.execute_query("""
            SELECT aircraft_type, COUNT(*) as count
            FROM aircraft
            GROUP BY aircraft_type
            ORDER BY count DESC
        """)
        
        assert len(result) > 0
        assert 'aircraft_type' in result[0]
        assert 'count' in result[0]
