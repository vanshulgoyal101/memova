# AI Business Insights

**Context-Aware Analysis for Strategic Questions**

The system automatically detects when questions require strategic analysis beyond simple data retrieval, then performs multi-stage AI analysis to provide actionable business insights.

---

## Overview

### Two Query Types

1. **Data Queries** (Original behavior)
   - "How many products?"
   - "Show top 10 sales"
   - "What are the most expensive items?"
   - **Result**: SQL → Table data → Basic summary

2. **Analytical Queries** (New in v3.2.0)
   - "Give me insights to improve sales"
   - "Recommend strategies to grow revenue"
   - "Analyze customer behavior patterns"
   - **Result**: Exploratory queries → AI analysis → Insights + Recommendations

### Automatic Detection

The system analyzes your question for strategic keywords:
- **Insights**: insight, analysis, pattern, trend
- **Strategy**: recommend, strategy, optimize, improve
- **Actions**: actionable, suggest, advice, solution

If detected → Business Analyst module handles it  
If not detected → Standard SQL query path

---

## How It Works

### Analytical Query Flow

```
User Question: "Give me insights to improve sales"
    ↓
[1] Detect Analytical Intent
    Keywords: "insights", "improve"
    → Route to BusinessAnalyst
    ↓
[2] Gather Data Context
    Run exploratory queries:
    ├─ Sales overview (revenue, orders, AOV)
    ├─ Top products (by revenue)
    ├─ Customer segments (lifetime value)
    ├─ Inventory status (stock levels)
    └─ Service quality (satisfaction, tickets)
    ↓
[3] AI Analysis (LLM)
    Prompt: "Analyze this business data..."
    Input: {sales_data, product_data, customer_data}
    ↓
[4] Generate Insights
    ✨ Key Insights (3-5 bullets)
    📊 Detailed Analysis (2-3 paragraphs)
    🎯 Actionable Recommendations (5-7 steps)
    ↓
[5] Return Structured Response
    {
      "analysis_text": "Full markdown analysis...",
      "insights": ["Revenue growth at 15%..."],
      "recommendations": ["Focus on top 20% products..."],
      "data_points": [{metric: "Total Revenue", value: 125000}]
    }
```

---

## Example Queries

### 🔍 Insights & Analysis

```plaintext
"What insights can you provide from the sales data?"
```

**Response**:
- **Key Insights**:
  - Revenue growing at 15% month-over-month
  - Top 20% of products generate 80% of revenue
  - Customer retention rate dropped 5% this quarter
  
- **Analysis**:
  Electronics sales show strong growth driven by premium products. However, customer service tickets increased 40% (127 open tickets), correlating with the retention drop. Average satisfaction rating fell from 4.2 to 3.8.
  
- **Recommendations**:
  1. Prioritize resolution of 23 high-priority service tickets
  2. Investigate quality issues in top-selling products
  3. Launch loyalty program to improve retention
  4. Increase inventory of top 10 products (current stock: 3.2 weeks)

### 📈 Strategic Recommendations

```plaintext
"Recommend strategies to improve my business performance"
```

**Response**:
- **Focus Areas**:
  - Product mix optimization (30% of SKUs have <10 units sold)
  - Customer experience (3.8 avg satisfaction, down from 4.2)
  - Inventory efficiency (15% of products out of stock)
  
- **High-Impact Actions**:
  1. **Discontinue low performers**: 45 products with <10 sales → free up $35K in capital
  2. **Restock winners**: Top 10 products generate $85K revenue but have 3-week supply
  3. **Service team expansion**: 127 open tickets, 2.3 days avg resolution time
  4. **Premium tier launch**: Top 15% of customers spend 5x more → create VIP program

### 🎯 Problem-Solving

```plaintext
"Why is my customer satisfaction declining and how can I fix it?"
```

**Response**:
- **Root Causes**:
  - Service ticket volume up 40% (127 open, 23 high-priority)
  - Average resolution time increased from 1.5 → 2.3 days
  - Product quality complaints mentioned in 18% of tickets
  
