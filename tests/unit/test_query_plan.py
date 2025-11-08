"""
Unit tests for QueryPlan and QueryStep classes.

Tests:
- QueryStep creation and serialization
- QueryPlan validation (unique IDs, dependencies)
- Topological sort (execution order)
- Circular dependency detection
- Helper functions (simple plan, comparison plan)
"""

import pytest
from src.core.query_plan import (
    QueryStep,
    QueryPlan,
    QueryStatus,
    create_comparison_plan
)


class TestQueryStep:
    """Test QueryStep data structure"""
    
    def test_create_simple_query_step(self):
        """Test creating a basic query step"""
        step = QueryStep(
            id="q1",
            description="Count employees",
            sql="SELECT COUNT(*) FROM employees",
            depends_on=[]
        )
        
        assert step.id == "q1"
        assert step.description == "Count employees"
        assert step.status == QueryStatus.PENDING
        assert step.results is None
        assert step.error is None
    
    def test_query_step_with_dependencies(self):
        """Test query step with dependencies"""
        step = QueryStep(
            id="q2",
            description="Filter high earners",
            sql="SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)",
            depends_on=["q1"]
        )
        
        assert step.depends_on == ["q1"]
        assert len(step.depends_on) == 1
    
    def test_query_step_to_dict(self):
        """Test serialization to dictionary"""
        step = QueryStep(
            id="q1",
            description="Get sales",
            sql="SELECT * FROM sales",
            depends_on=[]
        )
        step.status = QueryStatus.COMPLETED
        step.row_count = 42
        step.execution_time_ms = 125.5
        
        data = step.to_dict()
        
        assert data["id"] == "q1"
        assert data["status"] == "completed"
        assert data["row_count"] == 42
        assert data["execution_time_ms"] == 125.5
    
    def test_query_step_from_dict(self):
        """Test deserialization from dictionary"""
        data = {
            "id": "q1",
            "description": "Get data",
            "sql": "SELECT * FROM orders",
            "depends_on": ["q0"]
        }
        
        step = QueryStep.from_dict(data)
        
        assert step.id == "q1"
        assert step.description == "Get data"
        assert step.depends_on == ["q0"]


class TestQueryPlanValidation:
    """Test query plan validation logic"""
    
    def test_valid_simple_plan(self):
        """Test creating a valid single-query plan"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="Get data", sql="SELECT * FROM employees", depends_on=[])
            ],
            final_query_id="q1"
        )
        
        assert len(plan.queries) == 1
        assert plan.final_query_id == "q1"
    
    def test_valid_multi_query_plan(self):
        """Test valid plan with dependencies"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="Step 1", sql="SELECT ...", depends_on=[]),
                QueryStep(id="q2", description="Step 2", sql="SELECT ...", depends_on=["q1"]),
                QueryStep(id="q3", description="Step 3", sql="SELECT ...", depends_on=["q1", "q2"])
            ],
            final_query_id="q3"
        )
        
        assert len(plan.queries) == 3
        assert plan.final_query_id == "q3"
    
    def test_duplicate_query_ids(self):
        """Test that duplicate IDs raise ValueError"""
        with pytest.raises(ValueError, match="Query IDs must be unique"):
            QueryPlan(
                queries=[
                    QueryStep(id="q1", description="First", sql="SELECT 1", depends_on=[]),
                    QueryStep(id="q1", description="Duplicate", sql="SELECT 2", depends_on=[])
                ],
                final_query_id="q1"
            )
    
    def test_invalid_final_query_id(self):
        """Test that non-existent final_query_id raises ValueError"""
        with pytest.raises(ValueError, match="Final query ID 'q99' not found"):
            QueryPlan(
                queries=[
                    QueryStep(id="q1", description="Only query", sql="SELECT 1", depends_on=[])
                ],
                final_query_id="q99"
            )
    
    def test_non_existent_dependency(self):
        """Test that invalid dependency raises ValueError"""
        with pytest.raises(ValueError, match="depends on non-existent query 'q99'"):
            QueryPlan(
                queries=[
                    QueryStep(id="q1", description="Missing dep", sql="SELECT 1", depends_on=["q99"])
                ],
                final_query_id="q1"
            )
    
    def test_circular_dependency_simple(self):
        """Test circular dependency detection (A -> B -> A)"""
        with pytest.raises(ValueError, match="Circular dependencies detected"):
            QueryPlan(
                queries=[
                    QueryStep(id="q1", description="A", sql="SELECT 1", depends_on=["q2"]),
                    QueryStep(id="q2", description="B", sql="SELECT 2", depends_on=["q1"])
                ],
                final_query_id="q2"
            )
    
    def test_circular_dependency_complex(self):
        """Test circular dependency detection (A -> B -> C -> A)"""
        with pytest.raises(ValueError, match="Circular dependencies detected"):
            QueryPlan(
                queries=[
                    QueryStep(id="q1", description="A", sql="SELECT 1", depends_on=["q3"]),
                    QueryStep(id="q2", description="B", sql="SELECT 2", depends_on=["q1"]),
                    QueryStep(id="q3", description="C", sql="SELECT 3", depends_on=["q2"])
                ],
                final_query_id="q3"
            )


