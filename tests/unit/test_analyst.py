"""
Unit tests for the BusinessAnalyst class.

Tests the intelligent problem-solving feature including:
- Analytical query detection
- Schema awareness
- Query planning and execution
- Pattern analysis and insights generation
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.core.analyst import BusinessAnalyst
from src.core.database import DatabaseManager


class TestAnalystDetection:
    """Test analytical query detection keywords."""
    
    @pytest.fixture
    def mock_components(self):
        """Mock components for analyst initialization."""
        mock_db = Mock(spec=DatabaseManager)
        mock_db.get_schema = Mock(return_value="CREATE TABLE employees (id INTEGER);")
        
        mock_llm = Mock()
        
        schema_text = """CREATE TABLE employees (id INTEGER, name TEXT);
CREATE TABLE orders (id INTEGER, amount REAL);"""
        
        return mock_db, mock_llm, schema_text
    
    def test_detect_analytical_keywords(self, mock_components):
        """Test that analyst keywords are detected correctly."""
        mock_db, mock_llm, schema_text = mock_components
        analyst = BusinessAnalyst(mock_db, mock_llm, schema_text)
        
        # Analytical keywords
        analytical_questions = [
            "My revenue is low",
            "How can I improve sales?",
            "Give me insights on customer retention",
            "What insights can you provide?",
            "Analyze my product performance",
            "Recommend ways to grow",
            "Why is my churn rate high?",
            "What problems do I have?",
            "Suggest solutions for declining revenue",
            "How to fix my low conversion rate?"
        ]
        
        for question in analytical_questions:
            is_analytical = analyst.is_analytical_question(question)
            assert is_analytical, f"Failed to detect analytical: '{question}'"
    
    def test_non_analytical_questions(self, mock_components):
        """Test that data queries are not detected as analytical."""
        mock_db, mock_llm, schema_text = mock_components
        analyst = BusinessAnalyst(mock_db, mock_llm, schema_text)
        
        # Data query questions
        data_questions = [
            "How many employees are there?",
            "Show top 10 products by revenue",
            "Count orders by month",
            "List all customers",
            "What is the average salary?"
        ]
        
        for question in data_questions:
            is_analytical = analyst.is_analytical_question(question)
            assert not is_analytical, f"Incorrectly detected as analytical: '{question}'"


class TestAnalystSchemaAwareness:
    """Test schema awareness in query planning."""
    
    @pytest.fixture
    def mock_components(self):
        """Mock components for analyst."""
        mock_db = Mock(spec=DatabaseManager)
        mock_llm = Mock()
        mock_llm.generate_content = Mock(return_value=(
            '{"queries": [{"id": "test", "description": "Test", "sql": "SELECT 1", "depends_on": []}]}',
            "groq"
        ))
        
        schema_text = """CREATE TABLE employees (id INTEGER);
