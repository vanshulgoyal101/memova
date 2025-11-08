"""
Unit tests for SQLGenerator query plan generation.

Tests the AI-powered multi-query plan generation logic.
"""

import pytest
import json
from unittest.mock import Mock, patch

from src.core.sql_generator import SQLGenerator
from src.core.query_plan import QueryPlan, QueryStep
from src.core.llm_client import UnifiedLLMClient
from src.core.api_key_manager import APIKeyManager
from src.utils.exceptions import QueryError


@pytest.fixture
def mock_llm_client():
    """Mock UnifiedLLMClient for testing"""
    client = Mock(spec=UnifiedLLMClient)
    return client


@pytest.fixture
def mock_api_key_manager():
    """Mock APIKeyManager for testing"""
    manager = Mock(spec=APIKeyManager)
    return manager


@pytest.fixture
def sql_generator(mock_llm_client, mock_api_key_manager):
    """Create SQLGenerator with mocked dependencies"""
    schema_text = """
    TABLE: employees (id, name, department, salary)
    TABLE: sales (id, product, amount, month)
    """
    
    return SQLGenerator(
        schema_text=schema_text,
        llm_client=mock_llm_client,
        api_key_manager=mock_api_key_manager
    )


class TestNeedsMultiQuery:
    """Test multi-query detection heuristics"""
    
    def test_simple_question_single_query(self, sql_generator):
        """Test that simple questions don't need multi-query"""
        assert not sql_generator.needs_multi_query("How many employees?")
        assert not sql_generator.needs_multi_query("Show all products")
        assert not sql_generator.needs_multi_query("What is the average salary?")
    
    def test_comparison_needs_multi_query(self, sql_generator):
        """Test that comparisons need multi-query"""
        assert sql_generator.needs_multi_query("Compare November vs December sales")
        assert sql_generator.needs_multi_query("Show the difference between IT and Sales")
        assert sql_generator.needs_multi_query("Compare this year versus last year")
    
    def test_multi_entity_needs_multi_query(self, sql_generator):
        """Test that multi-entity queries need multi-query"""
        assert sql_generator.needs_multi_query("Show top 5 and bottom 5 products")
        assert sql_generator.needs_multi_query("Get the best and worst performers")
        assert sql_generator.needs_multi_query("Find highest and lowest salaries")
    
    def test_time_period_comparison(self, sql_generator):
        """Test time period comparisons"""
        assert sql_generator.needs_multi_query("This month vs last month sales")
        assert sql_generator.needs_multi_query("Year over year growth")
        assert sql_generator.needs_multi_query("Quarterly comparison")


