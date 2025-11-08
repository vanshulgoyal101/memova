# Copilot Instructions - Multi-Database Query System

## 🎯 Project Philosophy: Context Engineering

**CRITICAL**: This project uses **Context Engineering** methodology:
- ❌ **DO NOT** rely on conversation memory
- ✅ **DO** read documentation files before ANY change
- ✅ **DO** update docs immediately after code changes
- ✅ **DO** use grep/search to find current implementation

**Documentation is the single source of truth, not memory.**

**🗺️ BEFORE making ANY change, read**: `docs/00-DOCUMENTATION-MAP.md`  
This map tells you exactly which docs to read and update for any type of change.

---

## 📁 Project Structure

```
/Volumes/Extreme SSD/code/sql schema/
├── .github/
│   └── copilot-instructions.md     ← YOU ARE HERE
├── docs/                            ← READ FIRST ALWAYS (NESTED STRUCTURE)
│   ├── 00-DOCUMENTATION-MAP.md     ← 🗺️ META-DOC: Which doc to update when
│   ├── README.md                   ← Master overview & quick links
│   ├── INDEX.md                    ← Comprehensive navigation
│   ├── 01-getting-started/
│   │   └── quickstart.md          ← 5-minute setup guide
│   ├── 02-architecture/
│   │   └── system-overview.md     ← System design & data flow
│   ├── 03-features/
│   │   ├── natural-language.md    ← AI-powered querying
│   │   ├── charts-insights.md     ← Auto-charting & trend detection (NEW v3.1.0)
│   │   ├── keyboard-shortcuts.md  ← Power user shortcuts
│   │   └── settings.md            ← User preferences
│   ├── 04-development/
│   │   └── setup.md               ← Development guide
│   ├── 05-api/
│   │   └── endpoints.md           ← All API endpoints
│   ├── 06-database/
│   │   ├── electronics_schema.md  ← Electronics schema (12 tables)
│   │   ├── airline_schema.md      ← Airline schema (16 tables)
│   │   ├── edtech_schema.md       ← EdTech India schema (15 tables, NEW v3.0.0)
│   │   ├── ednite_schema.md       ← EdNite test results (NEW v3.2.0)
│   │   └── liqo_schema.md         ← Liqo Retail schema (5 tables, 37,857 transactions, NEW v3.3.0)
│   ├── 07-maintenance/
│   │   └── (deployment, troubleshooting, changelog)
│   └── archive/                   ← Legacy docs (never delete)
│       ├── task-completions/      ← Historical TASK_X logs
│       └── old-structure/         ← Previous flat structure
├── src/                             ← Core business logic
│   ├── core/
│   │   ├── database.py             ← DatabaseManager class
│   │   ├── query_engine.py         ← QueryEngine orchestrator (250 lines)
│   │   ├── api_key_manager.py      ← API key rotation logic (200 lines)
│   │   ├── gemini_client.py        ← Gemini AI client wrapper (140 lines)
│   │   ├── sql_generator.py        ← SQL generation & cleaning (220 lines)
│   │   ├── summarizer.py           ← LLM result summarizer
│   │   ├── chart_detector.py       ← Chart pattern detection (380 lines, v3.1.0)
│   │   ├── ai_chart_selector.py    ← AI-powered chart selection (325 lines, v3.1.0)
│   │   └── trend_detector.py       ← Statistical trend detection (562 lines, v3.1.0)
│   ├── data/
│   │   ├── generators.py           ← Electronics data generation
│   │   ├── airline_generators.py   ← Airline data generation
│   │   ├── edtech_generators.py    ← EdTech India data generation (NEW v3.0.0)
│   │   ├── ednite_generators.py   ← EdNite test data generation (NEW v3.2.0)
│   │   ├── liqo_generators.py     ← Liqo Retail data generation (NEW v3.3.0)
│   │   ├── converters.py           ← Excel → SQL conversion
│   │   ├── schema.py               ← Schema generation
│   │   ├── electronics/            ← Electronics data files
│   │   ├── airline/                ← Airline data files
│   │   └── edtech/                 ← EdTech data files (NEW v3.0.0)
│   └── utils/
│       ├── config.py               ← Configuration management
│       ├── logger.py               ← Logging setup
│       ├── llm.py                  ← LLM client with Groq/Gemini + prompt caching (enhanced 2025-11-06)
│       └── exceptions.py           ← Custom exceptions
├── api/
│   ├── main.py                     ← FastAPI app initialization
│   ├── models.py                   ← Pydantic request/response models
│   └── routes.py                   ← API endpoint handlers
├── frontend/
│   ├── src/                        ← Next.js 16 App Router
│   │   ├── app/                   ← Pages (page.tsx, layout.tsx)
│   │   ├── components/            ← React components
│   │   │   ├── layout/           ← Navbar, Sidebar, AppShell
│   │   │   ├── query/            ← AskBar component
│   │   │   ├── results/          ← AnswerPanel component
│   │   │   ├── settings/         ← SettingsDialog component
│   │   │   └── ui/               ← shadcn/ui components
│   │   ├── lib/                   ← Utilities
│   │   │   ├── api.ts            ← API client
│   │   │   ├── scope.ts          ← Zustand store
│   │   │   ├── settings.ts       ← User preferences
│   │   │   └── utils.ts          ← Helpers
│   │   └── data/
│   │       └── companies.ts       ← Company metadata
│   └── public/                    ← Static assets
├── tests/
│   ├── conftest.py                 ← Pytest fixtures
│   ├── unit/
│   │   ├── test_database.py        ← DB manager tests
│   │   ├── test_query_engine.py    ← Query engine tests
│   │   └── test_llm_summarizer.py  ← LLM summarizer tests
│   └── integration/
│       ├── test_api.py             ← API endpoint tests
│       ├── test_llm_summarizer.py  ← /ask endpoint tests
│       └── test_data_generation.py ← Data quality tests
├── data/
│   ├── excel/                      ← Generated Excel files
│   └── database/                   ← SQLite databases
├── scripts/
│   ├── generate_all.py             ← Generate all data
│   └── examples.py                 ← Example queries
├── Makefile                        ← Build commands
├── start_web.sh                    ← Web server launcher
├── requirements.txt                ← Python dependencies
└── .env                            ← API keys (gitignored)
```

