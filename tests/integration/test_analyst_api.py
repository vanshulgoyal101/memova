"""
Integration tests for analytical query API endpoints.

Tests the /ask endpoint with analytical queries:
- Query type detection
- Schema awareness
- Response structure
- Metadata tracking
- SQL/data extraction
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from api.main import app


client = TestClient(app)


@pytest.mark.skipif(
    not Path("data/database/electronics_company.db").exists(),
    reason="Database not found"
)
class TestAnalyticalQueryDetection:
    """Test that analytical queries are detected correctly."""
    
    @pytest.mark.slow
    def test_analytical_keyword_triggers_analyst(self):
        """Test that analytical keywords trigger analyst mode."""
        # This test requires API keys - mark as slow
        pytest.skip("Requires API keys and quota - run manually when needed")
        
        response = client.post("/ask", json={
            "question": "My revenue is low, how can I improve it?",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data.get('query_type') == 'analytical'
    
    def test_data_query_not_analytical(self):
        """Test that regular queries use data path."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "How many employees?",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data.get('query_type') == 'data'


@pytest.mark.skipif(
    not Path("data/database/electronics_company.db").exists(),
    reason="Database not found"
)
class TestAnalyticalResponseStructure:
    """Test the structure of analytical query responses."""
    
    @pytest.mark.slow
    def test_analytical_response_has_required_fields(self):
        """Test that analytical response includes all required fields."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "Give me insights on sales",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Required fields
        assert 'query_type' in data
        assert 'answer_text' in data
        assert 'sql' in data
        assert 'columns' in data
        assert 'rows' in data
        assert 'analysis' in data
        assert 'meta' in data
        
        # Query type should be analytical
        assert data['query_type'] == 'analytical'
    
    @pytest.mark.slow
    def test_analysis_object_structure(self):
        """Test that analysis object has correct structure."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "Analyze my customer retention",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        analysis = data.get('analysis', {})
        
        # Analysis fields
        assert 'insights' in analysis
        assert 'recommendations' in analysis
        assert 'data_points' in analysis
        assert 'queries_used' in analysis
        
        # Types
        assert isinstance(analysis['insights'], list)
        assert isinstance(analysis['recommendations'], list)
        assert isinstance(analysis['data_points'], list)
        assert isinstance(analysis['queries_used'], list)
    
    @pytest.mark.slow
    def test_meta_tracking_fields(self):
        """Test that meta includes query tracking."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "What problems exist in my sales?",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        meta = data.get('meta', {})
        
        # Meta tracking fields
        assert 'exploratory_queries' in meta
        assert 'queries_succeeded' in meta
        assert 'queries_failed' in meta
        assert 'row_count' in meta
        
        # Values should be non-negative
        assert meta['exploratory_queries'] >= 0
        assert meta['queries_succeeded'] >= 0
        assert meta['queries_failed'] >= 0


@pytest.mark.skipif(
    not Path("data/database/electronics_company.db").exists(),
    reason="Database not found"
)
class TestAnalyticalSQLExtraction:
    """Test that SQL and data are extracted correctly."""
    
    @pytest.mark.slow
    def test_sql_field_populated(self):
        """Test that SQL field contains query text."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "Recommend ways to improve revenue",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        sql = data.get('sql', '')
        
        # SQL should contain status comments
        assert '-- Query:' in sql or 'SELECT' in sql.upper()
        assert '-- Status:' in sql or len(sql) > 0
    
    @pytest.mark.slow
    def test_sql_includes_status_indicators(self):
        """Test that SQL includes success/failure indicators."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "Analyze my product performance",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        sql = data.get('sql', '')
        
        # Should have status indicators
        # Either "✓ X rows" or "❌ FAILED"
        has_status = '✓' in sql or '❌' in sql or 'Status:' in sql
        assert has_status or len(sql) == 0  # Empty SQL is also valid
    
    @pytest.mark.slow
    def test_columns_and_rows_extracted(self):
        """Test that columns and rows are extracted from successful queries."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "What insights about employees?",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # If queries succeeded, should have data
        meta = data.get('meta', {})
        if meta.get('queries_succeeded', 0) > 0:
            assert data.get('columns') is not None
            assert data.get('rows') is not None
            assert isinstance(data['columns'], list)
            assert isinstance(data['rows'], list)


@pytest.mark.skipif(
    not Path("data/database/electronics_company.db").exists(),
    reason="Database not found"
)
class TestAnalyticalSchemaAwareness:
    """Test schema awareness in production."""
    
    @pytest.mark.slow
    def test_no_hallucinated_tables(self):
        """Test that analyst doesn't hallucinate table names."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "Analyze customer feedback and satisfaction",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check SQL for common hallucinated tables
        sql = data.get('sql', '').lower()
        
        # Electronics DB doesn't have these tables
        hallucinated_tables = ['customer_feedback', 'satisfaction', 'reviews']
        
        for table in hallucinated_tables:
            if table in sql:
                # If table name appears, check if query failed
                meta = data.get('meta', {})
                # Should have at least one failure if using non-existent table
                assert meta.get('queries_failed', 0) > 0, f"Used non-existent table '{table}' but didn't fail"
    
    @pytest.mark.slow
    def test_uses_actual_schema_tables(self):
        """Test that analyst uses tables from actual schema."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "How can I improve sales?",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        sql = data.get('sql', '').lower()
        
        # Electronics DB has these tables
        actual_tables = ['employees', 'orders', 'products', 'customers', 'sales']
        
        # Should use at least one real table
        uses_real_table = any(table in sql for table in actual_tables)
        assert uses_real_table or len(sql) == 0, "Should use actual schema tables"


@pytest.mark.skipif(
    not Path("data/database/airline_company.db").exists(),
    reason="Airline database not found"
)
class TestAnalyticalMultipleDatabase:
    """Test analytical queries work across multiple databases."""
    
    @pytest.mark.slow
    def test_airline_analytical_query(self):
        """Test analytical query on airline database."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "Which aircraft require the most maintenance?",
            "company_id": "airline",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Should detect as analytical
        assert data.get('query_type') == 'analytical'
        
        # Should use airline schema tables
        sql = data.get('sql', '').lower()
        airline_tables = ['aircraft', 'maintenance', 'flights']
        uses_airline_table = any(table in sql for table in airline_tables)
        assert uses_airline_table or len(sql) == 0


@pytest.mark.skipif(
    not Path("data/database/electronics_company.db").exists(),
    reason="Database not found"
)
class TestAnalyticalErrorHandling:
    """Test error handling in analytical queries."""
    
    @pytest.mark.slow
    def test_partial_query_failures_still_return_results(self):
        """Test that partial failures still return analysis."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/ask", json={
            "question": "Analyze everything about my business",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Even with some failures, should have insights
        meta = data.get('meta', {})
        
        # If some queries failed but some succeeded
        if meta.get('queries_failed', 0) > 0 and meta.get('queries_succeeded', 0) > 0:
            # Should still have analysis
            assert data.get('analysis') is not None
            assert len(data['analysis'].get('insights', [])) > 0
    
    def test_invalid_company_id(self):
        """Test error handling for invalid company ID."""
        response = client.post("/ask", json={
            "question": "Analyze my sales",
            "company_id": "nonexistent",
            "section_ids": []
        })
        
        # Should return error
        assert response.status_code in [400, 404, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "not slow"])
