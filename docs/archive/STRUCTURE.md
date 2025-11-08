# 📊 Project Structure

## Directory Layout

```
.
├── .github/                    # GitHub configuration
├── .venv/                      # Python virtual environment
│
├── data/                       # 📁 Generated Data
│   ├── excel/                 # Excel files (12 files)
│   └── database/              # SQLite database
│
├── docs/                       # 📚 Documentation
│   ├── database_schema.md     # Complete schema documentation
│   ├── database_schema.sql    # SQL DDL statements
│   ├── QUICKSTART.md          # Quick start guide
│   ├── PRODUCTION_READY.md    # Production deployment guide
│   └── README_OLD.md          # Legacy documentation
│
├── logs/                       # 📝 Application Logs
│   └── app.log                # Main application log
│
├── scripts/                    # 🔧 Utility Scripts
│   ├── demo.py                # Quick demonstration
│   ├── examples.py            # Example queries
│   └── generate_all.py        # Full pipeline (legacy)
│
├── src/                        # 💻 Source Code
│   ├── __init__.py
│   │
│   ├── core/                  # Core Business Logic
│   │   ├── __init__.py
│   │   ├── database.py        # Database connection management
│   │   └── query_engine.py    # AI-powered query engine
│   │
│   ├── data/                  # Data Pipeline
│   │   ├── __init__.py
│   │   ├── generators.py      # Excel data generation
│   │   ├── converters.py      # Excel to SQL conversion
│   │   └── schema.py          # Schema documentation generation
│   │
│   ├── cli/                   # Command-Line Interfaces
│   │   ├── __init__.py
│   │   └── query_cli.py       # Interactive query CLI
│   │
│   └── utils/                 # Utilities & Infrastructure
│       ├── __init__.py
│       ├── config.py          # Configuration management
│       ├── logger.py          # Logging system
│       └── exceptions.py      # Custom exceptions
│
├── tests/                      # ✅ Test Suite
│   ├── __init__.py
│   ├── unit/                  # Unit tests
│   │   ├── __init__.py
│   │   └── test_system.py
│   └── integration/           # Integration tests
│       └── __init__.py
│
├── .env                        # Environment configuration
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── Makefile                    # Build automation
├── README.md                   # Main documentation
├── generate.py                 # 🎯 Main: Generate data
└── query.py                    # 🎯 Main: Query interface
```

## 🎯 Entry Points

### Primary Commands

1. **`generate.py`** - Data Generation Pipeline
   - Generates 12 Excel files with realistic business data
   - Converts Excel to SQLite database
   - Creates schema documentation
   - Verifies database integrity

2. **`query.py`** - AI Query Interface
   - Interactive query mode
   - Single question mode
   - Natural language to SQL conversion

### Utility Scripts

- **`scripts/demo.py`** - Quick demonstration with sample queries
- **`scripts/examples.py`** - Example query patterns
- **`scripts/generate_all.py`** - Legacy full pipeline script

## 📦 Source Code Organization

### Core Modules (`src/core/`)

**`database.py`**
- DatabaseManager class
- Connection pooling
- Query execution
- Schema introspection
- Transaction management

**`query_engine.py`**
- QueryEngine class
- Google Gemini integration
- Natural language processing
- SQL generation and validation
- Result formatting

### Data Pipeline (`src/data/`)

**`generators.py`**
- 12 data generation functions
- Realistic business data using Faker
- Referential integrity
- Configurable row counts

Datasets:
- Employees (150 rows)
- Products (120 rows)
- Customers (200 rows)
- Sales Orders (300 rows)
- Inventory (120 rows)
- Suppliers (30 rows)
- Financial Transactions (250 rows)
- Payroll (150 rows)
- Customer Service (180 rows)
- Marketing Campaigns (40 rows)
- Shipments (280 rows)
- Warranties (250 rows)

**`converters.py`**
- Excel to SQL conversion
- Database creation
- Data validation
- Sample queries for verification

**`schema.py`**
- Markdown documentation generation
- SQL DDL generation
- Table relationships
- Column descriptions

### CLI Interface (`src/cli/`)

**`query_cli.py`**
- Interactive mode
- Single query mode
- Result formatting
- Error handling

### Infrastructure (`src/utils/`)

**`config.py`**
- Configuration management
- Environment variable loading
- Path management
- Validation

**`logger.py`**
- Dual output (console + file)
- Structured formatting
- Log level configuration

**`exceptions.py`**
- Custom exception hierarchy
- Specific error types
- Better error messages

## 🔄 Data Flow

```
1. Data Generation
   generators.py → Excel files (data/excel/)

2. SQL Conversion
   converters.py → SQLite DB (data/database/)

3. Schema Documentation
   schema.py → Markdown + SQL (docs/)

4. Query Execution
   query_cli.py → query_engine.py → database.py → Results
```

## 🧪 Testing Structure

```
tests/
├── unit/               # Component tests
│   └── test_system.py  # System-wide tests
└── integration/        # End-to-end tests
```

## 📝 Configuration Files

- **`.env`** - Environment variables (paths, API keys, settings)
- **`requirements.txt`** - Python package dependencies
- **`Makefile`** - Build and automation commands
- **`.gitignore`** - Version control exclusions

## 🗂️ Generated Files

### Excel Files (`data/excel/`)
- `employees.xlsx`
- `products.xlsx`
- `customers.xlsx`
- `sales_orders.xlsx`
- `inventory.xlsx`
- `suppliers.xlsx`
- `financial_transactions.xlsx`
- `payroll.xlsx`
- `customer_service_tickets.xlsx`
- `marketing_campaigns.xlsx`
- `shipments.xlsx`
- `warranties.xlsx`

### Database (`data/database/`)
- `electronics_company.db` - SQLite database with all tables

### Documentation (`docs/`)
- `database_schema.md` - Human-readable schema
- `database_schema.sql` - SQL DDL statements

### Logs (`logs/`)
- `app.log` - Application execution logs

## 🏗️ Architecture Principles

1. **Separation of Concerns**
   - Core logic isolated from CLI
   - Data pipeline separate from queries
   - Utils independent of business logic

2. **Configuration Management**
   - Centralized in `config.py`
   - Environment-based (.env)
   - Easy to modify

3. **Error Handling**
   - Custom exception hierarchy
   - Specific error types
   - Proper logging

4. **Modularity**
   - Independent components
   - Clear interfaces
   - Easy to test and extend

5. **Production Ready**
   - Comprehensive logging
   - Error recovery
   - Input validation
   - Documentation

---

**Need to add a new feature?**
1. Add module in appropriate `src/` subdirectory
2. Update `__init__.py` if creating package
3. Add tests in `tests/`
4. Update documentation
