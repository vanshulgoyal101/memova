# Electronics Company Data Management System# Electronics Company Database + AI Query System# Electronics Appliance Company - Data Generation & LLM Query System



> **AI-Powered Database Query System with Automated Data Generation**



Production-ready Python application for generating realistic business data and querying it using natural language powered by Google Gemini AI.Generate realistic business data and query it with natural language using Google's Gemini AI.A comprehensive Python project that generates realistic business data for an electronics appliance company, converts it into a SQL database, and provides an **LLM-powered natural language query interface**.



## 🚀 Quick Start



### 1. Install Dependencies## ✨ Features## 🎯 Features

```bash

pip install -r requirements.txt

```

- 🎲 **Auto-generates** 12 Excel files with realistic business data- **Automated Data Generation**: Creates 12 realistic Excel files with 100+ rows each

### 2. Configure API Key

```bash- 🗄️ **Creates SQL database** automatically- **Multi-Department Coverage**: HR, Sales, Finance, Inventory, Products, Customers, Suppliers, and more

# Edit .env file

GOOGLE_API_KEY=your-key-here- 🤖 **AI-powered queries** - Ask questions in plain English- **SQL Database**: Automatic conversion to SQLite database

```

Get free API key: [Google AI Studio](https://makersuite.google.com/app/apikey)- 📊 **2000+ rows** of realistic data across departments- **Schema Documentation**: Auto-generated database schema in Markdown and SQL formats



### 3. Generate Data- 🆓 **Free API** - Uses Google AI Studio (Gemini)- **🤖 LLM-Powered Queries**: Ask questions in natural language and get SQL results!

```bash

python generate.py- **Multiple LLM Providers**: Supports OpenAI, Anthropic Claude, and Ollama (local)

```

## 🚀 Quick Start- **Interactive Mode**: Chat-like interface for exploring your data

### 4. Query with AI

```bash- **Production-Ready**: Clean, well-documented code with proper error handling

python query.py

```### 1. Install Dependencies



## 📁 Project Structure## 📊 Generated Data



``````bash

.

├── src/                          # Source codepip install -r requirements.txtThe system generates the following datasets:

│   ├── core/                     # Core business logic

│   │   ├── database.py          # Database management```

│   │   └── query_engine.py      # AI query engine

│   ├── data/                     # Data generation & conversion1. **Employees** (150 rows) - HR department data with salaries, departments, positions

│   │   ├── generators.py        # Excel data generation

│   │   ├── converters.py        # Excel to SQL conversion### 2. Get Free API Key2. **Products** (120 rows) - Electronic appliance catalog with pricing and specifications

│   │   └── schema.py            # Schema documentation

│   ├── cli/                      # Command-line interfaces3. **Customers** (200 rows) - Customer information and contact details

│   │   └── query_cli.py         # Interactive query CLI

│   └── utils/                    # Utilities1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)4. **Sales Orders** (300 rows) - Complete sales transaction records

│       ├── config.py            # Configuration management

│       ├── logger.py            # Logging system2. Click "Create API Key"5. **Inventory** (120 rows) - Stock levels and warehouse locations

│       └── exceptions.py        # Custom exceptions

├── data/                         # Data storage3. Copy your key6. **Suppliers** (30 rows) - Supplier information and contracts

│   ├── excel/                   # Generated Excel files

│   └── database/                # SQLite databases7. **Financial Transactions** (250 rows) - Financial records and accounting data

├── docs/                         # Documentation

│   ├── database_schema.md       # Database schema docs### 3. Configure API Key8. **Payroll** (150 rows) - Employee payroll and compensation data

│   └── API.md                   # API documentation

├── logs/                         # Application logs9. **Customer Service Tickets** (180 rows) - Support tickets and resolutions

├── scripts/                      # Utility scripts

│   ├── demo.py                  # Quick demoEdit `.env` file:10. **Marketing Campaigns** (40 rows) - Marketing campaign performance

│   ├── examples.py              # Example queries

│   └── generate_all.py          # Full pipeline (legacy)```bash11. **Shipments** (280 rows) - Delivery and logistics data

├── tests/                        # Test suite

│   ├── unit/                    # Unit testsGOOGLE_API_KEY=your-api-key-here12. **Warranties** (250 rows) - Product warranty information

│   └── integration/             # Integration tests

├── query.py                      # 🎯 Main entry point for queries```

├── generate.py                   # 🎯 Main entry point for data generation

├── .env                          # Configuration## 🚀 Quick Start

└── requirements.txt              # Python dependencies

```### 4. Generate Data



## 💡 Usage### Prerequisites



### Generate Data```bash

```bash

python generate.pypython main.py- Python 3.8 or higher

```

Creates 12 Excel files with 2000+ rows of realistic business data, converts to SQL database, and generates schema documentation.```- pip (Python package manager)



### Query with AI- (Optional) OpenAI API key, Anthropic API key, or Ollama for LLM queries

```bash

# Interactive modeThis creates:

python query.py

- `excel_files/` - 12 Excel files### Installation

# Single question

python query.py "How many employees do we have?"- `electronics_company.db` - SQLite database  

```

- `database_schema.md` - Documentation1. Clone or download this repository

### Example Questions

- "What are the top 10 customers by total purchases?"2. Install Python dependencies:

- "Show me products with inventory below 50 units"

- "Calculate average salary by department"### 5. Query with AI

- "Which warehouse has the highest inventory value?"

```bash

## 🏗️ Architecture

```bashpip install -r requirements.txt

### Core Components

python llm_query.py```

**Query Engine** (`src/core/query_engine.py`)

- Natural language to SQL conversion```

- Auto model detection (Gemini)

- Query validation and optimization### Basic Usage - Generate Data

- Result formatting

Then ask questions:

**Database Manager** (`src/core/database.py`)

- Connection pooling```Run the main pipeline to generate Excel files, SQL database, and schema:

- Transaction management

- Schema introspection💬 Question: How many employees do we have?

- Query execution

💬 Question: What are the top 5 products by price?```bash

**Data Generators** (`src/data/generators.py`)

- Realistic data generation using Faker💬 Question: Show me total revenue by departmentpython main.py

- 12 business datasets

- Referential integrity``````

- Configurable row counts



## 📊 Generated Datasets

## 📝 Example QuestionsThis will create:

| Dataset | Rows | Description |

|---------|------|-------------|- `excel_files/` - Directory with 12 Excel files

| Employees | 150 | HR records with salaries |

| Products | 120 | Product catalog |- "How many employees do we have?"- `electronics_company.db` - SQLite database

| Customers | 200 | Customer information |

| Sales Orders | 300 | Transaction records |- "What are the top 10 customers by total purchases?"- `database_schema.md` - Markdown documentation

| Inventory | 120 | Stock levels |

| Suppliers | 30 | Supplier data |- "Show me products with low inventory (less than 50 units)"- `database_schema.sql` - SQL DDL file

| Financial | 250 | Financial transactions |

| Payroll | 150 | Payroll records |- "Calculate average salary by department"

| Support Tickets | 180 | Customer service |

| Campaigns | 40 | Marketing data |- "Which warehouse has the highest inventory value?"## 🤖 LLM-Powered Query Interface

| Shipments | 280 | Delivery records |

| Warranties | 250 | Warranty information |- "List all pending customer service tickets"



## 🧪 Testing### Setup LLM Provider



```bash## 🧪 Run Tests

# Run all tests

pytestChoose ONE of the following options:



# Run with coverage```bash

pytest --cov=src

pytest tests/ -v#### Option 1: OpenAI (GPT-4)

# Run specific test suite

pytest tests/unit/```

pytest tests/integration/

```1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)