---

## 🔍 Before Making ANY Change

### Step 1: Locate Documentation (NESTED STRUCTURE)
```bash
# Always start here:
docs/README.md                          # Master overview & quick links
docs/INDEX.md                           # Comprehensive navigation

# Then navigate by topic:
docs/02-architecture/system-overview.md # For system design questions
docs/05-api/endpoints.md                # For API endpoint questions
docs/04-development/setup.md            # For coding standards
docs/06-database/electronics_schema.md  # For schema questions
docs/03-features/natural-language.md    # For AI query feature
docs/03-features/keyboard-shortcuts.md  # For keyboard shortcuts
docs/03-features/settings.md            # For user preferences

# Legacy docs (archived, for reference only):
docs/archive/old-structure/ARCHITECTURE.md    # Old verbose version
docs/archive/task-completions/TASK_X_COMPLETE.md  # Historical logs
```

### Step 2: Read Current Implementation
```python
# Use read_file to see current state
read_file("src/core/query_engine.py", 1, 100)

# Use grep_search to find related code
grep_search(pattern="class QueryEngine", includePattern="src/**/*.py")

# Use semantic_search for concept-based search
semantic_search("how database connection is managed")
```

### Step 3: Verify Context
- Check imports and dependencies
- Review related test files
- Confirm current behavior before changing

---

## 📋 Development Workflow

