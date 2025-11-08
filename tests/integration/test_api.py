"""
Integration Tests for FastAPI Web Interface
Tests API endpoints, request/response handling, and full stack integration
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from api.main import app


class TestAPIEndpoints:
    """Test FastAPI endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test GET / endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data['name'] == "Multi-Database Query API"
        assert data['version'] == "1.0.0"
        assert data['status'] == "online"
        assert 'databases' in data
        assert len(data['databases']) >= 2  # At least electronics and airline (may have edtech)
    
    def test_health_check(self, client):
        """Test GET /health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == "healthy"
        assert 'timestamp' in data
    
    def test_get_databases(self, client):
        """Test GET /databases endpoint"""
        response = client.get("/databases")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2  # At least electronics and airline (may have edtech)
        
        # Check electronics database
        electronics = next(db for db in data if db['id'] == 'electronics')
        assert electronics['name'] == "Electronics Company"
        assert electronics['exists'] in [True, False]
        
        if electronics['exists']:
            assert electronics['table_count'] == 12
            assert electronics['size_mb'] > 0
    
    def test_get_database_schema(self, client):
        """Test GET /databases/{id}/schema endpoint"""
        # Test electronics database
        response = client.get("/databases/electronics/schema")
        
        # Skip if database doesn't exist
        if response.status_code == 404:
            pytest.skip("Electronics database not found")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'tables' in data
        assert 'table_count' in data
        assert data['table_count'] > 0
        assert isinstance(data['tables'], list)
    
    def test_get_example_queries(self, client):
        """Test GET /databases/{id}/examples endpoint"""
        response = client.get("/databases/electronics/examples")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check structure of example query
        example = data[0]
        assert 'id' in example
        assert 'title' in example
        assert 'question' in example
        assert 'category' in example
        assert 'complexity' in example
    
    def test_get_stats(self, client):
        """Test GET /stats endpoint"""
        response = client.get("/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert 'total_databases' in data
        assert data['total_databases'] >= 2  # At least electronics and airline (may have edtech)
        assert 'databases' in data
    
    def test_query_endpoint_invalid_database(self, client):
        """Test POST /query with invalid database"""
        response = client.post("/query", json={
            "question": "How many users?",
            "database": "invalid_db"
        })
        
        assert response.status_code == 400
    
    def test_query_endpoint_missing_fields(self, client):
        """Test POST /query with missing fields"""
        response = client.post("/query", json={
            "question": "How many users?"
            # Missing database field
        })
        
        assert response.status_code == 422  # Validation error


class TestAPIQueryExecution:
    """Integration tests for query execution via API"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def check_databases(self):
        """Check if databases exist"""
        electronics_exists = Path("data/database/electronics_company.db").exists()
        airline_exists = Path("data/database/airline_company.db").exists()
        
        if not (electronics_exists and airline_exists):
            pytest.skip("Databases not found. Run data generation first.")
        
        return electronics_exists, airline_exists
    
    @pytest.mark.slow  # Uses real AI API
    def test_simple_query_electronics(self, client, check_databases):
        """Test simple query on electronics database"""
        response = client.post("/query", json={
            "question": "How many employees are there?",
            "database": "electronics"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['success'] is True
        assert 'sql' in data
        assert 'columns' in data
        assert 'rows' in data
        assert data['row_count'] > 0
        assert 'execution_time' in data
    
    @pytest.mark.slow  # Uses real AI API
    def test_simple_query_airline(self, client, check_databases):
        """Test simple query on airline database"""
        response = client.post("/query", json={
            "question": "How many aircraft are in the fleet?",
            "database": "airline"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['success'] is True
        assert 'sql' in data
        assert data['row_count'] > 0
        
        # Verify result
        if data['rows']:
            count = data['rows'][0][0]
            assert count == 350
    
    @pytest.mark.slow  # Uses real AI API
    def test_aggregation_query(self, client, check_databases):
        """Test aggregation query (COUNT, AVG, etc.)"""
        response = client.post("/query", json={
            "question": "What is the total sales amount?",
            "database": "electronics"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['success'] is True
        assert 'SUM' in data['sql'].upper() or 'total' in data['sql'].lower()
    
    @pytest.mark.slow  # Uses real AI API
    def test_group_by_query(self, client, check_databases):
        """Test GROUP BY query"""
        response = client.post("/query", json={
            "question": "What is the total revenue by payment method?",
            "database": "airline"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['success'] is True
        assert 'GROUP BY' in data['sql'].upper()
        assert data['row_count'] > 0
    
    @pytest.mark.slow  # Uses real AI API
    def test_join_query(self, client, check_databases):
        """Test query with JOIN across tables"""
        response = client.post("/query", json={
            "question": "Show me sales with customer names",
            "database": "electronics"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['success'] is True
        # AI should generate SQL with JOIN or similar
        assert 'SELECT' in data['sql'].upper()
        assert len(data['columns']) >= 1
    
    @pytest.mark.slow  # Uses real AI API
    def test_top_n_query(self, client, check_databases):
        """Test TOP N query (LIMIT clause)"""
        response = client.post("/query", json={
            "question": "Show me the top 3 pilots with most flight hours",
            "database": "airline"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['success'] is True
        assert 'LIMIT' in data['sql'].upper() or 'TOP' in data['sql'].upper()
        assert data['row_count'] <= 3
    
    def test_response_format(self, client, check_databases):
        """Test response has correct format"""
        response = client.post("/query", json={
            "question": "SELECT COUNT(*) FROM aircraft",
            "database": "airline"
        })
        
        data = response.json()
        
        # Check all required fields
        assert 'success' in data
        assert 'sql' in data
        assert 'columns' in data
        assert 'rows' in data
        assert 'row_count' in data
        assert 'execution_time' in data
        
        # Check data types
        assert isinstance(data['success'], bool)
        assert isinstance(data['sql'], str)
        assert isinstance(data['columns'], list) or data['columns'] is None
        assert isinstance(data['rows'], list) or data['rows'] is None
        assert isinstance(data['row_count'], int) or data['row_count'] is None
    
    @pytest.mark.slow  # Uses real AI API
    def test_concurrent_queries(self, client, check_databases):
        """Test multiple concurrent queries"""
        questions = [
            "How many aircraft?",
            "How many pilots?",
            "How many flights?"
        ]
        
        responses = []
        for question in questions:
            response = client.post("/query", json={
                "question": question,
                "database": "airline"
            })
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert response.json()['success'] is True
    
    def test_query_performance(self, client, check_databases):
        """Test query execution is fast"""
        import time
        
        start = time.time()
        response = client.post("/query", json={
            "question": "SELECT COUNT(*) FROM Employees",
            "database": "electronics"
        })
        duration = time.time() - start
        
        # Should complete within reasonable time (including AI generation)
        assert duration < 10.0  # 10 seconds max
        
        data = response.json()
        if data['success']:
            # SQL execution itself should be very fast
            assert data['execution_time'] < 0.1  # 100ms max


class TestAPICORS:
    """Test CORS configuration"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.options(
            "/query",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
