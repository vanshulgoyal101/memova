"""
Multi-Query Plan Data Structures

Supports executing multiple SQL queries to answer complex questions.
Handles query dependencies and execution ordering.

Author: AI Assistant
Date: 2025-11-06
Version: 1.4.0 (Prototype)
"""

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Set
from enum import Enum

logger = logging.getLogger(__name__)


class QueryStatus(Enum):
    """Execution status of a query step"""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class QueryStep:
    """
    Represents one SQL query in a multi-query plan.
    
    Attributes:
        id: Unique identifier (e.g., "q1", "q2")
        description: Human-readable purpose of this query
        sql: SQL statement to execute
        depends_on: List of query IDs that must complete first
        status: Current execution status
        results: Query results after execution (columns + rows)
        error: Error message if query failed
        execution_time_ms: Time taken to execute (milliseconds)
        row_count: Number of rows returned
    
    Example:
        >>> step = QueryStep(
        ...     id="q1",
        ...     description="Get November sales",
        ...     sql="SELECT SUM(total) FROM orders WHERE month='Nov'",
        ...     depends_on=[]
        ... )
    """
    id: str
    description: str
    sql: str
    depends_on: List[str] = field(default_factory=list)
    status: QueryStatus = QueryStatus.PENDING
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[float] = None
    row_count: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            "id": self.id,
            "description": self.description,
            "sql": self.sql,
            "depends_on": self.depends_on,
            "status": self.status.value,
            "row_count": self.row_count,
            "execution_time_ms": self.execution_time_ms,
            "error": self.error,
            "results": self.results  # Include intermediate results
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QueryStep':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            description=data.get('description', ''),
            sql=data['sql'],
            depends_on=data.get('depends_on', [])
        )


@dataclass
class QueryPlan:
    """
    Complete multi-query execution plan.
    
    Manages multiple SQL queries with dependency relationships.
    Ensures queries execute in correct order (topological sort).
    
    Attributes:
        queries: List of QueryStep objects
        final_query_id: ID of the query that produces the final answer
        question: Original natural language question
        total_execution_time_ms: Total time for all queries
    
    Example:
        >>> plan = QueryPlan(
        ...     queries=[
        ...         QueryStep(id="q1", sql="...", depends_on=[]),
        ...         QueryStep(id="q2", sql="...", depends_on=["q1"])
        ...     ],
        ...     final_query_id="q2",
        ...     question="Compare Q1 vs Q2 sales"
        ... )
        >>> order = plan.get_execution_order()
        >>> # Returns: [q1, q2] (dependency order)
    """
    queries: List[QueryStep]
    final_query_id: str
    question: Optional[str] = None
    total_execution_time_ms: Optional[float] = None
    
    def __post_init__(self):
        """Validate plan after initialization"""
        self._validate_plan()
    
    def _validate_plan(self):
        """
        Validate the query plan for consistency.
        
        Checks:
        - All query IDs are unique
        - Final query ID exists
        - No circular dependencies
        - All dependencies reference existing queries
        
        Raises:
            ValueError: If plan is invalid
        """
        # Check unique IDs
        ids = [q.id for q in self.queries]
        if len(ids) != len(set(ids)):
            raise ValueError("Query IDs must be unique")
        
        # Check final query exists
        if self.final_query_id not in ids:
            raise ValueError(f"Final query ID '{self.final_query_id}' not found in queries")
        
        # Check all dependencies exist
        id_set = set(ids)
        for query in self.queries:
            for dep_id in query.depends_on:
                if dep_id not in id_set:
                    raise ValueError(
                        f"Query '{query.id}' depends on non-existent query '{dep_id}'"
                    )
        
        # Check for circular dependencies
        if self._has_circular_dependencies():
            raise ValueError("Circular dependencies detected in query plan")
    
    def _has_circular_dependencies(self) -> bool:
        """
        Detect circular dependencies using DFS.
        
        Returns:
            True if circular dependency exists, False otherwise
        """
        visited = set()
        rec_stack = set()
        
        def visit(query_id: str) -> bool:
            """Recursive DFS to detect cycles"""
            if query_id in rec_stack:
                return True  # Cycle detected
            if query_id in visited:
                return False  # Already processed
            
            visited.add(query_id)
            rec_stack.add(query_id)
            
            # Get query
            query = self.get_query(query_id)
            
            # Visit dependencies
            for dep_id in query.depends_on:
                if visit(dep_id):
                    return True
            
            rec_stack.remove(query_id)
            return False
        
        # Check all queries
        for query in self.queries:
            if query.id not in visited:
                if visit(query.id):
                    return True
        
        return False
    
    def get_query(self, query_id: str) -> Optional[QueryStep]:
        """Get query by ID"""
        for query in self.queries:
            if query.id == query_id:
                return query
        return None
    
    def get_execution_order(self) -> List[QueryStep]:
        """
        Get queries in execution order using topological sort.
        
        Ensures queries execute after their dependencies.
        
        Returns:
            List of QueryStep objects in execution order
            
        Example:
            >>> # q1 (no deps), q2 (depends on q1), q3 (depends on q1, q2)
            >>> order = plan.get_execution_order()
            >>> # Returns: [q1, q2, q3]
        """
        # Build adjacency list (query_id -> list of dependent query IDs)
        dependents: Dict[str, List[str]] = {q.id: [] for q in self.queries}
        in_degree: Dict[str, int] = {q.id: len(q.depends_on) for q in self.queries}
        
        for query in self.queries:
            for dep_id in query.depends_on:
                dependents[dep_id].append(query.id)
        
        # Kahn's algorithm for topological sort
        queue: List[str] = []
        for query_id, degree in in_degree.items():
            if degree == 0:
                queue.append(query_id)
        
        execution_order: List[QueryStep] = []
        
        while queue:
            # Remove query with no dependencies
            query_id = queue.pop(0)
            query = self.get_query(query_id)
            execution_order.append(query)
            
            # Reduce in-degree for dependent queries
            for dependent_id in dependents[query_id]:
                in_degree[dependent_id] -= 1
                if in_degree[dependent_id] == 0:
                    queue.append(dependent_id)
        
        return execution_order
    
    def get_final_results(self) -> Optional[Dict[str, Any]]:
        """Get results from the final query"""
        final_query = self.get_query(self.final_query_id)
        if final_query and final_query.status == QueryStatus.COMPLETED:
            return final_query.results
        return None
    
    def is_complete(self) -> bool:
        """Check if all queries have completed"""
        return all(q.status == QueryStatus.COMPLETED for q in self.queries)
    
    def has_errors(self) -> bool:
        """Check if any query failed"""
        return any(q.status == QueryStatus.FAILED for q in self.queries)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            "queries": [q.to_dict() for q in self.queries],
            "final_query_id": self.final_query_id,
            "question": self.question,
            "total_execution_time_ms": self.total_execution_time_ms,
            "is_complete": self.is_complete(),
            "has_errors": self.has_errors()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QueryPlan':
        """Create from dictionary"""
        return cls(
            queries=[QueryStep.from_dict(q) for q in data['queries']],
            final_query_id=data['final_query_id'],
            question=data.get('question')
        )
    
    @classmethod
    def create_simple_plan(cls, sql: str, question: Optional[str] = None) -> 'QueryPlan':
        """
        Create a single-query plan (backward compatibility).
        
        Args:
            sql: SQL query
            question: Optional natural language question
            
        Returns:
            QueryPlan with one query
        """
        query = QueryStep(
            id="q1",
            description="Execute query",
            sql=sql,
            depends_on=[]
        )
        
        return cls(
            queries=[query],
            final_query_id="q1",
            question=question
        )


