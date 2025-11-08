# System Architecture

## Overview

Multi-Database Query System is an AI-powered natural language database query platform supporting multiple company databases with a modern web interface.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                           │
│                                                              │
│  ┌────────────────┐              ┌────────────────┐        │
│  │   Web Browser  │              │   CLI Terminal │        │
│  │  (localhost:   │              │   (Python REPL)│        │
│  │     3000)      │              │                │        │
│  └────────┬───────┘              └────────┬───────┘        │
└───────────┼──────────────────────────────┼─────────────────┘
            │                              │
            │ HTTP/JSON                    │ Direct
            │                              │
┌───────────▼──────────────────────────────▼─────────────────┐
│                   PRESENTATION LAYER                        │
│                                                              │
│  ┌──────────────────────┐      ┌──────────────────────┐   │
│  │  Frontend (React)    │      │   CLI Interface      │   │
│  │  - index.html        │      │   - query_multi.py   │   │
│  │  - Tailwind CSS      │      │   - query.py         │   │
│  │  - State Management  │      │                      │   │
│  └──────────┬───────────┘      └──────────┬───────────┘   │
└─────────────┼──────────────────────────────┼───────────────┘
              │                              │
              │ REST API                     │ Import
              │                              │
┌─────────────▼──────────────────────────────▼───────────────┐
│                     API LAYER                               │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          FastAPI Application (api/main.py)          │   │
│  │                                                      │   │
│  │  Routes:                                            │   │
│  │  • GET  /                - Root endpoint           │   │
│  │  • GET  /health          - Health check            │   │
│  │  • GET  /databases       - List databases          │   │
│  │  • GET  /databases/{id}  - Get database info       │   │
│  │  • POST /query           - Execute NL query        │   │
│  │  • GET  /stats           - System statistics       │   │
│  │  • GET  /docs            - OpenAPI docs            │   │
│  │                                                      │   │
│  │  Middleware:                                        │   │
│  │  • CORS (localhost:3000)                           │   │
│  │  • Error handling                                   │   │
│  │  • Request logging                                  │   │
│  └──────────────────────┬──────────────────────────────┘   │
└─────────────────────────┼──────────────────────────────────┘
                          │
                          │ Internal API
                          │
┌─────────────────────────▼──────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Query Engine (src/core/query_engine.py)       │  │
│  │                                                        │  │
│  │  Responsibilities:                                    │  │
│  │  1. Natural language → SQL conversion (via Gemini)   │  │
│  │  2. SQL validation & sanitization                    │  │
│  │  3. Query execution orchestration                    │  │
│  │  4. Result formatting                                 │  │
│  │  5. Error handling & logging                         │  │
│  │                                                        │  │
│  │  Methods:                                             │  │
│  │  • query(question, db_path) → Dict                   │  │
│  │  • _generate_sql(question) → str                     │  │
│  │  • _clean_sql(sql) → str                             │  │
│  │  • validate_query(sql) → bool                        │  │
│  └──────────────┬───────────────────┬───────────────────┘  │
│                 │                   │                       │
│                 │                   │                       │
│  ┌──────────────▼─────────┐  ┌────▼──────────────────┐    │
│  │  DatabaseManager       │  │  External AI Service  │    │
│  │  (src/core/           │  │  (Google Gemini)      │    │
│  │   database.py)         │  │                       │    │
│  │                        │  │  Model:               │    │
│  │  Responsibilities:     │  │  gemini-2.0-flash-exp │    │
│  │  • Connection mgmt     │  │                       │    │
│  │  • Query execution     │  │  Rate Limit:          │    │
│  │  • Schema inspection   │  │  10 req/min (free)    │    │
│  │  • Transaction handling│  └───────────────────────┘    │
│  │                        │                               │
│  │  Methods:              │                               │
│  │  • execute_query(sql)  │                               │
│  │  • get_tables()        │                               │
│  │  • get_schema()        │                               │
│  │  • get_table_info()    │                               │
│  └────────────┬───────────┘                               │
└───────────────┼───────────────────────────────────────────┘
                │
                │ SQLite Connections
                │
┌───────────────▼───────────────────────────────────────────┐
│                     DATA LAYER                             │
│                                                             │
│  ┌──────────────────────┐      ┌──────────────────────┐  │
│  │  Electronics DB      │      │   Airline DB         │  │
│  │  (480 KB)            │      │   (1.37 MB)          │  │
│  │                      │      │                      │  │
│  │  Tables (12):        │      │  Tables (16):        │  │
│  │  • employees         │      │  • aircraft          │  │
│  │  • products          │      │  • pilots            │  │
│  │  • customers         │      │  • cabin_crew        │  │
│  │  • sales_orders      │      │  • flights           │  │
│  │  • inventory         │      │  • passengers        │  │
│  │  • suppliers         │      │  • maintenance       │  │
│  │  • financial_trans   │      │  • airports          │  │
│  │  • payroll           │      │  • revenue           │  │
│  │  • customer_service  │      │  • fuel_consumption  │  │
│  │  • marketing         │      │  • ground_staff      │  │
│  │  • shipments         │      │  • baggage           │  │
│  │  • warranties        │      │  • incidents         │  │
│  │                      │      │  • loyalty_program   │  │
│  │                      │      │  • routes            │  │
│  │                      │      │  • catering          │  │
│  │                      │      │  • weather_data      │  │
│  └──────────────────────┘      └──────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Presentation Layer

