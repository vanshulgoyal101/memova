# API Reference

**Version**: 1.0.0  
**Base URL**: `http://localhost:8000`  
**Last Updated**: 2025-10-31

---

## Overview

The Multi-Database Query System exposes a REST API built with **FastAPI**. All endpoints return JSON responses and support CORS for frontend integration.

### Quick Links
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
   - [GET /](#get-)
   - [GET /health](#get-health)
   - [GET /databases](#get-databases)
   - [GET /databases/{database_id}/schema](#get-databasesdatabase_idschema)
   - [GET /databases/{database_id}/examples](#get-databasesdatabase_idexamples)
   - [POST /query](#post-query)
   - [GET /stats](#get-stats)
3. [Data Models](#data-models)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)

---

## Authentication

**Current Status**: No authentication required (development mode)

**Production Recommendations**:
- API key authentication (header-based)
- OAuth 2.0 / JWT tokens
- Rate limiting per user/API key

---

## Endpoints

### GET /

**Description**: API root endpoint with basic information

**Request**: None

**Response**: 200 OK
```json
{
  "name": "Multi-Database Query API",
  "version": "1.0.0",
  "status": "online",
  "databases": ["electronics", "airline"]
}
```

**Example**:
```bash
curl http://localhost:8000/
```

---

### GET /health

**Description**: Health check endpoint for monitoring

**Request**: None

**Response**: 200 OK
```json
{
  "status": "healthy",
  "timestamp": "2025-10-31"
}
```

**Use Cases**:
- Kubernetes liveness/readiness probes
- Load balancer health checks
- Monitoring systems

**Example**:
```bash
curl http://localhost:8000/health
```

---

### GET /databases

**Description**: Get list of available databases with metadata

**Request**: None

**Response**: 200 OK
```json
[
  {
    "id": "electronics",
    "name": "Electronics Company",
    "path": "/path/to/electronics_company.db",
    "exists": true,
    "size_mb": 0.48,
    "table_count": 12
  },
  {
    "id": "airline",
    "name": "Airline Company",
    "path": "/path/to/airline_company.db",
    "exists": true,
    "size_mb": 1.37,
    "table_count": 16
  }
]
```

**Response Fields**:
- `id` (string): Database identifier for queries
- `name` (string): Human-readable database name
- `path` (string): Absolute path to SQLite database file
- `exists` (boolean): Whether database file exists
- `size_mb` (float|null): Database file size in megabytes
- `table_count` (int|null): Number of tables in database

**Example**:
```bash
curl http://localhost:8000/databases
```

**Frontend Usage**:
```javascript
const response = await fetch('http://localhost:8000/databases');
const databases = await response.json();
console.log(databases);
```

---

### GET /databases/{database_id}/schema

**Description**: Get schema information (tables and columns) for a specific database

**Path Parameters**:
- `database_id` (string, required): Database identifier (`electronics` or `airline`)

**Response**: 200 OK
```json
{
  "tables": [
    {
      "name": "employees",
      "columns": [
        {
          "name": "employee_id",
          "type": "TEXT",
          "nullable": false,
          "primary_key": true
        },
        {
          "name": "first_name",
          "type": "TEXT",
          "nullable": false,
          "primary_key": false
        }
      ]
    }
  ],
  "table_count": 12
}
```

**Response Fields**:
- `tables` (array): List of table objects
  - `name` (string): Table name
  - `columns` (array): List of column objects
    - `name` (string): Column name
    - `type` (string): SQLite data type (TEXT, INTEGER, REAL, BLOB)
    - `nullable` (boolean): Whether column accepts NULL values
    - `primary_key` (boolean): Whether column is primary key
- `table_count` (int): Total number of tables

**Error Responses**:
- `404 Not Found`: Database ID not found or database file missing
- `500 Internal Server Error`: Database schema read error

**Example**:
```bash
curl http://localhost:8000/databases/electronics/schema
```

---

### GET /databases/{database_id}/examples

**Description**: Get example queries for a specific database

**Path Parameters**:
- `database_id` (string, required): Database identifier (`electronics` or `airline`)

**Response**: 200 OK
```json
[
  {
    "id": 1,
    "title": "Total Sales",
    "question": "What is the total sales amount?",
    "category": "Finance",
    "complexity": "simple"
  },
  {
    "id": 2,
    "title": "Top Customers",
    "question": "Show me the top 10 customers by total purchase amount",
    "category": "Sales",
    "complexity": "medium"
  }
]
```

**Response Fields**:
- `id` (int): Example query ID
- `title` (string): Short descriptive title
- `question` (string): Natural language query text
- `category` (string): Query category (Finance, Sales, HR, Operations, etc.)
- `complexity` (string): Query complexity level (`simple`, `medium`, `complex`)

**Complexity Levels**:
- **simple**: Single table, basic SELECT
- **medium**: JOIN, GROUP BY, or aggregation
- **complex**: Multiple JOINs, subqueries, advanced aggregation

**Error Responses**:
- `404 Not Found`: Database ID not found

**Example**:
```bash
curl http://localhost:8000/databases/airline/examples
```

---

### POST /query

**Description**: Execute a natural language query on the selected database using Google Gemini AI

**Request Body**:
```json
{
  "question": "What is the total sales amount?",
  "database": "electronics"
}
```

**Request Fields**:
- `question` (string, required): Natural language query
- `database` (string, required): Database ID (`electronics` or `airline`)

**Response**: 200 OK (Success)
```json
{
  "success": true,
  "sql": "SELECT SUM(total_amount) AS total_sales FROM sales_orders;",
  "columns": ["total_sales"],
  "rows": [[1234567.89]],
  "row_count": 1,
  "execution_time": 0.003,
  "error": null
}
```

**Response**: 200 OK (Failure)
```json
{
  "success": false,
  "sql": null,
  "columns": null,
  "rows": null,
  "row_count": null,
  "execution_time": null,
  "error": "Table 'invalid_table' not found in database"
}
```

**Response Fields**:
- `success` (boolean): Whether query executed successfully
- `sql` (string|null): Generated SQL query
- `columns` (array|null): Column names from result set
- `rows` (array|null): Result rows as 2D array
- `row_count` (int|null): Number of rows returned
- `execution_time` (float|null): SQL execution time in seconds
- `error` (string|null): Error message if `success: false`

**Error Responses**:
- `400 Bad Request`: Invalid database ID
- `404 Not Found`: Database file not found
- `429 Too Many Requests`: Google API rate limit exceeded (10 req/min)
- `500 Internal Server Error`: Query execution error

**Example**:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How many employees are in each department?",
    "database": "electronics"
  }'
```

**Frontend Usage**:
```javascript
const response = await fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'What is the total revenue?',
    database: 'electronics'
  })
});
const result = await response.json();

if (result.success) {
  console.log('SQL:', result.sql);
  console.log('Results:', result.rows);
} else {
  console.error('Error:', result.error);
}
```

**Rate Limiting**:
- Google Gemini API free tier: **10 requests/minute**
- Exceeded limit: Wait 60 seconds before retrying
- HTTP 429 response includes `Retry-After` header

---

### GET /stats

**Description**: Get overall system statistics (databases, tables, rows)

**Request**: None

**Response**: 200 OK
```json
{
  "total_databases": 2,
  "databases": {
    "electronics": {
      "name": "Electronics Company",
      "tables": 12,
      "total_rows": 3600,
      "size_mb": 0.48
    },
    "airline": {
      "name": "Airline Company",
      "tables": 16,
      "total_rows": 3920,
      "size_mb": 1.37
    }
  }
}
```

**Response Fields**:
- `total_databases` (int): Number of configured databases
- `databases` (object): Per-database statistics
  - `name` (string): Database display name
  - `tables` (int): Number of tables
  - `total_rows` (int): Total rows across all tables
  - `size_mb` (float): Database file size in MB

**Example**:
```bash
curl http://localhost:8000/stats
```

---

## Data Models

### QueryRequest
```typescript
{
  question: string;    // Natural language query
  database: string;    // Database ID ('electronics' | 'airline')
}
```

### QueryResponse
```typescript
{
  success: boolean;
  sql?: string;
  columns?: string[];
  rows?: any[][];
  row_count?: number;
  execution_time?: number;
  error?: string;
}
```

### DatabaseInfo
```typescript
{
  id: string;
  name: string;
  path: string;
  exists: boolean;
  size_mb?: number;
  table_count?: number;
}
```

### SchemaInfo
```typescript
{
  tables: {
    name: string;
    columns: {
      name: string;
      type: string;
      nullable: boolean;
      primary_key: boolean;
    }[];
  }[];
  table_count: number;
}
```

### ExampleQuery
```typescript
{
  id: number;
  title: string;
  question: string;
  category: string;
  complexity: 'simple' | 'medium' | 'complex';
}
```

---

## Error Handling

### Standard Error Response
```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes
- `200 OK`: Successful request
- `400 Bad Request`: Invalid input (e.g., unknown database ID)
- `404 Not Found`: Resource not found (e.g., database file missing)
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side error
- `503 Service Unavailable`: Dependency failure (e.g., Google API down)

### Error Examples

**Invalid Database**:
```json
{
  "detail": "Invalid database selection"
}
```

**Database Not Found**:
```json
{
  "detail": "Database not found: /path/to/db.db. Run data generation first."
}
```

**Query Execution Error**:
```json
{
  "success": false,
  "error": "no such table: invalid_table_name"
}
```

---

## Rate Limiting

### Google Gemini API Limits
- **Free Tier**: 10 requests per minute
- **Trigger**: POST /query endpoint
- **Response**: HTTP 429 with `Retry-After: 60` header
- **Recommendation**: Implement exponential backoff on client side

### Rate Limit Response
```json
{
  "detail": "Resource has been exhausted (e.g. check quota)."
}
```

### Best Practices
1. Cache query results on frontend
2. Debounce user input (wait 500ms before submitting)
3. Show "Please wait..." during query execution
4. Display rate limit errors clearly to users
5. Implement retry logic with exponential backoff

### Client-Side Example
```javascript
async function queryWithRetry(question, database, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, database })
      });
      
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After') || 60;
        console.log(`Rate limited. Retrying in ${retryAfter}s...`);
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
        continue;
      }
      
      return await response.json();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 2 ** i * 1000));
    }
  }
}
```

---

## CORS Configuration

### Allowed Origins
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)

### Production Setup
Update `api/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Production domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing the API

### Using cURL
```bash
# Get databases
curl http://localhost:8000/databases

# Get schema
curl http://localhost:8000/databases/electronics/schema

# Execute query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many employees?", "database": "electronics"}'

# Get stats
curl http://localhost:8000/stats
```

### Using Python
```python
import requests

# Get databases
response = requests.get('http://localhost:8000/databases')
print(response.json())

# Execute query
response = requests.post('http://localhost:8000/query', json={
    'question': 'What is the total revenue?',
    'database': 'electronics'
})
result = response.json()
print(result['sql'])
print(result['rows'])
```

### Using JavaScript (Fetch API)
```javascript
// Get databases
const databases = await fetch('http://localhost:8000/databases')
  .then(res => res.json());

// Execute query
const result = await fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'Show me top 10 customers',
    database: 'electronics'
  })
}).then(res => res.json());
```

---

## Performance Metrics

### Target Response Times
- **GET /health**: < 10ms
- **GET /databases**: < 50ms
- **GET /stats**: < 200ms (counts rows in all tables)
- **POST /query**: < 2s (AI processing + DB query)

### Actual Performance
- Database metadata retrieval: ~10-20ms
- Schema introspection: ~30-50ms
- AI SQL generation: ~1-2s (Google Gemini API)
- SQL execution: ~2-5ms (typical SELECT)
- Total query response: ~1.5-2.5s

---

## See Also

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and data flow
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development environment setup
- **[TESTING_SUMMARY.md](TESTING_SUMMARY.md)** - API endpoint tests
- **[.github/copilot-instructions.md](../.github/copilot-instructions.md)** - API development patterns

---

**FastAPI Documentation**: https://fastapi.tiangolo.com/  
**Interactive API Docs**: http://localhost:8000/docs (when server is running)
