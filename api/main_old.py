"""
FastAPI Backend for Multi-Database Query System
Modern REST API with CORS support for frontend integration

Refactored Structure:
- api/main.py: App initialization and middleware (this file)
- api/models.py: Pydantic request/response models
- api/routes.py: All endpoint handlers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.routes import router
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Database Query API",
    description="AI-powered natural language database queries",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class AskRequest(BaseModel):
    """Request model for natural language queries"""
    question: str
    company_id: str  # 'electronics' or 'airline'
    section_ids: List[str] = []  # subset of schema sections (optional)

class AskResponse(BaseModel):
    """Response model with natural language answer"""
    answer_text: str  # 💡 Natural language summary of results
    sql: str
    columns: List[str]
    rows: List[List[Any]]
    timings: Optional[Dict[str, float]] = None
    meta: Optional[Dict[str, Any]] = None  # e.g., row_count, truncation flags

# Legacy models (deprecated - use AskRequest/AskResponse)
class QueryRequest(BaseModel):
    question: str
    database: str  # 'electronics' or 'airline'

class QueryResponse(BaseModel):
    success: bool
    sql: Optional[str] = None
    columns: Optional[List[str]] = None
    rows: Optional[List[List[Any]]] = None
    row_count: Optional[int] = None
    execution_time: Optional[float] = None
    error: Optional[str] = None

class DatabaseInfo(BaseModel):
    id: str
    name: str
    path: str
    exists: bool
    size_mb: Optional[float] = None
    table_count: Optional[int] = None

class SchemaInfo(BaseModel):
    tables: List[Dict[str, Any]]
    table_count: int

class ExampleQuery(BaseModel):
    id: int
    title: str
    question: str
    category: str
    complexity: str  # 'simple', 'medium', 'complex'

# Database configuration
DATABASES = {
    'electronics': {
        'name': 'Electronics Company',
        'path': str(Config.DATABASE_DIR / 'electronics_company.db'),
        'description': '12 tables covering HR, Sales, Finance, Inventory, Products, Customers, and more'
    },
    'airline': {
        'name': 'Airline Company',
        'path': str(Config.DATABASE_DIR / 'airline_company.db'),
        'description': '16 tables covering Aircraft, Pilots, Flights, Passengers, Revenue, and more'
    }
}

# Helper Functions
def _generate_answer_text(
    question: str,
    sql: str,
    columns: List[str],
    rows: List[List[Any]],
    row_count: int
) -> str:
    """
    Generate a natural language answer from query results
    
    Args:
        question: Original user question
        sql: Generated SQL query
        columns: Column names from results
        rows: Data rows from results
        row_count: Total number of rows
    
    Returns:
        Natural language answer string
    """
    if row_count == 0:
        return "No results found for your query."
    
    # Handle single-value results (e.g., COUNT, SUM, AVG)
    if row_count == 1 and len(columns) == 1:
        value = rows[0][0]
        col_name = columns[0]
        
        # Format the answer based on column name
        if 'COUNT' in col_name.upper():
            return f"There are {value:,} records matching your query."
        elif 'SUM' in col_name.upper() or 'TOTAL' in col_name.upper():
            if isinstance(value, (int, float)):
                return f"The total is ${value:,.2f}." if 'price' in col_name.lower() or 'cost' in col_name.lower() or 'salary' in col_name.lower() else f"The total is {value:,}."
            return f"The total is {value}."
        elif 'AVG' in col_name.upper() or 'AVERAGE' in col_name.upper():
            if isinstance(value, (int, float)):
                return f"The average is {value:,.2f}."
            return f"The average is {value}."
        elif 'MAX' in col_name.upper() or 'MIN' in col_name.upper():
            return f"The value is {value}."
        else:
            return f"The result is: {value}"
    
    # Handle multiple rows
    if row_count <= 5:
        return f"Found {row_count} result{'s' if row_count != 1 else ''} with {len(columns)} column{'s' if len(columns) != 1 else ''}."
    elif row_count <= 100:
        return f"Found {row_count} results. Showing all records with {len(columns)} columns."
    else:
        return f"Found {row_count} results across {len(columns)} columns. Large dataset returned."

# Example queries for each database
EXAMPLE_QUERIES = {
    'electronics': [
        {
            'id': 1,
            'title': 'Total Sales',
            'question': 'What is the total sales amount?',
            'category': 'Finance',
            'complexity': 'simple'
        },
        {
            'id': 2,
            'title': 'Top Customers',
            'question': 'Show me the top 10 customers by total purchase amount',
            'category': 'Sales',
            'complexity': 'medium'
        },
        {
            'id': 3,
            'title': 'Low Inventory',
            'question': 'Which products have inventory below 50 units?',
            'category': 'Inventory',
            'complexity': 'simple'
        },
        {
            'id': 4,
            'title': 'Sales Performance',
            'question': 'Which sales employees exceeded their targets and by how much?',
            'category': 'HR',
            'complexity': 'complex'
        },
        {
            'id': 5,
            'title': 'Product Categories',
            'question': 'Show me sales by product category',
            'category': 'Products',
            'complexity': 'medium'
        }
    ],
    'airline': [
        {
            'id': 1,
            'title': 'Fleet Size',
            'question': 'How many aircraft are in the fleet?',
            'category': 'Fleet',
            'complexity': 'simple'
        },
        {
            'id': 2,
            'title': 'Top Pilots',
            'question': 'Show me the top 10 pilots with the most flight hours',
            'category': 'Personnel',
            'complexity': 'medium'
        },
        {
            'id': 3,
            'title': 'Flight Details',
            'question': 'Show me flights with their aircraft type and passenger count',
            'category': 'Operations',
            'complexity': 'medium'
        },
        {
            'id': 4,
            'title': 'Revenue Analysis',
            'question': 'What is the total revenue by payment method?',
            'category': 'Finance',
            'complexity': 'medium'
        },
        {
            'id': 5,
            'title': 'Fuel Efficiency',
            'question': 'Show me the average fuel cost per flight for each aircraft type',
            'category': 'Operations',
            'complexity': 'complex'
        }
    ]
}

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Multi-Database Query API",
        "version": "1.0.0",
        "status": "online",
        "databases": list(DATABASES.keys())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2025-10-31"}

@app.get("/databases", response_model=List[DatabaseInfo])
async def get_databases():
    """Get list of available databases with metadata"""
    databases = []
    
    for db_id, db_config in DATABASES.items():
        db_path = Path(db_config['path'])
        exists = db_path.exists()
        
        size_mb = None
        table_count = None
        
        if exists:
            # Get file size
            size_mb = round(db_path.stat().st_size / (1024 * 1024), 2)
            
            # Get table count
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

@app.get("/databases/{database_id}/schema", response_model=SchemaInfo)
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
        schema = db_manager.get_schema()
        
        return SchemaInfo(
            tables=schema,
            table_count=len(schema)
        )
    except Exception as e:
        logger.error(f"Error getting schema: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/databases/{database_id}/examples", response_model=List[ExampleQuery])
async def get_example_queries(database_id: str):
    """Get example queries for a specific database"""
    if database_id not in DATABASES:
        raise HTTPException(status_code=404, detail="Database not found")
    
    return EXAMPLE_QUERIES.get(database_id, [])

@app.post("/ask", response_model=AskResponse)
async def ask_query(request: AskRequest):
    """
    Execute a natural language query with AI-generated answer
    
    This is the modern endpoint that returns a natural language answer
    along with the SQL query and results.
    """
    logger.info(f"Ask request: {request.question} on {request.company_id}")
    
    # Validate database (company_id)
    if request.company_id not in DATABASES:
        raise HTTPException(status_code=400, detail=f"Invalid company_id: {request.company_id}")
    
    db_config = DATABASES[request.company_id]
    db_path = db_config['path']
    
    # Check if database exists
    if not Path(db_path).exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Database not found: {db_path}. Run data generation first."
        )
    
    try:
        # Initialize query engine with selected database
        engine = QueryEngine(db_path=db_path)
        
        # Execute query
        import time
        start_time = time.time()
        result = engine.ask(request.question)
        total_time = time.time() - start_time
        
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
            # Extract column names from first result dict
            columns = list(results[0].keys())
            # Convert list of dicts to list of lists
            rows = [[row.get(col) for col in columns] for row in results]
        
        # Generate natural language answer using LLM
        from src.core.query_engine import _summarize_result_with_llm
        
        answer_text = _summarize_result_with_llm(
            question=request.question,
            columns=columns,
            rows=rows,
            company_id=request.company_id,
            section_ids=request.section_ids,
            exec_ms=result.get('execution_time', 0) * 1000  # Convert to milliseconds
        )
        
        return AskResponse(
            answer_text=answer_text,
            sql=result.get('sql', ''),
            columns=columns,
            rows=rows,
            timings={
                'total': round(total_time, 3),
                'execution': round(result.get('execution_time', 0), 3)
            },
            meta={
                'row_count': result.get('row_count', 0),
                'truncated': result.get('truncated', False),
                'timestamp': result.get('timestamp', '')
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ask query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """Execute a natural language query on the selected database"""
    logger.info(f"Query request: {request.question} on {request.database}")
    
    # Validate database
    if request.database not in DATABASES:
        raise HTTPException(status_code=400, detail="Invalid database selection")
    
    db_config = DATABASES[request.database]
    db_path = db_config['path']
    
    # Check if database exists
    if not Path(db_path).exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Database not found: {db_path}. Run data generation first."
        )
    
    try:
        # Initialize query engine with selected database
        engine = QueryEngine(db_path=db_path)
        
        # Execute query
        result = engine.ask(request.question)
        
        if result['success']:
            # Transform results to columns/rows format
            results = result.get('results', [])
            columns = None
            rows = None
            
            if results and len(results) > 0:
                # Extract column names from first result dict
                columns = list(results[0].keys())
                # Convert list of dicts to list of lists
                rows = [[row.get(col) for col in columns] for row in results]
            
            return QueryResponse(
                success=True,
                sql=result.get('sql'),
                columns=columns,
                rows=rows,
                row_count=result.get('row_count'),
                execution_time=result.get('execution_time')
            )
        else:
            return QueryResponse(
                success=False,
                error=result.get('error', 'Unknown error occurred')
            )
    
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        return QueryResponse(
            success=False,
            error=str(e)
        )

@app.get("/stats")
async def get_stats():
    """Get overall system statistics"""
    stats = {
        'total_databases': len(DATABASES),
        'databases': {}
    }
    
    for db_id, db_config in DATABASES.items():
        db_path = Path(db_config['path'])
        
        if db_path.exists():
            try:
                db_manager = DatabaseManager(db_path=db_path)
                schema = db_manager.get_schema()
                
                # Count total rows across all tables
                total_rows = 0
                with db_manager.get_connection() as conn:
                    for table in schema:
                        cursor = conn.execute(f"SELECT COUNT(*) FROM {table['name']}")
                        total_rows += cursor.fetchone()[0]
                
                stats['databases'][db_id] = {
                    'name': db_config['name'],
                    'tables': len(schema),
                    'total_rows': total_rows,
                    'size_mb': round(db_path.stat().st_size / (1024 * 1024), 2)
                }
            except Exception as e:
                logger.error(f"Error getting stats for {db_id}: {e}")
                stats['databases'][db_id] = {'error': str(e)}
    
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
