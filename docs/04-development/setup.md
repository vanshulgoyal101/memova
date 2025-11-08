# Development Setup

**Audience**: Contributors, Developers  
**Time**: 15-20 minutes  
**Last Updated**: October 31, 2025

---

## Prerequisites

### Required
- Python 3.11+ ([Download](https://python.org))
- Node.js 18+ ([Download](https://nodejs.org))
- Git ([Download](https://git-scm.com))
- Google API Key ([Get Free Key](https://makersuite.google.com/app/apikey))

### Recommended
- VS Code with Python + TypeScript extensions
- SQLite Browser ([Download](https://sqlitebrowser.org))
- Make (pre-installed on macOS/Linux)

---

## Initial Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd "sql schema"
```

### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root with the following settings:

```bash
# .env file

# AI API Keys (at least one required)
# Primary: Groq (100,000 tokens/day free per organization) - Get from https://console.groq.com/
GROQ_API_KEY=your-groq-key-here
# GROQ_API_KEY=your-second-key  # ⚠️ IMPORTANT: Must be from different Groq account (different email)
# GROQ_API_KEY=your-third-key   # Rate limits are per-organization, not per-key!

# Fallback: Google Gemini (550 req/day with rotation) - Get from https://makersuite.google.com/
GOOGLE_API_KEY=your-gemini-key-here
# GOOGLE_API_KEY=your-second-key  # Optional: Add up to 11 keys for rotation

# Database Configuration
DATABASE_PATH=data/database/electronics_company.db
EXCEL_OUTPUT_DIR=data/excel

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Data Generation (affects demo data volume)
DEFAULT_EMPLOYEE_COUNT=150
DEFAULT_PRODUCT_COUNT=120
DEFAULT_CUSTOMER_COUNT=200
DEFAULT_SALES_COUNT=300

# Query Engine Guardrails
MAX_QUERY_RESULTS=1000          # Hard cap on query results (prevents large payloads)
QUERY_TIMEOUT_SECONDS=30        # Maximum query execution time
DEFAULT_RESULT_LIMIT=100        # Default LIMIT applied to queries without explicit LIMIT
```

#### Configuration Details

**Groq API Keys** (⚠️ Important):
- **Rate limits are per-organization, NOT per-key**
- All API keys from the same Groq account share the same quota (100,000 tokens/day)
- To increase capacity, create API keys from **different Groq accounts** (different email addresses)
- Each account gets its own organization with separate rate limits
- **Prompt Caching**: Reduces token usage by 98% on cached requests (40-50% faster)
  - First query: ~2500 tokens (caches database schema)
  - Subsequent queries: ~50 tokens (just the question)
  - Effective capacity: ~2,000 queries/day with caching (vs 39 without)
- Free tier: 100,000 tokens per day
- Upgrade to Dev Tier for higher limits: https://console.groq.com/settings/billing

**Gemini API Keys**:
- Each key has independent 50 requests/day limit
- System rotates through up to 11 keys = 550 requests/day total
- Keys from same Google account work independently (unlike Groq)

**Query Guardrails** (new in v3.2.0):
- `DEFAULT_RESULT_LIMIT`: Automatically appended to SELECT queries without a LIMIT clause (default: 100)
- `MAX_QUERY_RESULTS`: Hard server-side cap on any LIMIT value (default: 1000)
- `QUERY_TIMEOUT_SECONDS`: Maximum execution time before timeout (default: 30)

These guardrails protect the system from:
- Accidental full-table scans (10,000+ rows)
- Frontend performance issues (rendering large datasets)
- Network transfer bottlenecks
- Memory exhaustion

See [Query Guardrails](../05-api/endpoints.md#query-execution-guardrails) for details.

### 4. Generate Databases

```bash
# Generate all three databases
make generate

# Or manually:
python scripts/generate_all.py
```

**Output**:
```
data/database/
├── electronics_company.db (4 MB)
├── airline_company.db (4 MB)
└── edtech_company.db (4 MB)
```

### 5. Frontend Setup

```bash
cd frontend
npm install
```

---

## Running the Application

### Development Mode

```bash
# Start both servers (from root)
make start
```

This runs:
- **Frontend**: http://localhost:3000 (Next.js dev server)
- **Backend**: http://localhost:8000 (FastAPI with auto-reload)

### Individual Servers

```bash
# Backend only
cd api
uvicorn main:app --reload --port 8000

# Frontend only
cd frontend
npm run dev
```

---

## Project Structure
### Sidebar Quick Query Shortcuts

- Location: `frontend/src/components/layout/sidebar.tsx`
- UI: Pill-shaped buttons, color badges, icons for difficulty
- Event: Dispatches 'askbar-query-shortcut' to AskBar
- Accessibility: Keyboard/tab navigation, aria-labels
- Micro-interactions: Hover, focus ring, scale, shadow

```
/Volumes/Extreme SSD/code/sql schema/
├── src/                      ← Core Python modules
│   ├── core/
│   │   ├── database.py      ← DatabaseManager
│   │   └── query_engine.py  ← QueryEngine (AI)
│   ├── data/
│   │   ├── generators.py    ← Electronics data
│   │   └── airline_generators.py
│   └── utils/
│       ├── config.py         ← Configuration
│       ├── logger.py         ← Logging
│       └── exceptions.py     ← Custom errors
├── api/
│   └── main.py              ← FastAPI application
├── frontend/
│   └── src/
│       ├── app/             ← Next.js pages
│       ├── components/      ← React components
│       └── lib/             ← Utilities
├── tests/
│   ├── unit/                ← Unit tests
│   └── integration/         ← API tests
├── data/
│   ├── database/            ← SQLite databases
│   └── excel/               ← Generated Excel files
├── docs/                    ← Documentation (YOU ARE HERE)
├── scripts/
│   ├── generate_all.py      ← Data generation
│   └── examples.py          ← Example queries
├── Makefile                 ← Build commands
├── requirements.txt         ← Python dependencies
└── .env                     ← API keys (gitignored)
```

---

## Development Workflow

### Making Changes

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes (follow coding standards below)

# 3. Run tests
make test

# 4. Check code style
flake8 src/ tests/
black src/ tests/ --check

# 5. Commit changes
git add .
git commit -m "feat(scope): description"

# 6. Push and create PR
git push origin feature/my-feature
```

---

## Coding Standards

### Python (Backend)

**Style**: PEP 8  
**Formatter**: Black  
**Linter**: Flake8  
**Type Hints**: Required

```python
from typing import Dict, List, Optional

def execute_query(
    sql: str, 
    params: Optional[tuple] = None
) -> Dict[str, any]:
    """
    Execute SQL query and return results.
    
    Args:
        sql: SQL query string
        params: Query parameters
        
    Returns:
        Dict with keys: columns, rows, row_count
    """
    pass
```

### TypeScript (Frontend)

**Style**: Airbnb  
**Formatter**: Prettier  
**Linter**: ESLint

```typescript
interface QueryResponse {
  success: boolean;
  sql: string;
  columns: string[];
  rows: any[][];
}

export async function executeQuery(
  question: string,
  database: string
): Promise<QueryResponse> {
  // Implementation
}
```

---

## Testing

### Run All Tests
```bash
make test
```

### Unit Tests Only
```bash
pytest tests/unit/ -v
```

### Integration Tests
```bash
pytest tests/integration/ -v
```

### With Coverage
```bash
make test-cov
```

### Test Coverage Target
- **Minimum**: 80%
- **Current**: 95.2% (60/63 tests passing)

---

## Make Commands

```bash
# Development
make install      # Install dependencies
make generate     # Generate databases
make start        # Start both servers
make stop         # Stop servers
make restart      # Restart (clears cache)

# Testing
make test         # Run test suite
make test-cov     # Run with coverage report

# Cleanup
make clean        # Remove generated files
make clean-all    # Remove files + cache
```

See [Make Commands Reference](../docs/MAKE_COMMANDS.md) for details.

---

## Debugging

### Backend Debugging

**VS Code** (`launch.json`):
```json
{
  "name": "FastAPI",
  "type": "python",
  "request": "launch",
  "module": "uvicorn",
  "args": [
    "api.main:app",
    "--reload",
    "--port", "8000"
  ],
  "jinja": true
}
```

**PyCharm**: Run/Debug → Edit Configurations → Add FastAPI

### Frontend Debugging

**Browser DevTools**:
1. Open http://localhost:3000
2. Press F12
3. Go to Sources tab
4. Set breakpoints in TypeScript files

**VS Code**:
```json
{
  "name": "Next.js",
  "type": "node",
  "request": "launch",
  "runtimeExecutable": "npm",
  "runtimeArgs": ["run", "dev"],
  "cwd": "${workspaceFolder}/frontend"
}
```

---

## Logs

### Backend Logs
```bash
# View logs
tail -f logs/app.log

# Clear logs
rm logs/*.log
```

### Frontend Logs
- Browser console (F12)
- Terminal where `npm run dev` is running

---

## Database Inspection

### SQLite CLI
```bash
sqlite3 data/database/electronics_company.db

# Inside SQLite shell:
.tables                  # List tables
.schema employees        # Show table schema
SELECT COUNT(*) FROM employees;
.quit
```

### SQLite Browser (GUI)
1. Download from https://sqlitebrowser.org
2. File → Open Database
3. Select `data/database/electronics_company.db`
4. Browse tables, run queries

---

## Common Tasks

### Add New Endpoint

1. **Define route** (`api/main.py`):
```python
@app.get("/new-endpoint")
async def new_endpoint():
    return {"message": "Hello"}
```

2. **Add frontend function** (`frontend/src/lib/api.ts`):
```typescript
export async function callNewEndpoint() {
  const response = await fetch("http://localhost:8000/new-endpoint");
  return response.json();
}
```

3. **Update docs** (`docs/05-api/endpoints.md`)

4. **Write tests** (`tests/integration/test_api.py`)

---

### Add New Component

1. **Create component** (`frontend/src/components/my-component.tsx`):
```typescript
export function MyComponent() {
  return <div>Hello</div>;
}
```

2. **Import in page** (`frontend/src/app/page.tsx`):
```typescript
import { MyComponent } from '@/components/my-component';

export default function Page() {
  return <MyComponent />;
}
```

---

### Regenerate Data

```bash
# Delete old databases
rm data/database/*.db

# Generate new data
make generate

# Restart backend
make restart
```

---

## Troubleshooting

### Virtual Environment Issues
```bash
# Deactivate
deactivate

# Delete and recreate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Module Not Found
```bash
# Ensure virtual environment is activated
which python  # Should show .venv path

# Reinstall
pip install -r requirements.txt
```

---

## IDE Configuration

### VS Code Extensions
- Python (Microsoft)
- Pylance (Microsoft)
- TypeScript and JavaScript
- Tailwind CSS IntelliSense
- ESLint
- Prettier

### VS Code Settings (`.vscode/settings.json`)
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

---

## Next Steps

- [Coding Standards](coding-standards.md) - Detailed style guide
- [Testing Guide](testing.md) - Write and run tests
- [Contributing](contributing.md) - Contribution workflow
- [Architecture](../02-architecture/system-overview.md) - Understand the system

---

**Last Updated**: October 31, 2025