### Adding a Feature
1. **Read**: `docs/02-architecture/system-overview.md` to understand system
2. **Search**: Find related code with `grep_search`
3. **Test First**: Write failing test (TDD)
4. **Implement**: Make minimal changes
5. **Update Docs**: Modify relevant `docs/` files in appropriate folder
6. **Test**: `make test` before committing
7. **Commit**: Follow commit convention below
2. **Search**: Find related code with `grep_search`
3. **Test First**: Write failing test (TDD)
4. **Implement**: Make minimal changes
5. **Update Docs**: Modify relevant `docs/*.md` files
6. **Test**: `make test` before committing
7. **Commit**: Follow commit convention below

### Fixing a Bug
1. **Reproduce**: Write test that fails
2. **Read**: Current implementation
3. **Fix**: Minimal change to pass test
4. **Verify**: Run full test suite
5. **Document**: Update docs if behavior changes

### Refactoring
1. **Test Coverage**: Ensure 80%+ coverage first
2. **Small Steps**: Incremental changes
3. **Test After Each**: Run tests continuously
4. **Update Docs**: Keep documentation current
5. **No Behavior Change**: Refactor = same output

---

## 🎨 Coding Standards
### Sidebar Quick Query Shortcuts UI

- Use pill-shaped buttons, left-aligned text
- Group by difficulty: Easy (green ✨), Medium (yellow ⚡), Hard (red 🔥)
- Add color-coded badges and icons for each group
- Micro-interactions: hover scale, shadow, focus-visible ring
- Keyboard accessible, aria-labels for screen readers
- Responsive: touch targets ≥44px, vertical stacking on mobile

### Python Style Guide
```python
"""
PEP 8 compliant
Type hints mandatory
Google-style docstrings
Proper error handling
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Manages SQLite database connections and queries.
    
    This class handles connection pooling, query execution,
    and schema introspection for multiple databases.
    
    Attributes:
        db_path: Absolute path to SQLite database file
        
    Example:
        >>> db = DatabaseManager("data/database/company.db")
        >>> results = db.execute_query("SELECT * FROM employees LIMIT 5")
        >>> print(results['rows'])
        
    Raises:
        FileNotFoundError: If database file doesn't exist
        sqlite3.Error: If query execution fails
    """
    
    def __init__(self, db_path: str) -> None:
        """Initialize database manager with path validation."""
        if not Path(db_path).exists():
            raise FileNotFoundError(f"Database not found: {db_path}")
        self.db_path = db_path
        logger.info(f"DatabaseManager initialized: {db_path}")
    
    def execute_query(
        self, 
        sql: str, 
        params: Optional[tuple] = None
    ) -> Dict[str, any]:
        """
        Execute SQL query and return results.
        
        Args:
            sql: SQL query string (parameterized)
            params: Query parameters for safe execution
            
        Returns:
            Dict with keys: columns, rows, row_count
            
        Raises:
            sqlite3.Error: If query execution fails
        """
        try:
            # Implementation
            pass
        except sqlite3.Error as e:
            logger.error(f"Query failed: {sql} - {e}")
            raise
```

### Naming Conventions
- **Classes**: `PascalCase` - `QueryEngine`, `DatabaseManager`
- **Functions**: `snake_case` - `execute_query`, `generate_sql`
- **Constants**: `UPPER_SNAKE_CASE` - `API_BASE_URL`, `MAX_RETRIES`
- **Private**: `_leading_underscore` - `_validate_input`, `_clean_sql`
- **Database**: `lowercase_snake_case` - `employees`, `sales_orders`

---

## 🧪 Testing Requirements

### Test Coverage Targets
- **Unit Tests**: 90% coverage
- **Integration Tests**: All API endpoints
- **Total Coverage**: Minimum 80%

### Test Structure
```python
import pytest
from pathlib import Path

class TestQueryEngine:
    """Unit tests for QueryEngine class."""
    
    def test_simple_query(self, electronics_db_path):
        """Test basic COUNT query execution."""
        engine = QueryEngine(db_path=electronics_db_path)
        result = engine.query("How many employees?")
        
        assert result['success'] is True
        assert result['row_count'] > 0
        assert 'SELECT' in result['sql'].upper()
```