- **Immediate Actions**:
  1. **This Week**: Assign dedicated team to 23 high-priority tickets
  2. **This Month**: Audit top 5 products with most complaints
  3. **This Quarter**: Hire 2 support staff to handle volume
  4. **Proactive**: Implement automated follow-up after purchases

---

## Technical Implementation

### Backend Architecture

**Module**: `src/core/analyst.py`

```python
class BusinessAnalyst:
    """AI-powered business analyst for strategic questions"""
    
    def is_analytical_question(self, question: str) -> bool:
        """Detect if question needs strategic analysis"""
        analytical_keywords = [
            'insight', 'analyze', 'recommend', 'strategy',
            'improve', 'optimize', 'actionable', 'suggest'
        ]
        return any(kw in question.lower() for kw in analytical_keywords)
    
    def analyze(self, question: str) -> Dict[str, Any]:
        """
        Perform comprehensive business analysis
        
        Steps:
        1. Run exploratory queries (sales, products, customers, inventory, service)
        2. Format data context for LLM
        3. Generate AI analysis with insights + recommendations
        4. Parse structured response
        
        Returns:
            {
                'analysis_text': str,  # Full markdown analysis
                'insights': List[str],  # Key insights (3-5)
                'recommendations': List[str],  # Actions (5-7)
                'data_points': List[Dict],  # Metrics
                'queries_used': List[str]  # Exploratory queries
            }
        """
```

### Exploratory Queries

The analyst runs 5 automatic queries to gather context:

1. **Sales Overview**
   ```sql
   SELECT 
       COUNT(*) as total_orders,
       SUM(total_amount) as total_revenue,
       AVG(total_amount) as avg_order_value,
       MIN(order_date) as first_order,
       MAX(order_date) as last_order
   FROM sales_orders
   ```

2. **Top Products**
   ```sql
   SELECT 
       p.product_name,
       COUNT(DISTINCT so.order_id) as order_count,
       SUM(so.total_amount) as revenue
   FROM products p
   LEFT JOIN sales_orders so ON p.product_id = so.product_id
   GROUP BY p.product_id
   ORDER BY revenue DESC
   LIMIT 10
   ```

3. **Customer Segments**
   ```sql
   SELECT 
       COUNT(DISTINCT c.customer_id) as total_customers,
       COUNT(DISTINCT so.order_id) as total_orders,
       CAST(COUNT(DISTINCT so.order_id) AS FLOAT) / COUNT(DISTINCT c.customer_id) as orders_per_customer
   FROM customers c
   LEFT JOIN sales_orders so ON c.customer_id = so.customer_id
   ```

4. **Inventory Status**
   ```sql
   SELECT 
       COUNT(*) as total_products,
       SUM(CASE WHEN stock_quantity < 50 THEN 1 ELSE 0 END) as low_stock_products,
       AVG(stock_quantity) as avg_stock_level
   FROM products
   ```

5. **Service Quality**
   ```sql
   SELECT 
       COUNT(*) as total_tickets,
       AVG(CAST(satisfaction_rating AS FLOAT)) as avg_satisfaction,
       SUM(CASE WHEN priority = 'High' THEN 1 ELSE 0 END) as high_priority_tickets
   FROM customer_service_tickets
   ```

### AI Prompt Engineering

**System Message** (Cached):
```
{database_schema}

You are a senior business analyst with expertise in:
- Sales performance analysis
- Customer behavior insights
- Inventory optimization
- Operational efficiency
- Data-driven strategy
```

