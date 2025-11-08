# API Endpoints Reference

**Base URL**: `http://localhost:8000`  
**Version**: 1.0.0  
**Last Updated**: November 2, 2025

---

## Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/databases` | List all databases |
| GET | `/databases/{id}/schema` | Get database schema |
| GET | `/databases/{id}/examples` | Get example queries |
| POST | `/ask` | **AI-powered query with natural language answer** |
| POST | `/query` | Execute natural language query (raw results) |
| GET | `/stats` | System statistics |
| GET | `/docs` | Interactive API docs (Swagger) |

---

## Endpoints

### GET /

**Description**: Root endpoint with API information

**Response**: 200 OK
```json
{
  "name": "Multi-Database Query API",
  "version": "1.0.0",
  "status": "online",
  "databases": ["electronics", "airline", "edtech"]
}
```

---

### GET /health

**Description**: Health check for monitoring

**Response**: 200 OK
```json
{
  "status": "healthy",
  "timestamp": "2025-10-31T10:30:00Z"
}
```

**Use**: Kubernetes probes, load balancers

---

### GET /databases

**Description**: List all available databases

**Response**: 200 OK
```json
{
  "databases": [
    {
      "id": "electronics",
      "name": "Electronics Company",
      "description": "12 tables covering HR, Sales, Finance, Inventory, Products, Customers, and more",
      "tables": 12,
      "total_rows": 3760
    },
    {
      "id": "airline",
      "name": "Airline Company",
      "description": "16 tables covering Aircraft, Pilots, Flights, Passengers, Revenue, and more",
      "tables": 16,
      "total_rows": 3760
    },
    {
      "id": "edtech",
      "name": "EdTech India Company",
      "description": "15 tables covering Students, Instructors, Courses, Enrollments, Assessments, Payments, Placements, and more",
      "tables": 15,
      "total_rows": 3745
    }
  ]
}
```

---

### GET /databases/{database_id}/schema

**Description**: Get full schema for a database

**Parameters**:
- `database_id` (path): `electronics`, `airline`, or `edtech`

**Response**: 200 OK
```json
{
  "database_id": "electronics",
  "tables": [
    {
      "name": "employees",
      "columns": [
        {"name": "employee_id", "type": "TEXT", "pk": true},
        {"name": "first_name", "type": "TEXT"},
        {"name": "email", "type": "TEXT"}
      ],
      "row_count": 120
    }
  ],
  "relationships": [
    {
      "from_table": "employees",
      "from_column": "department",
      "to_table": "departments",
      "to_column": "department_id"
    }
  ]
}
```

**Errors**:
- `404`: Database not found

---

### GET /databases/{database_id}/examples

**Description**: Get example queries for a specific database

**Parameters**:
- `database_id` (path): `electronics`, `airline`, or `edtech`

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

**Errors**:
- `404`: Database not found

---

### POST /ask

**Description**: Execute natural language query with AI-generated summary, automatic charts, and trend insights

**ENHANCED FEATURES**:
1. Generate SQL from natural language question
2. Execute the SQL against the database
3. Summarize results in natural language
4. **🎨 Auto-detect and generate charts** (AI-powered)
5. **📊 Detect statistical trends and outliers**
6. **🧠 Intelligent problem-solving** (v3.2.0) - Strategic business analysis

**Query Types**:
- **Data Queries**: Simple questions → Single SQL query → Table results
  - Example: "How many employees?" or "Show top 10 customers"
- **Analytical Queries**: Vague business problems → Multi-query analysis → Insights + recommendations
  - Example: "My revenue is low" or "How can I improve customer retention?"

**Flow**:
```
Question → [Analytical Detection] → Branch:
  ├─ Data Query: SQL Generation → Execution → LLM Summary + Charts + Trends
  └─ Analytical Query: Problem Interpretation → Custom Query Planning → 
                       Multi-Query Execution → Deep Analysis → Insights + Recommendations
```

**Request Body**:
```json
{
  "question": "Compare top 3 and bottom 3 products by revenue",
  "company_id": "electronics",
  "section_ids": []
}
```

---

#### Response Type 1: Data Query (Regular SQL Path)