## 📝 Configuration## 📊 Generated Data2. Set environment variable:



Edit `.env` file:



```bash| Dataset | Rows | Description |```bash

# Database

DATABASE_PATH=data/database/electronics_company.db|---------|------|-------------|export OPENAI_API_KEY="sk-your-key-here"

EXCEL_OUTPUT_DIR=data/excel

| Employees | 150 | HR records with salaries, departments |```

# API

GOOGLE_API_KEY=your-api-key-here| Products | 120 | Product catalog with pricing |



# Logging| Customers | 200 | Customer information |#### Option 2: Anthropic (Claude)

LOG_LEVEL=INFO

LOG_FILE=logs/app.log| Sales Orders | 300 | Transaction records |



# Query Engine| Inventory | 120 | Stock levels |1. Get API key from [Anthropic Console](https://console.anthropic.com/)

MAX_QUERY_RESULTS=1000

DEFAULT_RESULT_LIMIT=100| Suppliers | 30 | Supplier data |2. Set environment variable:



# Data Generation| Financial | 250 | Financial transactions |

DEFAULT_EMPLOYEE_COUNT=150

DEFAULT_PRODUCT_COUNT=120| Payroll | 150 | Payroll records |```bash

```

| Support Tickets | 180 | Customer service |export ANTHROPIC_API_KEY="sk-ant-your-key-here"

## 🔒 Features

| Campaigns | 40 | Marketing data |```

