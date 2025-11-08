# System Architecture Overview

**Last Updated**: November 6, 2025  
**Version**: 3.2.0

---

## High-Level Architecture

```
┌──────────────┐
│    Browser   │  User asks question in natural language
│ (localhost:  │  ↓
│    3000)     │  "How many employees are there?"
└──────┬───────┘
       │ HTTP POST /query
       ↓
┌──────────────┐
│   FastAPI    │  Receives question + database context
│ (localhost:  │  ↓
│    8000)     │  Sends to Groq AI (primary) for SQL generation
└──────┬───────┘
       │ AI Request (with caching)
       ↓
┌──────────────┐
│  Groq AI     │  Generates SQL query (llama-3.3-70b-versatile)
│  (Cloud)     │  ↓ (Schema cached, only question sent on 2+ requests)
│              │  "SELECT COUNT(*) FROM employees"
│  CACHE: 98%  │  ↓ (Falls back to Gemini on error)
│  token save  │
└──────┬───────┘
       │ SQL Response
       ↓
┌──────────────┐
│  SQLite DB   │  Executes query
│  (Local)     │  ↓
└──────┬───────┘  Returns results
       │
       ↓
┌──────────────┐
│   Frontend   │  Displays natural language answer
│   (React)    │  + collapsible SQL and data tables
└──────────────┘
```

---

## Technology Stack

### Frontend
- **Framework**: Next.js 16.0.1 (App Router, Turbopack)
- **UI Library**: React 19 with TypeScript 5
- **Styling**: Tailwind CSS 4
- **Components**: shadcn/ui (13+ components)
- **Animations**: Framer Motion
- **State Management**: Zustand
- **Theme**: next-themes (dark/light mode)
- **Fonts**: Geist Sans & Geist Mono

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite 3
- **AI Service**: 
  - **Primary**: Groq (`llama-3.3-70b-versatile`) - 100K tokens/day per organization
    - **Prompt Caching**: 40-50% faster, 98% token reduction (51x capacity increase)
  - **Fallback**: Google Gemini 2.0 Flash (`gemini-2.0-flash-exp`) - 550 req/day with 11 keys
  - **Failover**: Automatic Groq→Gemini on any error
- **ORM**: Direct SQL (no ORM for simplicity)
- **Validation**: Pydantic v2

### Infrastructure
- **Ports**: 3000 (frontend), 8000 (backend)
- **Process Manager**: Make commands
- **Logging**: Python logging module
- **Configuration**: .env file (python-dotenv)
- **Databases**: 3 SQLite databases (electronics_company.db, airline_company.db, edtech_company.db)

---

## Data Flow
### Sidebar Quick Query Shortcuts (v3.0.0)

The sidebar provides grouped quick query buttons (Easy/Medium/Hard) with icons and color badges. Clicking a button dispatches a custom event to the AskBar, which runs the query and displays results. This enables one-click access to common business questions.

**UI Flow Diagram:**

```
Sidebar → Quick Query Button → AskBar (dispatch event) → Backend → Groq/Gemini AI → SQL → SQLite → Results → AnswerPanel
```

### Query Execution Flow (Modern /ask Endpoint)