class TestParseplanJSON:
    """Test JSON parsing for query plans"""
    
    def test_parse_valid_json(self, sql_generator):
        """Test parsing valid query plan JSON"""
        plan_json = """
        {
            "queries": [
                {
                    "id": "q1",
                    "description": "Get November sales",
                    "sql": "SELECT SUM(amount) FROM sales WHERE month='Nov'",
                    "depends_on": []
                },
                {
                    "id": "q2",
                    "description": "Get December sales",
                    "sql": "SELECT SUM(amount) FROM sales WHERE month='Dec'",
                    "depends_on": []
                }
            ],
            "final_query_id": "q2"
        }
        """
        
        result = sql_generator._parse_plan_json(plan_json)
        
        assert 'queries' in result
        assert 'final_query_id' in result
        assert len(result['queries']) == 2
        assert result['final_query_id'] == 'q2'
    
    def test_parse_json_with_markdown(self, sql_generator):
        """Test parsing JSON wrapped in markdown code blocks"""
        plan_json = """```json
        {
            "queries": [
                {"id": "q1", "description": "Test", "sql": "SELECT 1"}
            ],
            "final_query_id": "q1"
        }
        ```"""
        
        result = sql_generator._parse_plan_json(plan_json)
        
        assert len(result['queries']) == 1
    
    def test_parse_json_with_prefix_text(self, sql_generator):
        """Test parsing JSON with explanatory text before it"""
        plan_json = """Here is the query plan:
        {
            "queries": [
                {"id": "q1", "description": "Test", "sql": "SELECT 1"}
            ],
            "final_query_id": "q1"
        }
        That should work!"""
        
        result = sql_generator._parse_plan_json(plan_json)
        
        assert len(result['queries']) == 1
    
    def test_parse_invalid_json(self, sql_generator):
        """Test that invalid JSON raises QueryError"""
        with pytest.raises(QueryError, match="Invalid JSON"):
            sql_generator._parse_plan_json("not valid json {")
    
    def test_parse_missing_queries_field(self, sql_generator):
        """Test that missing 'queries' field raises error"""
        plan_json = '{"final_query_id": "q1"}'
        
        with pytest.raises(QueryError, match="missing 'queries' field"):
            sql_generator._parse_plan_json(plan_json)
    
    def test_parse_missing_final_query_id(self, sql_generator):
        """Test that missing 'final_query_id' raises error"""
        plan_json = '{"queries": []}'
        
        with pytest.raises(QueryError, match="missing 'final_query_id' field"):
            sql_generator._parse_plan_json(plan_json)
    
    def test_parse_empty_queries_list(self, sql_generator):
        """Test that empty queries list raises error"""
        plan_json = '{"queries": [], "final_query_id": "q1"}'
        
        with pytest.raises(QueryError, match="must have at least one query"):
            sql_generator._parse_plan_json(plan_json)
    
    def test_parse_query_missing_required_fields(self, sql_generator):
        """Test that queries missing required fields raise error"""
        plan_json = """
        {
            "queries": [
                {"id": "q1", "sql": "SELECT 1"}
            ],
            "final_query_id": "q1"
        }
        """
        
        with pytest.raises(QueryError, match="missing required field: description"):
            sql_generator._parse_plan_json(plan_json)
    
    def test_parse_adds_default_depends_on(self, sql_generator):
        """Test that missing depends_on gets default empty list"""
        plan_json = """
        {
            "queries": [
                {"id": "q1", "description": "Test", "sql": "SELECT 1"}
            ],
            "final_query_id": "q1"
        }
        """
        
        result = sql_generator._parse_plan_json(plan_json)
        
        assert result['queries'][0]['depends_on'] == []


class TestBuildQueryPlan:
    """Test QueryPlan object construction"""
    
    def test_build_simple_plan(self, sql_generator):
        """Test building a simple query plan"""
        plan_dict = {
            "queries": [
                {
                    "id": "q1",
                    "description": "Count employees",
                    "sql": "SELECT COUNT(*) FROM employees",
                    "depends_on": []
                }
            ],
            "final_query_id": "q1"
        }
        
        plan = sql_generator._build_query_plan(plan_dict, "How many employees?")
        
        assert isinstance(plan, QueryPlan)
        assert len(plan.queries) == 1
        assert plan.queries[0].id == "q1"
        assert plan.final_query_id == "q1"
        assert plan.question == "How many employees?"
    
    def test_build_plan_cleans_sql(self, sql_generator):
        """Test that SQL in plan gets cleaned"""
        plan_dict = {
            "queries": [
                {
                    "id": "q1",
                    "description": "Test",
                    "sql": "```sql\nSELECT * FROM employees\n```",
                    "depends_on": []
                }
            ],
            "final_query_id": "q1"
        }
        
        plan = sql_generator._build_query_plan(plan_dict, "Test question")
        
        # SQL should be cleaned (no markdown)
        assert "```" not in plan.queries[0].sql
        assert plan.queries[0].sql == "SELECT * FROM employees"
    
    def test_build_plan_with_dependencies(self, sql_generator):
        """Test building plan with query dependencies"""
        plan_dict = {
            "queries": [
                {
                    "id": "q1",
                    "description": "First query",
                    "sql": "SELECT AVG(salary) FROM employees",
                    "depends_on": []
                },
                {
                    "id": "q2",
                    "description": "Second query",
                    "sql": "SELECT COUNT(*) FROM employees WHERE salary > (SELECT AVG FROM q1)",
                    "depends_on": ["q1"]
                }
            ],
            "final_query_id": "q2"
        }
        
        plan = sql_generator._build_query_plan(plan_dict, "Test")
        
        assert len(plan.queries) == 2
        assert plan.queries[1].depends_on == ["q1"]


