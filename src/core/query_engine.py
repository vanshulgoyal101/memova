"""
AI-powered SQL query engine - Orchestrator
Coordinates API key management, AI client, SQL generation, and query execution
Uses Groq (primary) with Gemini fallback for both SQL generation and summarization
Supports multi-query execution with dependency resolution
"""

import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from src.core.database import DatabaseManager
from src.core.api_key_manager import APIKeyManager
from src.core.llm_client import UnifiedLLMClient
from src.core.sql_generator import SQLGenerator
from src.core.query_plan import QueryPlan, QueryStep, QueryStatus
from src.core.analyst import BusinessAnalyst
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.utils.exceptions import ConfigurationError

logger = setup_logger(__name__)


class QueryEngine:
    """
    Natural language to SQL query engine using Google Gemini AI
    
    This is the main orchestrator that coordinates:
    - API key rotation (APIKeyManager)
    - Gemini AI client (GeminiClient)
    - SQL generation (SQLGenerator)
    - Query execution (DatabaseManager)
    
    Example:
        >>> engine = QueryEngine()
        >>> result = engine.ask("How many employees are there?")
        >>> print(result['results'])
        [{'COUNT(*)': 150}]
    """
    
    def __init__(
        self,
        db_manager: Optional[DatabaseManager] = None,
        db_path: Optional[str] = None
    ):
        """
        Initialize the query engine
        
        Args:
            db_manager: Database manager instance. Creates new if None.
            db_path: Optional path to database file
            
        Raises:
            ConfigurationError: If configuration is invalid
            APIError: If cannot connect to Gemini API
        """
        # Validate configuration
        errors = Config.validate()
        if errors:
            raise ConfigurationError("\n".join(errors))
        
        # Initialize database manager
        if db_manager is not None:
            self.db_manager = db_manager
        elif db_path is not None:
            self.db_manager = DatabaseManager(db_path=Path(db_path))
        else:
            self.db_manager = DatabaseManager()
        
        # Verify database exists
        if not self.db_manager.database_exists():
            raise ConfigurationError(
                f"Database not found: {self.db_manager.db_path}\n"
                "Run 'python main.py' to generate data first."
            )
        
        # Initialize components
        self.api_key_manager = APIKeyManager()
        self.llm_client = UnifiedLLMClient()  # Groq primary + Gemini fallback
        
        # Load database schema
        self.schema_text = self._load_schema()
        
        # Initialize SQL generator with unified client
        self.sql_generator = SQLGenerator(
            schema_text=self.schema_text,
            llm_client=self.llm_client,
            api_key_manager=self.api_key_manager
        )
        
        # Initialize business analyst for strategic questions
        self.analyst = BusinessAnalyst(
            db_manager=self.db_manager,
            llm_client=self.llm_client,
            schema_text=self.schema_text
        )
        
        logger.info(
            f"QueryEngine initialized with model: {self.llm_client.get_model_name()}"
        )
    
    def _load_schema(self) -> str:
        """
        Load and format database schema for LLM context
        
        Returns:
            Formatted schema string
        """
        logger.debug("Loading database schema")
        
        schema = self.db_manager.get_schema_summary()
        
        schema_text = "DATABASE SCHEMA:\n\n"
        
        for table_name, info in schema.items():
            schema_text += f"Table: {table_name}\n"
            schema_text += f"  Rows: {info['row_count']}\n"
            schema_text += "  Columns:\n"
            
            for col in info['columns']:
                pk_marker = " (PRIMARY KEY)" if col['pk'] else ""
                null_marker = " NOT NULL" if col['notnull'] else ""
                schema_text += (
                    f"    - {col['name']} ({col['type']}){pk_marker}{null_marker}\n"
                )
            
            schema_text += "\n"
        
        return schema_text
    
    def generate_sql(self, question: str) -> str:
        """
        Generate SQL query from natural language question
        
        Args:
            question: Natural language question
            
        Returns:
            SQL query string
            
        Raises:
            QueryError: If query generation fails
        """
        return self.sql_generator.generate(question)
    
    def _clean_sql(self, sql: str) -> str:
        """
        Clean and validate SQL (for backward compatibility with tests)
        
        Args:
            sql: Raw SQL string
            
        Returns:
            Cleaned SQL string
        """
        return self.sql_generator._clean_sql(sql)
    
    def execute_query(
        self,
        sql: str,
        max_results: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute SQL query and return results
        
        Args:
            sql: SQL query to execute
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with query results and metadata:
            {
                'success': bool,
                'sql': str,
                'results': List[Dict],
                'row_count': int,
                'execution_time': float,
                'truncated': bool,
                'timestamp': str
            }
        """
        logger.debug(f"Executing query: {sql[:100]}...")
        
        max_results = max_results or Config.MAX_QUERY_RESULTS
        
        try:
            start_time = time.time()
            results = self.db_manager.execute_query(sql)
            execution_time = time.time() - start_time
            
            # Limit results if needed
            if len(results) > max_results:
                logger.warning(
                    f"Results truncated from {len(results)} to {max_results}"
                )
                results = results[:max_results]
                truncated = True
            else:
                truncated = False
            
            logger.info(
                f"Query returned {len(results)} rows in {execution_time:.3f}s"
            )
            
            return {
                'success': True,
                'sql': sql,
                'results': results,
                'row_count': len(results),
                'execution_time': execution_time,
                'truncated': truncated,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return {
                'success': False,
                'sql': sql,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def ask(
        self,
        question: str,
        max_results: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Ask a question in natural language and get results
        
        Automatically detects if question requires:
        - Simple data retrieval → SQL query
        - Strategic analysis → Business analyst
        
        This is the main entry point combining SQL generation and execution.
        
        Args:
            question: Natural language question
            max_results: Maximum number of results
            
        Returns:
            Dictionary with results and metadata:
            {
                'success': bool,
                'question': str,
                'sql': str (if data query),
                'analysis': dict (if analytical query),
                'results': List[Dict],
                'row_count': int,
                'execution_time': float,
                'timestamp': str
            }
            
        Example:
            >>> engine = QueryEngine()
            >>> # Data query
            >>> result = engine.ask("Show me the top 5 products by revenue")
            >>> for row in result['results']:
            ...     print(row)
            >>> 
            >>> # Analytical query
            >>> result = engine.ask("Give me insights to improve sales")
            >>> print(result['analysis']['recommendations'])
        """
        try:
            # Check if question requires strategic analysis
            if self.analyst.is_analytical_question(question):
                logger.info(f"Detected analytical question: {question[:100]}")
                
                # Perform business analysis
                analysis = self.analyst.analyze(question)
                
                return {
                    'success': analysis.get('success', True),
                    'question': question,
                    'query_type': 'analytical',
                    'analysis': analysis,
                    'timestamp': datetime.now().isoformat()
                }
            
            # Regular data query
            logger.info(f"Detected data query: {question[:100]}")
            sql = self.generate_sql(question)
            result = self.execute_query(sql, max_results)
            result['question'] = question
            result['query_type'] = 'data'
            return result
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return {
                'success': False,
                'question': question,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_schema_info(self) -> str:
        """
        Get formatted schema information
        
        Returns:
            Formatted schema string
        """
        return self.schema_text
    
    def get_available_tables(self) -> List[str]:
        """
        Get list of available tables
        
        Returns:
            List of table names
        """
        return self.db_manager.get_tables()
    
    def validate_query(self, sql: str) -> bool:
        """
        Validate SQL query without executing
        
        Args:
            sql: SQL query to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Use EXPLAIN to validate without executing
            explain_sql = f"EXPLAIN {sql}"
            self.db_manager.execute_query(explain_sql)
            return True
        except Exception as e:
            logger.debug(f"Query validation failed: {e}")
            return False
    
    @property
    def model_name(self) -> str:
        """
        Get the current model name (Groq primary + Gemini fallback)
        
        Returns:
            Model name string with provider info
        """
        return self.llm_client.get_model_name()
    
    def execute_plan(
        self,
        plan: QueryPlan,
        max_results: Optional[int] = None
    ) -> QueryPlan:
        """
        Execute a multi-query plan with dependency resolution.
        
        Executes queries in topological order (dependencies first).
        Supports result substitution via temporary tables/CTEs.
        
        Args:
            plan: QueryPlan to execute
            max_results: Maximum results for final query
            
        Returns:
            Updated QueryPlan with results and execution times
            
        Example:
            >>> plan = QueryPlan(
            ...     queries=[
            ...         QueryStep(id="q1", sql="SELECT ...", depends_on=[]),
            ...         QueryStep(id="q2", sql="SELECT ...", depends_on=["q1"])
            ...     ],
            ...     final_query_id="q2"
            ... )
            >>> executed_plan = engine.execute_plan(plan)
            >>> results = executed_plan.get_final_results()
        """
        logger.info(f"Executing query plan with {len(plan.queries)} queries")
        
        max_results = max_results or Config.MAX_QUERY_RESULTS
        plan_start_time = time.time()
        
        # Get execution order (topological sort)
        execution_order = plan.get_execution_order()
        
        # Store intermediate results by query ID
        results_cache: Dict[str, Dict[str, Any]] = {}
        
        # Execute queries in order
        for query in execution_order:
            max_retries = Config.MAX_SQL_ERROR_RETRIES if hasattr(Config, 'MAX_SQL_ERROR_RETRIES') else 2
            retry_count = 0
            sql = None
            
            while retry_count <= max_retries:
                try:
                    logger.debug(f"Executing query {query.id}: {query.description}")
                    query.status = QueryStatus.EXECUTING
                    
                    # Replace result references in SQL (e.g., "FROM q1" -> temp table)
                    if retry_count == 0:
                        # First attempt: use original SQL
                        sql = self._resolve_dependencies(query, results_cache)
                    # else: sql already contains the AI-corrected version from previous iteration
                    
                    # Execute query
                    start_time = time.time()
                    raw_results = self.db_manager.execute_query(sql)
                    execution_time = (time.time() - start_time) * 1000  # milliseconds
                    
                    # Store results
                    query_results = {
                        "columns": list(raw_results[0].keys()) if raw_results else [],
                        "rows": [list(row.values()) for row in raw_results] if raw_results else []
                    }
                    
                    # Apply max_results only to final query
                    if query.id == plan.final_query_id and len(query_results["rows"]) > max_results:
                        logger.warning(
                            f"Final query results truncated from {len(query_results['rows'])} to {max_results}"
                        )
                        query_results["rows"] = query_results["rows"][:max_results]
                    
                    # Update query step
                    query.status = QueryStatus.COMPLETED
                    query.results = query_results
                    query.execution_time_ms = execution_time
                    query.row_count = len(query_results["rows"])
                    
                    # Cache for dependent queries
                    results_cache[query.id] = query_results
                    
                    logger.info(
                        f"Query {query.id} completed: {query.row_count} rows in {execution_time:.1f}ms"
                    )
                    
                    # Success - break retry loop
                    break
                    
                except Exception as e:
                    error_message = str(e)
                    logger.error(f"Query {query.id} failed: {error_message}")
                    
                    # Check if this is a retryable SQL error
                    if retry_count < max_retries and self._is_retryable_error(error_message):
                        retry_count += 1
                        logger.warning(f"🔄 Attempting AI-powered SQL correction (retry {retry_count}/{max_retries})")
                        
                        try:
                            # Use AI to fix the SQL error
                            corrected_sql = self.sql_generator.fix_sql_error(
                                failing_sql=sql,
                                error_message=error_message,
                                question=query.description,
                                attempt=retry_count
                            )
                            
                            # Update the query SQL for next iteration
                            sql = corrected_sql
                            query.sql = corrected_sql  # Update the plan with corrected SQL
                            
                            logger.info(f"✅ AI generated corrected SQL, retrying execution...")
                            continue  # Retry with corrected SQL
                            
                        except Exception as fix_error:
                            logger.error(f"AI correction failed: {fix_error}")
                            # Fall through to mark query as failed
                    
                    # Either max retries reached or non-retryable error or AI fix failed
                    query.status = QueryStatus.FAILED
                    query.error = error_message
                    
                    # Stop execution on error
                    break
            
            # If query failed after all retries, stop execution
            if query.status == QueryStatus.FAILED:
                break
        
        # Calculate total time
        plan.total_execution_time_ms = (time.time() - plan_start_time) * 1000
        
        logger.info(
            f"Plan execution {'completed' if plan.is_complete() else 'failed'}: "
            f"{plan.total_execution_time_ms:.1f}ms total"
        )
        
        return plan
    
    def _is_retryable_error(self, error_message: str) -> bool:
        """
        Determine if a database error is retryable with AI correction
        
        Args:
            error_message: The database error message
            
        Returns:
            True if error can potentially be fixed by AI, False otherwise
        """
        error_lower = error_message.lower()
        
        # Retryable SQL errors that AI can typically fix
        retryable_patterns = [
            'ambiguous column',           # Missing table aliases
            'no such column',             # Wrong column name
            'no such table',              # Wrong table name  
            'syntax error',               # SQL syntax issues
            'near',                       # SQLite syntax error indicator
            'join',                       # JOIN-related issues
            'type mismatch',              # Type conversion issues
            'datatype mismatch',          # Type issues
            'invalid',                    # Various invalid operations
            'only execute one statement', # Multiple statements in single query
            'multiple statements',        # Similar to above
        ]
        
        # Non-retryable errors (system/permissions)
        non_retryable_patterns = [
            'permission denied',
            'database is locked',
            'disk i/o error',
            'out of memory',
            'database disk image is malformed',
        ]
        
        # Check non-retryable first (higher priority)
        for pattern in non_retryable_patterns:
            if pattern in error_lower:
                return False
        
        # Check if error matches retryable patterns
        for pattern in retryable_patterns:
            if pattern in error_lower:
                return True
        
        # Default: don't retry unknown errors
        return False
    
    def _resolve_dependencies(
        self,
        query: QueryStep,
        results_cache: Dict[str, Dict[str, Any]]
    ) -> str:
        """
        Resolve query dependencies by substituting result references.
        
        For now, uses CTEs (Common Table Expressions) to reference previous queries.
        
        Args:
            query: Query step to resolve
            results_cache: Results from previous queries
            
        Returns:
            SQL with dependencies resolved
            
        Example:
            Input SQL: "SELECT * FROM q1 WHERE total > 1000"
            Output SQL: "WITH q1 AS (...) SELECT * FROM q1 WHERE total > 1000"
        """
        sql = query.sql
        
        # No dependencies - return as is
        if not query.depends_on:
            return sql
        
        # Build CTEs for dependencies
        ctes = []
        for dep_id in query.depends_on:
            if dep_id not in results_cache:
                logger.warning(f"Dependency {dep_id} not found in cache")
                continue
            
            # Get previous query
            dep_results = results_cache[dep_id]
            
            # Convert results to VALUES clause for CTE
            # This is a simple implementation - production would use temp tables
            if dep_results["rows"]:
                columns = dep_results["columns"]
                rows = dep_results["rows"]
                
                # Format: (col1, col2, ...) AS (SELECT val1, val2, ... UNION ALL ...)
                values_clauses = []
                for row in rows:
                    formatted_values = []
                    for val in row:
                        if val is None:
                            formatted_values.append("NULL")
                        elif isinstance(val, str):
                            # Escape single quotes
                            escaped = val.replace("'", "''")
                            formatted_values.append(f"'{escaped}'")
                        else:
                            formatted_values.append(str(val))
                    
                    values_clauses.append(f"SELECT {', '.join(formatted_values)}")
                
                cte_sql = " UNION ALL ".join(values_clauses)
                cte = f"{dep_id}({', '.join(columns)}) AS ({cte_sql})"
                ctes.append(cte)
        
        # Prepend CTEs to query
        if ctes:
            sql = f"WITH {', '.join(ctes)} {sql}"
        
        return sql