```
1. USER INPUT
   ├─ User types: "How many employees?"
   └─ Click "Ask" or press Enter

2. FRONTEND PROCESSING
   ├─ Validate input (non-empty)
   ├─ Get current company from Zustand store
   ├─ POST to /ask with { question, company_id, section_ids }
   └─ Show loading state with animation

3. BACKEND PROCESSING - SQL GENERATION (WITH CACHING 🚀)
   ├─ Receive request
   ├─ Validate database ID
   ├─ Load database schema
   ├─ Send to AI (UnifiedLLMClient):
   │  ├─ Try Groq AI first (llama-3.3-70b-versatile, 100K tokens/day)
   │  ├─ **Prompt Caching**: Schema as system message (static, cached)
   │  │  └─ First request: ~2500 tokens (caches schema for ~hours)
   │  │  └─ Subsequent: ~50 tokens (just question, 98% reduction)
   │  ├─ On ANY Groq error → Fallback to Gemini (11 keys, 550 req/day)
   │  ├─ System prompt (schema + instructions) → CACHED by Groq
   │  └─ User question → Fresh each time
   ├─ Receive SQL from AI (tracks which provider succeeded)
   ├─ Clean & validate SQL
   └─ Track generation time (genMs: ~0.35s cached, ~0.66s cold)

4. AI PROCESSING - SQL GENERATION (Groq with Caching)
   ├─ Analyze schema (from cache if available)
   ├─ Understand question
   ├─ Generate SQL query
   ├─ Automatic retry on rate limits (429)
   ├─ Cache hit: 40-50% faster (0.35s vs 0.66s)
   └─ Return SQL string

5. DATABASE EXECUTION
   ├─ Parse SQL
   ├─ Server-side guardrails (DatabaseManager):
   │  ├─ Check if query is SELECT (vs PRAGMA, EXPLAIN, etc.)
   │  ├─ If SELECT without LIMIT → append LIMIT 100 (default)
   │  ├─ If SELECT with LIMIT → cap to MAX_QUERY_RESULTS (1000)
   │  └─ Non-SELECT queries bypass LIMIT enforcement
   ├─ Execute query against SQLite
   ├─ Fetch results (columns + rows)
   ├─ Track execution time (execMs)
   └─ Return rows + metadata

6. BACKEND PROCESSING - RESULT ANALYSIS ✨ ENHANCED
   ├─ Result Summarization (summarizer.py):
   │  ├─ Compute numeric aggregates (sum, mean, min, max)
   │  ├─ Identify categorical columns (low cardinality)
   │  ├─ Detect time columns for trends
   │  ├─ Intelligent sampling (head + tail for large datasets)
   │  ├─ Send to AI (UnifiedLLMClient):
   │  │  ├─ Try Groq AI first (llama-3.3-70b-versatile)
   │  │  ├─ On error → Gemini fallback (11 keys)
   │  │  ├─ Business analyst prompt
   │  │  └─ Automatic retry on rate limits
   │  └─ Receive natural language summary (tracks provider used)
   │
   ├─ Chart Detection (chart_detector.py + ai_chart_selector.py): 🎨 NEW
   │  ├─ AI-powered selection (primary):
   │  │  ├─ Analyze data summary (types, cardinality, sample values)
   │  │  ├─ Consider question context
   │  │  ├─ Decide: Should we visualize? (yes/no)
   │  │  ├─ If yes: Select best chart type (bar/pie/line/histogram)
   │  │  ├─ Generate chart config (x/y columns, data, title)
   │  │  └─ AI reasoning logged for debugging
   │  │
   │  └─ Heuristic fallback (if AI fails):
   │     ├─ Time series detection → Line charts
   │     ├─ Categorical aggregation → Bar/Pie charts
   │     ├─ Numeric distribution → Histograms
   │     └─ Return chart config or null
   │
   └─ Trend Detection (trend_detector.py): 📊 NEW
      ├─ Column analysis (temporal, numeric, categorical)
      ├─ Time series trend detection:
      │  ├─ Monotonic growth/decline patterns
      │  ├─ Growth rate calculation
      │  └─ Confidence scoring (0.0-1.0)
      ├─ Categorical outlier detection:
      │  ├─ Z-score calculation (|z| > 2.0)
      │  ├─ High/low outlier identification
      │  └─ Statistical significance
      ├─ Numeric distribution analysis:
      │  ├─ Quartile calculation (Q1, median, Q3)
      │  ├─ Range and spread insights
      │  └─ Concentration patterns
      └─ Return insights array with severity levels

7. AI PROCESSING - ANALYSIS (Groq/Gemini)
   ├─ SQL Generation: Groq (primary) → Gemini (fallback)
   ├─ Result Summarization: Groq (primary) → Gemini (fallback)
   ├─ Chart Selection: Groq (primary) → Gemini (fallback) → Heuristics
   └─ Performance: <50ms (charts/trends), 800-2000ms (SQL/summary)

8. RESPONSE FORMATTING
   ├─ answer_text: Natural language summary (paragraph + bullets)
   ├─ sql: Generated SQL query
   ├─ columns: Column names
   ├─ rows: Result data
   ├─ timings: { genMs, execMs }
   └─ meta: { row_count }

9. FRONTEND RENDERING
   ├─ Display natural language answer in HERO CARD (primary)
   ├─ SQL in collapsible accordion
   ├─ Data table in collapsible accordion
   └─ Timings badges (generation + execution)
```