class TestGenerateQueryPlan:
    """Test end-to-end query plan generation"""
    
    def test_generate_plan_success(self, sql_generator, mock_llm_client):
        """Test successful query plan generation"""
        # Mock LLM response with valid JSON
        mock_response = """
        {
            "queries": [
                {
                    "id": "q1",
                    "description": "Get November sales",
                    "sql": "SELECT SUM(amount) as total FROM sales WHERE month='Nov'",
                    "depends_on": []
                },
                {
                    "id": "q2",
                    "description": "Get December sales",
                    "sql": "SELECT SUM(amount) as total FROM sales WHERE month='Dec'",
                    "depends_on": []
                },
                {
                    "id": "q3",
                    "description": "Compare months",
                    "sql": "SELECT (SELECT total FROM q1) as nov, (SELECT total FROM q2) as dec",
                    "depends_on": ["q1", "q2"]
                }
            ],
            "final_query_id": "q3"
        }
        """
        mock_llm_client.generate_content.return_value = (mock_response, "groq")
        
        plan = sql_generator.generate_query_plan("Compare November vs December sales")
        
        assert isinstance(plan, QueryPlan)
        assert len(plan.queries) == 3
        assert plan.final_query_id == "q3"
        assert plan.question == "Compare November vs December sales"
        
        # Verify LLM was called
        mock_llm_client.generate_content.assert_called_once()
    
    def test_generate_plan_empty_question(self, sql_generator):
        """Test that empty question raises error"""
        with pytest.raises(QueryError, match="cannot be empty"):
            sql_generator.generate_query_plan("")
    
    def test_generate_plan_json_parse_error(self, sql_generator, mock_llm_client):
        """Test handling of invalid JSON from LLM"""
        mock_llm_client.generate_content.return_value = ("invalid json {", "groq")
        
        with pytest.raises(QueryError, match="Failed to generate query plan"):
            sql_generator.generate_query_plan("Test question")
    
    def test_generate_plan_llm_error(self, sql_generator, mock_llm_client):
        """Test handling of LLM errors"""
        mock_llm_client.generate_content.side_effect = Exception("API error")
        
        with pytest.raises(QueryError, match="Failed to generate query plan"):
            sql_generator.generate_query_plan("Test question")


class TestCreatePlanPrompt:
    """Test query plan prompt engineering"""
    
    def test_prompt_includes_schema(self, sql_generator):
        """Test that prompt includes database schema"""
        prompt = sql_generator._create_plan_prompt("Test question")
        
        assert "employees" in prompt
        assert "sales" in prompt
    
    def test_prompt_includes_question(self, sql_generator):
        """Test that prompt includes the question"""
        question = "Compare IT vs Sales departments"
        prompt = sql_generator._create_plan_prompt(question)
        
        assert question in prompt
    
    def test_prompt_includes_json_format(self, sql_generator):
        """Test that prompt specifies JSON output format"""
        prompt = sql_generator._create_plan_prompt("Test")
        
        assert "JSON" in prompt
        assert "queries" in prompt
        assert "final_query_id" in prompt
    
    def test_prompt_includes_dependency_rules(self, sql_generator):
        """Test that prompt explains dependency handling"""
        prompt = sql_generator._create_plan_prompt("Test")
        
        assert "depends_on" in prompt
        assert "FROM q1" in prompt or "FROM q2" in prompt