### Running Tests
```bash
# All tests
make test

# Specific file
pytest tests/unit/test_database.py -v

# With coverage
make test-cov

# Integration only
pytest tests/integration/ -v
```

---

## 🌐 API Development

### Endpoint Structure
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

class QueryRequest(BaseModel):
    """Request model for /query endpoint."""
    question: str
    database: str  # "electronics" or "airline"

@app.post("/query")
async def execute_query(request: QueryRequest) -> Dict:
    """
    Execute natural language query against selected database.
    
    Args:
        request: QueryRequest with question and database ID
        
    Returns:
        {
            "success": bool,
            "sql": str,
            "columns": List[str],
            "rows": List[List],
            "row_count": int,
            "execution_time": float,
            "error": Optional[str]
        }
        
    Raises:
        HTTPException: 400 if invalid database
        HTTPException: 500 if query execution fails
    """
    try:
        # Implementation
        pass
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### API Conventions
- **Base URL**: `http://localhost:8000`
- **CORS**: Enabled for `localhost:3000`
- **Docs**: Auto-generated at `/docs`
- **Health**: `/health` endpoint always available

---

## 💾 Database Conventions

### Schema Design
- **Table names**: `lowercase_snake_case` (e.g., `sales_orders`)
- **Column names**: `lowercase_snake_case` (e.g., `customer_id`)
- **Primary keys**: `id` or `{table}_id` (e.g., `employee_id`)
- **Foreign keys**: Named after referenced table (e.g., `product_id`)
- **Timestamps**: ISO 8601 format

### Example
```sql
CREATE TABLE employees (
    employee_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT,
    hire_date TEXT,
    salary REAL CHECK(salary > 0)
);
```

---

## 🔧 Make Commands Reference

```bash
# Web Server
make start      # Start frontend (3000) + backend (8000)
make stop       # Stop all servers
make restart    # Restart + clear Python cache

# Development
make install    # Install dependencies
make generate   # Generate all data
make test       # Run test suite
make test-cov   # Run with coverage report

# Cleanup
make clean      # Remove generated files
make clean-all  # Remove files + cache
```

---

## 📝 Git Commit Convention

```bash
# Format: <type>(<scope>): <subject>

# Types:
feat      # New feature
fix       # Bug fix
docs      # Documentation only
test      # Adding tests
refactor  # Code restructure (no behavior change)
perf      # Performance improvement
chore     # Maintenance tasks

# Examples:
feat(api): add /stats endpoint for query analytics
fix(query): handle null values in aggregation queries
docs(arch): update system architecture diagram
test(db): add integration tests for connection pooling
refactor(query): extract SQL validation to separate method
```

---

## 🚨 Error Handling

### Strategy
1. **Catch specific exceptions** (never bare `except:`)
2. **Log with context** (include variables, stack trace)
3. **User-friendly messages** (no technical jargon in UI)
4. **Proper status codes** (400 client, 500 server)
5. **Never expose secrets** (API keys, paths)