#### Frontend (React + Tailwind)
- **Technology**: React via CDN, Tailwind CSS
- **Port**: 3000 (HTTP server)
- **State Management**: React hooks (useState, useEffect)
- **Key Features**:
  - Database selection dropdown
  - Natural language query input
  - Real-time query results table
  - Example queries
  - System statistics
  - Error handling with user-friendly messages

#### CLI Interface
- **Files**: `query_multi.py`, `query.py`
- **Usage**: Direct Python REPL interaction
- **Features**:
  - Interactive database selection
  - Command-line query execution
  - Formatted table output

### 2. API Layer

#### FastAPI Application
- **File**: `api/main.py`
- **Port**: 8000
- **Auto Docs**: http://localhost:8000/docs

**Endpoints**:

```python
# Root
GET / 
→ {"message": "Multi-Database Query API", "databases": 2}

# Health Check
GET /health
→ {"status": "healthy"}

# List Databases
GET /databases
→ [
    {
        "id": "electronics",
        "name": "Electronics Company",
        "path": "/path/to/db",
        "exists": true,
        "size_mb": 0.47,
        "table_count": 12
    },
    {...}
]

# Get Database Schema
GET /databases/{database_id}
→ {
    "tables": [...],
    "total_rows": 3520
}

# Execute Query
POST /query
Body: {"question": "How many employees?", "database": "electronics"}
→ {
    "success": true,
    "sql": "SELECT COUNT(*) FROM employees",
    "columns": ["count(*)"],
    "rows": [[150]],
    "row_count": 1,
    "execution_time": 0.002,
    "error": null
}

# Get Statistics
GET /stats
→ {
    "total_databases": 2,
    "total_tables": 28,
    "total_rows": 7520
}
```

**CORS Configuration**:
```python
origins = [
    "http://localhost:3000",
    "file://"  # For local file access
]
```

### 3. Business Logic Layer

#### Query Engine
- **File**: `src/core/query_engine.py`
- **Purpose**: Natural language → SQL → Results

**Flow**:
```
1. Receive natural language question
2. Load database schema
3. Send to Google Gemini AI with schema context
4. Receive generated SQL
5. Clean and validate SQL
6. Execute via DatabaseManager
7. Format and return results
```

**Key Methods**:
```python
class QueryEngine:
    def query(question: str, db_path: str) -> Dict
    def _generate_sql(question: str) -> str
    def _clean_sql(sql: str) -> str
    def validate_query(sql: str) -> bool
```

#### Database Manager
- **File**: `src/core/database.py`
- **Purpose**: SQLite connection and query management

**Key Methods**:
```python
class DatabaseManager:
    def execute_query(sql: str) -> Dict
    def get_tables() -> List[str]
    def get_table_info(table: str) -> List[Dict]
    def get_schema() -> str
    def get_row_count(table: str) -> int
```

**Connection Pattern**:
```python
# Context manager for safe connections
with DatabaseManager(db_path) as db:
    result = db.execute_query(sql)
```

### 4. Data Layer

#### Database Structure

**Electronics Company** (`electronics_company.db`):
- Size: 480 KB
- Tables: 12
- Rows: ~3,520
- Focus: Retail operations

**Airline Company** (`airline_company.db`):
- Size: 1.37 MB
- Tables: 16  
- Rows: ~4,000
- Focus: Airline operations

**Schema Conventions**:
- Table names: `lowercase_snake_case`
- Column names: `lowercase_snake_case`
- Primary keys: `{table}_id` format
- Foreign keys: Reference parent table name

## Data Flow

### Query Execution Flow

```
User Input
    ↓
[Frontend] Submit question + database selection
    ↓ HTTP POST /query
[API Layer] Validate request
    ↓
[QueryEngine] Load schema from database
    ↓
[AI Service] Generate SQL from NL question + schema
    ↓ API Call (Google Gemini)
[AI Service] Return generated SQL
    ↓
[QueryEngine] Clean and validate SQL
    ↓
[DatabaseManager] Execute SQL query
    ↓ SQLite Connection
[Database] Return raw results
    ↓
[DatabaseManager] Format results
    ↓
[API Layer] JSON response
    ↓ HTTP 200 OK
[Frontend] Render results table
    ↓
User sees results
```

### Error Handling Flow

```
Error occurs at any layer
    ↓
Log error with context (logger)
    ↓
Transform to user-friendly message
    ↓
Set appropriate HTTP status code
    ↓
Return JSON error response:
{
    "success": false,
    "error": "User-friendly message",
    "sql": null,
    "rows": []
}
    ↓
Frontend displays error to user
```

## Technology Stack