### Error Handling & Resilience

**API Key Rotation** (Both SQL Generation & Summarization):
- 11 Google Gemini API keys configured
- Automatic rotation on rate limit (429) errors
- Total capacity: 550 requests/day (50/day × 11 keys)
- Detailed logging of rotation events

**Retry Logic**:
- SQL Generation: Up to 3 retries per key with exponential backoff
- Summarization: Up to 3 retries per key with exponential backoff
- Rate limits trigger immediate key rotation
- Other errors trigger retry with backoff (1.5s, 3s, 4.5s)

**Graceful Degradation**:
- If SQL generation fails: Return error to user
- If summarization fails: Return enhanced fallback message with data preview
- Users always receive valid SQL + complete results
- Fallback messages are informative, not generic

---
   ├─ Data table in collapsible accordion
   └─ Animate entrance with Framer Motion
```

---

## Component Architecture

### Frontend Structure

```
frontend/src/
├── app/
│   ├── layout.tsx          ← Root layout (theme provider)
│   ├── page.tsx            ← Home page (ask bar + results)
│   └── globals.css         ← Global styles + theme variables
├── components/
│   ├── layout/
│   │   ├── navbar.tsx      ← Top navigation
│   │   ├── sidebar.tsx     ← Company/section selector
│   │   └── app-shell.tsx   ← Layout wrapper
│   ├── query/
│   │   └── ask-bar.tsx     ← Question input + examples
│   ├── results/
│   │   └── answer-panel.tsx ← NL answer + accordions
│   ├── settings/
│   │   └── settings-dialog.tsx ← Preferences dialog
│   └── ui/                 ← shadcn components
├── lib/
│   ├── api.ts              ← API client functions
│   ├── scope.ts            ← Zustand store (company/sections)
│   ├── settings.ts         ← User preferences (localStorage)
│   └── utils.ts            ← Utilities (cn helper)
└── data/
    └── companies.ts        ← Company metadata + examples
```

### Backend Structure

```
src/
├── core/
│   ├── database.py          ← DatabaseManager class (215 lines)
│   ├── api_key_manager.py   ← API key rotation & failover (200 lines) ✨ NEW
│   ├── gemini_client.py     ← Gemini AI client wrapper (140 lines) ✨ NEW
│   ├── sql_generator.py     ← SQL generation & prompts (220 lines) ✨ NEW
│   ├── query_engine.py      ← Orchestrator (250 lines) ✨ REFACTORED
│   └── summarizer.py        ← Result summarization (153 lines)
├── data/
│   ├── generators.py        ← Electronics data generation (411 lines)
│   ├── airline_generators.py ← Airline data generation (684 lines)
│   ├── converters.py        ← Excel → SQLite conversion (160 lines)
│   ├── schema.py            ← Schema generation (278 lines)
│   ├── electronics/         ← (Planned: modular generators)
│   └── airline/             ← (Planned: modular generators)
├── utils/
│   ├── config.py            ← Configuration loading (121 lines)
│   ├── logger.py            ← Logging setup (52 lines)
│   ├── llm.py               ← Gemini client wrapper (84 lines)
│   └── exceptions.py        ← Custom exceptions (38 lines)
└── cli/
    └── query_cli.py         ← CLI interface (194 lines)