**Response**: 200 OK
```json
{
  "query_type": "data",
  "answer_text": "Product PRD00071 is the top performer by revenue, while PRD00010 lags significantly.",
  "sql": "SELECT ...",
  "columns": ["category", "product_id", "revenue"],
  "rows": [
    ["Top", "PRD00071", 133359.68],
    ["Top", "PRD00001", 103261.41],
    ["Bottom", "PRD00010", 2157.82]
  ],
  "timings": {
    "genMs": 1247.3,
    "execMs": 12.8
  },
  "meta": {
    "row_count": 6
  },
  "charts": [
    {
      "id": "chart_ai_selected",
      "type": "bar",
      "title": "Top vs Bottom Products by Revenue",
      "x_column": "category",
      "y_columns": ["revenue"],
      "data": [
        {"category": "Top", "revenue": 133359.68},
        {"category": "Bottom", "revenue": 2157.82}
      ],
      "x_type": "category",
      "confidence": 0.9
    }
  ],
  "trends": [
    {
      "type": "high_outlier",
      "description": "Top category significantly outperforms",
      "details": "Revenue of $133K is 62x higher than Bottom ($2.2K)",
      "confidence": 0.95,
      "severity": "info"
    }
  ],
  "query_plan": null
}
```

**Response Fields**:
- `answer_text`: Natural language summary (paragraph + bullets)
- `sql`: Generated SQL query
- `columns`: Column names from query results
- `rows`: Query result rows
- `timings.genMs`: SQL generation time in milliseconds
- `timings.execMs`: SQL execution time in milliseconds
- `meta.row_count`: Number of rows returned
- **`charts`** ✨: Auto-detected visualizations (array, may be null/empty)
- **`trends`** ✨: Statistical insights (array, may be null/empty)
- `query_plan`: Multi-query execution plan (if applicable)

**Charts Field** (NEW v3.4.0):
```typescript
charts?: Array<{
  id: string;              // "chart_ai_selected", "chart_multi_series_line", etc.
  type: "line" | "bar" | "pie" | "histogram" | "area" | "stacked_bar" | "grouped_bar" | "combo" | "none";
  title: string;           // "Revenue by Department"
  x_column: string;        // Column name for x-axis
  y_columns?: string[];    // Column name(s) for y-axis (backward compatible)
  series?: Array<{         // Rich series model (new)
    name: string;          // Display name
    column: string;        // Data column
    type?: "line" | "bar" | "area";  // For combo charts
    color?: string;        // Hex color
    yAxisId?: string;      // For dual-axis charts
  }>;
  data: Array<{[key: string]: any}>;  // Chart data points
  x_type: "date" | "category" | "numeric";
  confidence: number;      // 0.0-1.0 (AI confidence)
  granularity?: string;    // "daily", "weekly", "monthly" for time series
  chart_group?: number;    // For grouping related charts
  stacked?: boolean;       // For stacked bar/area charts
  dual_axis?: boolean;     // If chart uses two Y axes
  layout_hint?: string;    // "single", "horizontal", "vertical", "grid"
}>
```

**Chart Types**:
- `none`: AI decided no visualization needed (simple count, single value, etc.)
- `bar`: Category comparisons, rankings, top/bottom analysis
- `pie`: Part-to-whole relationships (2-7 categories with proportions)
- `line`: Single time series trends
- **`area`** ✨: Cumulative trends, stacked time series (v3.4.0)
- **`stacked_bar`** ✨: Part-to-whole comparisons across categories (v3.4.0)
- **`grouped_bar`** ✨: Side-by-side category comparisons (v3.4.0)
- **`combo`** ✨: Mixed metrics (line + bar) with different scales (v3.4.0)
- `histogram`: Numeric distributions

**Multi-Series Example** (v3.4.0):
```json
{
  "id": "chart_multi_series_line",
  "type": "line",
  "title": "Compare revenue, cost, profit over time",
  "x_column": "date",
  "y_columns": ["revenue", "cost", "profit"],
  "series": [
    {"name": "Revenue", "column": "revenue", "type": "line", "color": "#8884d8"},
    {"name": "Cost", "column": "cost", "type": "line", "color": "#82ca9d"},
    {"name": "Profit", "column": "profit", "type": "line", "color": "#ffc658"}
  ],
  "data": [
    {"date": "2024-01-01", "revenue": 10000, "cost": 6000, "profit": 4000},
    {"date": "2024-01-02", "revenue": 12000, "cost": 7000, "profit": 5000}
  ],
  "x_type": "date",
  "confidence": 0.85,
  "granularity": "daily"
}
```