def create_comparison_plan(
    question: str,
    category1: str,
    category2: str,
    table: str,
    value_column: str,
    filter_column: str
) -> QueryPlan:
    """
    Helper function to create a comparison query plan.
    
    Example: "Compare November vs December sales"
    
    Args:
        question: Natural language question
        category1: First category to compare (e.g., "November")
        category2: Second category to compare (e.g., "December")
        table: Table name
        value_column: Column to aggregate
        filter_column: Column to filter on
        
    Returns:
        QueryPlan with 3 queries (cat1 data, cat2 data, comparison)
    """
    queries = [
        QueryStep(
            id="q1",
            description=f"Get {category1} {value_column}",
            sql=f"SELECT SUM({value_column}) as total FROM {table} WHERE {filter_column} = '{category1}'",
            depends_on=[]
        ),
        QueryStep(
            id="q2",
            description=f"Get {category2} {value_column}",
            sql=f"SELECT SUM({value_column}) as total FROM {table} WHERE {filter_column} = '{category2}'",
            depends_on=[]
        ),
        QueryStep(
            id="q3",
            description=f"Compare {category1} vs {category2}",
            sql=f"""
                SELECT 
                    '{category1}' as period1,
                    (SELECT total FROM q1) as total1,
                    '{category2}' as period2,
                    (SELECT total FROM q2) as total2,
                    ((SELECT total FROM q2) - (SELECT total FROM q1)) as difference,
                    ROUND(((SELECT total FROM q2) - (SELECT total FROM q1)) * 100.0 / (SELECT total FROM q1), 2) as growth_pct
            """.strip(),
            depends_on=["q1", "q2"]
        )
    ]
    
    return QueryPlan(
        queries=queries,
        final_query_id="q3",
        question=question
    )
