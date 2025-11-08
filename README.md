# Multi-Database Query System

> **Production-Ready AI-Powered Database Query Platform**  
> Natural language queries • Multiple databases • Modern web interface • Context Engineering architecture

AI-powered database query system supporting multiple company databases with natural language queries via Google Gemini AI. Built with FastAPI, React, and Context Engineering principles for maximum maintainability and scalability.

## 🚀 Quick Start

### Web Interface (Recommended) 🌐

#### Using Make Commands (Easiest)
```bash
# Start web server (frontend + backend)
make start

# Stop web server
make stop

# Restart and clear cache
make restart
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

#### Manual Commands
```bash
# One-command start
./start_web.sh

# Or manually:
# 1. Start backend
python -m uvicorn api.main:app --reload --port 8000

# 2. Start frontend (in new terminal)
cd frontend && python3 -m http.server 3000

# 3. Open http://localhost:3000 in your browser
```

### Command Line Interface
```bash
# Interactive database selection
python query_multi.py

# Or specify database directly
python query_multi.py airline "How many aircraft are in the fleet?"
python query_multi.py electronics "What are our top selling products?"
```

### Setup Steps

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Configure API Key
```bash
# Create .env file
GOOGLE_API_KEY=your-key-here
```
Get free API key: [Google AI Studio](https://makersuite.google.com/app/apikey)

#### 3. Generate All Data
```bash
# Generate all three companies (electronics + airline + edtech)
python scripts/generate_all_companies.py
```

## ✨ Key Features

### � Context Engineering Architecture
- **Documentation-First**: Single source of truth in `docs/`
- **Scalable Design**: Multi-level documentation system
- **Zero Memory Dependency**: Works from current state, not conversation history
- **Professional Standards**: Industry best practices enforced
- **Comprehensive Testing**: 95% test coverage (60/63 tests passing)

### 🌐 Modern Web Interface
- **Elegant UI**: React + Tailwind CSS minimalistic design
- **Real-time Queries**: AI-powered SQL generation in seconds
- **Triple Databases**: Switch between Electronics, Airline & EdTech companies
- **Interactive Results**: Table visualization with syntax highlighting
- **Example Queries**: Pre-built queries for quick exploration
- **Live Statistics**: System metrics and database info
- **Error Handling**: User-friendly error messages
- **Ports**: Frontend (3000) • Backend API (8000)

### 🤖 AI-Powered Query Engine
- **Natural Language**: Ask questions in plain English
- **Google Gemini AI**: Latest gemini-2.0-flash-exp model
- **Schema-Aware**: Understands your database structure
- **Fast Execution**: < 2 second response time
- **SQL Transparency**: Shows generated SQL queries
- **Error Recovery**: Handles ambiguous questions gracefully
- **Rate Limit Aware**: 11 API keys with automatic rotation (550 req/day capacity)

### 📊 Comprehensive Databases
- **3 Complete Datasets**: Electronics + Airline + EdTech companies
- **43 Tables Total**: 12 electronics, 16 airline, 15 edtech
- **11,265+ Rows**: Realistic business data
- **Rich Relationships**: Foreign keys, constraints
- **Real-World Scenarios**: Sales, HR, operations, finance, education

### Database Coverage

#### Electronics Company (12 Tables)
- HR (employees, salaries, departments)
- Sales (transactions, targets, commissions)
- Finance (budgets, expenses, P&L)
- Inventory (stock levels, warehouses)
- Products (SKUs, categories, pricing)
- Customers (profiles, segments, loyalty)
- Suppliers (vendors, contracts, ratings)
- Orders (purchases, fulfillment, tracking)
- Returns (RMA, refunds, reasons)
- Warranty (claims, coverage, repairs)
- Shipments (logistics, carriers, tracking)
- Support (tickets, resolution, satisfaction)

#### Airline Company (16 Tables)
- Aircraft (fleet, maintenance, value)
- Pilots (certifications, hours, salary)
- Cabin Crew (positions, languages, training)
- Flights (schedules, delays, capacity)
- Passengers (tickets, baggage, loyalty)
- Maintenance Records (costs, downtime, work orders)
- Airports (facilities, capacity, location)
- Revenue (sources, payments, taxes)
- Fuel Consumption (usage, costs, efficiency)
- Ground Staff (positions, shifts, ratings)
- Baggage (tracking, status, handling)
- Incidents (safety reports, investigations)
- Loyalty Program (tiers, points, benefits)
- Routes (profitability, schedules, competition)
- Catering (meals, costs, quality)
- Weather Data (conditions, delays, forecasts)

#### EdTech India Company (15 Tables)
- Students (profiles, enrollment, demographics)
- Instructors (qualifications, experience, ratings)
- Courses (curriculum, pricing, duration)
- Enrollments (student-course relationships, progress)
- Assessments (quizzes, exams, assignments)
- Grades (scores, feedback, rankings)
- Payments (tuition, fees, scholarships)
- Attendance (tracking, reporting)
- Placements (job offers, companies, salaries)
- Certificates (completions, credentials)
- Course Materials (resources, videos, documents)
- Feedback (course reviews, instructor ratings)
- Departments (academic divisions, programs)
- Batches (cohorts, schedules, capacity)
- Financial Aid (scholarships, loans, grants)

## 📖 Usage Examples

### Interactive Mode
```bash
$ python query_multi.py

