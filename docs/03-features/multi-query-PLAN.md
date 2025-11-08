# Multi-Query Support Implementation Plan

**Feature**: Execute multiple SQL queries to answer complex questions  
**Status**: 📋 Planning Phase  
**Created**: 2025-11-06  
**Target**: v1.4.0

---

## Problem Statement

Currently, Memova executes **one SQL query per question**. Many business questions require **multiple queries** to answer properly:

### Examples Requiring Multi-Query Support

1. **Comparative Analysis**
   - "Compare Q1 vs Q2 sales" → 2 queries (Q1 data + Q2 data)
   - "Revenue by department vs budget" → 2 queries (actual + budget)

2. **Cross-Table Analysis**
   - "Top products and their reviews" → 2 queries (products + reviews)
   - "Customers who never ordered" → 2 queries (all customers - active customers)

3. **Calculated Metrics**
   - "Retention rate" → 2+ queries (new users, returning users, churn calculation)
   - "Customer lifetime value" → 3+ queries (orders, payments, segments)

4. **Multi-Step Aggregations**
   - "Departments with above-average salary" → 2 queries (avg salary + filtered departments)
   - "Month-over-month growth rate" → 2 queries (current month, previous month)

---

## Current Architecture (Single Query)

```
User Question → Groq/Gemini AI → Single SQL → Execute → Results → Summarize → Answer
```

**Limitations**:
- Cannot compare data from different time periods
- Cannot join across unrelated table sets
- Cannot perform multi-step calculations
- Cannot handle conditional logic requiring intermediate results

---

## Proposed Architecture (Multi-Query)

```
User Question 
  → Groq/Gemini AI 
  → Query Plan (1-N queries with dependencies)
  → Execute queries sequentially/parallel
  → Aggregate results
  → Summarize all results
  → Combined Answer
```

**Benefits**:
- Handle complex comparative questions
- Support multi-step business logic
- Enable calculated metrics (ratios, percentages)
- Maintain single user question → single answer UX

---

## Design Options

### Option 1: AI-Generated Query Plan (RECOMMENDED)
**Approach**: Ask AI to generate a **query plan** with multiple SQL statements

**AI Prompt**:
```
You are a SQL analyst. Generate a query plan to answer: "{question}"

Return JSON with this structure:
{
  "queries": [
    {
      "id": "q1",
      "description": "Fetch Q1 sales data",
      "sql": "SELECT ...",
      "depends_on": []
    },
    {
      "id": "q2", 
      "description": "Fetch Q2 sales data",
      "sql": "SELECT ...",
      "depends_on": []
    },
    {
      "id": "q3",
      "description": "Compare Q1 vs Q2",
      "sql": "SELECT q1.total, q2.total FROM q1, q2",
      "depends_on": ["q1", "q2"]
    }
  ],
  "final_query_id": "q3"
}
```

**Pros**:
- Leverages AI to decompose complex questions
- AI handles dependency resolution
- Flexible (AI decides how many queries needed)
- No hardcoded rules

**Cons**:
- Requires robust JSON parsing
- AI might generate incorrect plans
- Higher token usage (longer prompts)

---

### Option 2: Iterative Refinement
**Approach**: Execute one query, check if answer is complete, generate next query if needed

**Flow**:
```
1. Generate SQL for question
2. Execute query
3. Ask AI: "Is this answer complete? Need more data?"
4. If incomplete → Generate next SQL
5. Repeat until complete
```

**Pros**:
- Adaptive (queries as needed)
- Simpler prompt structure
- AI self-corrects

**Cons**:
- Multiple AI round-trips (slower)
- Hard to know when to stop
- Unpredictable latency

---

### Option 3: Hardcoded Patterns
**Approach**: Detect question patterns and apply multi-query templates

**Example**:
```python
if "compare" in question and "vs" in question:
    # Pattern: "Compare X vs Y"
    return [
        "SELECT ... WHERE category='X'",
        "SELECT ... WHERE category='Y'"
    ]
```

**Pros**:
- Fast (no AI for planning)
- Predictable
- Debuggable

**Cons**:
- Limited flexibility
- Requires maintenance
- Misses edge cases

---

## Recommended Approach: **Option 1 (AI-Generated Query Plan)**

### Why?
1. **Leverage AI Strengths**: AI is good at decomposing problems
2. **Scalable**: No pattern maintenance
3. **User-Friendly**: Works for any complex question
4. **Testable**: Query plans are inspectable/debuggable

### Implementation Strategy
1. **Phase 1**: Single AI call generates full query plan
2. **Phase 2**: Execute queries in dependency order
3. **Phase 3**: Combine results and summarize
4. **Phase 4**: Frontend displays aggregated answer

---

## Technical Changes Required

### 1. Backend Changes