✅ **Production-Ready**

- Comprehensive error handling| Shipments | 280 | Delivery records |

- Structured logging

- Configuration management| Warranties | 250 | Warranty info |#### Option 3: Ollama (Local/Free)

- Type hints throughout



✅ **AI-Powered**

- Google Gemini integration## 🏗️ Project Structure1. Install Ollama from [ollama.ai](https://ollama.ai)

- Auto model detection

- Complex query support2. Start Ollama server:

- Natural language understanding

```

✅ **Data Management**

- Automated Excel generation.```bash

- SQL database creation

- Schema documentation├── main.py                  # Generate all dataollama serve

- Data validation

├── generate_data.py         # Excel generation```

✅ **Developer-Friendly**

- Clean architecture├── convert_to_sql.py        # SQL conversion

- Comprehensive tests

- Well-documented code├── llm_query.py            # 🤖 AI query interface3. Pull a model (recommended: llama3.1 or codellama):

- Easy to extend

├── demo.py                  # Quick demo

## 📚 Documentation

├── example_queries.py       # Example questions```bash

- [Quick Start Guide](docs/QUICKSTART.md)

- [API Documentation](docs/API.md)├── tests/                   # Test suiteollama pull llama3.1

- [Database Schema](docs/database_schema.md)

- [Production Guide](docs/PRODUCTION_READY.md)├── .env                     # API key (create this)```



## 🤝 Contributing└── requirements.txt         # Dependencies



1. Fork the repository```### Interactive Query Mode

2. Create a feature branch

3. Make your changes

4. Run tests

5. Submit a pull request## 💡 Usage ModesStart the interactive LLM query interface:



## 📄 License



Open source - free for educational and commercial use.### Interactive Mode```bash



## 🆘 Support```bash# With OpenAI



- Check logs in `logs/app.log`python llm_query.pypython llm_query.py --provider openai

- Run tests: `pytest -v`

- View schema: `python query.py` then type `schema````



---# With Anthropic



**Made with ❤️ and AI** | Production-Ready | v1.0.0### Single Questionpython llm_query.py --provider anthropic


```bash

python llm_query.py "How many employees?"# With Ollama (local)

```python llm_query.py --provider ollama

```

### Run Demo

```bashThen ask questions in natural language:

python demo.py

``````

💬 Your question: What are the top 5 best-selling products?

### Run Examples💬 Your question: Show me employees earning more than $100,000

```bash💬 Your question: Which customers have made purchases in the last 30 days?

python example_queries.py💬 Your question: Calculate total revenue by product category

``````



## 🔧 How It Works### Single Question Mode



1. **Gemini AI** reads your database schemaAsk a single question without interactive mode:

2. You ask a question in plain English

3. **AI generates SQL** query automatically```bash

4. Query executes and returns resultspython llm_query.py --provider openai --question "What is the total revenue?"

5. Results displayed in formatted table```



## 🆓 Why Google AI Studio?### Example Queries



- ✅ **Free** - No credit card requiredRun pre-built example queries:

- ✅ **Fast** - Latest Gemini models

- ✅ **Auto-detection** - Uses best available model```bash

- ✅ **Simple** - Just one API key neededpython example_queries.py

```

## 📄 Files

## 📝 Example Questions You Can Ask

- **main.py** - Main data generation pipeline

- **llm_query.py** - AI query engine### Simple Queries

- **generate_data.py** - Creates realistic Excel data- "How many employees do we have?"

- **convert_to_sql.py** - Converts Excel to SQLite- "List all products"

- **demo.py** - Quick demonstration- "Show me customers from California"

- **example_queries.py** - Pre-built examples