🗄️  SELECT DATABASE TO QUERY
Available Databases:
  1. Electronics Company ✅
  2. Airline Company ✅
  3. EdTech India Company ✅

Select database (1-3): 2

📊 Selected: Airline Company

💬 Ask your question (or 'quit' to exit):
> How many aircraft are in the fleet?

📝 SQL: SELECT count(*) FROM aircraft
✅ Success! (1 rows in 0.003s)

count(*)
--------
350
```

### Command-Line Mode
```bash
# Simple COUNT
python query_multi.py airline "How many pilots do we have?"

# TOP N with ORDER BY
python query_multi.py airline "Show me the top 5 pilots with most flight hours"

# JOIN query
python query_multi.py airline "Show me flights with their aircraft type"

# GROUP BY aggregation
python query_multi.py airline "What is the total revenue by payment method?"

# Complex analysis
python query_multi.py electronics "Show me products with low inventory that need reordering"
```

## 📊 Query Test Results

### Airline Database - All Tests Passed ✅

| Test | Question | SQL Pattern | Rows | Time |
|------|----------|-------------|------|------|
| 1 | How many aircraft? | COUNT(*) | 1 | 0.003s |
| 2 | Top 5 pilots by hours | ORDER BY + LIMIT | 5 | 0.003s |
| 3 | Flights with aircraft | JOIN | 100 | 0.002s |
| 4 | Revenue by payment | GROUP BY + SUM | 4 | 0.002s |

### Electronics Database - All Tests Passed ✅
See [QUERY_TESTS.md](docs/QUERY_TESTS.md) for detailed test results (8 complex tests, 100% accuracy verified against Excel).

## 🏗️ Project Structure

```
sql-schema/
├── .github/
│   └── copilot-instructions.md      # ← Context Engineering guide
├── docs/                             # ← Documentation (READ FIRST)
│   ├── ARCHITECTURE.md              # System design & data flow
│   ├── API_REFERENCE.md             # REST API endpoints
│   ├── DATABASE_SCHEMA.md           # Database schema docs
│   ├── DEVELOPMENT.md               # Development guide
│   ├── TESTING_SUMMARY.md           # Test coverage report
│   ├── MAKE_COMMANDS.md             # Build commands reference
│   ├── electronics_schema.sql       # SQL DDL
│   └── airline_schema.sql           # SQL DDL
├── src/                              # Core business logic
│   ├── cli/
│   │   └── query_cli.py             # Interactive CLI
│   ├── core/
│   │   ├── database.py              # DatabaseManager class
│   │   └── query_engine.py          # AI query processing
│   ├── data/
│   │   ├── generators.py            # Electronics data gen
│   │   ├── airline_generators.py    # Airline data gen
│   │   ├── converters.py            # Excel → SQL converter
│   │   └── schema.py                # Schema generator
│   └── utils/
│       ├── config.py                # Configuration
│       ├── logger.py                # Logging setup
│       └── exceptions.py            # Custom exceptions
├── api/
│   └── main.py                      # FastAPI REST API
├── frontend/
│   ├── src/
│   │   └── app/                     # Next.js 14 App Router
│   │       ├── layout.tsx           # Root layout
│   │       ├── page.tsx             # Home page
│   │       └── globals.css          # Global styles
│   ├── public/                      # Static assets
│   ├── package.json                 # Node dependencies
│   ├── tsconfig.json                # TypeScript config
│   ├── tailwind.config.ts           # Tailwind CSS config
│   └── .nvmrc                       # Node version (20)
├── tests/                            # Test suite (95% coverage)
│   ├── conftest.py                  # Pytest fixtures
│   ├── unit/
│   │   ├── test_database.py         # DB manager tests
│   │   └── test_query_engine.py     # Query engine tests
│   └── integration/
│       ├── test_api.py              # API endpoint tests
│       └── test_data_generation.py  # Data quality tests
├── data/
│   ├── excel/
│   │   ├── electronics_company/     # 12 Excel files
│   │   └── airline_company/         # 16 Excel files
│   └── database/
│       ├── electronics_company.db   # SQLite (480 KB, 12 tables)
│       └── airline_company.db       # SQLite (1.37 MB, 16 tables)
├── scripts/
│   ├── generate_all.py              # Generate all data
│   └── examples.py                  # Example queries
├── Makefile                          # Build & run commands
├── start_web.sh                      # Web server launcher
├── requirements.txt                  # Python dependencies
├── .env                              # API keys (gitignored)
└── README.md                         # ← YOU ARE HERE
```

## 🛠️ Technology Stack

### Core Technologies
- **Python**: 3.10+ (type hints, dataclasses, async/await)
- **SQLite**: Embedded relational database (28 tables, 7,520+ rows)
- **Google Gemini AI**: gemini-2.0-flash-exp (natural language → SQL)

### Web Stack
- **Backend**: FastAPI 0.100+ (async REST API, auto-docs)
- **Frontend**: Next.js 16+ (App Router, TypeScript, React 19)
- **Styling**: Tailwind CSS 4+ (utility-first CSS framework)
- **HTTP Server**: Next.js dev server (development), Vercel/Node.js (production)

### Data Layer
- **Data Generation**: Faker 22+ (realistic synthetic data)
- **Data Processing**: Pandas 2+ (DataFrame manipulation, Excel export)
- **Excel I/O**: OpenPyXL 3.1+ (XLSX reading/writing)

### Testing & Quality
- **Testing**: Pytest 7.4+ (fixtures, markers, coverage)
- **Coverage**: pytest-cov (95.2% coverage target)
- **Linting**: PEP 8 compliance (via Pylance/Ruff)
- **Type Checking**: MyPy compatible type hints

### Development Tools
- **Configuration**: python-dotenv 1.0+ (environment variables)
- **Logging**: Python logging (DEBUG/INFO/WARNING/ERROR)
- **Build System**: Make (cross-platform commands)
- **Version Control**: Git (Context Engineering commit conventions)

### Architecture Patterns
- **Repository Pattern**: Database abstraction layer
- **Factory Pattern**: Data generator creation
- **Singleton Pattern**: Database connection pooling
- **Context Manager**: Resource cleanup (`with` statements)
- **Dependency Injection**: API endpoint services

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for complete technical architecture.

## 📝 Requirements

```txt
faker>=22.0.0
pandas>=2.0.0
openpyxl>=3.1.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
pytest>=7.4.0
```

## 🎯 Available Commands

### Make Commands (Recommended)
```bash
# Web Interface
make start      # Launch frontend (3000) + backend (8000)
make stop       # Stop all servers
make restart    # Restart + clear all caches (__pycache__, .pyc, .pytest_cache)

