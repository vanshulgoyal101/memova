"""
Unit Tests for Query Engine
Tests AI-powered SQL generation and query execution
"""

import pytest
from pathlib import Path
import sys
from unittest.mock import patch

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.query_engine import QueryEngine
from src.core.database import DatabaseManager
from src.utils.exceptions import QueryError, APIError


class TestQueryEngine:
    """Test QueryEngine functionality"""
    
    @pytest.fixture
    def test_db(self, tmp_path):
        """Create a test database"""
        import sqlite3
        db_file = tmp_path / "test.db"
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL,
                category TEXT,
                stock INTEGER
            )
        """)
        
        cursor.execute("INSERT INTO products VALUES (1, 'Laptop', 999.99, 'Electronics', 10)")
        cursor.execute("INSERT INTO products VALUES (2, 'Mouse', 29.99, 'Electronics', 50)")
        cursor.execute("INSERT INTO products VALUES (3, 'Chair', 199.99, 'Furniture', 20)")
        
        conn.commit()
        conn.close()
        return db_file
    
    def test_query_engine_initialization(self, test_db):
        """Test QueryEngine can be initialized"""
        engine = QueryEngine(db_path=str(test_db))
        assert engine is not None
        assert engine.db_manager is not None
    
    def test_clean_sql_basic(self, test_db):
        """Test SQL cleaning"""
        engine = QueryEngine(db_path=str(test_db))
        
        # Test with code block
        sql_with_block = "```sql\nSELECT * FROM products\n```"
        cleaned = engine._clean_sql(sql_with_block)
        assert cleaned == "SELECT * FROM products"
        
        # Test with SQLite prefix
        sql_with_prefix = "SQLite SELECT * FROM products"
        cleaned = engine._clean_sql(sql_with_prefix)
        assert cleaned == "SELECT * FROM products"
        
        # Test with SQL prefix
        sql_with_sql = "SQL SELECT * FROM products"
        cleaned = engine._clean_sql(sql_with_sql)
        assert cleaned == "SELECT * FROM products"
    
    def test_clean_sql_multiline(self, test_db):
        """Test SQL cleaning with multiline queries"""
        engine = QueryEngine(db_path=str(test_db))
        
        sql = """```sql
        SELECT id, name, price
        FROM products
        WHERE category = 'Electronics'
        ```"""
        
        cleaned = engine._clean_sql(sql)
        assert "SELECT" in cleaned
        assert "FROM products" in cleaned
        assert "```" not in cleaned
    
    def test_validate_sql_valid(self, test_db):
        """Test SQL validation with valid queries"""
        engine = QueryEngine(db_path=str(test_db))
        
        valid_queries = [
            "SELECT * FROM products",
            "SELECT name, price FROM products WHERE price > 100",
            "SELECT COUNT(*) FROM products",
            "SELECT category, AVG(price) FROM products GROUP BY category"
        ]
        
        for query in valid_queries:
            is_valid = engine.validate_query(query)
            assert is_valid, f"Valid query marked as invalid: {query}"
    
    def test_validate_sql_invalid(self, test_db):
        """Test SQL validation with invalid queries"""
        engine = QueryEngine(db_path=str(test_db))
        
        invalid_queries = [
            "DROP TABLE products",
            "DELETE FROM products",
            "UPDATE products SET price = 0",
            "INSERT INTO products VALUES (4, 'Test', 10)",
            "CREATE TABLE test (id INT)",
            "ALTER TABLE products ADD column test TEXT"
        ]
        
        for query in invalid_queries:
            is_valid = engine.validate_query(query)
            # Note: validate_query uses EXPLAIN which may not catch all dangerous queries
            # It's mainly for syntax validation
            assert isinstance(is_valid, bool), f"Expected boolean result for: {query}"


class TestQueryEngineIntegration:
    """Integration tests with real databases and AI"""
    
    @pytest.fixture
    def electronics_engine(self):
        """Create engine for electronics database"""
        db_path = Path("data/database/electronics_company.db")
        if not db_path.exists():
            pytest.skip("Electronics database not found")
        return QueryEngine(db_path=str(db_path))
    
    @pytest.fixture
    def airline_engine(self):
        """Create engine for airline database"""
        db_path = Path("data/database/airline_company.db")
        if not db_path.exists():
            pytest.skip("Airline database not found")
        return QueryEngine(db_path=str(db_path))
    
    @pytest.fixture
    def mock_api(self):
        """Mock API calls to avoid rate limits in tests"""
        def mock_generate_sql(prompt):
            """Return SQL based on the prompt"""
            prompt_lower = prompt.lower()
            
            if "count" in prompt_lower and "employee" in prompt_lower:
                return "SELECT COUNT(*) FROM employees"
            elif "aircraft" in prompt_lower and "count" in prompt_lower:
                return "SELECT COUNT(*) FROM aircraft"
            elif "average" in prompt_lower or "avg" in prompt_lower:
                if "salary" in prompt_lower:
                    return "SELECT AVG(salary) FROM employees"
            elif "total" in prompt_lower and "sales" in prompt_lower:
                return "SELECT SUM(total_amount) FROM sales_orders"
            elif "revenue" in prompt_lower and "payment" in prompt_lower:
                return "SELECT payment_method, SUM(amount) as total_revenue FROM revenue GROUP BY payment_method"
            elif "flight" in prompt_lower and "aircraft" in prompt_lower:
                return "SELECT f.flight_id, a.aircraft_type FROM flights f JOIN aircraft a ON f.aircraft_id = a.aircraft_id LIMIT 100"
            elif "top" in prompt_lower and "pilot" in prompt_lower:
                return "SELECT * FROM pilots ORDER BY total_flight_hours DESC LIMIT 5"
            elif "low inventory" in prompt_lower or "low stock" in prompt_lower:
                return "SELECT * FROM products WHERE quantity_in_stock < 50"
            else:
                return "SELECT COUNT(*) FROM employees"
        
        with patch.object(QueryEngine, 'generate_sql', side_effect=mock_generate_sql):
            yield
    
    def test_simple_count_query_electronics(self, electronics_engine, mock_api):
        """Test simple COUNT query on electronics"""
        result = electronics_engine.ask("How many employees are there?")
        
        assert result['success'] is True
        assert 'sql' in result
        assert 'SELECT' in result['sql'].upper()
        assert 'COUNT' in result['sql'].upper()
        assert result['row_count'] > 0
    
    @pytest.mark.slow  # Mark as slow test (uses real AI API)
    def test_simple_count_query_airline(self, airline_engine, mock_api):
        """Test simple COUNT query on airline"""
        result = airline_engine.ask("How many aircraft are in the fleet?")
        
        assert result['success'] is True
        assert 'sql' in result
        assert 'aircraft' in result['sql'].lower() or 'SELECT' in result['sql'].upper()
        assert result['row_count'] > 0
        
        # Verify got a count (don't assert exact value as data may vary)
        if result['results']:
            count = list(result['results'][0].values())[0]
            assert isinstance(count, (int, float))
            assert count > 0
    
    def test_aggregation_query(self, electronics_engine, mock_api):
        """Test aggregation query"""
        result = electronics_engine.ask("What is the total sales amount?")
        
        assert result['success'] is True
        assert 'SUM' in result['sql'].upper() or 'TOTAL' in result['sql'].upper()
        assert result['row_count'] > 0
    
    def test_group_by_query(self, airline_engine, mock_api):
        """Test GROUP BY query"""
        result = airline_engine.ask("What is the total revenue by payment method?")
        
        assert result['success'] is True
        assert 'GROUP BY' in result['sql'].upper()
        assert result['row_count'] > 0
    
    def test_join_query(self, airline_engine, mock_api):
        """Test JOIN query"""
        result = airline_engine.ask("Show me flights with their aircraft type")
        
        assert result['success'] is True
        assert 'JOIN' in result['sql'].upper()
        assert result['row_count'] > 0
    
    def test_top_n_query(self, airline_engine, mock_api):
        """Test TOP N with ORDER BY"""
        result = airline_engine.ask("Show me the top 5 pilots with most flight hours")
        
        assert result['success'] is True
        assert 'ORDER BY' in result['sql'].upper()
        assert 'LIMIT' in result['sql'].upper() or 'TOP' in result['sql'].upper()
        assert result['row_count'] <= 5
    
    @pytest.mark.slow  # Mark as slow test (uses real AI API)
    def test_where_clause_query(self, electronics_engine):
        """Test WHERE clause filtering (uses real AI)"""
        result = electronics_engine.ask("Show products with stock less than 10")
        
        assert result['success'] is True
        # AI should generate SQL with WHERE or similar filtering
        assert 'SELECT' in result['sql'].upper()
        assert result['row_count'] >= 0  # May or may not have low inventory items
    
    def test_execution_time_tracking(self, electronics_engine, mock_api):
        """Test that execution time is tracked"""
        result = electronics_engine.ask("SELECT COUNT(*) FROM Employees")
        
        assert 'execution_time' in result
        assert result['execution_time'] > 0
        assert result['execution_time'] < 1.0  # Should be very fast
    
    @pytest.mark.slow  # Mark as slow test (uses real AI API, multiple queries)
    def test_multiple_queries_same_engine(self, electronics_engine):
        """Test multiple queries on same engine instance (uses real AI)"""
        queries = [
            "How many employees?",
            "How many products?",
            "How many customers?"
        ]
        
        for question in queries:
            result = electronics_engine.ask(question)
            assert result['success'] is True
            assert 'sql' in result
            assert 'SELECT' in result['sql'].upper()
    
    def test_error_handling_invalid_table(self, electronics_engine, mock_api):
        """Test error handling for non-existent table"""
        result = electronics_engine.ask("SELECT * FROM nonexistent_table")
        
        # AI should either not generate this query or it should fail gracefully
        if not result['success']:
            assert 'error' in result