**Stacked Bar Example** (v3.4.0):
```json
{
  "id": "chart_stacked_bar",
  "type": "stacked_bar",
  "title": "Revenue by region with product breakdown",
  "x_column": "region",
  "y_columns": ["product_a", "product_b", "product_c"],
  "data": [
    {"region": "North", "product_a": 1000, "product_b": 2000, "product_c": 1500},
    {"region": "South", "product_a": 1200, "product_b": 1800, "product_c": 1600}
  ],
  "x_type": "category",
  "confidence": 0.8,
  "stacked": true
}
```

**Combo Chart Example** (v3.4.0):
```json
{
  "id": "chart_combo",
  "type": "combo",
  "title": "Revenue (bars) & growth rate (line)",
  "x_column": "date",
  "y_columns": ["revenue", "growth_rate"],
  "series": [
    {"name": "Revenue", "column": "revenue", "type": "bar"},
    {"name": "Growth %", "column": "growth_rate", "type": "line", "yAxisId": "right"}
  ],
  "data": [
    {"date": "2024-01-01", "revenue": 10000, "growth_rate": 0.05},
    {"date": "2024-01-02", "revenue": 12000, "growth_rate": 0.20}
  ],
  "x_type": "date",
  "confidence": 0.7,
  "dual_axis": true
}
```

**Trends Field** (NEW):
```typescript
trends?: Array<{
  type: "growth" | "decline" | "high_outlier" | "low_outlier" | "distribution";
  description: string;      // "Revenue shows strong growth trend"
  details: string;          // "45.2% increase from Q1 to Q4"
  confidence: number;       // 0.0-1.0 (statistical confidence)
  severity: "info" | "warning" | "success";
}>
```

**Trend Types**:
- `growth`: Consistent upward trend (≥3 points, monotonic increase)
- `decline`: Consistent downward trend (≥3 points, monotonic decrease)
- `high_outlier`: Value significantly above average (z-score > 2.0)
- `low_outlier`: Value significantly below average (z-score < -2.0)
- `distribution`: Quartile analysis for numeric columns

**AI Chart Selection** 🎨:

The system uses AI to intelligently decide:
1. **Should we visualize this data at all?**
   - No chart for: single values, simple counts, text-heavy data
   - Chart for: comparisons, trends, distributions, breakdowns

2. **If yes, what's the best chart type?**
   - Considers data characteristics (types, cardinality, temporal columns)
   - Analyzes question context ("compare", "trend", "breakdown")
   - Applies visualization best practices

**Chart Decision Examples**:
```bash
# No chart needed (simple count)
Question: "How many products are in inventory?"
Answer: "108 products"
Charts: null  # AI: "Single value, table is clearer"

# Bar chart (comparison/ranking)
Question: "Compare top vs bottom products by revenue"
Charts: [{ type: "bar", ... }]  # AI: "Perfect for comparisons"

# Line chart (trend over time)
Question: "Show monthly revenue trend"
Charts: [{ type: "line", ... }]  # AI: "Time series data"
```

---

#### Response Type 2: Analytical Query (Intelligent Problem-Solving) 🧠 NEW v3.2.0

For vague business problems like "My revenue is low" or "How can I improve sales?", the system uses the intelligent analyst:

**Response**: 200 OK
```json
{
  "query_type": "analytical",
  "answer_text": "### KEY INSIGHTS\n* Your average order value is high ($14,550) but customer base is small\n* Only 5 products account for majority of revenue...\n\n### DETAILED ANALYSIS\nThe data reveals...\n\n### ACTIONABLE RECOMMENDATIONS\n1. Expand customer acquisition channels...",
  
  "sql": "-- Query: Sales Overview\n-- Status: ✓ 1 rows\nSELECT COUNT(*) as total_orders...\n\n-- Query: Customer Overview\n-- Status: ✓ 1 rows\nSELECT COUNT(DISTINCT customer_id)...\n\n-- Query: Top Products\n-- Status: ✓ 10 rows\nSELECT product_name, SUM(revenue)...",
  
  "columns": ["total_orders", "total_revenue", "avg_order_value"],
  "rows": [[200, 2910028.14, 14550.14]],
  
  "analysis": {
    "analysis_text": "### KEY INSIGHTS\n* Insight 1...\n### DETAILED ANALYSIS\n...\n### ACTIONABLE RECOMMENDATIONS\n1. ...",
    "insights": [
      "Average order value is high ($14,550) indicating high-value customer base",
      "Only 200 total customers suggests acquisition bottleneck",
      "Top 5 products account for 60% of revenue - concentrated risk"
    ],
    "recommendations": [
      "Expand customer acquisition channels to reach more high-value buyers",
      "Diversify product portfolio to reduce concentration risk",
      "Implement referral program leveraging existing satisfied customers",
      "Consider premium service tier to capitalize on high willingness to pay",
      "Analyze customer segmentation to identify characteristics of high-value buyers"
    ],
    "data_points": [
      { "name": "Total Customers", "value": 200, "category": "customers" },
      { "name": "Average Order Value", "value": 14550.14, "category": "sales" }
    ],
    "queries_used": ["sales_overview", "customer_overview", "top_products"],
    "success": true
  },
  
  "meta": {
    "exploratory_queries": 3,
    "queries_succeeded": 3,
    "queries_failed": 0,
    "data_points_analyzed": 12,
    "insights_count": 6,
    "recommendations_count": 5,
    "row_count": 12
  }
}
```

**Analytical Response Fields**:
- `query_type`: "analytical" (vs "data")
- `analysis`: Structured business analysis object
  - `insights`: Key discoveries (4-6 bullets)
  - `recommendations`: Actionable steps (5-7 items)
  - `data_points`: Metrics extracted from queries
  - `queries_used`: IDs of exploratory queries executed
- `sql`: Combined SQL from all exploratory queries with status comments
- `columns`/`rows`: Combined results from successful queries (may be null if all failed)
- `meta.queries_succeeded`/`queries_failed`: Success rate tracking

**Analytical Query Detection**:

The system detects analytical questions using 27 keywords:
- `insight`, `insights`, `analyze`, `analysis`, `recommend`, `improve`, `why`
- `problem`, `issue`, `challenge`, `solution`, `grow`, `decline`
- Vague problems: "My X is low/high/poor/declining..."

**See**: [Intelligent Problem-Solving](../03-features/intelligent-problem-solving.md) for full documentation

---

#### Common Response Fields (Both Types)

**All responses include**:
- `answer_text`: Natural language summary (Markdown formatted)
- `genMs`: AI generation time (milliseconds)
- `execMs`: SQL execution time (milliseconds)
- `totalMs`: Total response time

**Summary Features**:
- **Smart Sampling**: Head + tail sampling with ellipsis for large datasets (>100 rows)
- **Numeric Aggregates**: Automatic sum, mean, min, max for numeric columns
- **Executive Tone**: Senior data analyst perspective, non-technical language

---

#### Error Response

**Response**: 500 Internal Server Error
- **Concise Format**: 1 paragraph + 2-5 bullets, under 120 words

**Example**:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show top 5 products by revenue",
    "company_id": "electronics",
    "section_ids": ["products", "sales"]
  }'