# Development
make install    # Install Python dependencies
make generate   # Generate all databases (electronics + airline)
make test       # Run test suite (63 tests)
make test-cov   # Run tests with coverage report

# Cleanup
make clean      # Remove generated files (Excel, databases)
make clean-all  # Clean + remove all caches
```

See [docs/MAKE_COMMANDS.md](docs/MAKE_COMMANDS.md) for complete command reference.

### Data Generation (Alternative)
```bash
# Generate both companies (recommended)
python scripts/generate_all.py

# Generate only electronics
python generate.py

# Generate only airline
python -c "from src.data.airline_generators import main; main()"
```

### Querying (Alternative)
```bash
# Interactive database selection (multi-database)
python query_multi.py

# Command-line with database selection
python query_multi.py airline "How many flights departed late?"
python query_multi.py electronics "Total revenue last month?"

# Single company (legacy)
python query.py "Your question here"
```

### Schema Generation
```bash
# Generate schema documentation (markdown + SQL)
python -c "from src.data.schema import main; main()"
```

## 🧪 Testing

### Quick Test Commands
```bash
# Fast tests only (no API calls, ~25s, 100% pass rate)
pytest -m "not slow" -q

# Run all tests including slow AI tests (~3-4 minutes)
make test

# Run with coverage report
make test-cov

# Slow integration tests only (real API calls)
pytest -m slow -v

