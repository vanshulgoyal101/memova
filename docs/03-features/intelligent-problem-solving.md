# Intelligent Problem-Solving System

**Version**: 3.2.0  
**Status**: ✅ Production Ready  
**Last Updated**: 2025-11-06

**Latest Enhancement (2025-11-06)**: **Schema Awareness Fix** - AI query generation now embeds database schema in prompts to prevent hallucinated table names. Query success rate improved from 0-20% to 80-100%.

---

## Overview

The **Intelligent Problem-Solving System** allows users to enter vague business problems in natural language, and the AI automatically:
- **Interprets** what the problem means
- **Determines** what data is needed to solve it
- **Generates** custom SQL queries specific to the problem
- **Analyzes** the data to discover insights
- **Provides** actionable recommendations

This is a **5-stage AI-driven pipeline** that replaces fixed exploratory queries with dynamic, problem-specific data gathering.

---

## How It Works

### Stage 1: Problem Interpretation 🧠
**AI analyzes the vague problem and breaks it down:**
- Generates 3-5 testable hypotheses about root causes
- Identifies relevant focus areas (sales, customers, products, etc.)
- Determines key metrics to investigate

**Example Input:**  
> "My business performance is poor and I need help"

**AI Output:**
```json
{
  "hypotheses": [
    "Inadequate sales strategies or ineffective marketing campaigns are leading to low revenue",
    "Poor customer service or low-quality products are resulting in high customer churn rates",
    "Inefficient inventory management is causing stockouts or overstocking"
  ],
  "focus_areas": ["sales", "customers", "products", "inventory", "marketing", "finance"],
  "metrics_to_check": ["revenue trend", "customer churn", "product performance", "inventory levels"]
}
```

---

### Stage 2: Custom Query Generation ⚙️
**AI generates 3-5 custom SQL queries** to test the hypotheses (NOT fixed queries):

**Example Queries Generated:**
1. **revenue_trend** - Monthly revenue to identify trends
   ```sql
   SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS revenue
   FROM sales_orders
   GROUP BY month
   ORDER BY month DESC
   LIMIT 12
   ```

2. **customer_churn** - Customers who haven't ordered recently
   ```sql
   SELECT c.customer_id, c.first_name, c.last_name, MAX(so.order_date) AS last_order
   FROM customers c
   LEFT JOIN sales_orders so ON c.customer_id = so.customer_id
   GROUP BY c.customer_id
   HAVING last_order < date('now', '-90 days')
   LIMIT 10
   ```

3. **product_performance** - Top and bottom performing products
   ```sql
   SELECT p.product_name, SUM(si.quantity) AS total_quantity
   FROM products p
   JOIN sales_items si ON p.product_id = si.product_id
   GROUP BY p.product_id
   ORDER BY total_quantity DESC
   LIMIT 10
   ```

4. **inventory_stockout** - Products at risk of stockout
   ```sql
   SELECT product_id, product_name, quantity_in_stock, reorder_level
   FROM products
   WHERE quantity_in_stock <= reorder_level
   ```

5. **customer_satisfaction** - Average satisfaction by channel
   ```sql
   SELECT feedback_channel, AVG(satisfaction_rating) AS avg_satisfaction
   FROM customer_feedback
   GROUP BY feedback_channel
   ```

---

### Stage 3: Query Execution 📊
**System executes all custom queries and gathers results:**
- Runs each query against the database
- Stores results with metadata (query ID, description, row count)
- Handles query failures gracefully (continues with other queries)
- Tracks execution time and data quality

**Example Output:**
```json
[
  {
    "query_id": "revenue_trend",
    "description": "Revenue by month to identify trend",
    "rows": 12,
    "columns": ["month", "revenue"],
    "sample_data": [
      {"month": "2025-10", "revenue": 257920.31},
      {"month": "2025-09", "revenue": 85751.97}
    ]
  },
  {
    "query_id": "customer_churn",
    "description": "Customers with no recent orders",
    "rows": 5,
    "columns": ["customer_id", "first_name", "last_name", "last_order"]
  }
]
```

---

### Stage 4: Deep Analysis 💡
**AI synthesizes all data to discover insights:**
- Tests each hypothesis against the data
- Identifies patterns, trends, and anomalies
- Explains root causes of the problem
- Connects multiple data points to tell the story

**Example Insights:**
1. **Declining Revenue Trend** - Revenue fluctuates significantly month-to-month, with a concerning drop from October 2025 ($257,920) to September 2025 ($85,752), indicating potential instability in sales performance.