```

**Errors**:
- `400`: Invalid request (missing fields, invalid company_id)
- `404`: Database not found
- `429`: Rate limit exceeded (automatic retry with API key rotation)
- `500`: Query execution failed
- `503`: AI service unavailable (returns enhanced fallback message)

**Enhanced Error Handling** ✨:

Even if AI summarization fails, you still receive:
- ✅ Valid SQL query
- ✅ Complete result set (columns + rows)
- ✅ Informative fallback message with data preview

**Fallback Example** (when all API keys exhausted):
```json
{
  "answer_text": "Found 5 records across 4 columns.\n\nSample: product_name: iPhone 15 Pro, revenue: 234500, units_sold: 156...\n\nNote: AI summary temporarily unavailable. View complete results below.",
  "sql": "SELECT product_name, SUM(revenue) as revenue, SUM(quantity) as units_sold FROM sales GROUP BY product_name ORDER BY revenue DESC LIMIT 5",
  "columns": ["product_name", "revenue", "units_sold", "avg_price"],
  "rows": [
    ["iPhone 15 Pro", 234500, 156, 1502.56],
    ["MacBook Air M3", 198750, 89, 2233.15]
  ],
  "timings": { "genMs": 1200, "execMs": 15 },
  "meta": { "row_count": 5 }
}
```

**API Key Rotation**:
- SQL Generation: Uses 11-key rotation (api_key_manager.py)
- Result Summarization: Uses same 11-key rotation (llm.py)
- Total Capacity: 550 requests/day (50/day × 11 keys)
- Automatic failover on rate limits (429 errors)
- Detailed logging of rotation events

**Performance**:
- Average response time: 1.5-3 seconds
  - SQL Generation: 800ms - 2s (60%)
  - SQL Execution: 50-200ms (10%)
  - LLM Summarization: 500ms - 1.5s (30%)
- Retry overhead: +1.5-4.5s if transient errors occur

---

### POST /query

**Description**: Execute natural language query (returns raw results without AI summary)

**Request Body**:
```json
{
  "question": "How many employees are there?",
  "database": "electronics"
}
```

**Response**: 200 OK
```json
{
  "success": true,
  "sql": "SELECT COUNT(*) FROM employees",
  "columns": ["COUNT(*)"],
  "rows": [[120]],
  "row_count": 1,
  "execution_time": 0.023
}
```

**Errors**:
- `400`: Invalid request (missing fields, invalid database)
- `404`: Database not found
- `429`: Rate limit exceeded (automatic retry with API key rotation)
- `500`: Query execution failed
- `503`: AI service unavailable

**Example**:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show top 5 products by sales",
    "database": "electronics"
  }'
```

---

### GET /stats

**Description**: System statistics (queries, errors, performance)

**Response**: 200 OK
```json
{
  "total_queries": 156,
  "successful_queries": 142,
  "failed_queries": 14,
  "average_execution_time": 1.234,
  "uptime_seconds": 3600,
  "databases": {
    "electronics": {
      "queries": 89,
      "avg_time": 1.1
    },
    "airline": {
      "queries": 67,
      "avg_time": 1.4
    }
  }
}
```

---

## Request/Response Schemas

### AskRequest (NEW)
```typescript
interface AskRequest {
  question: string;           // Natural language question
  company_id: string;         // "electronics" or "airline"
  section_ids: string[];      // Optional schema sections for context
}
```

### AskResponse (NEW)
```typescript
interface AskResponse {
  answer_text: string;        // AI-generated natural language summary
  sql: string;                // Generated SQL query
  columns: string[];          // Column names
  rows: any[][];             // Data rows
  timings: {                 // Performance metrics
    total: number;           // Total time in seconds
    execution: number;       // Query execution time in seconds
  };
  meta: {                    // Additional metadata
    row_count: number;       // Number of rows returned
    truncated: boolean;      // Whether large dataset was downsampled
    timestamp: string;       // ISO 8601 timestamp
  };
}
```

### QueryRequest
```typescript
interface QueryRequest {
  question: string;      // Natural language question
  database: string;      // "electronics" or "airline"
}
```

### QueryResponse
```typescript
interface QueryResponse {
  success: boolean;          // true if query succeeded
  sql: string;               // Generated SQL query
  columns: string[];         // Column names
  rows: any[][];            // Data rows
  row_count: number;        // Number of rows returned
  execution_time: number;   // Time in seconds
  error?: string;           // Error message (if failed)
}
```

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Database 'invalid' not found"
}
```

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found (invalid database ID)
- `429`: Too Many Requests (rate limit)
- `500`: Internal Server Error
- `503`: Service Unavailable (AI service down)

---

## Rate Limiting

### Current Limits
- **Free Tier**: 10 requests/minute per API key (15/minute for some models)
- **Total Capacity**: 110-165 requests/minute (11 keys)
- **Daily Capacity**: 550 requests/day (50/day × 11 keys)
- **Retry After**: 60 seconds on 429 error

### Best Practices
- Implement exponential backoff
- Cache common queries
- Monitor rate limit headers (if added)

See [API Key Rotation](../02-architecture/api-key-rotation.md) for details.

---

## CORS Configuration

### Allowed Origins
- `http://localhost:3000` (frontend dev server)
- `http://127.0.0.1:3000`

