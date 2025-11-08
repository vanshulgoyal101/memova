"""
API Route Handlers
All FastAPI endpoint implementations
"""

from fastapi import HTTPException, APIRouter, UploadFile, File
from typing import List, Dict, Any
from pathlib import Path
import time
import shutil
import uuid
from datetime import datetime

from api.models import (
    AskRequest, AskResponse,
    QueryRequest, QueryResponse,
    DatabaseInfo, SchemaInfo, ExampleQuery,
    UploadResponse, UploadedDatabase,
    ChartConfig, TrendInsight, BusinessAnalysis,
    QueryStepModel, QueryPlanModel
)
from src.core.query_engine import QueryEngine
from src.core.summarizer import summarize_result
from src.core.database import DatabaseManager
from src.core.schema_detector import SchemaDetector
from src.core.chart_detector import detect_charts_from_results
from src.core.trend_detector import detect_trends_from_results
from src.data.converters import excel_to_sql
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.utils.exceptions import QueryError

logger = setup_logger(__name__)

# Database configuration
DATABASES = {
    'electronics': {
        'name': 'Electronics Company',
        'path': str(Config.DATABASE_DIR / 'electronics_company.db'),
        'description': '12 tables covering HR, Sales, Finance, Inventory, Products, Customers, and more',
        'currency': 'USD',
        'currency_symbol': '$'
    },
    'airline': {
        'name': 'Airline Company',
        'path': str(Config.DATABASE_DIR / 'airline_company.db'),
        'description': '16 tables covering Aircraft, Pilots, Flights, Passengers, Revenue, and more',
        'currency': 'USD',
        'currency_symbol': '$'
    },
    'edtech': {
        'name': 'EdTech India Company',
        'path': str(Config.DATABASE_DIR / 'edtech_company.db'),
        'description': '15 tables covering Students, Instructors, Courses, Enrollments, Assessments, Payments, Placements, and more',
        'currency': 'INR',
        'currency_symbol': '₹'
    },
    'ednite': {
        'name': 'EdNite Test Results',
        'path': str(Config.DATABASE_DIR / 'ednite_company.db'),
        'description': '5 tables covering 2,540 students, 90 questions across Classes 5-10, with performance analysis and answer tracking',
        'currency': 'INR',
        'currency_symbol': '₹'
    },
    'liqo': {
        'name': 'Liqo Retail Chain',
        'path': str(Config.DATABASE_DIR / 'liqo_company.db'),
        'description': '5 tables: 37,857 transactions across 5 store locations in North India, covering electronics and home appliances sales (FY 2022-23)',
        'currency': 'INR',
        'currency_symbol': '₹'
    }
}

