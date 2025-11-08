# Natural Language Querying

**Feature**: AI-powered natural language to SQL conversion  
**Status**: ✅ Production Ready  
**Added**: v1.0.0

---

## Overview

Users can ask questions in plain English instead of writing SQL. The system uses **Google Gemini AI** to translate natural language into SQL queries, execute them, and return results.

---

## How It Works
---

## Sidebar Quick Query Shortcuts (v3.0.0)

The sidebar now features production-grade quick query shortcuts, grouped by difficulty (Easy, Medium, Hard) with color-coded badges and icons:

* ✨ **Easy**: Green badge, Sparkles icon
* ⚡ **Medium**: Yellow badge, Lightning icon
* 🔥 **Hard**: Red badge, Flame icon

Each button is a compact pill, left-aligned, with micro-interactions (hover, focus ring, scale, shadow) and full keyboard accessibility. Clicking a button instantly runs the query in the AskBar.

**Screenshot:**

![Sidebar Quick Queries](../images/sidebar-quick-queries-v3.png)

This feature makes the product highly actionable and intuitive for all users.

```
1. User types: "How many employees are there?"
2. Frontend sends to backend with database context
3. Backend sends to Gemini AI with schema
4. Gemini returns: "SELECT COUNT(*) FROM employees"
5. Backend executes SQL against SQLite
6. LLM analyzes results and generates natural language summary
7. Frontend displays rich answer with bullets + collapsible data
```

### Two Endpoints

**`/ask` (Recommended)** - Modern endpoint with AI-powered summarization:
- Generates SQL from natural language
- Executes query against database
- Analyzes results (numeric aggregates, trends, categorical insights)
- Returns **natural language summary** with paragraph + bullets
- Automatic API key rotation (11 keys) for robustness

**`/query` (Legacy)** - Raw results without summarization:
- Generates and executes SQL
- Returns raw columns and rows
- No natural language summary
- Use for programmatic access or debugging

---

## Natural Language Summarization

### Overview

The `/ask` endpoint automatically summarizes query results using AI, transforming raw data into business insights.

**Example**:

**Question**: "List top 5 customers by order count"

**AI Summary**:
```
Found 5 customers with the highest order counts.

• Sarah Johnson leads with 156 orders ($234,500 total revenue)
• Michael Chen follows with 142 orders ($198,750 revenue)
• Average order value across top 5: $1,582
• All customers are in "Premium" tier
• Date range spans 2023-01-15 to 2025-10-30
```

### How Summarization Works

1. **Data Analysis**:
   - Computes numeric aggregates (sum, mean, min, max)
   - Identifies categorical columns (low cardinality)
   - Detects time columns for trend analysis
   - Intelligently samples large datasets (head + tail)

2. **Prompt Engineering**:
   - System prompt: "You are a senior data analyst..."
   - Sends JSON payload with metadata and insights
   - Requests paragraph + 3-6 bullet points
   - Executive tone, under 130 words

3. **Robust Execution**:
   - Uses same 7-key rotation as SQL generation
   - Automatic retry on rate limits (429 errors)
   - Exponential backoff for transient failures
   - Enhanced fallback if all keys exhausted

### Error Handling & Fallback

If AI summarization fails (rate limits, network errors), you receive an **informative fallback** instead:

**Single Record**:
```
Found 1 record.

customer_name: Sarah Johnson, order_count: 156, total_revenue: 234500

Note: AI summary unavailable. View full details below.
```

**Multiple Records**:
```
Found 5 records across 4 columns.

Sample: customer_name: Sarah Johnson, order_count: 156, total_revenue: 234500...

Note: AI summary temporarily unavailable. View complete results below.
```

**Empty Results**:
```
No matching records found for your query.
```

**You always receive**:
- ✅ Valid SQL query
- ✅ Complete result set
- ✅ Either rich summary OR informative fallback

### API Key Rotation for Summarization

Both SQL generation AND result summarization use the same robust rotation system:

- **11 API keys** configured in `.env` (including commented lines)
- **Automatic failover** when any key hits rate limit
- **550 requests/day** total capacity (50/day × 11 keys)
- **Detailed logging** of key rotation events
- **No silent failures** - comprehensive error logging

---

## Supported Query Types

### ✅ Aggregations
```
"How many employees are there?"
"What is the average salary?"
"Show total sales by department"
```

### ✅ Filtering
```
"List employees in the Engineering department"
"Show products with price > $100"
"Find customers from California"
```

### ✅ Sorting
```
"Show top 5 bestselling products"
"List employees by hire date"
"Rank departments by employee count"
```

### ✅ Joins
```
"Show all employees with their department names"
"List orders with customer information"
"Display flights with aircraft details"
```

### ✅ Complex Queries
```
"Which department has the highest average salary?"
"Show customers who ordered more than 3 times"
"Find pilots certified for Boeing 737"
```

---

## AI Model Configuration

### Current Setup
- **Model**: `gemini-2.0-flash-exp`
- **Temperature**: 0 (deterministic)
- **Max Tokens**: 1000
- **Timeout**: 30 seconds