# Run specific test file
pytest tests/unit/test_database.py -v
```

### Test Organization
- **Fast Tests** (63 tests, ~25s): No API calls, always pass, safe for CI/CD
- **Slow Tests** (14 tests, ~2-3min): Real Groq/Gemini API calls, may hit quotas
- **Total**: 77 tests with 100% pass rate for fast tests

**📚 See [Testing Guide](docs/07-maintenance/TESTING.md) for detailed strategy and best practices.**

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required: Google AI API Key
GOOGLE_API_KEY=your-api-key-here

# Optional: Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Optional: Custom database paths
DB_PATH_ELECTRONICS=data/database/electronics_company.db
DB_PATH_AIRLINE=data/database/airline_company.db
```

### API Rate Limiting
- **Google Gemini Free Tier**: 10 requests/minute
- **Retry Strategy**: 60-second wait on 429 errors
- **Best Practice**: Avoid rapid-fire queries during testing

### Ports
- **Frontend**: `localhost:3000` (Python HTTP server)
- **Backend API**: `localhost:8000` (FastAPI + Uvicorn)

### Logs
- **Location**: `logs/` directory
- **Format**: Timestamped with log level
- **Rotation**: Manual cleanup required

## 📈 Performance

### Target Metrics
- **Query Response**: < 2 seconds (AI processing + database query)
- **API Response**: < 500ms (non-AI endpoints like `/databases`, `/health`)
- **Database Query**: < 100ms (SQLite execution)
- **Frontend Load**: < 1 second (initial page load)
- **Test Suite**: < 120 seconds (all 63 tests)

### Actual Performance
- **Data Generation**: ~1-2 minutes for both companies (28 tables, 7,520+ rows)
- **SQL Execution**: ~2-3ms per query (typical SELECT)
- **AI SQL Generation**: ~1-2 seconds (Google Gemini API call)
- **Database Size**: 1.88 MB total (electronics: 480 KB, airline: 1.37 MB)
- **Memory Usage**: ~50-100 MB (Python process + SQLite)

### Scalability Limits (Current)
- **Single Process**: No multi-threading/multiprocessing
- **No Caching**: Every query hits AI service
- **No Connection Pool**: Creates new DB connection per request
- **Rate Limited**: Google API free tier (10 req/min)

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for scalability improvements.

## 🚀 Advanced Usage

### Adding New Companies

1. Create generator in `src/data/`:
```python
# src/data/hospital_generators.py
def generate_patients(num_rows=300):
    # Your generator logic
    pass
```

2. Update `scripts/generate_all_companies.py`:
```python
companies = [
    ('electronics', generators),
    ('airline', airline_generators),
    ('hospital', hospital_generators),  # Add new
]
```

3. Update `query_multi.py`:
```python
databases = {
    '1': ('Electronics', 'electronics_company.db'),
    '2': ('Airline', 'airline_company.db'),
    '3': ('Hospital', 'hospital_company.db'),  # Add new
}
```

## 📚 Documentation

### Context Engineering Approach
This project uses **documentation-first development**. Before making any changes:
1. Check **[docs/INDEX.md](docs/INDEX.md)** for documentation navigation
2. Read **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** for system design
3. Check **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** for API specs  
4. Review **[.github/copilot-instructions.md](.github/copilot-instructions.md)** for coding standards
5. Use `grep` to find current implementation
6. Make changes, then update docs

### Core Documentation
- **[docs/INDEX.md](docs/INDEX.md)** ← **START HERE** for documentation navigation
  - Quick navigation by task
  - Documentation reading order
  - FAQ and troubleshooting

- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Complete development guide
  - Context Engineering philosophy (READ FIRST before coding)
  - Project structure explained
  - Development workflows (feature/bug/refactor)
  - Python coding standards & best practices
  - Testing requirements (80% min coverage)
  - API development patterns
  - Database conventions
  - Git commit conventions
  - Error handling & security
  - Performance targets & refactoring triggers

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design documentation
  - Complete architecture diagrams (ASCII art)
  - Component interactions & data flow
  - Technology stack breakdown
  - Deployment architecture (dev + production)
  - Security model & performance characteristics
  - Design patterns used (Repository, Factory, Singleton)
  - Scalability considerations & future enhancements

- **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - REST API specification
  - All 7 endpoints with request/response examples
  - Data models (TypeScript interfaces)
  - Error codes and handling
  - Rate limiting (Google API: 10 req/min)
  - CORS configuration
  - Testing examples (cURL, Python, JavaScript)

- **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Development environment guide
  - Prerequisites and system requirements
  - Environment setup (virtual env, dependencies, API keys)
  - Development workflow (5-step process)
  - Code standards (PEP 8, type hints, docstrings)
  - Testing guide (running/writing tests)
  - Debugging tips (logging, VS Code, pdb)
  - Common development tasks
  - IDE configuration (VS Code, PyCharm)
  - Troubleshooting