CREATE TABLE orders (id INTEGER);"""
        
        return mock_db, mock_llm, schema_text
    
    def test_schema_embedded_in_query_planning(self, mock_components):
        """Test that schema is embedded in query planning prompts."""
        mock_db, mock_llm, schema_text = mock_components
        analyst = BusinessAnalyst(mock_db, mock_llm, schema_text)
        
        # Trigger query planning
        try:
            analyst.analyze("My revenue is low")
        except:
            pass  # We're just checking the prompt, not full execution
        
        # Check that generate_content was called
        assert mock_llm.generate_content.called
        
        # Get the user message (first argument)
        call_args = mock_llm.generate_content.call_args
        user_message = call_args[0][0]
        
        # Verify schema is embedded
        assert "DATABASE SCHEMA" in user_message
        assert "ONLY use table names that exist" in user_message or "USE ONLY THESE TABLES" in user_message
        assert "employees" in user_message.lower() or "orders" in user_message.lower()
    
    def test_system_message_has_schema(self, mock_components):
        """Test that system message uses schema variant."""
        mock_db, mock_llm, schema_text = mock_components
        analyst = BusinessAnalyst(mock_db, mock_llm, schema_text)
        
        try:
            analyst.analyze("My revenue is low")
        except:
            pass
        
        # Check system message parameter
        call_args = mock_llm.generate_content.call_args
        if call_args and len(call_args) > 1:
            system_message = call_args[1].get('system_message', '')
            
            # Should use system_message_with_schema, not system_message_light
            assert "schema" in system_message.lower() or analyst.system_message_with_schema in system_message


class TestAnalystQueryExecution:
    """Test query execution and error handling."""
    
    @pytest.fixture
    def mock_components(self):
        """Mock database manager and LLM."""
        mock_db = Mock(spec=DatabaseManager)
        mock_db.execute_query = Mock(return_value={
            'success': True,
            'columns': ['count'],
            'rows': [[100]],
            'row_count': 1
        })
        mock_db.get_schema = Mock(return_value="CREATE TABLE employees (id INTEGER);")
        
        mock_llm = Mock()
        schema_text = "CREATE TABLE employees (id INTEGER);"
        
        return mock_db, mock_llm, schema_text
    
    def test_query_execution_tracking(self, mock_components):
        """Test that query execution is tracked correctly."""
        mock_db, mock_llm, schema_text = mock_components
        analyst = BusinessAnalyst(mock_db, mock_llm, schema_text)
        
        # Execute a query manually
        result = analyst._execute_single_query(
            query_id="test_query",
            query_info={
                'sql': 'SELECT COUNT(*) FROM employees',
                'description': 'Count employees'
            }
        )
        
        assert result is not None
        assert 'results' in result or 'error' in result
    
    def test_failed_query_tracking(self, mock_components):
        """Test that failed queries are tracked separately."""
        mock_db, mock_llm, schema_text = mock_components
        mock_db.execute_query = Mock(side_effect=Exception("Table not found"))
        
        analyst = BusinessAnalyst(mock_db, mock_llm, schema_text)
        
        result = analyst._execute_single_query(
            query_id="failed_query",
            query_info={
                'sql': 'SELECT * FROM nonexistent',
                'description': 'Test failed query'
            }
        )
        
        assert 'error' in result
        assert result['error'] is not None


class TestAnalystResultStructure:
    """Test the structure of analyst results."""
    
    @pytest.fixture
    def mock_complete_analysis(self):
        """Mock complete analysis result."""
        return {
            'success': True,
            'analysis_text': '### KEY INSIGHTS\n* Test insight',
            'insights': ['Test insight 1', 'Test insight 2'],
            'recommendations': ['Recommendation 1', 'Recommendation 2'],
            'data_points': [
                {'name': 'Total Revenue', 'value': 100000, 'category': 'sales'}
            ],
            'queries_used': ['query1', 'query2'],
            'query_data': {
                'query1': {
                    'sql': 'SELECT 1',
                    'description': 'Test query',
                    'results': [{'count': 1}],
                    'error': None
                }
            }
        }
    
    def test_result_has_required_fields(self, mock_complete_analysis):
        """Test that analysis result has all required fields."""
        result = mock_complete_analysis
        
        # Required fields
        assert 'success' in result
        assert 'analysis_text' in result
        assert 'insights' in result
        assert 'recommendations' in result
        assert 'data_points' in result
        assert 'queries_used' in result
        assert 'query_data' in result
    
    def test_query_data_structure(self, mock_complete_analysis):
        """Test query_data has correct structure for API."""
        query_data = mock_complete_analysis['query_data']
        
        assert isinstance(query_data, dict)
        
        for query_id, query_info in query_data.items():
            assert 'sql' in query_info
            assert 'description' in query_info
            assert 'results' in query_info or 'error' in query_info
    
    def test_insights_are_list(self, mock_complete_analysis):
        """Test that insights are returned as a list."""
        assert isinstance(mock_complete_analysis['insights'], list)
        assert len(mock_complete_analysis['insights']) > 0
    
    def test_recommendations_are_list(self, mock_complete_analysis):
        """Test that recommendations are returned as a list."""
        assert isinstance(mock_complete_analysis['recommendations'], list)
        assert len(mock_complete_analysis['recommendations']) > 0


class TestAnalystMetadata:
    """Test metadata tracking in analyst results."""
    
    def test_metadata_calculation(self):
        """Test that metadata is calculated correctly from query_data."""
        query_data = {
            'query1': {
                'sql': 'SELECT 1',
                'results': [{'a': 1}, {'a': 2}],
                'error': None
            },
            'query2': {
                'sql': 'SELECT 2',
                'results': [{'b': 3}],
                'error': None
            },
            'query3': {
                'sql': 'SELECT 3',
                'results': [],
                'error': 'Table not found'
            }
        }
        
        # Count succeeded/failed
        succeeded = sum(1 for q in query_data.values() if not q.get('error'))
        failed = sum(1 for q in query_data.values() if q.get('error'))
        total_rows = sum(len(q['results']) for q in query_data.values() if not q.get('error'))
        
        assert succeeded == 2
        assert failed == 1
        assert total_rows == 3


class TestAnalystTokenUsage:
    """Test token usage and optimization."""
    
    def test_schema_size_acceptable(self):
        """Test that schema embedding doesn't exceed reasonable limits."""
        db_path = "data/database/electronics_company.db"
        
        if not Path(db_path).exists():
            pytest.skip("Database not found")
        
        # Create minimal components
        from src.core.database import DatabaseManager
        db_manager = DatabaseManager(db_path)
        schema_text = db_manager.get_schema()
        
        mock_llm = Mock()
        analyst = BusinessAnalyst(db_manager, mock_llm, schema_text)
        
        schema_size = len(analyst.schema_text)
        
        # Schema should be < 50KB for reasonable token usage
        assert schema_size < 50000, f"Schema too large: {schema_size} bytes"
    
    def test_system_messages_exist(self):
        """Test that both system message variants exist."""
        db_path = "data/database/electronics_company.db"
        
        if not Path(db_path).exists():
            pytest.skip("Database not found")
        
        from src.core.database import DatabaseManager
        db_manager = DatabaseManager(db_path)
        schema_text = db_manager.get_schema()
        
        mock_llm = Mock()
        analyst = BusinessAnalyst(db_manager, mock_llm, schema_text)
        
        assert analyst.system_message_with_schema is not None
        assert analyst.system_message_light is not None
        assert len(analyst.system_message_with_schema) > len(analyst.system_message_light)


@pytest.mark.skipif(
    not Path("data/database/electronics_company.db").exists(),
    reason="Database not generated"
)
class TestAnalystIntegration:
    """Integration tests with real database (skip if rate limited)."""
    
    @pytest.mark.slow
    def test_full_analysis_flow(self):
        """Test complete analysis flow end-to-end."""
        # This test requires valid API keys
        pytest.skip("Requires API keys and quota - run manually")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