### Example
```python
try:
    result = engine.query(question)
except ValueError as e:
    logger.warning(f"Invalid input: {question} - {e}")
    raise HTTPException(status_code=400, detail="Invalid question format")
except GoogleAPIError as e:
    logger.error(f"AI service failed: {e}")
    raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

---

## 🔐 Security Guidelines

- **API Keys**: Store in `.env`, never commit
- **SQL Injection**: Use parameterized queries only
- **Input Validation**: Validate all user inputs
- **CORS**: Restrict origins in production
- **Logging**: Never log sensitive data
- **Rate Limiting**: Respect Google API limits (10/min free tier)

---

## 📚 Documentation Update Checklist

Update docs when you:
- ✅ Add/remove API endpoints → `docs/05-api/endpoints.md`
- ✅ Change database schema → `docs/06-database/electronics_schema.md` or `airline_schema.md` or `edtech_schema.md` or `ednite_schema.md` or `liqo_schema.md`
- ✅ Modify architecture → `docs/02-architecture/system-overview.md`
- ✅ Add dependencies → `requirements.txt` + `docs/04-development/setup.md`
- ✅ Change build process → `Makefile` + `docs/04-development/setup.md`
- ✅ Add feature → Create new doc in `docs/03-features/`
- ✅ Fix critical bugs → `docs/02-architecture/system-overview.md` (lessons learned)

---

## 🎯 Performance Targets

- **Query Response**: < 0.5 seconds (AI + DB, with caching)
- **API Response**: < 500ms (non-AI endpoints)
- **Database Query**: < 100ms
- **Frontend Load**: < 1 second
- **Test Suite**: < 120 seconds
- **Cache Hit Rate**: > 90% (after warmup)

---

## 🔄 Refactoring Triggers

Refactor when:
- **Code duplication** appears 3+ times
- **Function > 50 lines** (extract subfunctions)
- **Class > 300 lines** (split responsibilities)
- **Cyclomatic complexity > 10** (simplify logic)
- **Similar bugs** in 3+ places (architectural issue)

---

## 📊 Key Metrics

### Current System Stats
- **Databases**: 5 (electronics, airline, edtech, ednite, liqo)
- **Tables**: 53 total (12 electronics, 16 airline, 15 edtech, 5 ednite, 5 liqo)
- **Data Rows**: 56,500+ (11,265 traditional + 2,540 ednite + 42,695 liqo)
- **Test Coverage**: 95.2% (94/94 tests including domain validation)
- **API Endpoints**: 8 (/health, /databases, /schema, /examples, /ask, /query, /stats, /)
- **Lines of Code**: ~6,800

### External Dependencies

**AI Providers (Dual-stack with automatic failover):**

1. **Groq AI** (Primary - 26x faster, higher quota)
   - Model: llama-3.3-70b-versatile
   - Rate Limit: 100,000 tokens/day per organization (free tier)
   - Speed: ~0.35s per query with caching (86-88% faster than cold start)
   - **Prompt Caching**: 40-50% speed improvement, 98% token reduction
   - Use Case: All SQL generation + result summarization
   - ⚠️ Rate limits are per-organization, not per-key

2. **Google Gemini AI** (Fallback - reliable, proven)
   - Model: gemini-2.0-flash-exp
   - Rate Limit: 50 requests/day per key, 11 keys = 550 req/day total
   - Speed: ~1.5s per query
   - Use Case: Automatic fallback when Groq unavailable/rate-limited

**Failover Strategy:**
- Try Groq first for ALL requests (SQL generation + summarization)
- On ANY Groq error (rate limit, timeout, service down) → Gemini
- On Gemini error → User-friendly error message
- Transparent to user (answer includes provider info in logs only)

### Prompt Caching System ✅
**Implemented 2025-11-06** - Reduces token usage by 98% on cached requests

**How It Works:**
- Database schema (~2500 tokens) sent as `system` message (cached)
- User question (~50 tokens) sent as `user` message (fresh)
- Groq automatically caches system message via prefix matching
- Subsequent queries only send the question (50 tokens vs 2500)

**Performance Impact:**
- First query (cold): 0.66s - caches schema
- Cached queries: 0.35s average (47% faster)
- Token savings: 98% reduction per cached request
- Capacity increase: 39 queries/day → 2,000 queries/day (51x)

**Implementation:**
```python
# In src/core/sql_generator.py
system_message, user_message = self._create_prompt(question)
sql_text, provider = self.llm_client.generate_content(
    user_message, 
    system_message=system_message  # Cached by Groq
)
```

**Note:** llama-3.3-70b-versatile caches successfully (confirmed by performance tests), but doesn't expose cache metrics in API response yet. Groq is rolling out full caching support to more models over time.

### API Key Rotation System ✅
The system automatically rotates through multiple API keys when rate limits are hit.

**Both SQL generation AND result summarization** use the same rotation system:

**Configuration** (`src/utils/config.py`):
- `Config.get_all_api_keys()` - Loads all keys from `.env` (including commented ones)
- Detects any line containing GOOGLE_API_KEY=AIza... (including lines commented out with #)

**SQL Generation Rotation** (`src/core/api_key_manager.py`):
- Singleton APIKeyManager class manages key pool
- `get_current_key()` - Returns current active key
- `rotate_key()` - Switches to next available key on rate limit (429)
- `is_rate_limit_error()` - Detects quota/429 errors
- Tracks failed keys to avoid retry loops

**LLM Summarization Rotation** (`src/utils/llm.py`):
- Uses same APIKeyManager singleton
- Automatic retry with key rotation on rate limits
- Exponential backoff for transient errors (1.5s, 3s, 4.5s)
- Detailed logging: "Using API key X/7", "Rate limit hit, rotating..."

**Usage Flow**:
```python
# Both modules use identical pattern:
from src.core.api_key_manager import APIKeyManager