- **[docs/TESTING_SUMMARY.md](docs/TESTING_SUMMARY.md)** - Test coverage report
  - 60/63 tests passing (95.2% success rate)
  - Unit tests (database, query engine)
  - Integration tests (API, data generation)
  - Known issues (Google API rate limit)

- **[docs/MAKE_COMMANDS.md](docs/MAKE_COMMANDS.md)** - Build commands reference
  - `make start` - Launch web interface
  - `make stop` - Stop all servers
  - `make restart` - Restart + clear cache
  - `make test` - Run test suite
  - `make generate` - Generate data

### Schema Documentation
- **[docs/electronics_schema.md](docs/electronics_schema.md)** - Electronics database schema (12 tables)
- **[docs/airline_schema.md](docs/airline_schema.md)** - Airline database schema (16 tables)
- **[docs/electronics_schema.sql](docs/electronics_schema.sql)** - SQL DDL
- **[docs/airline_schema.sql](docs/airline_schema.sql)** - SQL DDL

## 🤝 Contributing

This project follows **Context Engineering** principles:

### Development Workflow
1. **Read Documentation First**
   - Check `.github/copilot-instructions.md` for coding standards
   - Review `docs/ARCHITECTURE.md` for system design
   - Use `grep_search` to find current implementation

2. **Make Changes**
   - Follow TDD (test-first development)
   - Keep functions < 50 lines
   - Add type hints and docstrings
   - Handle errors properly

3. **Update Documentation**
   - Update relevant `docs/*.md` files
   - Update `.github/copilot-instructions.md` if needed
   - Keep documentation as single source of truth

4. **Test Everything**
   - Run `make test` (must pass 80%+ coverage)
   - Test manually via web interface
   - Check no regressions

5. **Commit Properly**
   ```bash
   # Format: <type>(<scope>): <subject>
   git commit -m "feat(api): add /stats endpoint for query analytics"
   git commit -m "fix(query): handle null values in aggregation"
   git commit -m "docs(arch): update data flow diagram"
   ```

### Extension Ideas
- **More Databases**: Retail, healthcare, finance companies
- **Advanced Analytics**: Trends, forecasting, anomaly detection
- **Cross-Database Queries**: JOIN across multiple databases
- **Query Optimization**: Caching, query planning
- **Enhanced UI**: Charts, graphs, export to CSV/Excel
- **Authentication**: User management, access control
- **API Rate Limiting**: Smart retry with backoff
- **Real-time Updates**: WebSocket for live query results

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system design.

## ❓ Getting Help

### Troubleshooting
1. **"Query not working"** → Check Google API quota (10 req/min free tier)
2. **"Database not found"** → Run `make generate` first
3. **"Port already in use"** → Run `make stop` then `make start`
4. **"Import errors"** → Activate virtual environment: `source .venv/bin/activate`
5. **"Tests failing"** → Check logs in `logs/` directory

### Common Issues
- **API Rate Limit**: Google Gemini free tier = 10 requests/minute
  - Wait 60 seconds between query bursts
  - See `docs/ARCHITECTURE.md` for rate limiting details
- **CORS Errors**: Frontend must be on `localhost:3000` (not `file://`)
- **Database Locked**: Close other connections to `.db` files
- **Cache Issues**: Run `make restart` to clear all caches

### Documentation Reference
- System not working? → Read `docs/ARCHITECTURE.md`
- API questions? → Check `docs/API_REFERENCE.md`
- Development setup? → See `docs/DEVELOPMENT.md`
- Coding standards? → Review `.github/copilot-instructions.md`

## 📄 License

MIT License - Feel free to use this for learning and commercial projects!

## 🙏 Acknowledgments

- **Google Gemini AI**: Natural language to SQL translation (gemini-2.0-flash-exp)
- **Faker**: Realistic synthetic data generation
- **FastAPI**: Modern, high-performance Python web framework
- **React + Tailwind CSS**: Beautiful, responsive UI components
- **SQLite**: Lightweight, embedded relational database
- **Pandas**: Data manipulation and Excel export
- **Pytest**: Comprehensive testing framework
- **Context Engineering**: Documentation-first development methodology

---

**Built with ❤️ using Context Engineering principles**

**Documentation is the single source of truth** → See `docs/` for everything  
**Questions?** → Start with `.github/copilot-instructions.md`  
**Contributing?** → Follow the workflow above ⬆️
