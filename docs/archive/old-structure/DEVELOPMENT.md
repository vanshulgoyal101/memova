# Development Guide

**Project**: Multi-Database Query System  
**Last Updated**: 2025-10-31  
**Methodology**: Context Engineering

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [Code Standards](#code-standards)
6. [Testing](#testing)
7. [Debugging](#debugging)
8. [Common Tasks](#common-tasks)
9. [IDE Configuration](#ide-configuration)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python**: 3.10 or higher
- **pip**: Latest version
- **Git**: For version control
- **Text Editor**: VS Code (recommended) or PyCharm

### Recommended Tools
- **Make**: For build commands (pre-installed on macOS/Linux)
- **curl**: For API testing
- **SQLite Browser**: For database inspection
- **Postman/Insomnia**: API testing (optional)

### System Requirements
- **OS**: macOS, Linux, or Windows (WSL recommended)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk**: 500 MB for project + dependencies
- **Network**: Internet connection for Google Gemini API

---

## Environment Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd "sql schema"
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Verify activation (should show .venv path)
which python
```

### 3. Install Dependencies
```bash
# Using Make (recommended)
make install

# Or using pip directly
pip install -r requirements.txt
```

**Dependencies Installed**:
- **Core**: pandas, openpyxl, Faker, sqlalchemy
- **AI**: google-generativeai
- **API**: fastapi, uvicorn, pydantic
- **Config**: python-dotenv
- **Testing**: pytest, pytest-cov
- **Type Checking**: mypy

### 4. Configure Environment Variables
```bash
# Create .env file
cp .env.example .env  # If example exists, or create manually

# Edit .env file
nano .env
```

**Required Variables**:
```bash
# Google Gemini API Key (REQUIRED)
GOOGLE_API_KEY=your_api_key_here

# Optional: Logging level
LOG_LEVEL=INFO

# Optional: Custom database paths
DB_PATH_ELECTRONICS=data/database/electronics_company.db
DB_PATH_AIRLINE=data/database/airline_company.db
```

**Get Google API Key**:
1. Visit: https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy key to `.env` file

### 5. Generate Sample Data
```bash
# Generate both databases (electronics + airline)
make generate

# Or use Python directly
python scripts/generate_all.py
```

**Expected Output**:
```
data/database/electronics_company.db  (480 KB, 12 tables, 3,600+ rows)
data/database/airline_company.db      (1.37 MB, 16 tables, 3,920+ rows)
data/excel/electronics_company/       (12 Excel files)
data/excel/airline_company/           (16 Excel files)
```

### 6. Verify Installation
```bash
# Run tests to verify setup
make test

# Should see: 60/63 tests passing (95.2%)
# 3 failures are expected (Google API rate limit)
```

---

## Project Structure

```
/Volumes/Extreme SSD/code/sql schema/
├── .venv/                           # Virtual environment (gitignored)
├── .env                             # Environment variables (gitignored)
├── .gitignore                       # Git ignore rules
├── Makefile                         # Build commands
├── README.md                        # Project overview
├── requirements.txt                 # Python dependencies
├── start_web.sh                     # Web server launcher
│
├── .github/
│   └── copilot-instructions.md     # Development standards (READ FIRST)
│
├── docs/                            # Documentation (Context Engineering)
│   ├── ARCHITECTURE.md             # System design
│   ├── API_REFERENCE.md            # REST API specs
│   ├── DEVELOPMENT.md              # ← YOU ARE HERE
│   ├── TESTING_SUMMARY.md          # Test coverage
│   ├── MAKE_COMMANDS.md            # Build commands
│   ├── electronics_schema.md       # Electronics DB schema
│   ├── airline_schema.md           # Airline DB schema
│   └── archive/                    # Legacy documentation
│
├── src/                             # Core business logic
│   ├── __init__.py
│   ├── cli/
│   │   └── query_cli.py            # Interactive CLI
│   ├── core/
│   │   ├── database.py             # DatabaseManager class
│   │   └── query_engine.py         # QueryEngine (AI + DB)
│   ├── data/
│   │   ├── generators.py           # Electronics data generation
│   │   ├── airline_generators.py   # Airline data generation
│   │   ├── converters.py           # Excel ↔ SQL conversion
│   │   └── schema.py               # Schema documentation generator
│   └── utils/
│       ├── config.py               # Configuration management
│       ├── logger.py               # Logging setup
│       └── exceptions.py           # Custom exceptions
│
├── api/
│   └── main.py                     # FastAPI REST API (7 endpoints)
│
├── frontend/
│   └── index.html                  # React SPA (Tailwind CSS)
│
├── tests/                           # Test suite (95% coverage)
│   ├── conftest.py                 # Pytest fixtures & config
│   ├── unit/
│   │   ├── test_database.py        # DatabaseManager tests (17)
│   │   └── test_query_engine.py    # QueryEngine tests (15)
│   └── integration/
│       ├── test_api.py             # API endpoint tests (18)
│       └── test_data_generation.py # Data quality tests (13)
│
├── scripts/
│   ├── generate_all.py             # Generate all databases
│   └── examples.py                 # Example query scripts
│
├── data/                            # Generated data (gitignored)
│   ├── database/
│   │   ├── electronics_company.db
│   │   └── airline_company.db
│   └── excel/
│       ├── electronics_company/
│       └── airline_company/
│
└── logs/                            # Application logs (gitignored)
```

---

## Development Workflow

### Context Engineering Principles

**CRITICAL**: This project uses **documentation-first development**:

1. ❌ **DO NOT** rely on conversation memory
2. ✅ **DO** read documentation files before making changes
3. ✅ **DO** update docs immediately after code changes
4. ✅ **DO** use `grep`/search to find current implementation

**Documentation is the single source of truth.**

### Making Changes (5-Step Process)

#### Step 1: Read Documentation First
```bash
# System design question?
cat docs/ARCHITECTURE.md

# API endpoint question?
cat docs/API_REFERENCE.md

# Coding standards?
cat .github/copilot-instructions.md

# Database schema?
cat docs/electronics_schema.md
cat docs/airline_schema.md
```

#### Step 2: Find Current Implementation
```bash
# Search for class/function
grep -r "class QueryEngine" src/

# Search for specific code pattern
grep -r "def execute_query" src/

# Search for imports
grep -r "from src.core" .
```

#### Step 3: Write Test First (TDD)
```python
# tests/unit/test_new_feature.py
import pytest
from src.core.new_module import NewClass

class TestNewFeature:
    """Test suite for new feature."""
    
    def test_basic_functionality(self):
        """Test that new feature works."""
        obj = NewClass()
        result = obj.do_something()
        assert result == expected_value
```

```bash
# Run test (should fail)
pytest tests/unit/test_new_feature.py -v
```

#### Step 4: Implement Feature
```python
# src/core/new_module.py
"""
New feature module.

This module implements [description].
See docs/ARCHITECTURE.md for design details.
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class NewClass:
    """
    Brief description.
    
    Detailed description with usage example.
    
    Attributes:
        attr_name: Description
        
    Example:
        >>> obj = NewClass()
        >>> result = obj.do_something()
        >>> print(result)
        
    Raises:
        ValueError: If input is invalid
    """
    
    def __init__(self) -> None:
        """Initialize new class."""
        logger.info("NewClass initialized")
    
    def do_something(self) -> Any:
        """
        Do something useful.
        
        Returns:
            Result of operation
            
        Raises:
            ValueError: If operation fails
        """
        try:
            # Implementation
            return result
        except Exception as e:
            logger.error(f"Operation failed: {e}")
            raise ValueError(f"Invalid input: {e}")
```

#### Step 5: Update Documentation
```bash
# Update relevant documentation
nano docs/ARCHITECTURE.md  # If system design changed
nano docs/API_REFERENCE.md  # If API endpoints changed
nano .github/copilot-instructions.md  # If dev standards changed

# Update README if user-facing changes
nano README.md
```

#### Step 6: Test Everything
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Must pass 80%+ coverage
```

#### Step 7: Commit Changes
```bash
# Stage changes
git add src/core/new_module.py
git add tests/unit/test_new_feature.py
git add docs/ARCHITECTURE.md

# Commit with proper convention
git commit -m "feat(core): add new feature for X

- Implement NewClass with do_something() method
- Add unit tests (100% coverage)
- Update ARCHITECTURE.md with design notes

Closes #123"
```

**Commit Convention**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

---

## Code Standards

### Python Style (PEP 8)
```python
# Good
def calculate_total(items: List[Item]) -> float:
    """Calculate total price of items."""
    return sum(item.price for item in items)

# Bad
def calc(x):  # No type hints, unclear name
    return sum([i.price for i in x])  # Unnecessary list comprehension
```

### Type Hints (Mandatory)
```python
from typing import Dict, List, Optional, Any

def process_data(
    data: List[Dict[str, Any]], 
    filter_key: Optional[str] = None
) -> Dict[str, int]:
    """Process data with optional filtering."""
    # Implementation
    return result
```

### Docstrings (Google Style)
```python
def execute_query(sql: str, params: Optional[tuple] = None) -> Dict[str, Any]:
    """
    Execute SQL query and return results.
    
    Args:
        sql: SQL query string (parameterized)
        params: Query parameters for safe execution
        
    Returns:
        Dict with keys: columns, rows, row_count
        
    Raises:
        sqlite3.Error: If query execution fails
        ValueError: If SQL is malformed
        
    Example:
        >>> db = DatabaseManager("data.db")
        >>> result = db.execute_query("SELECT * FROM users WHERE id = ?", (1,))
        >>> print(result['rows'])
    """
    # Implementation
```

### Error Handling
```python
# Good - specific exceptions, proper logging
try:
    result = engine.query(question)
except ValueError as e:
    logger.warning(f"Invalid input: {question} - {e}")
    raise HTTPException(status_code=400, detail=str(e))
except GoogleAPIError as e:
    logger.error(f"AI service failed: {e}")
    raise HTTPException(status_code=503, detail="AI service unavailable")

# Bad - bare except, no logging
try:
    result = engine.query(question)
except:
    return {"error": "something went wrong"}
```

### Naming Conventions
- **Classes**: `PascalCase` - `QueryEngine`, `DatabaseManager`
- **Functions**: `snake_case` - `execute_query`, `generate_sql`
- **Constants**: `UPPER_SNAKE_CASE` - `API_BASE_URL`, `MAX_RETRIES`
- **Private**: `_leading_underscore` - `_validate_input`, `_clean_sql`
- **Database**: `lowercase_snake_case` - `employees`, `sales_orders`

### Code Complexity Limits
- **Function length**: < 50 lines
- **Class length**: < 300 lines
- **Cyclomatic complexity**: < 10
- **Nesting depth**: < 4 levels

---

## Testing

### Running Tests
```bash
# All tests
make test

# With coverage
make test-cov

# Specific file
pytest tests/unit/test_database.py -v

# Specific test
pytest tests/unit/test_database.py::TestDatabaseManager::test_execute_query -v

# Watch mode (re-run on file changes)
pytest-watch tests/
```

### Writing Tests
```python
# tests/unit/test_example.py
import pytest
from pathlib import Path

class TestExampleFeature:
    """Test suite for example feature."""
    
    @pytest.fixture
    def sample_data(self):
        """Fixture providing sample data."""
        return {"key": "value"}
    
    def test_basic_case(self, sample_data):
        """Test basic functionality."""
        result = process(sample_data)
        assert result == expected
    
    def test_error_handling(self):
        """Test error is raised for invalid input."""
        with pytest.raises(ValueError):
            process(invalid_data)
    
    @pytest.mark.slow
    def test_integration(self, electronics_db_path):
        """Test integration with database."""
        # Uses fixture from conftest.py
        db = DatabaseManager(db_path=electronics_db_path)
        result = db.execute_query("SELECT COUNT(*) FROM employees")
        assert result['row_count'] > 0
```

### Test Coverage Requirements
- **Unit Tests**: 90% coverage
- **Integration Tests**: All API endpoints
- **Total Coverage**: Minimum 80%

### Current Test Status
```
tests/unit/test_database.py         17/17 passing ✓
tests/unit/test_query_engine.py     12/15 passing (3 fail: API rate limit)
tests/integration/test_api.py       18/18 passing ✓
tests/integration/test_data_generation.py  13/13 passing ✓

Total: 60/63 passing (95.2%)
```

---

## Debugging

### Logging Levels
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Detailed debugging information")
logger.info("General informational messages")
logger.warning("Warning messages for potential issues")
logger.error("Error messages for failures")
logger.exception("Error with full stack trace")
```

**Configure in .env**:
```bash
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

### VS Code Debugging
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "api.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "jinja": true,
      "justMyCode": false
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "${file}",
        "-v"
      ]
    }
  ]
}
```

### Debugging Tips
```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint (Python 3.7+)
breakpoint()

# Print debugging (use logger instead in production)
print(f"DEBUG: variable = {variable}")

# Better: Use logging
logger.debug(f"Variable value: {variable}")
```

### Common Issues

**Import Errors**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt
```

**Database Locked**:
```bash
# Close all database connections
pkill -f "sqlite3"

# Or delete lock file
rm data/database/*.db-journal
```

**API Rate Limit**:
```bash
# Wait 60 seconds between query bursts
# Google Gemini free tier: 10 requests/minute

# Check logs for rate limit errors
tail -f logs/app.log
```

---

## Common Tasks

### Start Development Server
```bash
# Using Make (recommended)
make start

# Manual
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
cd frontend && python3 -m http.server 3000
```

### Generate Data
```bash
# All databases
make generate

# Electronics only
python -c "from src.data.generators import main; main()"

# Airline only
python -c "from src.data.airline_generators import main; main()"
```

### Run Interactive CLI
```bash
# Multi-database CLI
python query_multi.py

# Select database interactively
python -m src.cli.query_cli
```

### Update Schema Documentation
```bash
# Generate markdown + SQL files
python -c "from src.data.schema import main; main()"
```

### Clean Generated Files
```bash
# Remove Excel + databases
make clean

# Remove everything + caches
make clean-all
```

### Run Specific Tests
```bash
# Database tests only
pytest tests/unit/test_database.py -v

# API tests only
pytest tests/integration/test_api.py -v

# Skip slow tests
pytest -m "not slow" -v

# Run with verbose output
pytest -vv --tb=short
```

---

## IDE Configuration

### VS Code (Recommended)

**Extensions**:
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "ms-toolsai.jupyter",
    "github.copilot"
  ]
}
```

**Settings** (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

### PyCharm

**Setup**:
1. Open project folder
2. File → Settings → Project → Python Interpreter
3. Select `.venv/bin/python`
4. Enable pytest: Settings → Tools → Python Integrated Tools → Testing → pytest

---

## Troubleshooting

### Virtual Environment Not Activating
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Module Import Errors
```bash
# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/Volumes/Extreme SSD/code/sql schema"

# Or in Python
import sys
sys.path.insert(0, '/Volumes/Extreme SSD/code/sql schema')
```

### Tests Failing
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall test dependencies
pip install pytest pytest-cov

# Run with verbose output
pytest -vv --tb=long
```

### Server Won't Start
```bash
# Check port availability
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Kill existing processes
make stop

# Clear cache and restart
make restart
```

### Database Generation Fails
```bash
# Check logs
tail -f logs/app.log

# Verify dependencies
pip list | grep -E "pandas|Faker|openpyxl"

# Manually create directories
mkdir -p data/database data/excel
```

---

## See Also

- **[.github/copilot-instructions.md](../.github/copilot-instructions.md)** - Complete development standards
- **[docs/ARCHITECTURE.md](ARCHITECTURE.md)** - System design
- **[docs/API_REFERENCE.md](API_REFERENCE.md)** - API specifications
- **[docs/TESTING_SUMMARY.md](TESTING_SUMMARY.md)** - Test coverage
- **[docs/MAKE_COMMANDS.md](MAKE_COMMANDS.md)** - Build commands

---

**Trust the docs, not the memory.** 📚  
**Read first, code second.** 🎯