**User Message** (Per-query):
```
QUESTION: {user_question}

BUSINESS DATA ANALYSIS:

### Sales Overview
- total_orders: 1,245
- total_revenue: 125,000
- avg_order_value: 100.40

### Top Products
- Product A: 250 orders, $35K revenue
- Product B: 180 orders, $28K revenue
...

Please provide:

1. KEY INSIGHTS (3-5 bullets)
   - Patterns in the data
   - Strengths and weaknesses
   - Opportunities or risks

2. DETAILED ANALYSIS (2-3 paragraphs)
   - Current business situation
   - Root causes of trends
   - Connected metrics

3. ACTIONABLE RECOMMENDATIONS (5-7 steps)
   - Specific and measurable
   - High-impact, achievable
   - Prioritized list
```

### API Response Format

**Endpoint**: `POST /ask`

**Request**:
```json
{
  "question": "Give me insights to improve sales",
  "company_id": "electronics",
  "section_ids": []
}
```

**Response** (Analytical):
```json
{
  "answer_text": "# Business Analysis\n\n## Key Insights\n...",
  "query_type": "analytical",
  "analysis": {
    "success": true,
    "analysis_text": "Full markdown with insights + recommendations",
    "insights": [
      "Revenue growing at 15% month-over-month",
      "Top 20% products generate 80% revenue"
    ],
    "recommendations": [
      "Prioritize resolution of 23 high-priority tickets",
      "Increase inventory of top 10 products"
    ],
    "data_points": [
      {"name": "Total Revenue", "value": 125000, "category": "Sales"},
      {"name": "Avg Satisfaction", "value": 3.8, "category": "Service"}
    ],
    "queries_used": [
      "sales_overview",
      "top_products",
      "customer_segments"
    ]
  },
  "meta": {
    "exploratory_queries": 5,
    "data_points_analyzed": 12,
    "insights_count": 4,
    "recommendations_count": 7
  }
}
```

**Response** (Data Query - Unchanged):
```json
{
  "answer_text": "There are 150 products in the inventory.",
  "query_type": "data",
  "sql": "SELECT COUNT(*) FROM products",
  "columns": ["COUNT(*)"],
  "rows": [[150]],
  "charts": null,
  "trends": null
}
```

---

## Performance Characteristics

### Timing Breakdown

| Step | Time | Description |
|------|------|-------------|
| Question Detection | <10ms | Keyword matching (local) |
| Exploratory Queries | 50-150ms | 5 SQL queries (parallel) |
| AI Analysis | 1.5-3s | LLM generates insights |
| Response Formatting | <10ms | Parse markdown structure |
| **Total** | **1.6-3.2s** | End-to-end analytical query |

Compare to data query: **0.3-0.6s** (SQL gen + execution)

### Caching Strategy

1. **Database Schema** (System message)
   - Cached by Groq for 24 hours
   - ~2,500 tokens saved per request
   - Reduces analysis time by ~40%

2. **Exploratory Query Results** (Not yet implemented)
   - Future: Cache for 5 minutes
   - Would reduce time to ~0.5s for repeat analytics

### Cost Analysis (Groq)

**Analytical Query**:
- Input tokens: 50 (question) + 500 (data context) = 550
- Output tokens: ~800 (insights + recommendations)
- **Total**: 1,350 tokens per analytical query

**Daily Capacity**:
- Groq free tier: 100,000 tokens/day
- Analytical queries: ~74 queries/day
- vs. Data queries: ~2,000 queries/day (with caching)

**Recommendation**: Use analytical queries for strategic planning (5-10/day), data queries for exploration (100+/day)

---

## Frontend Integration

### Detecting Analytical Response

```typescript
// In frontend/src/lib/api.ts
interface AskResponse {
  answer_text: string;
  query_type: 'data' | 'analytical';
  
  // Data query fields
  sql?: string;
  columns?: string[];
  rows?: any[][];
  charts?: ChartConfig[];
  
  // Analytical query fields
  analysis?: {
    analysis_text: string;
    insights: string[];
    recommendations: string[];
    data_points: Array<{
      name: string;
      value: number;
      category: string;
    }>;
  };
}
```

### Rendering Analysis