api/
├── main.py                  ← FastAPI app initialization (44 lines) ✨ REFACTORED
├── models.py                ← Pydantic request/response models (72 lines) ✨ NEW
└── routes.py                ← Route handlers (336 lines) ✨ NEW
```

**Recent Changes** (October 31, 2025):

**🔧 Core Module Refactoring** (Major improvement):
- ✅ **QueryEngine Refactored**: Split monolithic `query_engine.py` (614 lines) into 4 modular components
  - `api_key_manager.py`: API key rotation & failover logic (200 lines)
  - `gemini_client.py`: Gemini AI client management (140 lines)
  - `sql_generator.py`: SQL generation & prompt engineering (220 lines)
  - `query_engine.py`: Orchestrator following SOLID principles (250 lines, -59%)
- ✨ **Benefits**: 
  - Single Responsibility Principle applied
  - Easier testing (mock individual components)
  - Better maintainability (smaller, focused modules)
  - Reusability (APIKeyManager can be used elsewhere)
  - Zero breaking changes (100% backward compatible)

**🌐 API Module Refactoring**:
- ✅ **API Refactored**: Split monolithic `api/main.py` (498 lines) into 3 focused modules
  - `main.py`: FastAPI app + middleware (44 lines)
  - `models.py`: Pydantic models (72 lines)
  - `routes.py`: Route handlers (336 lines)
- ✨ **Benefits**: Better separation of concerns, improved maintainability, enhanced testability

---

## Modular Architecture (QueryEngine)

### Before Refactoring
The original `query_engine.py` was a monolithic 614-line file with mixed responsibilities:
- API key rotation logic
- Gemini AI client initialization
- SQL generation and prompt engineering
- Query execution and result formatting

### After Refactoring
Split into 4 focused modules following **Single Responsibility Principle**:

#### 1. **APIKeyManager** (`api_key_manager.py`)
```python
class APIKeyManager:
    """Manages API key rotation for Google Gemini"""
    
    # Singleton pattern with class-level state
    _all_api_keys: List[str] = []
    _current_key_index: int = 0
    _failed_keys: Set[str] = set()
```

**Responsibilities**:
- Load all 11 API keys from `.env` (including commented ones)
- Automatic rotation on rate limit (429) errors
- Track failed keys to avoid retry loops
- Detect rate limit errors via `is_rate_limit_error()`

**Key Methods**:
- `get_current_key()` - Returns active API key
- `rotate_key()` - Switches to next available key
- `reset_failed_keys()` - Reset after quota refresh

#### 2. **GeminiClient** (`gemini_client.py`)
```python
class GeminiClient:
    """Wrapper for Google Gemini AI client"""
    
    def __init__(self, api_key_manager: APIKeyManager):
        self.api_key_manager = api_key_manager
        self.model: GenerativeModel
```

**Responsibilities**:
- Initialize connection to Google Gemini API
- Auto-detect best available model (prefers `gemini-2.0-flash-exp`)
- Reinitialize after API key rotation

**Key Methods**:
- `get_model()` - Returns configured GenerativeModel
- `reinitialize()` - Reconnect with new API key
- `_get_best_model()` - Auto-detect available models

#### 3. **SQLGenerator** (`sql_generator.py`)
```python
class SQLGenerator:
    """Natural language to SQL query generator"""
    
    def __init__(self, schema_text: str, gemini_client: GeminiClient,
                 api_key_manager: APIKeyManager):
        self.schema_text = schema_text
        self.gemini_client = gemini_client
        self.api_key_manager = api_key_manager
```

**Responsibilities**:
- Generate SQL from natural language questions
- Build optimized prompts with schema context
- Clean and validate generated SQL
- Retry logic with automatic key rotation

**Key Methods**:
- `generate(question)` - Main entry point for SQL generation
- `_create_prompt(question)` - Build context-aware prompts
- `_clean_sql(sql)` - Remove markdown, normalize whitespace

#### 4. **QueryEngine** (`query_engine.py`) - Orchestrator
```python
class QueryEngine:
    """Natural language to SQL query engine - Orchestrator"""
    
    def __init__(self, db_manager=None, db_path=None):
        self.api_key_manager = APIKeyManager()
        self.gemini_client = GeminiClient(self.api_key_manager)
        self.sql_generator = SQLGenerator(...)
        self.db_manager = db_manager or DatabaseManager()
