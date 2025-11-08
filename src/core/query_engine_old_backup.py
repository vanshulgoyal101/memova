"""
AI-powered SQL query generator using Google Gemini
Production-ready implementation with proper error handling and logging
"""

import time
import json
import math
from typing import Dict, Any, Optional, List
from datetime import datetime

import google.generativeai as genai

from src.utils.config import Config
from src.core.database import DatabaseManager
from src.utils.logger import setup_logger
from src.utils.exceptions import APIError, QueryError, ConfigurationError
from src.utils.llm import generate_text

logger = setup_logger(__name__)


def _summarize_result_with_llm(
    question: str,
    columns: List[str],
    rows: List[List[Any]],
    company_id: str,
    section_ids: List[str],
    exec_ms: float,
    max_cells: int = 2000,
) -> str:
    """
    Summarize SQL result into a natural language answer.
    - Downsamples very large tables with head+tail sampling
    - Computes simple aggregates (row_count, numeric sums/means) to aid LLM
    - Returns a concise, decision-oriented summary; no code blocks
    
    Args:
        question: Original user question
        columns: List of column names
        rows: List of row data (each row is a list)
        company_id: Database identifier ('electronics' or 'airline')
        section_ids: Selected schema sections (for context)
        exec_ms: Query execution time in milliseconds
        max_cells: Maximum cells to send to LLM (downsample if exceeded)
        
    Returns:
        Natural language summary (paragraph + bullets)
        
    Example:
        >>> summary = _summarize_result_with_llm(
        ...     question="What are top products by revenue?",
        ...     columns=["product", "revenue", "units_sold"],
        ...     rows=[["Widget A", 15000, 100], ["Widget B", 12000, 80]],
        ...     company_id="electronics",
        ...     section_ids=["products", "sales"],
        ...     exec_ms=25.5
        ... )
        >>> print(summary)
        The top products by revenue are Widget A and Widget B, generating $27,000 
        in total sales.
        
        • Widget A leads with $15,000 in revenue from 100 units
        • Widget B follows with $12,000 from 80 units  
        • Average revenue per product: $13,500
    """
    try:
        # 1) Light metadata
        row_count = len(rows)
        col_count = len(columns)
        
        # 2) Truncate if too large (cells threshold)
        cells = row_count * col_count
        truncated = False
        sample_rows = rows
        
        if cells > max_cells:
            truncated = True
            # Head + tail sampling with ellipsis separator
            head = rows[:min(50, row_count)]
            tail = rows[max(0, row_count - 50):]
            sample_rows = head + ([["…"] * col_count] if row_count > 100 else []) + tail
            logger.info(f"Downsampled {row_count} rows to {len(sample_rows)} (max_cells={max_cells})")
        
        # 3) Simple aggregates for numeric columns
        numeric_summary: Dict[str, Dict[str, float]] = {}
        for j, name in enumerate(columns):
            nums = []
            for r in rows:
                try:
                    v = r[j] if j < len(r) else None
                    if isinstance(v, (int, float)) and not (isinstance(v, float) and math.isnan(v)):
                        nums.append(float(v))
                except Exception:
                    pass
            
            if nums:
                numeric_summary[name] = {
                    "count": len(nums),
                    "sum": float(sum(nums)),
                    "mean": float(sum(nums) / max(1, len(nums))),
                    "min": float(min(nums)),
                    "max": float(max(nums)),
                }
        
        # 4) Build compact JSON payload for the LLM
        payload = {
            "question": question,
            "company_id": company_id,
            "section_ids": section_ids,
            "row_count": row_count,
            "columns": columns,
            "sample_rows": sample_rows,  # may be truncated
            "numeric_summary": numeric_summary,
            "execution_ms": exec_ms,
            "truncated": truncated,
        }
        
        # 5) Prompt template (concise, executive tone)
        system = (
            "You are a senior data analyst. Summarize SQL results in clear, non-technical language. "
            "Lead with the direct answer, then 2–5 bullet insights. Use exact numbers if small; "
            "otherwise round appropriately. If time-like columns look monthly/daily, mention trend. "
            "If result is empty, say 'No matching records.' Do not show SQL. No code blocks."
        )
        user = (
            "Summarize this result for the question. Keep under 120 words for the paragraph, "
            "then provide 2–5 concise bullet points with key drivers or notable rows. "
            "If data was truncated, mention it as a caveat.\n\n"
            f"QUESTION:\n{question}\n\n"
            "RESULT JSON:\n" + json.dumps(payload, ensure_ascii=False, default=str)
        )
        
        # 6) Call Gemini
        t0 = time.time()
        answer = generate_text(system_prompt=system, user_prompt=user)
        _ms = (time.time() - t0) * 1000.0
        
        logger.debug(f"LLM summary generated in {_ms:.1f}ms ({len(answer)} chars)")
        return answer.strip()
        
    except Exception as e:
        logger.error(f"Failed to generate LLM summary: {e}")
        # Fallback to basic summary
        return f"Query returned {row_count} row(s) with {col_count} column(s)."