**Option 1: Markdown Display** (Recommended)
```tsx
import ReactMarkdown from 'react-markdown';

{response.query_type === 'analytical' && response.analysis && (
  <div className="analysis-panel">
    <ReactMarkdown>
      {response.analysis.analysis_text}
    </ReactMarkdown>
  </div>
)}
```

**Option 2: Structured Components**
```tsx
{response.query_type === 'analytical' && response.analysis && (
  <>
    <InsightsPanel insights={response.analysis.insights} />
    <RecommendationsPanel recs={response.analysis.recommendations} />
    <MetricsPanel metrics={response.analysis.data_points} />
  </>
)}
```

---

## Use Cases

### ✅ When to Use Analytical Queries

- **Monthly business reviews**: "Analyze last month's performance"
- **Strategic planning**: "What should I focus on next quarter?"
- **Problem diagnosis**: "Why are sales declining?"
- **Opportunity identification**: "Where can I grow revenue?"
- **Resource allocation**: "Should I hire more staff or invest in inventory?"

### ❌ When to Use Data Queries

- **Quick lookups**: "How many orders today?"
- **Specific metrics**: "What's the average order value?"
- **Lists/tables**: "Show all products under $50"
- **Comparisons**: "Compare sales in Q1 vs Q2"
- **Visualizations**: "Chart revenue by category"

### 💡 Hybrid Approach (Future)

Some questions benefit from both:
1. User asks: "Why did Product X sales drop 30%?"
2. System runs data query: Get Product X sales trend
3. System runs analytical query: Analyze the drop with context
4. Response combines: Chart (data) + Insights (analysis)

---

## Configuration

### Environment Variables

```bash
# Required for analytical queries
GROQ_API_KEY=your_key_here          # Primary (faster, higher quota)
GOOGLE_API_KEY=backup_key_here      # Fallback
```

### Adjusting Detection Sensitivity

**File**: `src/core/analyst.py`

```python
def is_analytical_question(self, question: str) -> bool:
    # Add more keywords to increase sensitivity
    analytical_keywords = [
        'insight', 'analyze', 'recommend', 'strategy',
        'improve', 'optimize', 'actionable', 'suggest',
        # Add your custom triggers:
        'diagnose', 'investigate', 'deep dive'
    ]
```

### Customizing Exploratory Queries

**File**: `src/core/analyst.py` → `_gather_data_context()`

```python
# Add industry-specific queries
exploratory_queries['churn_risk'] = """
    SELECT customer_id, last_order_date,
           JULIANDAY('now') - JULIANDAY(last_order_date) as days_since_order
    FROM customers
    WHERE days_since_order > 90
"""
```

### Adjusting Response Length

**File**: `src/core/analyst.py` → `_generate_analysis()`

```python
# Shorter responses (3-4s → 2-3s)
user_message = f"""
Please provide a CONCISE analysis:
1. KEY INSIGHTS (3 bullets max)
2. TOP 3 RECOMMENDATIONS
"""

# Deeper analysis (3-4s → 5-6s)
user_message = f"""
Please provide an EXECUTIVE BRIEFING:
1. KEY INSIGHTS (5-7 bullets)
2. DETAILED ANALYSIS (4-5 paragraphs with examples)
3. STRATEGIC RECOMMENDATIONS (10-15 specific actions)
4. RISK ASSESSMENT
5. IMPLEMENTATION ROADMAP
```

---

## Testing

### Unit Tests

```bash
# Test analytical question detection
pytest tests/unit/test_analyst.py::test_is_analytical_question -v

# Test exploratory query execution
pytest tests/unit/test_analyst.py::test_gather_data_context -v
```

### Integration Tests

```bash
# Test full analysis flow
pytest tests/integration/test_analyst.py::test_business_analysis -v

# Test API endpoint
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Give me insights to improve sales",
    "company_id": "electronics"
  }'
```

### Example Test