### Backend
- **Python**: 3.10.1
- **Framework**: FastAPI 0.104+
- **Database**: SQLite 3
- **AI**: Google Gemini (gemini-2.0-flash-exp)
- **Data**: Pandas, Faker
- **Testing**: pytest, pytest-cov

### Frontend
- **Framework**: React 18 (CDN)
- **Styling**: Tailwind CSS
- **HTTP**: Fetch API
- **Server**: Python http.server

### DevOps
- **Build**: Make
- **Env**: python-dotenv
- **Logging**: Python logging module
- **Docs**: Markdown

## Deployment Architecture

### Development
```
├── Backend: localhost:8000 (FastAPI dev server)
├── Frontend: localhost:3000 (Python http.server)
├── Database: Local SQLite files
└── AI: Google Cloud API (free tier)
```

### Production Considerations
```
├── Backend: Uvicorn workers (4-8)
├── Frontend: Nginx static hosting
├── Database: Read replicas for scaling
├── AI: Paid tier with higher rate limits
├── Caching: Redis for query results
├── Monitoring: Prometheus + Grafana
└── Logging: ELK stack
```

## Security Model

### API Security
- **CORS**: Restricted origins
- **Input Validation**: Pydantic models
- **SQL Injection**: Parameterized queries only
- **Rate Limiting**: To be implemented
- **API Keys**: Environment variables only

### Data Security
- **Secrets**: `.env` file (gitignored)
- **Logging**: No sensitive data in logs
- **Database**: Local access only (dev)
- **AI Communication**: HTTPS only

## Performance Characteristics

### Response Times
- **Simple Query**: < 500ms
- **AI Query**: 1-2 seconds
- **Complex Join**: < 1 second
- **Database Load**: < 100ms

### Rate Limits
- **Google AI**: 10 requests/minute (free)
- **Retry Strategy**: Exponential backoff
- **Timeout**: 30 seconds max

### Caching Strategy
- **None currently** (to be implemented)
- **Future**: Redis for repeated queries
- **TTL**: 5 minutes for query results

## Scalability Considerations

### Current Limitations
- Single SQLite database (not concurrent)
- Synchronous API calls
- No query result caching
- In-memory state only

### Scale-Up Path
1. **Database**: PostgreSQL with connection pooling
2. **API**: Multiple Uvicorn workers
3. **Caching**: Redis for query results
4. **Queue**: Celery for async AI calls
5. **CDN**: Static asset delivery
6. **Load Balancer**: Nginx reverse proxy

## Monitoring & Logging

### Logging Levels
- **DEBUG**: SQL queries, AI prompts
- **INFO**: Request/response, query execution
- **WARNING**: Rate limits, slow queries
- **ERROR**: Failed queries, AI errors
- **CRITICAL**: System failures

### Log Locations
- **Application**: `logs/app.log`
- **API**: `logs/api.log`
- **Database**: `logs/db.log`

### Metrics to Track
- Query execution time
- AI API latency
- Error rates
- Cache hit ratios
- Database connection pool

## Design Patterns Used

### Patterns
- **Repository Pattern**: DatabaseManager
- **Factory Pattern**: Query generator
- **Singleton**: Logger configuration
- **Context Manager**: Database connections
- **Dependency Injection**: FastAPI dependencies

### SOLID Principles
- **S**ingle Responsibility: Each class has one job
- **O**pen/Closed: Extensible via inheritance
- **L**iskov Substitution: Database implementations swappable
- **I**nterface Segregation: Minimal interfaces
- **D**ependency Inversion: Depend on abstractions

## Future Enhancements

### Planned Features
1. **Query History**: Store and replay queries
2. **Favorites**: Save common queries
3. **Export**: CSV/Excel download
4. **Visualization**: Charts from query results
5. **Multi-user**: Authentication and sessions
6. **Real-time**: WebSocket for live updates
7. **Advanced AI**: Query suggestions, auto-complete

### Technical Debt
- Add comprehensive error recovery
- Implement query result caching
- Add rate limiting middleware
- Improve test coverage to 95%+
- Add performance benchmarks
- Implement CI/CD pipeline

---

## See Also

### Related Documentation
- **[INDEX.md](INDEX.md)** - Documentation navigation guide
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete REST API specification
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development environment setup and workflows
- **[TESTING_SUMMARY.md](TESTING_SUMMARY.md)** - Test coverage and results
- **[MAKE_COMMANDS.md](MAKE_COMMANDS.md)** - Build system commands
- **[../.github/copilot-instructions.md](../.github/copilot-instructions.md)** - Development standards

### Database Schemas
- **[electronics_schema.md](electronics_schema.md)** - Electronics company schema (12 tables)
- **[airline_schema.md](airline_schema.md)** - Airline company schema (16 tables)
- **[electronics_schema.sql](electronics_schema.sql)** - SQL DDL
- **[airline_schema.sql](airline_schema.sql)** - SQL DDL

### User Documentation
- **[../README.md](../README.md)** - Project overview and quick start

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-31  
**Methodology**: Context Engineering  
**Next Review**: When adding new databases or major features
