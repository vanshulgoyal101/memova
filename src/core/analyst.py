"""
AI Business Analyst
Handles strategic questions that require analysis beyond data retrieval
"""

from typing import Dict, List, Any, Tuple
import logging

from src.core.llm_client import UnifiedLLMClient
from src.core.database import DatabaseManager
from src.utils.logger import setup_logger
from src.utils.exceptions import QueryError

logger = setup_logger(__name__)


class BusinessAnalyst:
    """
    AI-powered business analyst that provides strategic insights
    
    Handles questions like:
    - "Give me actionable steps to improve sales"
    - "What insights can you provide from the data?"
    - "Analyze customer behavior and recommend strategies"
    
    Approach:
    1. Identify key metrics from database
    2. Run exploratory queries to gather context
    3. Analyze patterns and trends
    4. Generate actionable recommendations
    """
    
    def __init__(self, db_manager: DatabaseManager, llm_client: UnifiedLLMClient, schema_text: str):
        """
        Initialize business analyst
        
        Args:
            db_manager: Database connection manager
            llm_client: LLM client for analysis
            schema_text: Database schema context
        """
        self.db_manager = db_manager
        self.llm_client = llm_client
        self.schema_text = schema_text
        
        # System message with schema (for first call only)
        self.system_message_with_schema = f"""{schema_text}

You are an expert business analyst and data scientist."""
        
        # Lightweight system message (for subsequent calls)
        self.system_message_light = """You are an expert business analyst and data scientist.
        
You have access to the database schema from the previous conversation. Continue using that context."""
    
    def is_analytical_question(self, question: str) -> bool:
        """
        Determine if question requires strategic analysis vs simple data retrieval
        
        Detects vague business problems like:
        - "My sales are declining" (observation + implied "why?")
        - "Revenue is too low" (complaint + implied "what to do?")
        - "Customers are unhappy" (symptom + implied "how to fix?")
        
        Args:
            question: User question
            
        Returns:
            True if question needs analysis, False if just data query
        """
        question_lower = question.lower()
        
        # Keywords indicating analytical/strategic questions
        analytical_keywords = [
            # Explicit analysis requests
            'insight', 'insights', 'analyze', 'analysis', 'recommend',
            'recommendation', 'strategy', 'strategic', 'improve',
            'improvement', 'optimize', 'optimization', 'actionable',
            'action', 'suggest', 'suggestion', 'advice', 'why',
            'understand', 'explain', 'pattern', 'trend', 'opportunity',
            'problem', 'issue', 'challenge', 'solution', 'grow', 'growth',
            'increase', 'decrease', 'boost', 'enhance', 'better',
            
            # Vague problem patterns (observation + emotion)
            'too low', 'too high', 'too many', 'too few', 'too much', 'too little',
            'not enough', 'declining', 'dropping', 'falling', 'shrinking',
            'struggling', 'worried', "don't know", "dont know", 'confused',
            'stuck', 'frustrated', 'concerned', 'alarmed', 'unhappy',
            'disappointed', 'unexpected', 'surprising', 'strange', 'unusual',
            
            # Negative performance indicators
            'poor', 'bad', 'worse', 'worst', 'failing', 'failed', 'losing',
            'loss', 'inefficient', 'slow', 'costly', 'expensive', 'low',
            
            # Help/support requests
            'help', 'fix', 'solve', 'need to', 'how can', 'how do',
            'what should', 'ways to', 'guide', 'support'
        ]
        
        # Phrases that strongly indicate analytical need (more specific)
        analytical_phrases = [
            'i need', 'i want', 'help me', 'not sure',
            'my business', 'our business', 'the business',
            'performance is', 'sales are', 'revenue is', 'customers are'
        ]
        
        # Check keywords
        if any(keyword in question_lower for keyword in analytical_keywords):
            return True
        
        # Check phrases (more specific patterns)
        if any(phrase in question_lower for phrase in analytical_phrases):
            return True
        
        return False
    
    def analyze(self, question: str) -> Dict[str, Any]:
        """
        Perform comprehensive business analysis with AI-driven data gathering
        
        Multi-stage process:
        1. Understand the problem and formulate hypotheses
        2. AI determines WHAT data is needed to analyze the problem
        3. Generate and execute custom exploratory queries
        4. Analyze results and identify patterns
        5. Generate insights and actionable recommendations
        6. (Optional) Follow up with additional queries if needed
        
        Args:
            question: Strategic question or vague business problem from user
            
        Returns:
            Dictionary with:
            - analysis_text: Natural language insights
            - data_points: Key metrics discovered
            - recommendations: Actionable steps
            - queries_used: SQL queries that gathered the data
            - hypotheses: Initial problem interpretation
        """
        logger.info(f"Starting intelligent business analysis for: {question[:100]}")
        
        # Pre-validate: Check if question keywords match available tables
        question_lower = question.lower()
        
        # Extract table names from schema
        schema_tables = []
        for line in self.schema_text.split('\n'):
            if line.startswith('Table: '):
                table_name = line.replace('Table: ', '').strip()
                schema_tables.append(table_name.lower())
        
        # Check for common domain mismatches
        mismatch_keywords = {
            'student': ['students', 'enrollment', 'learner'],
            'class': ['classes', 'course', 'grade'],
            'question': ['questions', 'quiz', 'test', 'exam', 'assessment'],
            'teacher': ['teachers', 'instructor', 'faculty'],
            'score': ['scores', 'marks', 'grades', 'results'],
        }
        
        # Detect if question asks about concepts not in schema
        for keyword, related_terms in mismatch_keywords.items():
            if keyword in question_lower or any(term in question_lower for term in related_terms):
                # Check if ANY related table exists
                has_related_table = any(
                    any(term in table for term in related_terms + [keyword])
                    for table in schema_tables
                )
                
                if not has_related_table:
                    available_tables_str = ", ".join(schema_tables)
                    raise QueryError(
                        f"This database does not contain data about '{keyword}'. "
                        f"Available tables: {available_tables_str}. "
                        f"Tip: Switch to the correct database that matches your question."
                    )
        
        try:
            # Stage 1: Problem interpretation - What are we trying to solve?
            problem_breakdown = self._interpret_problem(question)
            logger.info(f"Problem breakdown: {problem_breakdown.get('focus_areas', [])}")
            
            # Stage 2: Query planning - What data do we need?
            query_plan = self._plan_data_gathering(question, problem_breakdown)
            logger.info(f"Generated {len(query_plan)} custom exploratory queries")
            
            # Stage 3: Execute custom queries
            data_context = self._execute_query_plan(query_plan)
            
            # Stage 3.5: Validate that we have actual data (prevent hallucination)
            successful_queries = sum(1 for q in data_context.values() if not q.get('error') and q.get('results'))
            total_queries = len(data_context)
            
            if successful_queries == 0:
                logger.warning("All queries failed - cannot generate analysis")
                
                # Get available tables for better error message
                table_names = []
                for line in self.schema_text.split('\n'):
                    if line.startswith('Table: '):
                        table_names.append(line.replace('Table: ', '').strip())
                
                tables_list = "\n".join(f"- {t}" for t in table_names) if table_names else "No tables found"
                
                return {
                    "success": False,
                    "error": "No data available - question doesn't match database",
                    "analysis_text": f"""❌ **Unable to analyze**: All database queries failed. 

**This database contains the following tables:**
{tables_list}

**Why this happened:**
1. Your question doesn't match the data available in this database
2. The question references concepts/entities not present in these tables
3. The AI tried to query tables that don't exist

**What to try instead:**
- Ask questions about the actual tables listed above
- Use "Show me a sample of [table_name]" to explore the data
- Ask "What data is available in this database?"
- Switch to a different company/database that matches your question

**Example:** If you want to analyze student test results, switch to the "EdNite Test Results" database.""",
                    "data_points": [],
                    "insights": [],
                    "recommendations": [],
                    "hypotheses": [],
                    "query_data": data_context
                }
            
            if successful_queries < total_queries * 0.5:
                logger.warning(f"Only {successful_queries}/{total_queries} queries succeeded - analysis may be limited")
            
            # Stage 4: Deep analysis with context
            analysis = self._generate_deep_analysis(question, problem_breakdown, data_context)
            
            # Stage 5: Add metadata
            analysis['hypotheses'] = problem_breakdown.get('hypotheses', [])
            analysis['focus_areas'] = problem_breakdown.get('focus_areas', [])
            
            # Stage 6: Add raw query data for frontend display
            analysis['query_data'] = data_context  # Full query results with SQL
            
            logger.info("Intelligent business analysis completed successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"Business analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "analysis_text": f"Unable to complete analysis: {e}",
                "data_points": [],
                "recommendations": [],
                "hypotheses": []
            }
    
    def _interpret_problem(self, question: str) -> Dict[str, Any]:
        """
        Use AI to understand the vague business problem and formulate hypotheses
        
        Args:
            question: Vague business problem (e.g., "sales are declining")
            
        Returns:
            Dict with:
            - problem_statement: Clarified version of the problem
            - hypotheses: Possible causes/factors to investigate
            - focus_areas: Which data domains to examine
            - metrics_to_check: Specific metrics that might be relevant
        """
        logger.debug("Interpreting business problem with AI")
        
        # Extract table names from schema for context
        table_names = []
        for line in self.schema_text.split('\n'):
            if line.startswith('Table: '):
                table_names.append(line.replace('Table: ', '').strip())
        
        tables_str = ", ".join(table_names) if table_names else "unknown"
        
        user_message = f"""ROLE: You are a business analyst who excels at breaking down vague problems into investigable components.

AVAILABLE DATA TABLES IN THIS DATABASE:
{tables_str}

BUSINESS PROBLEM: {question}

Please analyze this problem and provide a structured breakdown:

1. **Problem Statement**: Restate the problem clearly and specifically
2. **Hypotheses**: List 3-5 possible root causes or factors contributing to this problem
3. **Focus Areas**: Which of the AVAILABLE tables should we investigate? (ONLY use table names from the list above)
4. **Key Metrics**: What specific metrics would help us understand this problem?

CRITICAL: Only suggest focus areas (tables) that actually exist in the database above. DO NOT suggest tables like "customers" or "products" if they're not in the available tables list.

Respond in JSON format:
{{
  "problem_statement": "Clear restatement of the problem",
  "hypotheses": ["Hypothesis 1", "Hypothesis 2", "Hypothesis 3"],
  "focus_areas": ["actual_table_name1", "actual_table_name2"],
  "metrics_to_check": ["metric1", "metric2", "metric3"]
}}"""
        
        try:
            response_text, provider = self.llm_client.generate_content(
                user_message,
                system_message=self.system_message_with_schema  # First call - send full schema
            )
            
            # Parse JSON response
            import json
            import re
            
            # Extract JSON from response (may have markdown)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                problem_breakdown = json.loads(json_match.group(0))
                logger.info(f"Problem interpreted by {provider.upper()}")
                return problem_breakdown
            else:
                # Fallback if JSON parsing fails
                return {
                    "problem_statement": question,
                    "hypotheses": ["Insufficient data", "Process inefficiency", "Market changes"],
                    "focus_areas": ["sales", "customers", "products"],
                    "metrics_to_check": ["revenue", "orders", "customer_count"]
                }
                
        except Exception as e:
            logger.warning(f"Problem interpretation failed: {e}, using fallback")
            return {
                "problem_statement": question,
                "hypotheses": ["Data quality issues", "External factors"],
                "focus_areas": ["sales", "customers"],
                "metrics_to_check": ["revenue", "orders"]
            }
    
    def _plan_data_gathering(self, question: str, problem_breakdown: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Use AI to determine WHAT exploratory queries we need to run
        
        Instead of fixed queries, AI generates custom SQL based on the problem.
        
        Args:
            question: Original user question
            problem_breakdown: Result from _interpret_problem()
            
        Returns:
            List of query plans: [{"id": "...", "description": "...", "sql": "..."}]
        """
        logger.debug("Planning custom data gathering queries with AI")
        
        focus_areas_str = ", ".join(problem_breakdown.get('focus_areas', []))
        hypotheses_str = "\n".join(f"- {h}" for h in problem_breakdown.get('hypotheses', []))
        metrics_str = ", ".join(problem_breakdown.get('metrics_to_check', []))
        
        user_message = f"""ROLE: You are a data analyst who writes SQL queries to investigate business problems.

DATABASE SCHEMA (USE ONLY THESE TABLES):
{self.schema_text}

PROBLEM: {problem_breakdown.get('problem_statement', question)}

HYPOTHESES TO INVESTIGATE:
{hypotheses_str}

FOCUS AREAS: {focus_areas_str}
KEY METRICS: {metrics_str}

Generate 3-5 SQL queries that will help us:
1. Understand the current state of these metrics
2. Identify patterns or anomalies
3. Test the hypotheses
4. Find root causes

For each query, provide:
- id: Short identifier (e.g., "revenue_trend", "customer_churn")
- description: What this query reveals
- sql: The actual SQL query (must be valid SQLite)

CRITICAL RULES:
- ONLY use table names and column names that exist in the schema above
- DO NOT invent or assume table names (e.g., don't use "customer_feedback" unless it's in the schema)
- Use LIMIT to prevent large result sets (max 100 rows)
- Use aggregations where appropriate (COUNT, SUM, AVG)
- Include time-based analysis if date columns exist
- Join tables correctly with proper foreign keys from schema

Respond in JSON format:
{{
  "queries": [
    {{
      "id": "revenue_trend",
      "description": "Revenue by month to identify trend",
      "sql": "SELECT strftime('%Y-%m', order_date) as month, SUM(total_amount) as revenue FROM sales_orders GROUP BY month ORDER BY month DESC LIMIT 12"
    }}
  ]
}}"""
        
        try:
            response_text, provider = self.llm_client.generate_content(
                user_message,
                system_message=self.system_message_with_schema  # IMPORTANT: Include schema for SQL generation!
            )
            
            # Parse JSON response
            import json
            import re
            
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                query_plan = json.loads(json_match.group(0))
                queries = query_plan.get('queries', [])
                logger.info(f"Generated {len(queries)} custom queries via {provider.upper()}")
                return queries
            else:
                # Fallback to basic queries
                return self._get_fallback_queries(problem_breakdown)
                
        except Exception as e:
            logger.warning(f"Query planning failed: {e}, using fallback queries")
            return self._get_fallback_queries(problem_breakdown)
    
    def _get_fallback_queries(self, problem_breakdown: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Fallback queries if AI query generation fails
        
        Returns basic exploratory queries based on focus areas
        """
        focus_areas = problem_breakdown.get('focus_areas', ['sales'])
        queries = []
        
        if 'sales' in focus_areas:
            queries.append({
                "id": "sales_overview",
                "description": "Overall sales performance",
                "sql": "SELECT COUNT(*) as total_orders, SUM(total_amount) as total_revenue, AVG(total_amount) as avg_order_value FROM sales_orders"
            })
        
        if 'customers' in focus_areas:
            queries.append({
                "id": "customer_overview",
                "description": "Customer base summary",
                "sql": "SELECT COUNT(DISTINCT c.customer_id) as total_customers, COUNT(DISTINCT so.order_id) as total_orders FROM customers c LEFT JOIN sales_orders so ON c.customer_id = so.customer_id"
            })
        
        if 'products' in focus_areas:
            queries.append({
                "id": "top_products",
                "description": "Top performing products",
                "sql": "SELECT p.product_name, SUM(so.total_amount) as revenue FROM products p LEFT JOIN sales_orders so ON p.product_id = so.product_id GROUP BY p.product_id ORDER BY revenue DESC LIMIT 10"
            })
        
        return queries
    
    def _execute_query_plan(self, query_plan: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Execute the custom query plan and gather results
        
        Args:
            query_plan: List of queries from _plan_data_gathering()
            
        Returns:
            Dict mapping query IDs to results
        """
        logger.debug(f"Executing {len(query_plan)} custom exploratory queries")
        
        context = {}
        
        for query_def in query_plan:
            query_id = query_def.get('id', 'unknown')
            sql = query_def.get('sql', '')
            description = query_def.get('description', '')
            
            try:
                result = self.db_manager.execute_query(sql)
                
                # Store results with metadata
                context[query_id] = {
                    'description': description,
                    'sql': sql,
                    'results': result,
                    'row_count': len(result) if isinstance(result, list) else 0
                }
                
                logger.debug(f"Query '{query_id}': {len(result) if isinstance(result, list) else 0} rows")
                
            except Exception as e:
                logger.warning(f"Query '{query_id}' failed: {e}")
                context[query_id] = {
                    'description': description,
                    'sql': sql,
                    'error': str(e),
                    'results': []
                }
        
        return context
    
    def _generate_deep_analysis(
        self, 
        question: str, 
        problem_breakdown: Dict[str, Any],
        data_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate deep analysis using AI with full problem context
        
        Args:
            question: Original user question
            problem_breakdown: Problem interpretation
            data_context: Results from custom queries
            
        Returns:
            Structured analysis with insights and recommendations
        """
        logger.debug("Generating deep AI-powered analysis")
        
        # Validate we have actual data (prevent hallucination)
        successful_data = {k: v for k, v in data_context.items() 
                          if not v.get('error') and v.get('results')}
        
        if not successful_data:
            logger.error("No successful queries with data - cannot generate meaningful analysis")
            return {
                "success": False,
                "analysis_text": "Unable to generate analysis: No data available from queries",
                "data_points": [],
                "insights": [],
                "recommendations": [],
                "queries_used": []
            }
        
        # Format data context for LLM
        data_summary = self._format_data_for_deep_analysis(data_context)
        
        # Create analysis prompt
        hypotheses_str = "\n".join(f"{i+1}. {h}" for i, h in enumerate(problem_breakdown.get('hypotheses', [])))
        
        user_message = f"""ROLE: You are a senior business consultant with expertise in data-driven problem solving.

BUSINESS PROBLEM: {question}

PROBLEM BREAKDOWN:
{problem_breakdown.get('problem_statement', question)}

HYPOTHESES WE'RE TESTING:
{hypotheses_str}

DATA ANALYSIS RESULTS:

{data_summary}

Based on this data, provide a comprehensive business analysis:

1. **KEY INSIGHTS** (4-6 bullet points)
   - Which hypotheses are supported or refuted by the data?
   - What patterns, trends, or anomalies did you discover?
   - What are the root causes of the problem?
   - Include specific numbers and percentages

2. **DETAILED ANALYSIS** (3-4 paragraphs)
   - Synthesize the data into a coherent narrative
   - Explain WHY this problem is occurring
   - Connect multiple data points to tell the story
   - Identify both immediate causes and underlying factors

3. **ACTIONABLE RECOMMENDATIONS** (6-10 specific, data-driven actions)
   
   Each recommendation MUST follow this format:
   
   **[Priority: HIGH/MEDIUM/LOW] [Action Title]**
   - **What to do**: Exact step-by-step action (not vague advice)
   - **Why**: Reference specific data point that justifies this (e.g., "Because X metric shows Y")
   - **How**: Concrete implementation details (tools, methods, processes)
   - **Timeline**: Specific timeframe (e.g., "Within 2 weeks", "Q1 2025")
   - **Expected Impact**: Quantified outcome (e.g., "Increase by 15%", "Reduce by $50K/month")
   - **Owner**: Who should execute this (role/department)
   
   BAD EXAMPLE (too vague): "Conduct deeper analysis of patterns"
   GOOD EXAMPLE: "[HIGH] Launch targeted promotion for top 5 products generating 23% of sales. Test 15% discount for 2 weeks in December peak season. Expected: +$120K revenue. Owner: Marketing team."
   
   BAD EXAMPLE: "Implement data collection systems"
   GOOD EXAMPLE: "[MEDIUM] Add salesperson tracking to POS system (currently NULL for all 37,857 transactions). Integrate with CRM by Jan 15. Expected: Identify top performers, optimize territories. Cost: $8K setup. Owner: IT + Sales Ops."
   
   BAD EXAMPLE: "Review and optimize processes"
   GOOD EXAMPLE: "[HIGH] Address February sales drop (1,965 transactions vs Dec's 6,778 = -71%). Analyze inventory stockouts, staffing levels, and promo calendar. Launch recovery campaign by Feb 5. Expected: Recover 2,000+ transactions = $200K. Owner: Store managers + Regional VP."
   
   Focus on:
   - Quick wins (implement in < 1 month)
   - Revenue opportunities (cite specific $ amounts)
   - Cost reductions (quantify savings)
   - Operational fixes (cite efficiency gains)
   - Customer/product focus (cite top/bottom performers)

4. **IMPLEMENTATION ROADMAP** (30/60/90 day plan)
   - **Month 1 (Quick Wins)**: List 2-3 highest priority actions
   - **Month 2 (Foundation)**: List 2-3 medium-priority actions
   - **Month 3 (Scaling)**: List 2-3 long-term initiatives

Format as structured markdown with clear sections."""
        
        try:
            # Generate analysis using AI
            analysis_text, provider = self.llm_client.generate_content(
                user_message,
                system_message=self.system_message_light  # Lightweight - reference previous context
            )
            
            logger.info(f"Deep analysis generated by {provider.upper()}")
            
            # Parse the response to extract structured parts
            insights, recommendations = self._parse_analysis(analysis_text)
            
            return {
                "success": True,
                "analysis_text": analysis_text,
                "data_points": self._extract_key_metrics_from_context(data_context),
                "insights": insights,
                "recommendations": recommendations,
                "queries_used": list(data_context.keys())
            }
            
        except Exception as e:
            logger.error(f"AI analysis generation failed: {e}")
            raise
    
    def _format_data_for_deep_analysis(self, data_context: Dict[str, Any]) -> str:
        """
        Format collected data from custom queries into readable text for LLM
        
        Args:
            data_context: Dictionary of query results from _execute_query_plan()
            
        Returns:
            Formatted string with data insights
        """
        formatted = []
        
        for query_id, query_data in data_context.items():
            description = query_data.get('description', query_id)
            results = query_data.get('results', [])
            error = query_data.get('error')
            
            formatted.append(f"\n### {description} ({query_id})")
            
            if error:
                formatted.append(f"⚠️ Query failed: {error}")
                continue
            
            if not results:
                formatted.append("No data available")
                continue
            
            # Format results based on type
            if isinstance(results, list) and len(results) > 0:
                # Show first row as key metrics
                first_row = results[0]
                for key, value in first_row.items():
                    # Format numbers nicely
                    if isinstance(value, (int, float)):
                        if value is None:
                            formatted.append(f"- {key}: N/A")
                        elif abs(value) >= 1000:
                            formatted.append(f"- {key}: {value:,.2f}")
                        else:
                            formatted.append(f"- {key}: {value:.2f}")
                    else:
                        formatted.append(f"- {key}: {value}")
                
                # For multi-row results, show top items
                if len(results) > 1:
                    formatted.append(f"\nShowing {min(len(results), 5)} of {len(results)} records:")
                    for i, row in enumerate(results[:5], 1):
                        # Get the main identifying field (usually first column)
                        identifier = list(row.values())[0] if row else f"Row {i}"
                        # Get the main value field (usually last column)
                        value = list(row.values())[-1] if row and len(row) > 1 else ""
                        if isinstance(value, (int, float)) and value is not None:
                            formatted.append(f"  {i}. {identifier}: {value:,.2f}")
                        else:
                            formatted.append(f"  {i}. {identifier}: {value}")
        
        return "\n".join(formatted)
    
    def _extract_key_metrics_from_context(self, data_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract key performance metrics from custom query results
        
        Args:
            data_context: Dictionary of query results
            
        Returns:
            List of metric dictionaries
        """
        metrics = []
        
        for query_id, query_data in data_context.items():
            results = query_data.get('results', [])
            description = query_data.get('description', query_id)
            
            if not results or not isinstance(results, list) or len(results) == 0:
                continue
            
            # Extract metrics from first row
            first_row = results[0]
            for key, value in first_row.items():
                if isinstance(value, (int, float)) and value is not None:
                    metrics.append({
                        "name": key.replace('_', ' ').title(),
                        "value": value,
                        "category": description,
                        "query_id": query_id
                    })
        
        return metrics
    
    def _parse_analysis(self, analysis_text: str) -> Tuple[List[str], List[str]]:
        """
        Parse AI-generated analysis to extract insights and recommendations
        
        Args:
            analysis_text: Raw analysis from LLM
            
        Returns:
            Tuple of (insights list, recommendations list)
        """
        insights = []
        recommendations = []
        
        lines = analysis_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Detect sections
            if 'KEY INSIGHT' in line.upper() or 'INSIGHT' in line.upper():
                current_section = 'insights'
                continue
            elif 'RECOMMENDATION' in line.upper() or 'ACTION' in line.upper():
                current_section = 'recommendations'
                continue
            elif 'DETAILED ANALYSIS' in line.upper() or 'ANALYSIS' in line.upper():
                current_section = 'analysis'
                continue
            
            # Extract bullet points
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                item = line.lstrip('-•* ').strip()
                if current_section == 'insights' and item:
                    insights.append(item)
                elif current_section == 'recommendations' and item:
                    recommendations.append(item)
            
            # Extract numbered items
            elif len(line) > 2 and line[0].isdigit() and line[1] in '.):':
                item = line[2:].strip()
                if current_section == 'insights' and item:
                    insights.append(item)
                elif current_section == 'recommendations' and item:
                    recommendations.append(item)
        
        # If no recommendations found, generate defaults based on insights
        if not recommendations and insights:
            recommendations = [
                "Conduct deeper analysis of the identified patterns to understand root causes",
                "Implement data collection systems to fill critical data gaps identified in the analysis",
                "Review and optimize processes in areas showing inefficiency or underperformance",
                "Develop targeted action plans to address specific issues highlighted in the insights",
                "Monitor key metrics regularly to track improvement and adjust strategies as needed",
                "Prioritize high-impact areas for immediate intervention based on the data analysis"
            ]
        
        return insights, recommendations