# Example queries for each database
EXAMPLE_QUERIES = {
    'electronics': [
        ExampleQuery(id=1, title='Total Sales', question='What is the total sales amount?', category='Finance', complexity='simple'),
        ExampleQuery(id=2, title='Top Customers', question='Show me the top 10 customers by total purchase amount', category='Sales', complexity='medium'),
        ExampleQuery(id=3, title='Low Inventory', question='Which products have inventory below 50 units?', category='Inventory', complexity='simple'),
        ExampleQuery(id=4, title='Sales Performance', question='Which sales employees exceeded their targets and by how much?', category='HR', complexity='complex'),
        ExampleQuery(id=5, title='Product Categories', question='Show me sales by product category', category='Products', complexity='medium'),
    ],
    'airline': [
        ExampleQuery(id=1, title='Fleet Size', question='How many aircraft are in the fleet?', category='Fleet', complexity='simple'),
        ExampleQuery(id=2, title='Top Pilots', question='Show me the top 10 pilots with the most flight hours', category='Personnel', complexity='medium'),
        ExampleQuery(id=3, title='Flight Details', question='Show me flights with their aircraft type and passenger count', category='Operations', complexity='medium'),
        ExampleQuery(id=4, title='Revenue Analysis', question='What is the total revenue by payment method?', category='Finance', complexity='medium'),
        ExampleQuery(id=5, title='Fuel Efficiency', question='Show me the average fuel cost per flight for each aircraft type', category='Operations', complexity='complex'),
    ],
    'edtech': [
        ExampleQuery(id=1, title='Total Students', question='How many students are enrolled?', category='Students', complexity='simple'),
        ExampleQuery(id=2, title='Top Courses', question='Show me the top 10 courses by enrollment count', category='Courses', complexity='medium'),
        ExampleQuery(id=3, title='Revenue Analysis', question='What is the total revenue from course payments?', category='Payments', complexity='simple'),
        ExampleQuery(id=4, title='Instructor Performance', question='Which instructors have the highest average course ratings?', category='Instructors', complexity='medium'),
        ExampleQuery(id=5, title='Student Success', question='Show me students with highest placement salaries and their courses', category='Placements', complexity='complex'),
    ],
    'ednite': [
        ExampleQuery(id=1, title='Top Performers', question='Show me the top 10 students by score percentage', category='Performance', complexity='simple'),
        ExampleQuery(id=2, title='Class Comparison', question='What is the average score for each class?', category='Classes', complexity='simple'),
        ExampleQuery(id=3, title='Question Analysis', question='Which questions had the lowest correct answer rate?', category='Questions', complexity='medium'),
        ExampleQuery(id=4, title='Student Performance', question='Show students who scored above 80%', category='Performance', complexity='simple'),
        ExampleQuery(id=5, title='Difficult Questions', question='Find questions where less than 30% of students answered correctly', category='Questions', complexity='complex'),
    ],
    'liqo': [
        ExampleQuery(id=1, title='Total Revenue', question='What is the total revenue for FY 2022-23?', category='Finance', complexity='simple'),
        ExampleQuery(id=2, title='Top Locations', question='Show me sales by location', category='Sales', complexity='simple'),
        ExampleQuery(id=3, title='Best Sellers', question='What are the top 10 products by revenue?', category='Products', complexity='medium'),
        ExampleQuery(id=4, title='Brand Performance', question='Which brands generate the most revenue?', category='Sales', complexity='medium'),
        ExampleQuery(id=5, title='Monthly Trends', question='Show monthly sales trends across the year', category='Analytics', complexity='complex'),
        ExampleQuery(id=6, title='Top Salespeople', question='Show me the top 5 salespeople by total revenue', category='Performance', complexity='medium'),
        ExampleQuery(id=7, title='B2B vs B2C', question='Compare B2B and B2C sales', category='Analytics', complexity='medium'),
        ExampleQuery(id=8, title='Category Analysis', question='Show me sales breakdown by main category', category='Products', complexity='simple'),
    ]
}



# Helper function (legacy - kept for backward compatibility)
def _generate_answer_text(
    question: str,
    sql: str,
    columns: List[str],
    rows: List[List[Any]],
    row_count: int
) -> str:
    """
    Generate basic answer text (fallback for when LLM unavailable)
    Deprecated: Use _summarize_result_with_llm instead
    """
    if row_count == 0:
        return "No results found for your query."
    
    if row_count == 1 and len(columns) == 1:
        value = rows[0][0]
        col_name = columns[0]
        
        if 'COUNT' in col_name.upper():
            return f"There are {value:,} records matching your query."
        elif 'SUM' in col_name.upper() or 'TOTAL' in col_name.upper():
            if isinstance(value, (int, float)):
                return f"The total is ${value:,.2f}." if any(x in col_name.lower() for x in ['price', 'cost', 'salary']) else f"The total is {value:,}."
            return f"The total is {value}."
        elif 'AVG' in col_name.upper() or 'AVERAGE' in col_name.upper():
            if isinstance(value, (int, float)):
                return f"The average is {value:,.2f}."
            return f"The average is {value}."
        elif 'MAX' in col_name.upper() or 'MIN' in col_name.upper():
            return f"The value is {value}."
        else:
            return f"The result is: {value}"
    
    if row_count <= 5:
        return f"Found {row_count} result{'s' if row_count != 1 else ''} with {len(columns)} column{'s' if len(columns) != 1 else ''}."
    elif row_count <= 100:
        return f"Found {row_count} results. Showing all records with {len(columns)} columns."
    else:
        return f"Found {row_count} results across {len(columns)} columns. Large dataset returned."


# Create router
router = APIRouter()