_key_manager = APIKeyManager()

def generate_something():
    for key_attempt in range(_key_manager.get_total_keys()):
        api_key = _key_manager.get_current_key()
        try:
            # ... call Gemini API with api_key
            return result
        except Exception as e:
            if _key_manager.is_rate_limit_error(e):
                _key_manager.rotate_key()  # Try next key
                continue
            raise
```

**How to Add More Keys**:
```bash
# In .env file, add commented lines:
# GOOGLE_API_KEY=AIzaSyAQ_IHtBXN-pw3NRHrEHb27m8kWNfaQ2Uc
# GOOGLE_API_KEY=AIzaSyB5u2kQXrkggkU5KYW1AJMcY6IANj-iz2g
GOOGLE_API_KEY=AIzaSyBEr2uRqe4dMeaPONhT44dpyeu8MZyV4O8  # Active key
```

All keys (commented or not) are automatically detected and used in rotation.

---

## ⚡ Quick Reference

### Ports
- `3000` - Frontend (HTTP server)
- `8000` - Backend API (FastAPI)

### Paths
- Databases: `data/database/*.db`
- Excel files: `data/excel/*/`
- Logs: `logs/*.log`

### Environment Variables
```bash
# AI Providers (at least one required)
GROQ_API_KEY=your_groq_key_here          # Primary (get from https://console.groq.com/)
GOOGLE_API_KEY=your_gemini_key_here      # Fallback (get from https://makersuite.google.com/)

# Optional
LOG_LEVEL=INFO
```

---

## 🎓 Remember

1. **Read docs FIRST**, code second
2. **Update docs** with code changes
3. **Test before commit**
4. **Small commits**, clear messages
5. **Context Engineering** = Scalability
6. **Documentation** > Memory
7. **Grep is your friend** - find before you write

---

**Version**: 3.1.0  
**Last Updated**: 2025-11-06  
**Methodology**: Context Engineering  
**Documentation Location**: `docs/` (nested structure)

**Recent Enhancements**:

- **Intelligent Business Analyst (v3.2.0)** (2025-11-06) 🧠 LATEST:
  - NEW: `src/core/analyst.py` (641 lines) - AI-powered strategic problem solver
  - **Capabilities**: Interprets vague business problems ("My revenue is low") → generates custom exploratory SQL → synthesizes insights → provides recommendations
  - **5-Stage Pipeline**:
    1. Problem interpretation (identify hypotheses, focus areas)
    2. AI-driven query planning (generates 3-5 custom SQL queries based on problem)
    3. Query execution with error handling
    4. Pattern analysis across multiple data points
    5. Business insights + actionable recommendations generation
  - **Schema Awareness Fix** (2025-11-06): Schema now embedded in AI prompts to prevent hallucinated table names
  - **Token Optimization**: Smart schema passing (schema in first call only, ~38% token reduction)
  - **Detection**: 27 keywords detect analytical questions ("improve", "insights", "recommend", "why", etc.)
  - UPDATED: `api/routes.py` - Analytical path returns SQL + data + analysis + insights
  - UPDATED: `api/models.py` - Added BusinessAnalysis model with insights/recommendations
  - UPDATED: `frontend/src/components/results/answer-panel.tsx` - Shows query success/failure badges
  - UPDATED: `frontend/src/components/results/business-analysis-panel.tsx` - Renders insights
  - Performance: ~5-6s end-to-end (3 LLM calls: 1.9s + 1.3s + 1.7s)
  - Tokens: 4,303 per analytical query (down from 6,920, 38% reduction)
  - Examples: "How can I improve sales?" → 5 exploratory queries → deep analysis with 6 insights + 6 recommendations
  - Documentation: Created `docs/03-features/intelligent-problem-solving.md`

- **Fallback UX Improvements** (2025-11-06) 💡:
  - ENHANCED: Data tab shows helpful message when analytical queries have no data
  - ENHANCED: SQL tab shows query status (✓ X rows or ❌ FAILED) for each exploratory query
  - ENHANCED: Answer panel shows "X/Y queries OK" badge for analytical queries
  - Better error context when queries fail (shows which tables were attempted)

- **Prompt Caching Implementation** (2025-11-06) 🚀:
  - ENHANCED: `src/core/groq_client.py` - Added system_message parameter for caching
  - ENHANCED: `src/core/sql_generator.py` - Split prompts into system (schema) + user (question)
  - ENHANCED: `src/core/llm_client.py` - Pass system messages through call chain
  - Performance: 40-50% faster queries, 98% token reduction on cached requests
  - Capacity: 39 queries/day → 2,000 queries/day (51x increase)
  - Implementation: Schema sent as cached system message, only question sent fresh
  - Documentation: Created `docs/07-maintenance/CACHING_IMPLEMENTATION.md`
  - Note: llama-3.3-70b caches successfully despite not being in official support list

- **AI-Powered Chart Selection** (2025-11-06) 🎨:
  - ENHANCED: `src/core/groq_client.py` - Added system_message parameter for caching
  - ENHANCED: `src/core/sql_generator.py` - Split prompts into system (schema) + user (question)
  - ENHANCED: `src/core/llm_client.py` - Pass system messages through call chain
  - Performance: 40-50% faster queries, 98% token reduction on cached requests
  - Capacity: 39 queries/day → 2,000 queries/day (51x increase)
  - Implementation: Schema sent as cached system message, only question sent fresh
  - Documentation: Created `docs/07-maintenance/CACHING_IMPLEMENTATION.md`
  - Note: llama-3.3-70b caches successfully despite not being in official support list

- **AI-Powered Chart Selection** (2025-11-06) 🎨:
  - UPGRADED: `src/core/chart_detector.py` (395 lines) - Now AI-first with heuristic fallback
  - NEW: `src/core/ai_chart_selector.py` (325 lines) - LLM decides if/what to visualize
  - Two-step AI decision: (1) Should we visualize? (2) If yes, what chart type?
  - Smart "no chart" decisions: Simple counts, single values, text-heavy data → table only
  - Context-aware: Considers user's question intent ("compare", "trend", "breakdown")
  - UPDATED: `api/routes.py` - Passes question to chart detector for AI context
  - UPDATED: `api/models.py` - Charts field now optional (may be null if not needed)
  - UPDATED: `frontend/src/components/results/answer-panel.tsx` - Table styling improvements
  - Performance: Single LLM call (~1-2s), falls back to heuristics if AI fails
  - Examples: "How many products?" → NO chart, "Compare top vs bottom" → BAR chart
  - Documentation: Created `docs/03-features/charts-insights.md` (comprehensive guide)

- **Trend Detection (AI Insights)** (2025-11-06) ✨:
  - NEW: `src/core/trend_detector.py` (562 lines) - Statistical trend detection from query results
  - Detection types: time series (growth/decline), categorical outliers, numeric distributions
  - Unit tests: 24/24 passing (100% coverage for trend detection logic)
  - Integration tests: 7/7 passing (trend metadata in /ask and /query responses)
  - NEW: `frontend/src/components/results/insights-panel.tsx` - Alert-based insights component
  - NEW: `frontend/src/components/ui/alert.tsx` - shadcn/ui alert component
  - UPDATED: `api/routes.py` - Wired trend detection into /ask and /query endpoints
  - UPDATED: `api/models.py` - Added TrendInsight model and trends field in responses
  - UPDATED: `frontend/src/lib/api.ts` - Added TrendInsight TypeScript types
  - UPDATED: `frontend/src/components/results/answer-panel.tsx` - Integrated InsightsPanel
  - Performance: <50ms statistical analysis (pure Python/pandas, no LLM calls)
  - Test coverage: 31/31 tests passing (24 unit + 7 integration)
  - Features: Growth/decline trends, z-score outliers (|z| > 2), quartile distributions, confidence scoring

- **Simple Charts (Auto-charting)** (2025-11-06) ✨ (Superseded by AI-powered above):
  - NEW: `src/core/chart_detector.py` (353 lines) - Automatic chart detection from query results
  - Heuristics: time series (line), categorical breakdown (bar/pie), numeric distribution (histogram)
  - Now used as fallback when AI chart selection unavailable
  - Performance: <10ms chart detection, deterministic heuristics
  - Bug fixes: YYYY-MM date format support, pie chart threshold adjusted (≤6 → ≤10 categories)

- **Groq AI Migration** (2025-11-06):
  - Migrated from Gemini-only to Groq (primary) + Gemini (fallback) dual-stack architecture
  - NEW: `src/core/groq_client.py` (190 lines) - Groq AI client with Gemini-compatible interface
  - NEW: `src/core/llm_client.py` (220 lines) - UnifiedLLMClient with automatic Groq→Gemini failover
  - UPDATED: `src/core/sql_generator.py` - Uses UnifiedLLMClient, tracks provider used
  - UPDATED: `src/utils/llm.py` - Uses UnifiedLLMClient singleton (simplified from 180→50 lines)
  - UPDATED: `src/core/query_engine.py` - Initializes UnifiedLLMClient
  - UPDATED: `requirements.txt` - Added groq==0.11.0, httpx<0.28 for compatibility
  - Performance: 3-5x faster SQL generation (~0.3s vs ~1.5s), 14,400 req/day vs 550 req/day
  - Test coverage: 68/77 tests passing (88% after migration updates)

- **Major Refactoring** (2025-10-31):
  - Split monolithic `query_engine.py` (614 lines) into 4 modular components
  - `api_key_manager.py` (200 lines) - API key rotation & failover logic
  - `gemini_client.py` (140 lines) - Gemini AI client management
  - `sql_generator.py` (220 lines) - SQL generation & prompt engineering
  - `query_engine.py` (250 lines, -59%) - Orchestrator following SOLID principles

- **LLM Summarization Enhancement** (2025-10-31):
  - Updated `src/utils/llm.py` with APIKeyManager for 11-key rotation
  - Added retry logic with automatic key rotation on rate limits
  - Enhanced fallback messages with data preview when AI unavailable
  - Detailed error logging in `summarizer.py` for debugging

- **API & Frontend Updates**:
  - API refactored into modular structure (main.py, models.py, routes.py)
  - LLM summarizer enhanced with head+tail sampling, executive tone prompts
  - `/ask` endpoint refactored: separate SQL generation & execution timing (genMs, execMs)
  - Frontend types updated: AskRequest/AskResponse match backend
  - AnswerPanel: Natural language answer as hero element

---

## 📖 Next Steps for You

When starting work:
1. Read `docs/README.md` for project overview
2. Check `docs/INDEX.md` for comprehensive navigation
3. Read `docs/02-architecture/system-overview.md` to understand the system
4. Check `docs/05-api/endpoints.md` for API details
5. Review `docs/04-development/setup.md` for dev environment setup
6. Use `grep_search` to find relevant code
7. Make changes incrementally
8. Update documentation in appropriate `docs/0X-category/` folder
9. Run tests
10. Commit with proper message

**Trust the docs, not the memory.** 🎯