2. **Customer Churn** - Several customers have not placed recent orders, suggesting potential churn issues that need immediate attention.

3. **Product Performance Disparity** - Electrolux Air Conditioners significantly outperform other products (57 units sold), while other products lag behind, showing an imbalance in sales performance.

4. **Inventory Stockout Risk** - Several products have inventory levels below reorder level (e.g., 32 in stock vs. reorder level of 49), increasing risk of stockouts.

---

### Stage 5: Actionable Recommendations 🎯
**AI generates 6-10 SMART recommendations** based on the insights:
- Prioritized by impact (high/medium/low)
- Specific, Measurable, Achievable, Relevant, Time-bound
- Both quick wins and long-term strategies
- References the data that supports each recommendation

**Example Recommendations:**
1. **Optimize Marketing Spend (High)** - Analyze marketing ROI by campaign and reallocate budget to high-performing channels. Expected impact: 15-20% revenue increase in 3 months.

2. **Implement Real-Time Inventory Tracking (High)** - Deploy automated inventory system to prevent stockouts and reduce holding costs. Expected impact: 30% reduction in stockouts.

3. **Offer Promotions on Slow-Moving Products (Medium)** - Target discounts and promotions on underperforming products to clear inventory and boost sales.

4. **Review Supply Chain (Medium)** - Identify bottlenecks in supply chain and evaluate alternative suppliers to improve efficiency.

5. **Enhance Customer Retention (High)** - Launch customer win-back campaign for churned customers with personalized offers. Expected impact: 10-15% churn reduction.

6. **Monitor Key Metrics Weekly (Low)** - Set up automated dashboards to track revenue, churn, inventory levels, and product performance weekly.

---

## Detection Logic

The system detects vague business problems using **keywords and phrases**:

### Analytical Keywords
```python
analytical_keywords = [
    # Explicit analysis requests
    'insight', 'analyze', 'recommend', 'strategy', 'improve',
    'optimize', 'suggest', 'advice', 'why', 'understand',
    'explain', 'pattern', 'trend', 'opportunity', 'solution',
    
    # Negative performance indicators
    'poor', 'bad', 'worse', 'worst', 'failing', 'failed',
    'losing', 'loss', 'inefficient', 'slow', 'costly',
    
    # Problem indicators
    'problem', 'issue', 'challenge', 'struggling', 'worried',
    'confused', 'stuck', 'frustrated', 'concerned', 'unhappy',
    
    # Help requests
    'help', 'fix', 'solve', 'need to', 'how can', 'how do',
    'what should', 'ways to', 'guide', 'support'
]
```

### Analytical Phrases
```python
analytical_phrases = [
    'i need', 'i want', 'help me', 'not sure',
    'my business', 'our business', 'the business',
    'performance is', 'sales are', 'revenue is', 'customers are'
]
```

### Examples That Trigger Intelligent Analysis
- ✅ "My sales are declining"
- ✅ "Revenue is too low"
- ✅ "Customers are unhappy"
- ✅ "Business performance is poor"
- ✅ "I'm struggling with profitability"
- ✅ "How can I improve revenue"
- ✅ "I need help with my business"
- ✅ "Why are we losing customers"

---

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| **Problem Interpretation** | ~1-2s | Uses Groq AI (llama-3.3-70b) with prompt caching |
| **Query Generation** | ~1-2s | AI generates 3-5 custom queries |
| **Query Execution** | ~0.5-1s | Total for all queries (parallel) |
| **Deep Analysis** | ~5-15s | AI synthesizes all data (Gemini fallback if Groq unavailable) |
| **Total Time** | ~8-20s | End-to-end (interpretation → recommendations) |
| **Cache Hit Rate** | ~90% | After first query (schema cached) |

---

## Fallback Mechanisms

### 1. Query Planning Fallback
If AI query generation fails (JSON parsing error, rate limit):
```python
fallback_queries = [
    {
        "id": "revenue_overview",
        "description": "Overall revenue trends",
        "sql": "SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS revenue FROM sales_orders GROUP BY month ORDER BY month DESC LIMIT 12"
    },
    {
        "id": "customer_overview",
        "description": "Customer summary statistics",
        "sql": "SELECT COUNT(*) AS total_customers, COUNT(DISTINCT so.customer_id) AS active_customers FROM customers c LEFT JOIN sales_orders so ON c.customer_id = so.customer_id"
    },
    {
        "id": "top_products",
        "description": "Best selling products",
        "sql": "SELECT p.product_name, SUM(si.quantity) AS total_sold FROM products p JOIN sales_items si ON p.product_id = si.product_id GROUP BY p.product_id ORDER BY total_sold DESC LIMIT 10"
    }
]
```