@router.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Multi-Database Query API",
        "version": "1.0.0",
        "status": "online",
        "databases": list(DATABASES.keys())
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/databases", response_model=List[DatabaseInfo])
async def get_databases():
    """Get list of available databases"""
    databases = []
    
    for db_id, db_config in DATABASES.items():
        db_path = Path(db_config['path'])
        exists = db_path.exists()
        size_mb = None
        table_count = None
        
        if exists:
            size_mb = round(db_path.stat().st_size / (1024 * 1024), 2)
            try:
                db_manager = DatabaseManager(db_path=db_path)
                schema = db_manager.get_schema()
                table_count = len(schema)
            except Exception as e:
                logger.error(f"Error getting schema for {db_id}: {e}")
        
        databases.append(DatabaseInfo(
            id=db_id,
            name=db_config['name'],
            path=db_config['path'],
            exists=exists,
            size_mb=size_mb,
            table_count=table_count
        ))
    
    return databases


@router.get("/databases/{database_id}/schema", response_model=SchemaInfo)
async def get_database_schema(database_id: str):
    """Get schema information for a specific database"""
    if database_id not in DATABASES:
        raise HTTPException(status_code=404, detail="Database not found")
    
    db_config = DATABASES[database_id]
    db_path = Path(db_config['path'])
    
    if not db_path.exists():
        raise HTTPException(status_code=404, detail="Database file not found")
    
    try:
        db_manager = DatabaseManager(db_path=db_path)
        schema_list = db_manager.get_schema()
        
        return SchemaInfo(
            tables=schema_list,
            table_count=len(schema_list)
        )
    except Exception as e:
        logger.error(f"Error getting schema: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/databases/{database_id}/examples", response_model=List[ExampleQuery])
async def get_example_queries(database_id: str):
    """Get example queries for a specific database"""
    if database_id not in DATABASES:
        raise HTTPException(status_code=404, detail="Database not found")
    
    return EXAMPLE_QUERIES.get(database_id, [])


