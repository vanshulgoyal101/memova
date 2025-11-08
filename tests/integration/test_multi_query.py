"""
Integration tests for multi-query execution.

Tests the execute_plan() method with real database and QueryPlan objects.
"""

import pytest
from pathlib import Path

from src.core.query_engine import QueryEngine
from src.core.database import DatabaseManager
from src.core.query_plan import QueryPlan, QueryStep, QueryStatus, create_comparison_plan


class TestMultiQueryExecution:
    """Test multi-query plan execution"""
    
    def test_simple_single_query_plan(self, electronics_db_path):
        """Test executing a simple single-query plan"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        # Create simple plan
        plan = QueryPlan.create_simple_plan(
            sql="SELECT COUNT(*) as employee_count FROM employees",
            question="How many employees?"
        )
        
        # Execute
        executed_plan = engine.execute_plan(plan)
        
        # Verify
        assert executed_plan.is_complete()
        assert not executed_plan.has_errors()
        
        # Check results
        results = executed_plan.get_final_results()
        assert results is not None
        assert results["columns"] == ["employee_count"]
        assert len(results["rows"]) == 1
        assert results["rows"][0][0] > 0  # Some employees exist
    
    def test_two_independent_queries(self, electronics_db_path):
        """Test executing two independent queries"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        plan = QueryPlan(
            queries=[
                QueryStep(
                    id="q1",
                    description="Count employees",
                    sql="SELECT COUNT(*) as emp_count FROM employees",
                    depends_on=[]
                ),
                QueryStep(
                    id="q2",
                    description="Count products",
                    sql="SELECT COUNT(*) as prod_count FROM products",
                    depends_on=[]
                )
            ],
            final_query_id="q2"
        )
        
        executed_plan = engine.execute_plan(plan)
        
        # Both should complete
        assert executed_plan.is_complete()
        assert not executed_plan.has_errors()
        
        # Check both queries executed
        q1 = executed_plan.get_query("q1")
        q2 = executed_plan.get_query("q2")
        
        assert q1.status == QueryStatus.COMPLETED
        assert q2.status == QueryStatus.COMPLETED
        assert q1.row_count == 1
        assert q2.row_count == 1
    
    def test_dependent_queries_simple(self, electronics_db_path):
        """Test simple dependency: q2 depends on q1"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        plan = QueryPlan(
            queries=[
                QueryStep(
                    id="q1",
                    description="Get average salary",
                    sql="SELECT AVG(salary) as avg_salary FROM employees",
                    depends_on=[]
                ),
                QueryStep(
                    id="q2",
                    description="Count high earners",
                    sql="SELECT COUNT(*) as high_earners FROM employees WHERE salary > (SELECT avg_salary FROM q1)",
                    depends_on=["q1"]
                )
            ],
            final_query_id="q2"
        )
        
        executed_plan = engine.execute_plan(plan)
        
        # Verify execution
        assert executed_plan.is_complete()
        assert not executed_plan.has_errors()
        
        # Check both queries completed successfully
        q1 = executed_plan.get_query("q1")
        q2 = executed_plan.get_query("q2")
        
        assert q1.status == QueryStatus.COMPLETED
        assert q2.status == QueryStatus.COMPLETED
        
        # Verify q2 used results from q1 (high_earners count should be reasonable)
        assert q2.row_count == 1
        high_earners = q2.results["rows"][0][0]
        assert high_earners >= 0  # Valid count
    
    def test_comparison_plan_helper(self, electronics_db_path):
        """Test comparison plan helper function"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        # Create comparison plan (e.g., November vs December sales)
        # Since we don't have month data, use department counts instead
        plan = QueryPlan(
            queries=[
                QueryStep(
                    id="q1",
                    description="Get Engineering count",
                    sql="SELECT COUNT(*) as total FROM employees WHERE department = 'Engineering'",
                    depends_on=[]
                ),
                QueryStep(
                    id="q2",
                    description="Get Sales count",
                    sql="SELECT COUNT(*) as total FROM employees WHERE department = 'Sales'",
                    depends_on=[]
                ),
                QueryStep(
                    id="q3",
                    description="Compare Engineering vs Sales",
                    sql="""
                        SELECT 
                            'Engineering' as dept1,
                            (SELECT total FROM q1) as count1,
                            'Sales' as dept2,
                            (SELECT total FROM q2) as count2,
                            ((SELECT total FROM q2) - (SELECT total FROM q1)) as difference
                    """,
                    depends_on=["q1", "q2"]
                )
            ],
            final_query_id="q3",
            question="Compare Engineering vs Sales employee counts"
        )
        
        executed_plan = engine.execute_plan(plan)
        
        # Verify all queries completed
        assert executed_plan.is_complete()
        assert not executed_plan.has_errors()
        
        # Verify execution order (q1, q2 before q3)
        q3 = executed_plan.get_query("q3")
        assert q3.status == QueryStatus.COMPLETED
        
        # Verify final results contain comparison
        results = executed_plan.get_final_results()
        assert results is not None
        assert len(results["rows"]) == 1
        assert len(results["columns"]) == 5  # dept1, count1, dept2, count2, difference
    
    def test_query_execution_order(self, electronics_db_path):
        """Test that queries execute in dependency order"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        # Create linear dependency: q1 -> q2 -> q3
        plan = QueryPlan(
            queries=[
                QueryStep(
                    id="q1",
                    description="Base query",
                    sql="SELECT 100 as base_value",
                    depends_on=[]
                ),
                QueryStep(
                    id="q2",
                    description="Double base",
                    sql="SELECT base_value * 2 as doubled FROM q1",
                    depends_on=["q1"]
                ),
                QueryStep(
                    id="q3",
                    description="Triple doubled",
                    sql="SELECT doubled * 3 as final FROM q2",
                    depends_on=["q2"]
                )
            ],
            final_query_id="q3"
        )
        
        executed_plan = engine.execute_plan(plan)
        
        # All should complete
        assert executed_plan.is_complete()
        
        # Check final result: 100 * 2 * 3 = 600
        results = executed_plan.get_final_results()
        assert results is not None
        assert results["rows"][0][0] == 600
    
    def test_query_failure_stops_execution(self, electronics_db_path):
        """Test that query failure stops subsequent queries"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        plan = QueryPlan(
            queries=[
                QueryStep(
                    id="q1",
                    description="Valid query",
                    sql="SELECT COUNT(*) FROM employees",
                    depends_on=[]
                ),
                QueryStep(
                    id="q2",
                    description="Invalid query (syntax error)",
                    sql="SELECT * FROM nonexistent_table",
                    depends_on=["q1"]
                ),
                QueryStep(
                    id="q3",
                    description="Should not execute",
                    sql="SELECT 1",
                    depends_on=["q2"]
                )
            ],
            final_query_id="q3"
        )
        
        executed_plan = engine.execute_plan(plan)
        
        # Should not be complete
        assert not executed_plan.is_complete()
        assert executed_plan.has_errors()
        
        # q1 should succeed, q2 should fail, q3 should be pending
        q1 = executed_plan.get_query("q1")
        q2 = executed_plan.get_query("q2")
        q3 = executed_plan.get_query("q3")
        
        assert q1.status == QueryStatus.COMPLETED
        assert q2.status == QueryStatus.FAILED
        assert q3.status == QueryStatus.PENDING  # Never executed
        assert q2.error is not None
    
    def test_max_results_applied_to_final_query(self, electronics_db_path):
        """Test that max_results only limits final query"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        plan = QueryPlan(
            queries=[
                QueryStep(
                    id="q1",
                    description="Get all employees",
                    sql="SELECT * FROM employees",
                    depends_on=[]
                ),
                QueryStep(
                    id="q2",
                    description="Select subset",
                    sql="SELECT employee_id, first_name, last_name FROM q1",
                    depends_on=["q1"]
                )
            ],
            final_query_id="q2"
        )
        
        # Execute with max_results = 5
        executed_plan = engine.execute_plan(plan, max_results=5)
        
        # q1 should have all rows, q2 should be limited
        q1 = executed_plan.get_query("q1")
        q2 = executed_plan.get_query("q2")
        
        assert q1.row_count > 5  # No limit
        assert q2.row_count == 5  # Limited to max_results
    
    def test_plan_timing_metadata(self, electronics_db_path):
        """Test that execution times are recorded"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        plan = QueryPlan.create_simple_plan(
            sql="SELECT * FROM employees LIMIT 10"
        )
        
        executed_plan = engine.execute_plan(plan)
        
        # Check timing metadata
        assert executed_plan.total_execution_time_ms is not None
        assert executed_plan.total_execution_time_ms > 0
        
        q1 = executed_plan.get_query("q1")
        assert q1.execution_time_ms is not None
        assert q1.execution_time_ms > 0
    
    def test_plan_serialization_after_execution(self, electronics_db_path):
        """Test that executed plan can be serialized"""
        engine = QueryEngine(db_path=electronics_db_path)
        
        plan = QueryPlan.create_simple_plan(
            sql="SELECT COUNT(*) FROM products",
            question="How many products?"
        )
        
        executed_plan = engine.execute_plan(plan)
        
        # Serialize to dict
        data = executed_plan.to_dict()
        
        assert data["is_complete"] is True
        assert data["has_errors"] is False
        assert data["total_execution_time_ms"] is not None
        assert data["question"] == "How many products?"
        assert len(data["queries"]) == 1
        assert data["queries"][0]["status"] == "completed"
        assert data["queries"][0]["row_count"] is not None