- **tests/** - Automated test suite### Aggregations

- "What is the total revenue from all sales?"

## 🛠️ Customization- "Calculate average salary by department"

- "How many products in each category?"

### Change Data Volume

### Complex Joins

Edit `generate_data.py`:- "Top 10 customers by total purchase amount"

```python- "Which employees processed the most orders?"

num_employees = 150  # Change this- "Products with low inventory (less than 50 units)"

num_products = 120   # Change this

```### Analytics

- "Monthly sales trend for the last 6 months"

### Add More Tables- "Customer retention rate"

- "Most profitable product categories"

Add new generator functions in `generate_data.py` following existing patterns.- "Warehouse with highest inventory value"



## 🐛 Troubleshooting### Time-Based

- "Sales in the last 30 days"

### API Key Error- "Pending customer service tickets"

```bash- "Employees hired this year"

# Make sure .env file has your key

cat .env## 🏗️ Project Structure

# Should show: GOOGLE_API_KEY=AIza...

``````

.

### Module Not Found├── main.py                      # Main pipeline - generates everything

```bash├── generate_data.py             # Excel file generation logic

pip install -r requirements.txt├── convert_to_sql.py            # Excel to SQL conversion

```├── generate_schema.py           # Schema documentation generator

├── llm_query.py                # 🤖 LLM-powered query interface

### Database Not Found├── example_queries.py           # Example query demonstrations

```bash├── requirements.txt             # Python dependencies

# Run data generation first├── .env.example                 # Environment variables template

python main.py├── README.md                    # This file

```├── excel_files/                 # Generated Excel files (created on run)

├── electronics_company.db       # SQLite database (created on run)

## 📚 Learn More├── database_schema.md           # Schema documentation (created on run)

└── database_schema.sql          # SQL DDL (created on run)

- [Google AI Studio](https://makersuite.google.com/)```

- [Gemini API Docs](https://ai.google.dev/)

## 💡 How It Works

## 🤝 Contributing

### 1. Data Generation (`generate_data.py`)

Feel free to submit issues and pull requests!- Uses Faker library to generate realistic data

- Creates 12 different datasets for various business functions

## 📄 License- Maintains referential integrity with realistic relationships

- Exports to Excel format with proper formatting

Open source - free for educational and commercial use.

### 2. SQL Conversion (`convert_to_sql.py`)

---- Reads all Excel files from `excel_files/` directory

- Infers data types automatically

**Made with ❤️ and AI** | Get started in < 5 minutes- Creates SQLite database with proper schema

- Handles data type conversions and NULL values

### 3. Schema Documentation (`generate_schema.py`)
- Analyzes database structure
- Generates comprehensive Markdown documentation
- Creates SQL DDL for database recreation
- Includes table relationships and sample data

### 4. LLM Query Engine (`llm_query.py`)
- Feeds database schema to LLM as context
- Converts natural language questions to SQL
- Executes generated queries safely
- Formats and displays results in readable tables
- Supports OpenAI, Anthropic, and Ollama

## 🔒 Security Notes

- The LLM only generates SELECT queries (read-only by default)
- No API keys are stored in code - use environment variables
- Database file is local (SQLite) - no external connections
- All queries are executed in a sandboxed environment

## 🎓 Use Cases

- **Learning SQL**: Ask questions and see how they translate to SQL
- **Data Analysis**: Quickly explore your business data
- **Prototyping**: Test database designs with realistic data
- **Training**: Demonstrate natural language to SQL capabilities
- **Development**: Rapid querying without writing SQL manually

## 🛠️ Customization

### Add More Tables

Edit `generate_data.py` and add new data generation functions following the existing pattern.

### Change Data Volume

Modify the row counts in `generate_data.py`:
```python
num_employees = 150  # Change this number
num_products = 120   # Change this number
# etc.
```

### Use Different LLM Models

Edit the model names in `llm_query.py`:
```python
self.model = "gpt-4o"  # Change to gpt-4-turbo, gpt-3.5-turbo, etc.
self.model = "claude-3-5-sonnet-20241022"  # Latest Claude
self.model = "llama3.1"  # Or codellama, mistral, etc.
```

## 📊 Database Schema Quick Reference

**Main Tables:**
- `employees` - Employee records
- `products` - Product catalog
- `customers` - Customer information
- `sales_orders` - Sales transactions
- `inventory` - Stock levels
- `suppliers` - Supplier data
- `financial_transactions` - Financial records
- `payroll` - Payroll data
- `customer_service_tickets` - Support tickets
- `marketing_campaigns` - Campaign data
- `shipments` - Shipping records
- `warranties` - Warranty information

See `database_schema.md` for complete details.

## 🐛 Troubleshooting

### LLM API Key Not Found
```bash
# Make sure to export your API key
export OPENAI_API_KEY="your-key"
# Or add to ~/.zshrc or ~/.bashrc for persistence
```

### Ollama Connection Error
```bash
# Make sure Ollama is running
ollama serve

# In another terminal, verify it's working
ollama list
```

### Module Not Found Error
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 📄 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📧 Support

For questions or issues, please create an issue in the repository.

---

**Happy Querying! 🚀**