### 2. Recommendation Fallback
If AI doesn't return recommendations, generate defaults:
```python
default_recommendations = [
    "Conduct deeper analysis of the identified patterns to understand root causes",
    "Implement data collection systems to fill critical data gaps identified in the analysis",
    "Review and optimize processes in areas showing inefficiency or underperformance",
    "Develop targeted action plans to address specific issues highlighted in the insights",
    "Monitor key metrics regularly to track improvement and adjust strategies as needed",
    "Prioritize high-impact areas for immediate intervention based on the data analysis"
]
```

### 3. Provider Fallback
- **Primary**: Groq AI (llama-3.3-70b-versatile) - 26x faster
- **Fallback**: Google Gemini (gemini-2.0-flash-exp) - reliable
- **Automatic**: Switches on rate limits, errors, or timeouts

---

## API Response Format

### Request
```json
{
  "question": "My business performance is poor and I need help",
  "database": "electronics"
}
```

### Response
```json
{
  "query_type": "analytical",
  "success": true,
  "genMs": 1200,
  "execMs": 850,
  "totalMs": 18300,
  "analysis": {
    "success": true,
    "hypotheses": [
      "Inadequate sales strategies or ineffective marketing campaigns are leading to low revenue",
      "Poor customer service or low-quality products are resulting in high customer churn rates",
      "Inefficient inventory management is causing stockouts or overstocking"
    ],
    "focus_areas": ["sales", "customers", "products", "inventory", "marketing", "finance"],
    "queries_used": [
      {
        "id": "revenue_trend",
        "description": "Revenue by month to identify trend",
        "rows": 12
      },
      {
        "id": "customer_churn",
        "description": "Customers with no recent orders",
        "rows": 5
      },
      {
        "id": "product_performance",
        "description": "Top and bottom performing products",
        "rows": 10
      },
      {
        "id": "inventory_stockout",
        "description": "Products at risk of stockout",
        "rows": 8
      },
      {
        "id": "customer_satisfaction",
        "description": "Average satisfaction by channel",
        "rows": 3
      }
    ],
    "insights": [
      "Declining Revenue Trend: Revenue fluctuates significantly month-to-month, with a concerning drop from October 2025 ($257,920) to September 2025 ($85,752)",
      "Customer Churn: Several customers have not placed recent orders, suggesting potential churn issues",
      "Product Performance Disparity: Electrolux Air Conditioners significantly outperform other products (57 units sold)",
      "Inventory Stockout Risk: Several products have inventory levels below reorder level"
    ],
    "recommendations": [
      "Optimize marketing spend based on ROI analysis (High impact, 3 months)",
      "Implement real-time inventory tracking system (High impact, 2 months)",
      "Offer promotions on slow-moving products (Medium impact, 1 month)",
      "Review supply chain to identify bottlenecks (Medium impact, 2 months)",
      "Launch customer win-back campaign (High impact, 1 month)",
      "Monitor key metrics weekly via automated dashboards (Low impact, ongoing)"
    ],
    "data_points": 5,
    "analysis_text": "### Business Analysis\n#### KEY INSIGHTS\n* Declining Revenue Trend..."
  }
}
```

---

## Implementation Details

### File: `src/core/analyst.py`

**Key Methods:**
```python
class BusinessAnalyst:
    def is_analytical_question(self, question: str) -> bool:
        """Detect if question is vague business problem vs. data query"""
        # Check keywords and phrases
        
    def analyze(self, question: str) -> Dict[str, Any]:
        """5-stage intelligent analysis pipeline"""
        # Stage 1: Interpret problem
        problem_breakdown = self._interpret_problem(question)
        
        # Stage 2: Generate custom queries
        query_plan = self._plan_data_gathering(question, problem_breakdown)
        
        # Stage 3: Execute queries
        data_context = self._execute_query_plan(query_plan)
        
        # Stage 4: Deep analysis
        analysis = self._generate_deep_analysis(question, problem_breakdown, data_context)
        
        # Stage 5: Return with recommendations
        return analysis
    
    def _interpret_problem(self, question: str) -> Dict:
        """AI generates hypotheses and focus areas"""
        
    def _plan_data_gathering(self, question, problem_breakdown) -> List[Dict]:
        """AI generates custom SQL queries (3-5)"""
        
    def _execute_query_plan(self, query_plan) -> List[Dict]:
        """Run all custom queries and gather results"""
        
    def _generate_deep_analysis(self, question, problem_breakdown, data_context) -> Dict:
        """AI synthesizes insights and recommendations"""
```