class QueryEngine:
    """
    Natural language to SQL query engine using Google Gemini AI
    Supports automatic API key rotation on rate limit errors
    """
    
    # Class-level variables for key rotation
    _all_api_keys: List[str] = []
    _current_key_index: int = 0
    _failed_keys: set = set()
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None, db_path: Optional[str] = None):
        """
        Initialize the query engine
        
        Args:
            db_manager: Database manager instance. Creates new if None.
            db_path: Optional path to database file
            
        Raises:
            ConfigurationError: If configuration is invalid
            APIError: If cannot connect to Gemini API
        """
        # Load all available API keys on first initialization
        if not QueryEngine._all_api_keys:
            QueryEngine._all_api_keys = Config.get_all_api_keys()
            logger.info(f"Loaded {len(QueryEngine._all_api_keys)} API key(s) for rotation")
        
        # Validate configuration
        errors = Config.validate()
        if errors:
            raise ConfigurationError("\n".join(errors))
        
        # Initialize database manager
        if db_manager is not None:
            self.db_manager = db_manager
        elif db_path is not None:
            # Convert string path to Path object
            from pathlib import Path
            self.db_manager = DatabaseManager(db_path=Path(db_path))
        else:
            self.db_manager = DatabaseManager()
        
        # Verify database exists
        if not self.db_manager.database_exists():
            raise ConfigurationError(
                f"Database not found: {self.db_manager.db_path}\n"
                "Run 'python main.py' to generate data first."
            )
        
        # Initialize Gemini
        self._initialize_gemini()
        
        # Load database schema
        self.schema_text = self._load_schema()
        
        logger.info(f"QueryEngine initialized with model: {self.model_name}")
    
    def _initialize_gemini(self):
        """Initialize Google Gemini API with current key"""
        try:
            # Get current API key
            current_key = self._get_current_api_key()
            genai.configure(api_key=current_key)
            
            # Auto-detect best model
            self.model_name = self._get_best_model()
            self.model = genai.GenerativeModel(self.model_name)
            
            logger.info(f"Connected to Google AI Studio")
            logger.info(f"Using model: {self.model_name}")
            logger.info(f"Using API key index: {QueryEngine._current_key_index + 1}/{len(QueryEngine._all_api_keys)}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            raise APIError(f"Cannot connect to Google AI Studio: {e}")
    
    def _get_current_api_key(self) -> str:
        """Get the current API key for use"""
        if not QueryEngine._all_api_keys:
            raise ConfigurationError("No API keys available")
        
        # Skip failed keys
        attempts = 0
        while attempts < len(QueryEngine._all_api_keys):
            key = QueryEngine._all_api_keys[QueryEngine._current_key_index]
            
            if key not in QueryEngine._failed_keys:
                return key
            
            # This key failed, try next one
            QueryEngine._current_key_index = (QueryEngine._current_key_index + 1) % len(QueryEngine._all_api_keys)
            attempts += 1
        
        # All keys have failed
        raise APIError("All API keys have been exhausted or rate-limited")
    
    def _rotate_api_key(self) -> bool:
        """
        Rotate to the next API key
        
        Returns:
            True if rotated successfully, False if all keys exhausted
        """
        if not QueryEngine._all_api_keys or len(QueryEngine._all_api_keys) <= 1:
            return False
        
        # Mark current key as failed
        current_key = QueryEngine._all_api_keys[QueryEngine._current_key_index]
        QueryEngine._failed_keys.add(current_key)
        
        # Try next key
        original_index = QueryEngine._current_key_index
        attempts = 0
        
        while attempts < len(QueryEngine._all_api_keys):
            QueryEngine._current_key_index = (QueryEngine._current_key_index + 1) % len(QueryEngine._all_api_keys)
            attempts += 1
            
            # Check if we've cycled back to original (all keys tried)
            if QueryEngine._current_key_index == original_index:
                logger.error("All API keys have been exhausted")
                return False
            
            # Try to initialize with new key
            try:
                new_key = QueryEngine._all_api_keys[QueryEngine._current_key_index]
                
                if new_key in QueryEngine._failed_keys:
                    continue
                
                logger.info(f"Rotating to API key {QueryEngine._current_key_index + 1}/{len(QueryEngine._all_api_keys)}")
                genai.configure(api_key=new_key)
                self.model = genai.GenerativeModel(self.model_name)
                logger.info("API key rotation successful")
                return True
                
            except Exception as e:
                logger.warning(f"Key rotation failed for key {QueryEngine._current_key_index}: {e}")
                QueryEngine._failed_keys.add(new_key)
                continue
        
        return False
    
    def _get_best_model(self) -> str:
        """
        Auto-detect the best available Gemini model
        
        Returns:
            Model name string
        """
        preferred_models = [
            'gemini-2.0-flash-exp',
            'gemini-exp-1206',
            'gemini-2.0-flash-thinking-exp-1219',
            'gemini-exp-1121',
            'gemini-1.5-pro',
            'gemini-1.5-flash',
            'gemini-pro'
        ]
        
        try:
            available_models = genai.list_models()
            available_names = [m.name.replace('models/', '') for m in available_models]
            
            # Return first preferred model that's available
            for model in preferred_models:
                if model in available_names:
                    logger.debug(f"Selected model: {model}")
                    return model
            
            # Fallback to first available model with generateContent
            for model in available_models:
                if 'generateContent' in model.supported_generation_methods:
                    name = model.name.replace('models/', '')
                    logger.warning(f"Using fallback model: {name}")
                    return name
            
            raise APIError("No compatible Gemini models found")
            
        except Exception as e:
            logger.warning(f"Could not auto-detect model: {e}. Using fallback.")
            return 'gemini-1.5-flash'
    
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
                schema_text += f"    - {col['name']} ({col['type']}){pk_marker}{null_marker}\n"
            
            schema_text += "\n"
        
        return schema_text
    
    def _create_prompt(self, question: str) -> str:
        """
        Create optimized prompt for Gemini
        
        Args:
            question: Natural language question
            
        Returns:
            Complete prompt string
        """
        return f"""{self.schema_text}

INSTRUCTIONS:
You are an expert SQL query generator for SQLite databases.

RULES:
1. Generate ONLY valid SQLite SQL queries
2. Return ONLY the SQL query with no explanations, markdown, or code blocks
3. Use proper JOIN syntax when querying multiple tables
4. Include appropriate WHERE, GROUP BY, HAVING, ORDER BY clauses
5. Use aggregate functions (COUNT, SUM, AVG, MAX, MIN) when appropriate
6. Add LIMIT {Config.DEFAULT_RESULT_LIMIT} unless specific limit is requested
7. Use table aliases for better readability
8. Handle NULL values appropriately
9. Use LIKE with wildcards for text searches
10. Generate efficient queries with proper indexing considerations

QUESTION: {question}

SQL QUERY:"""
    
    def generate_sql(self, question: str) -> str:
        """
        Generate SQL query from natural language question
        Automatically rotates API keys on rate limit errors
        
        Args:
            question: Natural language question
            
        Returns:
            SQL query string
            
        Raises:
            QueryError: If query generation fails
        """
        logger.info(f"Generating SQL for: {question}")
        
        if not question or not question.strip():
            raise QueryError("Question cannot be empty")
        
        max_retries = len(QueryEngine._all_api_keys)
        attempt = 0
        
        while attempt < max_retries:
            try:
                prompt = self._create_prompt(question)
                
                start_time = time.time()
                response = self.model.generate_content(prompt)
                generation_time = time.time() - start_time
                
                logger.debug(f"SQL generation took {generation_time:.2f}s")
                
                sql = self._clean_sql(response.text)
                
                logger.info(f"Generated SQL: {sql[:100]}...")
                
                return sql
                
            except Exception as e:
                error_str = str(e).lower()
                
                # Check if it's a rate limit error (429)
                if 'quota' in error_str or 'rate limit' in error_str or '429' in error_str or 'resource_exhausted' in error_str:
                    logger.warning(f"Rate limit hit on API key {QueryEngine._current_key_index + 1}: {e}")
                    
                    # Try to rotate to next key
                    if self._rotate_api_key():
                        attempt += 1
                        logger.info(f"Retrying with new API key (attempt {attempt + 1}/{max_retries})")
                        continue
                    else:
                        logger.error("All API keys exhausted due to rate limits")
                        raise QueryError(
                            f"All {len(QueryEngine._all_api_keys)} API key(s) have hit rate limits. "
                            "Please wait 60 seconds and try again."
                        )
                else:
                    # Non-rate-limit error, don't retry
                    logger.error(f"SQL generation failed: {e}")
                    raise QueryError(f"Failed to generate SQL: {e}")
        
        # Should not reach here, but just in case
        raise QueryError(f"Failed to generate SQL after {max_retries} attempts")
    
    def _clean_sql(self, sql: str) -> str:
        """
        Clean and validate generated SQL
        
        Args:
            sql: Raw SQL from LLM
            
        Returns:
            Cleaned SQL string
        """
        original_sql = sql
        
        # Remove markdown code blocks
        sql = sql.replace('```sql', '').replace('```', '').strip()
        
        # Remove common prefixes that AI might add (case-insensitive check)
        prefixes_to_remove = ['SQLite ', 'SQL ', 'Query: ', 'sqlite ', 'sql ']
        for prefix in prefixes_to_remove:
            if sql.lower().startswith(prefix.lower()):
                sql = sql[len(prefix):].strip()
                logger.debug(f"Removed prefix '{prefix}' from SQL")
                break  # Only remove first matching prefix
        
        # If still starts with word before SELECT, find SELECT and start from there
        if not sql.upper().startswith('SELECT'):
            select_idx = sql.upper().find('SELECT')
            if select_idx > 0:
                logger.debug(f"Found SELECT at position {select_idx}, trimming prefix")
                sql = sql[select_idx:].strip()
        
        # Remove trailing semicolon
        sql = sql.rstrip(';').strip()
        
        # Remove multiple whitespaces
        sql = ' '.join(sql.split())
        
        # Basic validation - ensure it's a SELECT query
        if not sql.upper().startswith('SELECT'):
            logger.warning(f"Generated query is not a SELECT: {sql[:50]}")
        
        return sql
    
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
            Dictionary with query results and metadata
        """
        logger.debug(f"Executing query: {sql[:100]}...")
        
        max_results = max_results or Config.MAX_QUERY_RESULTS
        
        try:
            start_time = time.time()
            results = self.db_manager.execute_query(sql)
            execution_time = time.time() - start_time
            
            # Limit results if needed
            if len(results) > max_results:
                logger.warning(f"Results truncated from {len(results)} to {max_results}")
                results = results[:max_results]
                truncated = True
            else:
                truncated = False
            
            logger.info(f"Query returned {len(results)} rows in {execution_time:.3f}s")
            
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
        
        Args:
            question: Natural language question
            max_results: Maximum number of results
            
        Returns:
            Dictionary with results and metadata
        """
        try:
            sql = self.generate_sql(question)
            result = self.execute_query(sql, max_results)
            result['question'] = question
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
