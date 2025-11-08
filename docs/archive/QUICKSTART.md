# Quick Start Guide

## 1. Setup (2 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Get free API key from: https://makersuite.google.com/app/apikey
# Add to .env file:
GOOGLE_API_KEY=your-key-here
```

## 2. Generate Data (30 seconds)

```bash
python main.py
```

Creates:
- 12 Excel files
- SQLite database
- Schema documentation

## 3. Ask Questions (Start querying!)

```bash
python llm_query.py
```

Example questions:
```
💬 How many employees do we have?
💬 What are the top 5 products?
💬 Show me total revenue
💬 List customers from California
```

## Quick Commands

| Command | What it does |
|---------|--------------|
| `python main.py` | Generate all data |
| `python llm_query.py` | Start AI query interface |
| `python demo.py` | Quick demo (3 queries) |
| `python example_queries.py` | Run 15+ examples |
| `pytest tests/ -v` | Run tests |

## Example Session

```bash
$ python llm_query.py

✅ Connected to Google AI Studio
📦 Using model: gemini-2.0-flash-exp
🗄️  Database: electronics_company.db

💬 Question: How many employees do we have?

🤔 Question: How many employees do we have?
🔄 Generating SQL query...

📝 SQL: SELECT COUNT(*) as total_employees FROM employees

✅ Success! (1 rows in 0.002s)

total_employees
--------------
150

💬 Question: exit
👋 Goodbye!
```

## Tips

- Type `exit` or `quit` to stop
- Ask complex questions - AI can handle JOINs
- Use natural language - no SQL needed
- Check `example_queries.py` for inspiration

## Need Help?

- API key issues? Check `.env` file
- No database? Run `python main.py` first
- Module errors? Run `pip install -r requirements.txt`

---

**Ready to start? Run:** `python demo.py`