### API Key Rotation
- **Keys**: 7 Google API keys configured
- **Free Tier**: 10 requests/minute per key
- **Total Capacity**: 70 requests/minute
- **Failover**: Automatic rotation on 429 errors
- **Retry**: Wait 60 seconds before retry

See [API Key Rotation](../02-architecture/api-key-rotation.md) for details.

---

## Schema Context

The AI receives the database schema to understand:
- Table names and relationships
- Column names and data types
- Foreign key constraints
- Sample data (optional)

### Example Schema Sent to AI

```sql
-- Electronics Company Schema
CREATE TABLE employees (
    employee_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    department TEXT,
    salary REAL
);

CREATE TABLE departments (
    department_id TEXT PRIMARY KEY,
    department_name TEXT NOT NULL,
    manager_id TEXT,
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);
```

---

## Query Validation

### Pre-Execution Checks
1. **SQL Syntax**: Parse SQL to ensure valid syntax
2. **Dangerous Keywords**: Block DROP, DELETE, UPDATE, INSERT
3. **Row Limit**: Enforce MAX 1000 rows per query
4. **Timeout**: 10-second execution limit

### Safety Features
- Read-only queries (SELECT only)
- Parameterized execution (prevents injection)
- Schema-aware generation (AI knows structure)

---

## Response Format

### Natural Language Answer
```json
{
  "answer": "There are 120 employees in the database."
}
```

### Full Response
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

---

## Error Handling

### Common Errors

| Error | Cause | User Message |
|-------|-------|--------------|
| 429 | Rate limit exceeded | "Too many requests. Please wait..." |
| 400 | Invalid question | "Could not understand question" |
| 500 | AI generation failed | "Failed to generate SQL" |
| 503 | Database unavailable | "Database temporarily unavailable" |

### AI Errors
- **No SQL Generated**: "I couldn't generate a valid query for that question"
- **Invalid SQL**: "The generated query is invalid"
- **Unsupported Query**: "This type of query is not supported"

---

## Limitations

### Current Limitations
- ❌ No INSERT/UPDATE/DELETE operations (read-only)
- ❌ No cross-database queries (single DB per request)
- ❌ No query optimization hints
- ❌ No support for views or stored procedures
- ❌ Limited to 1000 rows per response

### Known Issues
- Complex nested queries may fail
- Ambiguous questions may generate incorrect SQL
- Schema changes require restart

---

## Usage Examples

### Electronics Company

**Question**: "How many products are in stock?"  
**SQL**: `SELECT SUM(quantity_in_stock) FROM inventory`  
**Answer**: "There are 4,523 products in stock."

**Question**: "Show departments with more than 10 employees"  
**SQL**: 
```sql
SELECT d.department_name, COUNT(e.employee_id) as employee_count
FROM departments d
JOIN employees e ON d.department_id = e.department
GROUP BY d.department_name
HAVING COUNT(e.employee_id) > 10
```

### Airline Company

**Question**: "Which aircraft have maintenance due this week?"  
**SQL**:
```sql
SELECT aircraft_id, aircraft_model, next_maintenance
FROM aircraft
WHERE next_maintenance BETWEEN date('now') AND date('now', '+7 days')
```

---

## Best Practices

### For Users
1. **Be specific**: "Show top 5 products" instead of "Show some products"
2. **Use proper names**: Reference exact table/column names when possible
3. **Ask one thing**: Break complex questions into multiple queries
4. **Check SQL**: Review generated SQL before trusting results

### For Developers
1. **Keep schema updated**: AI needs accurate schema
2. **Monitor errors**: Track failed queries for improvements
3. **Cache common queries**: Reduce AI calls for frequent questions
4. **Log all queries**: Audit trail for debugging

---

## Future Enhancements

### Planned Features
- ✨ Query caching (Redis)
- ✨ Query history (last 10 queries)
- ✨ Query suggestions (autocomplete)
- ✨ Multi-step queries (follow-up questions)
- ✨ Natural language result summaries
- ✨ Chart generation from results

### Under Consideration
- Multiple AI providers (Claude, GPT-4)
- User feedback loop (thumbs up/down)
- Query explanation ("Why this SQL?")
- Schema recommendations

---

## Performance

### Typical Response Times
- **Simple COUNT**: 1-2 seconds
- **Single JOIN**: 1.5-2.5 seconds
- **Complex aggregation**: 2-3 seconds
- **Large result set (1000 rows)**: 3-4 seconds

### Breakdown
- AI generation: 800ms - 2s (70% of time)
- SQL execution: 50-200ms (15% of time)
- Network + formatting: 100-300ms (15% of time)

---

## Related Documentation

- [Multi-Database Support](multi-database.md) - Switching databases
- [API Reference](../05-api/endpoints.md) - `/query` endpoint details
- [Architecture](../02-architecture/system-overview.md) - How it all works

---

**Last Updated**: October 31, 2025