class TestExecutionOrder:
    """Test topological sort for execution order"""
    
    def test_simple_linear_order(self):
        """Test linear dependency chain (q1 -> q2 -> q3)"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="First", sql="SELECT 1", depends_on=[]),
                QueryStep(id="q2", description="Second", sql="SELECT 2", depends_on=["q1"]),
                QueryStep(id="q3", description="Third", sql="SELECT 3", depends_on=["q2"])
            ],
            final_query_id="q3"
        )
        
        order = plan.get_execution_order()
        order_ids = [q.id for q in order]
        
        assert order_ids == ["q1", "q2", "q3"]
    
    def test_parallel_queries(self):
        """Test independent queries can execute in any order"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="Independent 1", sql="SELECT 1", depends_on=[]),
                QueryStep(id="q2", description="Independent 2", sql="SELECT 2", depends_on=[]),
                QueryStep(id="q3", description="Combines both", sql="SELECT 3", depends_on=["q1", "q2"])
            ],
            final_query_id="q3"
        )
        
        order = plan.get_execution_order()
        order_ids = [q.id for q in order]
        
        # q1 and q2 can be in any order, but both before q3
        assert len(order_ids) == 3
        assert order_ids[2] == "q3"
        assert set(order_ids[:2]) == {"q1", "q2"}
    
    def test_diamond_dependency(self):
        """Test diamond-shaped dependencies (q1 -> q2, q3 -> q4)"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="Root", sql="SELECT 1", depends_on=[]),
                QueryStep(id="q2", description="Branch A", sql="SELECT 2", depends_on=["q1"]),
                QueryStep(id="q3", description="Branch B", sql="SELECT 3", depends_on=["q1"]),
                QueryStep(id="q4", description="Merge", sql="SELECT 4", depends_on=["q2", "q3"])
            ],
            final_query_id="q4"
        )
        
        order = plan.get_execution_order()
        order_ids = [q.id for q in order]
        
        # q1 must be first, q4 must be last
        assert order_ids[0] == "q1"
        assert order_ids[3] == "q4"
        # q2 and q3 can be in any order
        assert set(order_ids[1:3]) == {"q2", "q3"}
    
    def test_no_dependencies(self):
        """Test plan with all independent queries"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="A", sql="SELECT 1", depends_on=[]),
                QueryStep(id="q2", description="B", sql="SELECT 2", depends_on=[]),
                QueryStep(id="q3", description="C", sql="SELECT 3", depends_on=[])
            ],
            final_query_id="q1"
        )
        
        order = plan.get_execution_order()
        
        # All queries can execute in any order
        assert len(order) == 3
        order_ids = [q.id for q in order]
        assert set(order_ids) == {"q1", "q2", "q3"}