#### A. New Data Structures (`src/core/query_plan.py`) - NEW FILE
```python
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class QueryStep:
    """Represents one query in a multi-query plan"""
    id: str  # e.g., "q1", "q2"
    description: str  # Human-readable purpose
    sql: str  # SQL statement
    depends_on: List[str]  # IDs of prerequisite queries
    results: Optional[List[Dict[str, Any]]] = None  # Populated after execution

@dataclass
class QueryPlan:
    """Complete multi-query execution plan"""
    queries: List[QueryStep]
    final_query_id: str  # Which query produces the answer
    
    def get_execution_order(self) -> List[QueryStep]:
        """Topological sort by dependencies"""
        pass
```

#### B. Update `SQLGenerator` (`src/core/sql_generator.py`)
```python
class SQLGenerator:
    def generate_query_plan(self, question: str) -> QueryPlan:
        """
        Generate multi-query plan for complex questions
        
        Args:
            question: Natural language question
            
        Returns:
            QueryPlan with 1-N queries
        """
        # Build prompt for query planning
        prompt = f"""
        You are a SQL analyst. Analyze this question and create a query plan.
        
        Question: {question}
        Schema: {self.schema_text}
        
        For simple questions, return 1 query.
        For complex questions (comparisons, calculations), return multiple queries.
        
        Return JSON:
        {{
          "queries": [
            {{"id": "q1", "description": "...", "sql": "...", "depends_on": []}}
          ],
          "final_query_id": "q1"
        }}
        """
        
        response = self.llm_client.generate_content(prompt)
        plan_json = self._extract_json(response)
        return QueryPlan.from_dict(plan_json)
```

#### C. Update `QueryEngine` (`src/core/query_engine.py`)
```python
class QueryEngine:
    def ask_with_plan(self, question: str) -> Dict[str, Any]:
        """
        Execute multi-query plan to answer question
        
        Returns:
            {
                'success': True,
                'question': str,
                'plan': QueryPlan,
                'results': {...},  # Final query results
                'all_results': {...},  # All intermediate results
                'execution_time': float
            }
        """
        # 1. Generate query plan
        plan = self.sql_generator.generate_query_plan(question)
        
        # 2. Execute queries in dependency order
        executed_results = {}
        for query_step in plan.get_execution_order():
            # Substitute results from dependent queries
            sql = self._substitute_dependencies(
                query_step.sql, 
                executed_results, 
                query_step.depends_on
            )
            
            # Execute query
            result = self.db_manager.execute_query(sql)
            executed_results[query_step.id] = result
            query_step.results = result
        
        # 3. Return final query results
        final_result = executed_results[plan.final_query_id]
        
        return {
            'success': True,
            'question': question,
            'plan': plan,
            'results': final_result,
            'all_results': executed_results,
            'execution_time': time.time() - start_time
        }
```

#### D. Update API Routes (`api/routes.py`)
```python
@router.post("/ask", response_model=AskResponse)
async def ask_query(request: AskRequest):
    """
    Execute natural language query (supports multi-query plans)
    """
    engine = QueryEngine(db_path=db_path)
    
    # Generate and execute query plan
    result = engine.ask_with_plan(request.question)
    
    # Get final results
    columns = result['results']['columns']
    rows = result['results']['rows']
    
    # Summarize with context from all queries
    answer_text = summarize_result_with_plan(
        question=request.question,
        plan=result['plan'],
        final_results=(columns, rows),
        all_results=result['all_results']
    )
    
    return AskResponse(
        answer_text=answer_text,
        sql=result['plan'].queries[-1].sql,  # Show final SQL
        sql_plan=result['plan'].to_dict(),  # NEW: Include full plan
        columns=columns,
        rows=rows,
        timings={'planMs': ..., 'execMs': ...}
    )
```

#### E. Update Pydantic Models (`api/models.py`)
```python
class QueryStepModel(BaseModel):
    """Single query in a multi-query plan"""
    id: str
    description: str
    sql: str
    depends_on: List[str]
    row_count: Optional[int] = None

class AskResponse(BaseModel):
    answer_text: str
    sql: str  # Final SQL (backward compatible)
    sql_plan: Optional[List[QueryStepModel]] = None  # NEW: Multi-query plan
    columns: List[str]
    rows: List[List[Any]]
    charts: Optional[List[ChartConfig]] = None
    trends: Optional[List[TrendInsight]] = None
    timings: Optional[Dict[str, float]] = None
```

---

### 2. Frontend Changes

#### A. Update TypeScript Types (`frontend/src/lib/api.ts`)
```typescript
export interface QueryStep {
  id: string;
  description: string;
  sql: string;
  depends_on: string[];
  row_count?: number;
}

export type AskResponse = {
  answer_text: string;
  sql: string;  // Final SQL
  sql_plan?: QueryStep[] | null;  // NEW: Multi-query plan
  columns: string[];
  rows: (string | number | null)[][];
  charts?: ChartConfig[] | null;
  trends?: TrendInsight[] | null;
  timings?: Record<string, number>;
  meta?: Record<string, any>;
};
```

