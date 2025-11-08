"""
Integration tests for AI-powered query plan generation.

Tests actual LLM calls to generate multi-query execution plans.
"""

import pytest
from pathlib import Path

from src.core.query_engine import QueryEngine
from src.core.query_plan import QueryPlan, QueryStatus
from src.utils.exceptions import QueryError


class TestAIQueryPlanGeneration:
    """Test AI-generated query plans with real LLM"""
    
    def test_generate_comparison_plan(self, electronics_db_path):
        """Test generating a plan for department comparison"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        question = "Compare IT vs Sales department employee counts"
        
        # Generate query plan using AI
        plan = engine.sql_generator.generate_query_plan(question)
        
        # Verify plan structure
        assert isinstance(plan, QueryPlan)
        assert len(plan.queries) >= 2  # At least 2 queries for comparison
        assert plan.final_query_id is not None
        assert plan.question == question
        
        # Verify queries have required fields
        for query in plan.queries:
            assert query.id is not None
            assert query.description is not None
            assert query.sql is not None
            assert "SELECT" in query.sql.upper()
    
    def test_execute_ai_generated_plan(self, electronics_db_path):
        """Test executing an AI-generated query plan"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        question = "Compare Finance vs Sales department salaries"
        
        # Generate plan
        plan = engine.sql_generator.generate_query_plan(question)
        
        # Execute plan
        executed_plan = engine.execute_plan(plan)
        
        # Verify execution
        assert executed_plan.is_complete()
        assert not executed_plan.has_errors()
        
        # Verify final results
        results = executed_plan.get_final_results()
        assert results is not None
        assert len(results["rows"]) > 0
    
    def test_needs_multi_query_detection(self, electronics_db_path):
        """Test that comparison questions are detected as needing multi-query"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        # Questions that should need multi-query
        comparison_questions = [
            "Compare IT vs Sales departments",
            "Show the difference between Finance and Marketing",
            "Compare this year versus last year",
        ]
        
        for question in comparison_questions:
            needs_multi = engine.sql_generator.needs_multi_query(question)
            assert needs_multi, f"Should detect multi-query need for: {question}"
        
        # Questions that should NOT need multi-query
        simple_questions = [
            "How many employees?",
            "What is the average salary?",
            "Show all departments",
        ]
        
        for question in simple_questions:
            needs_multi = engine.sql_generator.needs_multi_query(question)
            assert not needs_multi, f"Should NOT detect multi-query need for: {question}"
    
    def test_plan_has_valid_dependencies(self, electronics_db_path):
        """Test that generated plans have valid dependency structure"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        question = "Compare average salaries in IT vs Sales"
        
        plan = engine.sql_generator.generate_query_plan(question)
        
        # Verify no circular dependencies (will raise if circular)
        execution_order = plan.get_execution_order()
        
        # Verify execution order makes sense
        assert len(execution_order) == len(plan.queries)
        
        # Verify all dependencies are valid query IDs
        query_ids = {q.id for q in plan.queries}
        for query in plan.queries:
            for dep_id in query.depends_on:
                assert dep_id in query_ids, f"Invalid dependency: {dep_id}"
    
    def test_plan_sql_queries_are_valid(self, electronics_db_path):
        """Test that SQL in generated plans is valid SQLite"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        question = "Compare IT and Sales employee counts"
        
        plan = engine.sql_generator.generate_query_plan(question)
        
        # Verify each query has valid SQL structure
        for query in plan.queries:
            sql = query.sql
            
            # Should be a SELECT query
            assert sql.upper().startswith("SELECT"), f"Query {query.id} not a SELECT: {sql}"
            
            # Should not have markdown or code blocks
            assert "```" not in sql, f"Query {query.id} has markdown: {sql}"
            
            # Should not have explanatory text
            assert not sql.lower().startswith("sql "), f"Query {query.id} has prefix: {sql}"
    
    def test_comparison_plan_structure(self, electronics_db_path):
        """Test that comparison plans follow expected structure"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        question = "Compare November vs December sales"
        
        plan = engine.sql_generator.generate_query_plan(question)
        
        # Typical comparison plan: q1 (cat1 data), q2 (cat2 data), q3 (comparison)
        # Should have at least 2 independent queries and 1 dependent
        independent_queries = [q for q in plan.queries if len(q.depends_on) == 0]
        dependent_queries = [q for q in plan.queries if len(q.depends_on) > 0]
        
        assert len(independent_queries) >= 1, "Should have independent data queries"
        
        # Final query should depend on earlier queries
        final_query = plan.get_query(plan.final_query_id)
        assert final_query is not None
    
    def test_plan_execution_produces_results(self, electronics_db_path):
        """Test that executing AI-generated plan produces actual results"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        question = "Compare IT and Finance departments"
        
        # Generate and execute
        plan = engine.sql_generator.generate_query_plan(question)
        executed_plan = engine.execute_plan(plan)
        
        # Verify all queries produced results
        for query in executed_plan.queries:
            if query.status == QueryStatus.COMPLETED:
                assert query.results is not None
                assert "columns" in query.results
                assert "rows" in query.results
                assert query.row_count >= 0
                assert query.execution_time_ms is not None