class TestQueryPlanMethods:
    """Test QueryPlan helper methods"""
    
    def test_get_query(self):
        """Test retrieving query by ID"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="First", sql="SELECT 1", depends_on=[]),
                QueryStep(id="q2", description="Second", sql="SELECT 2", depends_on=["q1"])
            ],
            final_query_id="q2"
        )
        
        query = plan.get_query("q1")
        assert query is not None
        assert query.id == "q1"
        assert query.description == "First"
        
        missing = plan.get_query("q99")
        assert missing is None
    
    def test_is_complete(self):
        """Test checking if all queries completed"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="First", sql="SELECT 1", depends_on=[]),
                QueryStep(id="q2", description="Second", sql="SELECT 2", depends_on=["q1"])
            ],
            final_query_id="q2"
        )
        
        assert not plan.is_complete()
        
        # Mark all as completed
        for query in plan.queries:
            query.status = QueryStatus.COMPLETED
        
        assert plan.is_complete()
    
    def test_has_errors(self):
        """Test detecting failed queries"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="First", sql="SELECT 1", depends_on=[]),
                QueryStep(id="q2", description="Second", sql="SELECT 2", depends_on=["q1"])
            ],
            final_query_id="q2"
        )
        
        assert not plan.has_errors()
        
        # Mark one as failed
        plan.queries[0].status = QueryStatus.FAILED
        plan.queries[0].error = "Syntax error"
        
        assert plan.has_errors()
    
    def test_get_final_results(self):
        """Test retrieving final query results"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="First", sql="SELECT 1", depends_on=[]),
                QueryStep(id="q2", description="Final", sql="SELECT 2", depends_on=["q1"])
            ],
            final_query_id="q2"
        )
        
        # No results yet
        assert plan.get_final_results() is None
        
        # Add results to final query
        final_query = plan.get_query("q2")
        final_query.status = QueryStatus.COMPLETED
        final_query.results = {
            "columns": ["count"],
            "rows": [[42]]
        }
        
        results = plan.get_final_results()
        assert results is not None
        assert results["rows"] == [[42]]
    
    def test_plan_to_dict(self):
        """Test serializing plan to dictionary"""
        plan = QueryPlan(
            queries=[
                QueryStep(id="q1", description="First", sql="SELECT 1", depends_on=[]),
                QueryStep(id="q2", description="Second", sql="SELECT 2", depends_on=["q1"])
            ],
            final_query_id="q2",
            question="Test question"
        )
        
        data = plan.to_dict()
        
        assert data["final_query_id"] == "q2"
        assert data["question"] == "Test question"
        assert len(data["queries"]) == 2
        assert data["is_complete"] is False
        assert data["has_errors"] is False
    
    def test_plan_from_dict(self):
        """Test deserializing plan from dictionary"""
        data = {
            "queries": [
                {"id": "q1", "description": "First", "sql": "SELECT 1", "depends_on": []},
                {"id": "q2", "description": "Second", "sql": "SELECT 2", "depends_on": ["q1"]}
            ],
            "final_query_id": "q2",
            "question": "Test question"
        }
        
        plan = QueryPlan.from_dict(data)
        
        assert len(plan.queries) == 2
        assert plan.final_query_id == "q2"
        assert plan.question == "Test question"


class TestHelperFunctions:
    """Test helper functions for creating plans"""
    
    def test_create_simple_plan(self):
        """Test creating single-query plan"""
        plan = QueryPlan.create_simple_plan(
            sql="SELECT COUNT(*) FROM employees",
            question="How many employees?"
        )
        
        assert len(plan.queries) == 1
        assert plan.queries[0].id == "q1"
        assert plan.final_query_id == "q1"
        assert plan.question == "How many employees?"
        assert len(plan.queries[0].depends_on) == 0
    
    def test_create_comparison_plan(self):
        """Test creating comparison query plan"""
        plan = create_comparison_plan(
            question="Compare November vs December sales",
            category1="November",
            category2="December",
            table="sales_orders",
            value_column="total_price",
            filter_column="month"
        )
        
        assert len(plan.queries) == 3
        assert plan.final_query_id == "q3"
        assert plan.question == "Compare November vs December sales"
        
        # Check execution order
        order = plan.get_execution_order()
        order_ids = [q.id for q in order]
        
        # q1 and q2 are independent, q3 depends on both
        assert order_ids[2] == "q3"
        assert set(order_ids[:2]) == {"q1", "q2"}
        
        # Verify final query depends on both
        final_query = plan.get_query("q3")
        assert set(final_query.depends_on) == {"q1", "q2"}