```python
def test_analytical_vs_data_query():
    """Test automatic routing between data and analytical paths"""
    engine = QueryEngine(db_path="data/database/electronics_company.db")
    
    # Data query
    result1 = engine.ask("How many products?")
    assert result1['query_type'] == 'data'
    assert 'sql' in result1
    assert 'rows' in result1
    
    # Analytical query
    result2 = engine.ask("Give me insights to improve sales")
    assert result2['query_type'] == 'analytical'
    assert 'analysis' in result2
    assert len(result2['analysis']['insights']) >= 3
    assert len(result2['analysis']['recommendations']) >= 5
```

---

## Troubleshooting

### Issue: All Questions Treated as Data Queries

**Symptom**: Questions with "insights" or "recommend" still return SQL results

**Solution**: Check keyword detection
```python
# Test detection directly
from src.core.analyst import BusinessAnalyst
analyst = BusinessAnalyst(db_manager, llm_client, schema)
print(analyst.is_analytical_question("Give me insights"))  # Should be True
```

### Issue: Analysis Takes Too Long (>5s)

**Possible Causes**:
1. **No caching**: Ensure GROQ_API_KEY is set (caches schema)
2. **Slow queries**: Check database indexes
3. **Large result sets**: Exploratory queries returning 1000s of rows

**Solution**: Limit exploratory queries
```python
# In _gather_data_context()
exploratory_queries["top_products"] = """
    SELECT ... 
    LIMIT 10  -- Add LIMIT to prevent large result sets
```

### Issue: Generic/Unhelpful Insights

**Symptom**: AI says "Sales are good" without specifics

**Solution**: Improve prompt engineering
```python
# In _generate_analysis() user_message
user_message = f"""
{data_summary}

Provide SPECIFIC, QUANTIFIED insights:
❌ Bad: "Sales are trending upward"
✅ Good: "Sales grew 15% MoM ($85K → $98K), driven by Product A (+40%)"

Include NUMBERS and COMPARISONS in every point.
"""
```

### Issue: Rate Limit Errors

**Symptom**: "429 Too Many Requests" from Groq

**Solution**: Analytical queries use more tokens
- Groq free tier: 100K tokens/day = ~74 analytical queries
- Solution 1: Upgrade to paid tier (60/min rate limit)
- Solution 2: Cache exploratory query results (5min TTL)
- Solution 3: Use Gemini fallback (slower but 550 req/day with 11 keys)

---

## Future Enhancements

### Planned (v3.3.0)

1. **Multi-Database Analysis**
   - Compare metrics across electronics vs airline databases
   - "How does my electronics sales compare to industry benchmarks?"

2. **Time-Series Insights**
   - Detect seasonality, trends, anomalies automatically
   - "Sales spike every December" or "Revenue declined 30% in March (unusual)"

3. **Predictive Recommendations**
   - Forecast next quarter based on trends
   - "If growth continues at 15%, expect $150K revenue in Q3"

4. **Custom Analysis Templates**
   - User-defined analysis frameworks
   - "Run my quarterly health check" → predefined exploratory queries

### Under Consideration

- **Interactive Clarification**: "What time period should I analyze?" (if question ambiguous)
- **Visual Insights**: Auto-generate charts for key metrics in analysis
- **Export to PDF/PowerPoint**: Download analysis as executive report
- **Scheduled Analysis**: Daily/weekly automated business reviews

---

## Version History

- **v3.2.0** (2025-11-06): Initial release
  - Automatic analytical question detection
  - 5 exploratory queries (sales, products, customers, inventory, service)
  - AI-generated insights + recommendations
  - Structured API response format

---

## Related Documentation

- **[Natural Language Queries](./natural-language.md)**: How data queries work
- **[Charts & Insights](./charts-insights.md)**: Auto-charting for data queries
- **[API Reference](../05-api/endpoints.md)**: `/ask` endpoint details
- **[System Architecture](../02-architecture/system-overview.md)**: Overall system design

**Questions?** See [Getting Started](../01-getting-started/quickstart.md) or check [API docs](../05-api/endpoints.md).