@router.post("/ask", response_model=AskResponse)
async def ask_query(request: AskRequest):
    """
    Execute a natural language query with AI-generated answer
    Modern endpoint with LLM-powered natural language summaries
    
    Supports both single-query and multi-query execution:
    - Simple questions → Single SQL query
    - Comparison questions → Multi-query plan with dependencies
    
    Flow:
    1. Detect if multi-query is needed
    2. Generate SQL (single) or QueryPlan (multi)
    3. Execute query/plan against database
    4. Summarize results with LLM
    """
    logger.info(f"Ask request: {request.question} on {request.company_id}")
    
    if request.company_id not in DATABASES:
        raise HTTPException(status_code=400, detail=f"Invalid company_id: {request.company_id}")
    
    db_config = DATABASES[request.company_id]
    db_path = db_config['path']
    
    if not Path(db_path).exists():
        raise HTTPException(
            status_code=404,
            detail=f"Database not found: {db_path}. Run data generation first."
        )
    
    try:
        engine = QueryEngine(db_path=db_path)
        
        # Check if this is an analytical question (insights, recommendations, strategy)
        is_analytical = engine.analyst.is_analytical_question(request.question)
        
        if is_analytical:
            # Analytical path: Use business analyst for strategic insights
            logger.info("Using analytical path (business insights)")
            
            analysis_result = engine.analyst.analyze(request.question)
            
            logger.info(f"Analysis result keys: {list(analysis_result.keys())}")
            logger.info(f"Has query_data: {'query_data' in analysis_result}")
            
            if not analysis_result.get('success', True):
                raise HTTPException(
                    status_code=500,
                    detail=analysis_result.get('error', 'Analysis failed')
                )
            
            # Extract query data for display (SQL plan and results)
            query_data = analysis_result.get('query_data', {})
            logger.info(f"Query data keys: {list(query_data.keys())}")
            logger.info(f"Number of queries in query_data: {len(query_data)}")
            
            all_sqls = []
            combined_results = []
            all_charts = []  # Collect charts from all queries
            queries_succeeded = 0
            queries_failed = 0
            
            for query_id, query_info in query_data.items():
                logger.info(f"Processing query: {query_id}")
                sql = query_info.get('sql', '')
                results = query_info.get('results', [])
                error = query_info.get('error')
                description = query_info.get('description', query_id)
                
                if sql:
                    # Add SQL with comment header and status
                    status = "❌ FAILED" if error else f"✓ {len(results) if isinstance(results, list) else 0} rows"
                    all_sqls.append(f"-- Query: {description}\n-- Status: {status}\n{sql}")
                
                # Track success/failure
                if error:
                    queries_failed += 1
                else:
                    queries_succeeded += 1
                    # Only include successful queries with data
                    if results and isinstance(results, list) and len(results) > 0:
                        combined_results.extend(results)
                        
                        # Generate chart for this query if it has visualizable data
                        if len(results) > 1:  # Need at least 2 rows for meaningful chart
                            # Convert dict results to column/row format for chart detection
                            result_columns = list(results[0].keys())
                            result_rows = [[row.get(col) for col in result_columns] for row in results]
                            
                            chart_configs = detect_charts_from_results(
                                columns=result_columns,
                                rows=result_rows,
                                question=description,  # Use query description as context
                                currency_symbol=db_config.get('currency_symbol')
                            )
                            
                            if chart_configs:
                                for chart_config in chart_configs:
                                    # Add query context to chart title
                                    chart_config['title'] = f"{description}"
                                    chart_config['id'] = f"chart_{query_id}"
                                    all_charts.append(ChartConfig(**chart_config))
                                    logger.info(f"Generated chart for query '{query_id}': {chart_config['type']}")
            
            # Combine SQLs for display
            combined_sql = "\n\n".join(all_sqls) if all_sqls else None
            
            # Format results for table display
            columns = []
            rows = []
            if combined_results:
                # Get columns from first result
                columns = list(combined_results[0].keys())
                rows = [[row.get(col) for col in columns] for row in combined_results[:100]]  # Limit to 100 rows
            
            return AskResponse(
                answer_text=analysis_result['analysis_text'],
                sql=combined_sql,
                columns=columns if columns else None,
                rows=rows if rows else None,
                charts=all_charts if all_charts else None,  # Include all charts
                analysis=BusinessAnalysis(**analysis_result),
                query_type="analytical",
                meta={
                    'exploratory_queries': len(query_data),
                    'queries_succeeded': queries_succeeded,
                    'queries_failed': queries_failed,
                    'data_points_analyzed': len(analysis_result.get('data_points', [])),
                    'insights_count': len(analysis_result.get('insights', [])),
                    'recommendations_count': len(analysis_result.get('recommendations', [])),
                    'charts_generated': len(all_charts),
                    'row_count': len(rows) if rows else 0
                }
            )
        
        # Detect if multi-query is needed
        needs_multi_query = engine.sql_generator.needs_multi_query(request.question)
        logger.info(f"Multi-query needed: {needs_multi_query}")
        
        query_plan_model = None
        
        if needs_multi_query:
            # Multi-query path
            logger.info("Using multi-query execution path")
            
            # 1) Generate query plan with AI
            gen_start = time.time()
            query_plan = engine.sql_generator.generate_query_plan(request.question)
            gen_ms = (time.time() - gen_start) * 1000.0
            
            # 2) Execute plan
            exec_start = time.time()
            executed_plan = engine.execute_plan(query_plan)
            exec_ms = (time.time() - exec_start) * 1000.0
            
            # Get final results
            final_results = executed_plan.get_final_results()
            
            if final_results is None:
                raise HTTPException(
                    status_code=500,
                    detail="Multi-query plan execution failed to produce results"
                )
            
            columns = final_results.get('columns', [])
            rows = final_results.get('rows', [])
            
            # Get SQL from final query for display
            final_query = executed_plan.get_query(executed_plan.final_query_id)
            sql = final_query.sql if final_query else ""
            
            # Convert QueryPlan to API model
            query_plan_model = QueryPlanModel(
                queries=[
                    QueryStepModel(
                        id=q.id,
                        description=q.description,
                        sql=q.sql,
                        depends_on=q.depends_on,
                        status=q.status.value,
                        row_count=q.row_count,
                        execution_time_ms=q.execution_time_ms,
                        error=q.error,
                        results=q.results  # Include intermediate results
                    ) for q in executed_plan.queries
                ],
                final_query_id=executed_plan.final_query_id,
                question=executed_plan.question,
                total_execution_time_ms=executed_plan.total_execution_time_ms,
                is_complete=executed_plan.is_complete(),
                has_errors=executed_plan.has_errors()
            )
            
        else:
            # Single-query path (original logic)
            logger.info("Using single-query execution path")
            
            # 1) Generate SQL from natural language
            gen_start = time.time()
            sql = engine.generate_sql(request.question)
            gen_ms = (time.time() - gen_start) * 1000.0
            
            # 2) Execute SQL
            exec_start = time.time()
            result = engine.execute_query(sql)
            exec_ms = (time.time() - exec_start) * 1000.0
            
            if not result['success']:
                raise HTTPException(
                    status_code=500,
                    detail=result.get('error', 'Query execution failed')
                )
            
            # Transform results to columns/rows format
            results = result.get('results', [])
            columns = []
            rows = []
            
            if results and len(results) > 0:
                columns = list(results[0].keys())
                rows = [[row.get(col) for col in columns] for row in results]
        
        # 3) Summarize results with intelligent LLM summarizer
        db_config = DATABASES.get(request.company_id, {})
        currency_symbol = db_config.get('currency_symbol', '$')
        
        answer_text = summarize_result(
            question=request.question,
            columns=columns,
            rows=rows,
            company_id=request.company_id,
            section_ids=request.section_ids,
            exec_ms=exec_ms,
            currency_symbol=currency_symbol
        )
        
        # 4) Detect charts from results (AI-powered)
        chart_configs = detect_charts_from_results(
            columns=columns,
            rows=rows,
            question=request.question,
            use_ai=True,
            currency_symbol=currency_symbol
        )
        charts = [ChartConfig(**config) for config in chart_configs] if chart_configs else None
        
        # 5) Detect trends from results
        trend_configs = detect_trends_from_results(columns, rows)
        trends = [TrendInsight(**config) for config in trend_configs] if trend_configs else None
        
        return AskResponse(
            answer_text=answer_text,
            sql=sql,
            columns=columns,
            rows=rows,
            charts=charts,
            trends=trends,
            query_type="data",
            query_plan=query_plan_model,
            timings={
                'genMs': gen_ms,
                'execMs': exec_ms
            },
            meta={
                'row_count': len(rows),
                'multi_query': needs_multi_query,
                'query_count': len(query_plan_model.queries) if query_plan_model else 1
            }
        )
    
    except HTTPException:
        raise
    except QueryError as e:
        # Domain mismatch or schema validation error - user-friendly 400
        logger.warning(f"Query validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ask query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """
    Execute natural language query (legacy endpoint)
    Returns raw results without AI summary
    """
    logger.info(f"Query request: {request.question} on {request.database}")
    
    if request.database not in DATABASES:
        raise HTTPException(status_code=400, detail=f"Invalid database: {request.database}")
    
    db_config = DATABASES[request.database]
    db_path = db_config['path']
    
    if not Path(db_path).exists():
        raise HTTPException(
            status_code=404,
            detail=f"Database not found: {db_path}. Run data generation first."
        )
    
    try:
        engine = QueryEngine(db_path=db_path)
        result = engine.ask(request.question)
        
        if not result['success']:
            return QueryResponse(
                success=False,
                error=result.get('error', 'Unknown error'),
                sql=result.get('sql', ''),
                columns=[],
                rows=[],
                row_count=0,
                execution_time=0
            )
        
        # Transform dict results to lists
        results = result.get('results', [])
        columns = list(results[0].keys()) if results else []
        rows = [[row.get(col) for col in columns] for row in results] if results else []
        
        # Detect charts from results (AI-powered)
        chart_configs = detect_charts_from_results(
            columns=columns, 
            rows=rows,
            question=request.question,
            use_ai=True
        )
        charts = [ChartConfig(**config) for config in chart_configs] if chart_configs else None
        
        # Detect trends from results
        trend_configs = detect_trends_from_results(columns, rows)
        trends = [TrendInsight(**config) for config in trend_configs] if trend_configs else None
        
        return QueryResponse(
            success=True,
            sql=result.get('sql', ''),
            columns=columns,
            rows=rows,
            row_count=result.get('row_count', 0),
            execution_time=result.get('execution_time', 0),
            charts=charts,
            trends=trends
        )
    
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        return QueryResponse(
            success=False,
            error=str(e),
            sql='',
            columns=[],
            rows=[],
            row_count=0,
            execution_time=0
        )


@router.get("/stats")
async def get_stats():
    """Get system statistics"""
    stats = {
        "total_queries": 0,
        "total_databases": len(DATABASES),
        "databases": {}
    }
    
    for db_id in DATABASES.keys():
        stats["databases"][db_id] = {
            "queries": 0,
            "avg_time": 0
        }
    
    return stats


@router.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload Excel/CSV files and automatically detect schema
    
    Args:
        files: List of Excel/CSV files to upload
        
    Returns:
        UploadResponse with detected schema and database info
        
    Process:
        1. Save uploaded files to temp directory
        2. Detect schema using SchemaDetector
        3. Convert Excel → SQLite database
        4. Store in user_uploads directory
        5. Return schema + database ID
    """
    try:
        # Generate unique upload ID
        upload_id = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # Create directories
        upload_dir = Config.DATA_DIR / 'user_uploads' / upload_id
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        temp_dir = upload_dir / 'temp'
        temp_dir.mkdir(exist_ok=True)
        
        # Save uploaded files
        saved_files = []
        for file in files:
            if not file.filename:
                continue
                
            # Validate file extension
            file_ext = Path(file.filename).suffix.lower()
            if file_ext not in ['.xlsx', '.xls', '.csv']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid file type: {file.filename}. Only .xlsx, .xls, .csv allowed"
                )
            
            # Save file
            file_path = temp_dir / file.filename
            with file_path.open('wb') as f:
                shutil.copyfileobj(file.file, f)
            
            saved_files.append(str(file_path))
            logger.info(f"Saved uploaded file: {file.filename}")
        
        if not saved_files:
            raise HTTPException(
                status_code=400,
                detail="No valid files uploaded"
            )
        
        # Detect schema using SchemaDetector
        logger.info(f"Analyzing schema for {len(saved_files)} file(s)...")
        detector = SchemaDetector()
        detector.analyze_directory(str(temp_dir))
        
        schema_dict = detector.to_dict()
        table_count = len(detector.tables)
        total_rows = sum(table.row_count for table in detector.tables.values())
        relationship_count = len(detector.relationships) if hasattr(detector, 'relationships') else 0
        
        logger.info(f"✅ Detected {table_count} tables, {total_rows} rows, {relationship_count} relationships")
        
        # Convert Excel files to SQLite database
        db_name = f"{upload_id}.db"
        db_path = upload_dir / db_name
        
        logger.info(f"Creating SQLite database: {db_path}")
        excel_to_sql(
            excel_dir=str(temp_dir),
            db_name=str(db_path)
        )
        
        # Add to DATABASES registry (in-memory, not persistent)
        DATABASES[upload_id] = {
            'name': f"Upload {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            'path': str(db_path),
            'description': f'{table_count} tables uploaded by user',
            'uploaded': True,
            'upload_date': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Upload complete: {upload_id}")
        
        return UploadResponse(
            upload_id=upload_id,
            database_name=DATABASES[upload_id]['name'],
            database_path=str(db_path),
            detected_schema=schema_dict,
            table_count=table_count,
            total_rows=total_rows,
            relationships=relationship_count,
            message=f"Successfully uploaded {len(saved_files)} file(s) and created database"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


@router.get("/uploads", response_model=List[UploadedDatabase])
async def list_uploads():
    """List all uploaded databases"""
    uploads = []
    
    for db_id, db_info in DATABASES.items():
        if db_info.get('uploaded'):
            db_path = Path(db_info['path'])
            size_mb = db_path.stat().st_size / (1024 * 1024) if db_path.exists() else 0
            
            # Get table count from database
            try:
                db_manager = DatabaseManager(str(db_path))
                schema = db_manager.get_schema()
                table_count = len(schema)
                
                # Count total rows
                total_rows = 0
                for table in schema:
                    result = db_manager.execute_query(f"SELECT COUNT(*) FROM {table['name']}")
                    total_rows += result['rows'][0][0] if result['rows'] else 0
            except:
                table_count = db_info.get('table_count', 0)
                total_rows = 0
            
            uploads.append(UploadedDatabase(
                id=db_id,
                name=db_info['name'],
                upload_date=db_info.get('upload_date', ''),
                table_count=table_count,
                total_rows=total_rows,
                size_mb=round(size_mb, 2)
            ))
    
    return uploads


@router.delete("/uploads/{upload_id}")
async def delete_upload(upload_id: str):
    """Delete an uploaded database"""
    if upload_id not in DATABASES:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    if not DATABASES[upload_id].get('uploaded'):
        raise HTTPException(status_code=400, detail="Cannot delete built-in database")
    
    try:
        # Delete files
        upload_dir = Config.DATA_DIR / 'user_uploads' / upload_id
        if upload_dir.exists():
            shutil.rmtree(upload_dir)
        
        # Remove from registry
        del DATABASES[upload_id]
        
        logger.info(f"Deleted upload: {upload_id}")
        return {"message": "Upload deleted successfully"}
        
    except Exception as e:
        logger.error(f"Delete failed: {e}")
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