#### B. Update AnswerPanel (`frontend/src/components/results/answer-panel.tsx`)
```tsx
// Show multi-query plan if present
{res.sql_plan && res.sql_plan.length > 1 && (
  <Card className="mt-4">
    <CardHeader>
      <CardTitle className="flex items-center gap-2">
        <Layers className="h-5 w-5" />
        Query Plan ({res.sql_plan.length} steps)
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="space-y-2">
        {res.sql_plan.map((step, idx) => (
          <div key={step.id} className="flex items-start gap-3">
            <Badge variant="outline">{idx + 1}</Badge>
            <div>
              <div className="font-medium">{step.description}</div>
              <code className="text-xs text-muted-foreground">
                {step.sql}
              </code>
              {step.row_count && (
                <div className="text-xs text-muted-foreground">
                  → {step.row_count} rows
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </CardContent>
  </Card>
)}
```

---

### 3. Testing Strategy

#### A. Unit Tests (`tests/unit/test_query_plan.py`) - NEW FILE
```python
def test_simple_query_generates_single_step():
    """Test: 'Count employees' → 1-query plan"""
    pass

def test_comparison_generates_multi_step():
    """Test: 'Compare Q1 vs Q2 sales' → 2+ query plan"""
    pass

def test_dependency_resolution():
    """Test: Queries execute in correct order"""
    pass

def test_result_substitution():
    """Test: Later queries use earlier results"""
    pass
```

#### B. Integration Tests (`tests/integration/test_multi_query.py`) - NEW FILE
```python
def test_ask_endpoint_handles_multi_query():
    """Test: /ask endpoint with multi-query plan"""
    response = client.post("/ask", json={
        "question": "Compare November and December sales",
        "company_id": "electronics"
    })
    
    assert response.json()['sql_plan'] is not None
    assert len(response.json()['sql_plan']) >= 2
```

---

### 4. Documentation Updates

#### A. Create Feature Doc (`docs/03-features/multi-query.md`) - NEW
- Purpose & use cases
- Architecture diagram
- Example query plans
- Limitations

#### B. Update System Overview (`docs/02-architecture/system-overview.md`)
- Add "Multi-Query Execution Flow" section
- Update data flow diagram
- Document QueryPlan data structure

#### C. Update API Endpoints (`docs/05-api/endpoints.md`)
- Document new `sql_plan` field in AskResponse
- Add examples with multi-query responses

#### D. Update Copilot Instructions (`.github/copilot-instructions.md`)
- Add multi-query to Recent Enhancements
- Update architecture summary

---

## Migration Strategy

### Phase 1: Backward-Compatible Single Query (Week 1)
- Add `QueryPlan` data structure (default: 1 query)
- Update `QueryEngine.ask()` to use plans internally
- **No frontend changes**
- Test with existing queries

### Phase 2: Multi-Query Generation (Week 2)
- Implement `generate_query_plan()` with AI
- Test with comparative questions
- **Still single-query fallback**

### Phase 3: Frontend Display (Week 3)
- Add `sql_plan` display in AnswerPanel
- Show query execution steps
- Add loading states for multi-step execution

### Phase 4: Production Rollout (Week 4)
- Enable multi-query by default
- Monitor performance (latency, token usage)
- Gather user feedback

---

## Performance Considerations

### Latency
- **Single Query**: ~2s (1.5s AI + 0.5s DB)
- **Multi-Query (3 steps)**: ~3-4s (2s planning + 3×0.5s DB)
- **Mitigation**: Parallel execution where no dependencies

### Token Usage
- **Current**: ~500 tokens per query
- **Multi-Query**: ~800 tokens (plan) + 300 per step
- **Cost**: Still within free tier limits

### Caching
- Cache query plans for identical questions
- Cache intermediate results for 5 minutes

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| AI generates invalid plans | High | Fallback to single-query mode |
| Circular dependencies | Medium | Validate plan before execution |
| Increased latency | Medium | Show progress indicator, parallel execution |
| Higher token costs | Low | Monitor usage, implement caching |
| Complex debugging | Medium | Log full plan, add debug endpoint |

---

## Success Metrics

1. **Functionality**: 80% of comparative questions return multi-query plans
2. **Accuracy**: 95% of multi-query results are correct
3. **Performance**: <5s latency for 3-query plans
4. **User Satisfaction**: Positive feedback on complex questions

---

## Open Questions

1. **Max Queries**: Limit to 5 queries per plan?
2. **Parallel Execution**: Worth the complexity?
3. **Result Caching**: How long to cache intermediate results?
4. **UI Display**: Show all query steps or just final SQL?
5. **Error Handling**: Retry individual failed queries?

---

## Next Steps

1. ✅ Create this planning document
2. ⬜ Review with stakeholders
3. ⬜ Prototype `QueryPlan` data structure
4. ⬜ Test AI prompt for plan generation
5. ⬜ Implement Phase 1 (backward-compatible)
6. ⬜ Write tests
7. ⬜ Update documentation
8. ⬜ Deploy to production

---

**Status**: 📋 Planning Complete - Ready for Implementation  
**Estimated Effort**: 3-4 weeks  
**Version**: 1.4.0  
**Created**: 2025-11-06