### Allowed Methods
- GET, POST, OPTIONS

### Allowed Headers
- Content-Type, Authorization

**Production**: Update to production domain

---

## Authentication

**Current**: None (development mode)

**Production Recommendations**:
- API key in header: `X-API-Key: your_key_here`
- JWT tokens for user auth
- Rate limiting per user/key

---

## Query Execution Guardrails

All SELECT queries are executed with server-side safeguards to protect performance:

### Result Limits

The system enforces result limits at the database layer:

- **DEFAULT_RESULT_LIMIT**: `100` rows (default, configurable via `.env`)
  - Applied automatically to SELECT queries that don't specify a LIMIT clause
  - Can be overridden by LLM-generated or user-specified LIMIT values
  
- **MAX_QUERY_RESULTS**: `1000` rows (hard server-side cap)
  - Enforced on all SELECT queries regardless of requested LIMIT
  - If a query requests `LIMIT 5000`, it's automatically capped to 1000
  - Protects frontend rendering and network transfer

- **QUERY_TIMEOUT_SECONDS**: `30` seconds maximum execution time

### How It Works

1. LLM generates SQL (may include LIMIT clause based on question)
2. `DatabaseManager.execute_query()` checks if query is a SELECT statement
3. **If SELECT without LIMIT** → appends `LIMIT 100` (or configured default)
4. **If SELECT with LIMIT** → validates it's ≤ 1000 (or configured max), caps if needed
5. **Non-SELECT queries** (PRAGMA, EXPLAIN, etc.) are exempt from LIMIT enforcement

### Configuration

```bash
# .env file
DEFAULT_RESULT_LIMIT=100    # Default rows when no LIMIT specified
MAX_QUERY_RESULTS=1000      # Hard cap on any LIMIT value
QUERY_TIMEOUT_SECONDS=30    # Execution timeout
```

### Examples

```sql
-- User asks: "Show me employees"
-- LLM generates: SELECT * FROM employees
-- Server appends: SELECT * FROM employees LIMIT 100

-- User asks: "Show me top 50 products"
-- LLM generates: SELECT * FROM products ORDER BY revenue DESC LIMIT 50
-- Server validates: 50 ≤ 1000 ✓ (no change)

-- User asks: "Show me all 10,000 transactions"
-- LLM generates: SELECT * FROM transactions LIMIT 10000
-- Server caps: SELECT * FROM transactions LIMIT 1000

-- Internal schema query: PRAGMA table_info(employees)
-- Server skips LIMIT: PRAGMA query executed as-is
```

**Rationale**: Prevents accidental full-table scans, protects frontend from rendering thousands of rows, and ensures consistent performance.

---

## Interactive Documentation

### Swagger UI
- **URL**: http://localhost:8000/docs
- **Features**: Try endpoints, see schemas, auto-generated

### ReDoc
- **URL**: http://localhost:8000/redoc
- **Features**: Alternative docs UI, printable

### OpenAPI JSON
- **URL**: http://localhost:8000/openapi.json
- **Use**: Import into Postman, generate clients

---

## Example Usage

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "question": "How many employees?",
        "database": "electronics"
    }
)

data = response.json()
print(data["sql"])
print(data["rows"])
```

### JavaScript (Fetch)
```javascript
const response = await fetch("http://localhost:8000/query", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    question: "How many employees?",
    database: "electronics"
  })
});

const data = await response.json();
console.log(data.sql);
console.log(data.rows);
```

### cURL
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"How many employees?","database":"electronics"}'
```

---

## Related Documentation

- [Architecture Overview](../02-architecture/system-overview.md)
- [Error Handling](error-handling.md)
- [Development Setup](../04-development/setup.md)

---

**Last Updated**: November 2, 2025