---

## Testing

### Test Script: `test_intelligent_analyst.py`

**Verifies all 5 stages:**
```bash
cd "/Volumes/Extreme SSD/code/sql schema"
.venv/bin/python3 test_intelligent_analyst.py
```

**Expected Output:**
```
🧠 INTELLIGENT BUSINESS ANALYST TEST
📝 VAGUE BUSINESS PROBLEM: "My business performance is poor and I need help"

📋 STAGE 1: PROBLEM INTERPRETATION
   Generated 3 hypotheses:
   1. Inadequate sales strategies...
   2. Poor customer service...
   3. Inefficient inventory management...
   Focus areas: sales, customers, products, inventory, marketing, finance

⚙️  STAGE 2: CUSTOM QUERY GENERATION
   AI generated 5 targeted SQL queries:
   1. revenue_trend
   2. customer_churn
   3. product_performance
   4. inventory_stockout
   5. customer_satisfaction

📊 STAGE 3: DATA ANALYSIS
   Analyzed 5 key metrics

💡 STAGE 4: KEY INSIGHTS (4 discovered)
   1. Declining Revenue Trend...
   2. Customer Churn...
   3. Product Performance Disparity...
   4. Inventory Stockout Risk...

🎯 STAGE 5: ACTIONABLE RECOMMENDATIONS (8 steps)
   1. Optimize marketing spend (High impact)
   2. Implement real-time inventory tracking (High impact)
   ...

✅ INTELLIGENT ANALYST CAPABILITIES VERIFIED
🎉 SYSTEM IS PRODUCTION-READY FOR VAGUE BUSINESS PROBLEMS!
```

---

## Comparison: Before vs. After

### Before (Fixed Queries)
❌ User: "My sales are declining"  
❌ System: Runs same 5 exploratory queries regardless of problem  
❌ Analysis: Generic insights not specific to the problem  
❌ Recommendations: Vague suggestions  

### After (Intelligent Problem-Solving)
✅ User: "My sales are declining"  
✅ System: Interprets problem → "Sales performance issue"  
✅ Generates: Custom queries to analyze sales trends, customer behavior, product performance  
✅ Analysis: Specific insights about WHY sales are declining  
✅ Recommendations: Actionable steps to fix the identified root causes  

---

## Limitations

1. **Groq Rate Limits** - Free tier: 100K tokens/day per organization (not per key)
   - System automatically falls back to Gemini when Groq exhausted
   - Multiple Groq accounts can increase capacity

2. **Query Complexity** - AI-generated queries limited to available schema
   - System uses schema context (cached) for query generation
   - Cannot query data that doesn't exist in the database

3. **Analysis Depth** - Limited by LLM context window
   - System samples data if results are too large (head + tail)
   - May miss nuances in very large datasets

4. **Recommendation Quality** - Depends on data quality
   - Incomplete or missing data → less specific recommendations
   - System includes data gaps in analysis

---

## Future Enhancements

### Planned (v3.3.0)
- [ ] **Follow-up Questions** - System asks clarifying questions if problem is too vague
- [ ] **Multi-Database Analysis** - Analyze across multiple databases simultaneously
- [ ] **Recommendation Tracking** - Track which recommendations were implemented and their impact
- [ ] **A/B Testing** - Compare different problem-solving strategies

### Considered
- [ ] **Visual Analytics** - Generate charts/graphs for insights
- [ ] **Report Export** - Export analysis as PDF or PowerPoint
- [ ] **Scheduled Analysis** - Run analysis on schedule (weekly/monthly)
- [ ] **Historical Comparison** - Compare current problem to past similar situations

---

## Related Documentation

- [Natural Language Querying](natural-language.md) - Standard SQL generation
- [AI Insights](charts-insights.md) - Chart detection and trend analysis
- [System Architecture](../02-architecture/system-overview.md) - Overall system design
- [API Reference](../05-api/endpoints.md) - API endpoints

---

**Questions?** See [Getting Started](../01-getting-started/quickstart.md) or [Development Guide](../04-development/setup.md)