```

**Responsibilities**:
- Coordinate all components (delegation pattern)
- Provide unified public API
- Maintain backward compatibility

**Public API** (unchanged):
- `ask(question)` - Main entry point
- `generate_sql(question)` - Generate SQL only
- `execute_query(sql)` - Execute SQL only
- `get_schema_info()` - Get database schema
- `get_available_tables()` - List tables
- `validate_query(sql)` - Validate without executing

### Benefits of Refactoring

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Main file size | 614 lines | 250 lines | **-59%** |
| Longest method | ~90 lines | ~40 lines | **-56%** |
| Cyclomatic complexity | ~25 | ~8 | **-68%** |
| Test structure | 77 tests | 77 tests | **0 regressions** |

**Advantages**:
- ✅ **Testability**: Mock `APIKeyManager`, `GeminiClient` independently
- ✅ **Maintainability**: Find/modify specific logic faster
- ✅ **Reusability**: `APIKeyManager` can be used by other services
- ✅ **Readability**: 250 lines vs 614 lines in main orchestrator
- ✅ **Backward Compatible**: Zero breaking changes to public API

---

## Key Design Decisions

### 1. Answer-First UX
**Decision**: Display natural language answer prominently, hide SQL/data in accordions  
**Rationale**: End users care about answers, not implementation details  
**Trade-off**: Power users need one click to see SQL

### 2. Multi-Database via Zustand
**Decision**: Client-side state management for company/section selection  
**Rationale**: Fast switching without page reloads, persistent in localStorage  
**Trade-off**: State not server-managed (requires client JS)

### 3. SQLite over Postgres
**Decision**: Use SQLite for local databases  
**Rationale**: Zero configuration, portable, perfect for demo/development  
**Trade-off**: Single-writer limitation (acceptable for read-heavy queries)

### 4. Direct SQL (No ORM)
**Decision**: Execute raw SQL queries from AI  
**Rationale**: ORMs add complexity, AI generates SQL anyway  
**Trade-off**: Manual SQL sanitization required

### 5. API Key Rotation
**Decision**: Rotate through 7 Google API keys on 429 errors  
**Rationale**: Free tier limit is 10 req/min per key → 70 req/min total  
**Trade-off**: Requires managing multiple keys

### 6. Framer Motion Animations
**Decision**: Add entrance animations to answer panel  
**Rationale**: Professional feel, visual feedback on state changes  
**Trade-off**: Slight performance overhead (acceptable)

### 7. Settings in localStorage
**Decision**: Persist user preferences in browser localStorage  
**Rationale**: No backend user management needed  
**Trade-off**: Not synced across devices

---

## Data Model

### Company Structure

```typescript
interface Company {
  id: 'electronics' | 'airline';
  name: string;
  description: string;
  icon: string;
  database: string;  // Path to .db file
  sections: Section[];
  examples: string[];
}

interface Section {
  id: string;
  name: string;
  description: string;
  tables: string[];
}
```

### Query Request/Response

```typescript
// Request
interface QueryRequest {
  question: string;
  database: 'electronics' | 'airline';
}

