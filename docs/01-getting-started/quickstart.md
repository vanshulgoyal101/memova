# Quickstart Guide

**Time to First Query**: 5 minutes  
**Difficulty**: Beginner

---

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- Google API Key ([Get one free](https://makersuite.google.com/app/apikey))

---

## Setup

### 1. Install Backend Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### 3. Generate Database

```bash
# Generate sample data
make generate

# Or manually:
python scripts/generate_all.py
```

**Output**: Creates 3 SQLite databases in `data/database/`:
- `electronics_company.db` (12 tables, 3,760 rows)
- `airline_company.db` (16 tables, 3,760 rows)
- `edtech_company.db` (15 tables, 3,745 rows)

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 5. Start Servers

```bash
# From root directory
make start
```

This opens:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Your First Query

1. Open http://localhost:3000 in your browser
2. Ensure "Electronics Company" is selected in the left sidebar
3. Type in the ask bar: **"How many employees are there?"**
4. Press Enter or click "Ask"
5. View the natural language answer, then expand accordions for SQL and data

### Example Queries

**Electronics Company**:
- "Show all departments with their employee counts"
- "What are the top 5 bestselling products?"
- "List customers who spent more than $1000"

**Airline Company** (switch company in sidebar first):
- "How many flights are scheduled today?"
- "Which aircraft have the highest maintenance costs?"
- "Show me all pilots and their certifications"

**EdTech Company** (switch company in sidebar first):
- "How many students are enrolled?"
- "Show me the top 5 courses by enrollment"
- "Which instructors have the highest ratings?"

---

## Quick Commands

```bash
# Start both frontend + backend
make start

# Stop servers
make stop

# Run tests
make test

# Clean generated data
make clean

# View logs
tail -f logs/app.log
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘K` or `Ctrl+K` | Focus ask bar |
| `Shift+S` | Open settings |
| `Shift+D` | Toggle database (Electronics ↔ Airline) |
| `T` | Toggle theme (Dark ↔ Light) |

---

## Troubleshooting

### "Module not found" error
```bash
# Ensure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

### "Database not found" error
```bash
# Generate databases
make generate
```

### "API key invalid" error
```bash
# Check .env file exists and has valid key
cat .env
# Should show: GOOGLE_API_KEY=your_key_here
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend 429 error (Rate limit)
- **Free tier**: 10 requests/minute
- **Solution**: Wait 60 seconds between queries
- **Better**: Get 7 API keys and configure rotation (see [API Key Rotation](../02-architecture/api-key-rotation.md))

---

## Next Steps

- [Architecture Overview](../02-architecture/system-overview.md) - Understand how it works
- [Features Guide](../03-features/natural-language.md) - Learn all features
- [Development Setup](../04-development/setup.md) - Contribute to the project
- [API Reference](../05-api/endpoints.md) - Use the REST API

---

**You're ready to start querying!** 🚀