// Response
interface QueryResponse {
  success: boolean;
  sql: string;
  columns: string[];
  rows: any[][];
  row_count: number;
  execution_time: number;
  error?: string;
}
```

---

## Intelligent Business Analyst Architecture 🧠 NEW v3.2.0

### Overview

The intelligent analyst handles **vague business problems** that require exploratory analysis rather than single SQL queries. It transforms questions like "My revenue is low" into comprehensive business insights.

**Detection**: 27 keywords trigger analytical mode:
- Analysis-focused: `insight`, `insights`, `analyze`, `analysis`, `recommend`, `improve`, `why`
- Problem-focused: `problem`, `issue`, `challenge`, `solution`, `grow`, `decline`
- Vague problems: "My X is low/high/poor/declining..."

### 5-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│ Stage 1: PROBLEM INTERPRETATION                                 │
├─────────────────────────────────────────────────────────────────┤
│ Input: "My revenue is low"                                      │
│ AI Analysis:                                                    │
│  • Identify focus areas (revenue, customers, products)          │
│  • Generate hypotheses (small customer base, pricing, etc.)     │
│  • Define success metrics                                       │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Stage 2: AI-DRIVEN QUERY PLANNING (WITH SCHEMA AWARENESS) ✨    │
├─────────────────────────────────────────────────────────────────┤
│ Input: Problem + DATABASE SCHEMA (embedded in prompt)           │
│ AI Generates: 3-5 exploratory SQL queries                       │
│  ✅ CRITICAL: Schema sent in BOTH system + user messages        │
│  ✅ Prevents hallucinated table names                           │
│                                                                 │
│ Example queries:                                                │
│  1. "Sales Overview" → COUNT orders, SUM revenue, AVG value     │
│  2. "Customer Overview" → COUNT customers, retention metrics    │
│  3. "Top Products" → Revenue by product, top 10                 │
│  4. "Revenue Trends" → Monthly revenue over last 12 months      │
│  5. "Customer Segments" → High/medium/low value breakdown       │
│                                                                 │
│ Token Impact: 9,701 tokens (vs 4,295 without schema)           │
│ Trade-off: +126% tokens BUT 100% query success (worth it!)     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Stage 3: QUERY EXECUTION WITH ERROR HANDLING                    │
├─────────────────────────────────────────────────────────────────┤
│ For each query:                                                 │
│  • Execute against SQLite                                       │
│  • Track success/failure                                        │
│  • Collect results + errors                                     │
│  • Add status to SQL comments ("✓ 5 rows" or "❌ FAILED")       │
│                                                                 │
│ Meta tracking:                                                  │
│  • queries_succeeded: 5                                         │
│  • queries_failed: 0                                            │
│  • row_count: 251 (combined)                                    │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Stage 4: PATTERN ANALYSIS ACROSS DATA POINTS                    │
├─────────────────────────────────────────────────────────────────┤
│ AI Synthesizes:                                                 │
│  • Cross-query patterns (correlations, contradictions)          │
│  • Statistical significance                                     │
│  • Business context interpretation                             │
│  • Root cause hypotheses                                        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Stage 5: INSIGHTS + RECOMMENDATIONS GENERATION                  │
├─────────────────────────────────────────────────────────────────┤
│ Output:                                                         │
│  • 4-6 key insights (markdown bullets)                          │
│  • 5-7 actionable recommendations                               │
│  • Data points extracted (metrics with categories)              │
│  • Natural language analysis (executive summary)                │
└─────────────────────────────────────────────────────────────────┘
```

### Schema Awareness Fix (2025-11-06) 🔧

**Problem**: AI hallucinating table names (e.g., `customer_feedback`, `sales_orders` that don't exist)

**Root Cause**: 
```python
# OLD: Claimed "use previous context" but no context exists
system_message = "You have the database schema from previous conversation."
```

**Solution**: Embed schema explicitly in BOTH prompts
```python
# NEW: Schema in user message for query planning
user_message = f"""
DATABASE SCHEMA (USE ONLY THESE TABLES):
{self.schema_text}  # Full schema embedded (~2500 tokens)

PROBLEM: {problem}

CRITICAL RULES:
- ONLY use table names that exist in schema above
- DO NOT invent or assume table names
"""

# NEW: Also use system_message_with_schema (not system_message_light)
response = llm_client.generate_content(
    user_message,
    system_message=self.system_message_with_schema  # Schema here too
)
```

**Results**:
- **Before**: 0/5 queries succeeded (all hallucinated tables)
- **After**: 5/5 queries succeeded, 251 rows collected
- **Token Cost**: 4,295 → 9,701 tokens (+126%)
- **Decision**: Accuracy prioritized over token savings

### API Response Structure

**Analytical Query Response**:
```json
{
  "query_type": "analytical",
  "answer_text": "### KEY INSIGHTS\n* Insight 1...\n### RECOMMENDATIONS\n1. ...",
  "sql": "-- Query: Sales Overview\n-- Status: ✓ 1 rows\nSELECT...",
  "columns": ["total_orders", "total_revenue"],
  "rows": [[200, 2910028.14]],
  "analysis": {
    "insights": ["High AOV ($14,550)", "Small customer base (200)"],
    "recommendations": ["Expand acquisition", "Diversify products"],
    "data_points": [{"name": "Total Orders", "value": 200}],
    "queries_used": ["sales_overview", "customer_overview"],
    "success": true
  },
  "meta": {
    "exploratory_queries": 3,
    "queries_succeeded": 3,
    "queries_failed": 0,
    "row_count": 12
  }
}
```

### Fallback UX Enhancements (2025-11-06) 💡

**Data Tab Empty State**:
- Contextual message: "Analysis completed without retrieving raw data"
- Explanation: Why analytical queries might not show tables
- Helpful guidance: Focus on insights tab

**SQL Tab Status Indicators**:
```sql
-- Query: Sales Overview
-- Status: ✓ 5 rows
SELECT COUNT(*) as total_orders...

-- Query: Customer Feedback
-- Status: ❌ FAILED (no such table: customer_feedback)
SELECT * FROM customer_feedback...
```

**Answer Panel Badge**:
- Success: "5/5 queries OK" (green badge)
- Partial: "3/5 queries OK" (yellow badge)
- Shows query success rate at a glance

### Performance Characteristics

- **Total Time**: ~5-6 seconds end-to-end
  - Stage 1 (interpretation): ~1.2s
  - Stage 2 (query planning): ~1.9s (with schema embedding)
  - Stage 3 (execution): ~0.05s per query (0.25s total for 5)
  - Stage 4-5 (analysis): ~1.7s
  
- **Token Usage**: 9,701 per analytical query
  - Schema embedding: ~5,000 tokens (2× for system + user)
  - Problem description: ~500 tokens
  - AI responses: ~4,000 tokens
  - Trade-off: Accuracy (100% success) > token savings

- **Capacity**: With Groq 100K tokens/day
  - ~10 analytical queries/day (vs 39 data queries/day)
  - Each analytical query = ~10 data queries in complexity

### Code Organization

```
src/core/analyst.py (641 lines)
├── BusinessAnalyst class
├── _interpret_problem()        # Stage 1
├── _plan_data_gathering()      # Stage 2 (with schema embedding)
├── _execute_queries()          # Stage 3
├── _analyze_patterns()         # Stage 4
└── _generate_insights()        # Stage 5

api/routes.py (705 lines)
├── /ask endpoint
├── Analytical query detection (27 keywords)
├── Extract query_data from analyst results
├── Combine SQLs with status comments
└── Return analysis + SQL + data

frontend/src/components/results/
├── answer-panel.tsx            # Contextual empty states
├── business-analysis-panel.tsx # Insights rendering
└── insights-panel.tsx          # Trend visualization
```

### Documentation

- **Feature Guide**: [Intelligent Problem-Solving](../03-features/intelligent-problem-solving.md)
- **API Reference**: [/ask Endpoint](../05-api/endpoints.md#post-ask)
- **Maintenance Log**: [Schema Awareness Fix](../07-maintenance/INTELLIGENT_ANALYST_2025-11-06.md)

---

## Security Considerations

### Current Implementation (Development)
- ✅ API keys in .env (not committed)
- ✅ CORS restricted to localhost:3000
- ✅ SQL injection prevented via Gemini AI (generates safe queries)
- ❌ No authentication on API endpoints
- ❌ No rate limiting per user
- ❌ No input sanitization on frontend

### Production Recommendations
- Add API key authentication
- Implement per-user rate limiting
- Add input validation/sanitization
- Use HTTPS for all traffic
- Add SQL query whitelisting
- Log all queries for auditing
- Add CSRF protection
- Restrict CORS to production domain

---

## Performance Characteristics

### Current Metrics
- **Query Response Time**: 1-3 seconds (AI + DB)
  - AI generation: 800ms - 2s
  - SQL execution: 50-200ms
  - Network overhead: 100ms
- **Database Size**: 12 MB total (both databases)
- **Memory Usage**: ~150 MB (backend), ~200 MB (frontend)
- **Concurrent Users**: 10-20 (SQLite limitation)

### Bottlenecks
1. **Google Gemini API latency** (1-2s) - Largest bottleneck
2. **SQLite write locks** - Not an issue for read-only queries
3. **Frontend bundle size** - 1.2 MB (acceptable)

### Optimization Opportunities
- Cache common queries (e.g., "How many employees?")
- Prefetch database schemas
- Use streaming responses for large datasets
- Add pagination for 1000+ row results

---

## Schema Size Limits & Context Window Analysis

### Current Schema Sizes

| Database | Size (Bytes) | Estimated Tokens | % of Context Window |
|----------|--------------|------------------|---------------------|
| Airline (largest) | 8,254 | ~3,301 | 0.33% |
| EdTech | 6,306 | ~2,522 | 0.25% |
| Electronics | 4,235 | ~1,694 | 0.17% |

**Token Estimation Formula**: `tokens ≈ bytes × 0.4` (conservative estimate)

### Maximum Schema Size Capacity

Based on **Gemini 2.0 Flash's 1 million token context window**:

| Limit Type | Size (Bytes) | Size (KB) | % of Context | Multiplier vs Current | Use Case |
|------------|--------------|-----------|--------------|----------------------|----------|
| **Safe Limit** | 250,000 | 244 KB | 10% | 30x | **Recommended for production** |
| **Comfortable Limit** | 500,000 | 488 KB | 20% | 60x | Good balance |
| **Aggressive Limit** | 1,250,000 | 1,220 KB | 50% | 151x | Maximum theoretical |

### Practical Capacity Estimates

**Safe Limit (250 KB)**:
- **50-60 complex tables** with detailed columns, constraints, and relationships
- **150-200 simple tables** with basic structures
- Leaves 90% of context for prompts, queries, and responses
- ✅ **Recommended for production use**

**Comfortable Limit (500 KB)**:
- **100-120 complex tables**
- **300-400 simple tables**
- Leaves 80% of context window available
- ⚠️ Use with monitoring

**Aggressive Limit (1.2 MB)**:
- Theoretical maximum before impacting performance
- Not recommended - reduces space for query complexity
- Would require careful prompt engineering

### Current System Headroom

Your current largest schema (Airline: 8.2 KB) uses only **0.33%** of the available context window, providing:
- **30x capacity** before reaching safe limits
- **60x capacity** before reaching comfortable limits
- **151x capacity** before reaching theoretical maximum

This means you can comfortably add:
- **45-50 more airline-sized databases** within safe limits
- OR scale a single database to **30x its current complexity**

### Calculation Method

```python
# Token estimation (conservative)
tokens_per_char = 0.4
gemini_context_window = 1_000_000  # tokens

# Example: Airline schema
airline_size = 8254  # bytes
schema_tokens = airline_size * tokens_per_char  # ~3,301 tokens
context_usage = (schema_tokens / gemini_context_window) * 100  # 0.33%

# Safe limit calculation (10% of context)
safe_limit_tokens = gemini_context_window * 0.10  # 100,000 tokens
safe_limit_bytes = safe_limit_tokens / tokens_per_char  # 250,000 bytes
```

### Bottlenecks Beyond Context Window

While the AI context window is generous, watch for these limits:

1. **FastAPI Request Size**: Default ~1 MB (adjustable)
2. **SQLite Metadata Queries**: Slow with 500+ tables
3. **Frontend Rendering**: Large schemas impact UI performance
4. **Memory Usage**: Full schema loaded into RAM

### Recommendations

✅ **Current Status**: Excellent headroom, no concerns  
✅ **Growth Path**: Can scale 30x before any optimizations needed  
⚠️ **Monitor**: Schema size if planning 100+ table databases  
🔧 **Optimize When**: Schema exceeds 200 KB (not likely soon)

---

## Scalability Considerations

### Current Limitations
- **Single-threaded SQLite**: Max 10-20 concurrent users
- **API Rate Limits**: 110-165 req/min (11 keys × 10-15 req/min)
- **No horizontal scaling**: Stateful backend

### Scaling Path
1. **Phase 1** (100 users): Add Redis caching, query result caching
2. **Phase 2** (1,000 users): Migrate to PostgreSQL, add read replicas
3. **Phase 3** (10,000 users): Microservices, queue-based query processing
4. **Phase 4** (100,000 users): Kubernetes, auto-scaling, CDN for frontend

---

## Next Steps

- [Data Flow Diagram](data-flow.md) - Detailed sequence diagrams
- [Tech Stack Details](tech-stack.md) - Deep dive into each technology
- [API Key Rotation](api-key-rotation.md) - How 11-key rotation works
- [Design Decisions](design-decisions.md) - Why we chose what we chose

---

**For Implementation Details**: See [Development Setup](../04-development/setup.md)  
**For API Usage**: See [API Reference](../05-api/endpoints.md)
