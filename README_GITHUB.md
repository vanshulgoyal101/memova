# 🚀 Memova

**AI-Powered Multi-Database Query Platform**

Ask questions in plain English, get instant insights from your data. No SQL required.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/memova)

---

## ✨ Features

🗣️ **Natural Language Queries** - Ask questions like "How many sales last month?"  
🧠 **AI Business Analyst** - Get strategic insights and recommendations  
📊 **Auto-Charting** - Visualizations automatically generated from query results  
🔍 **Trend Detection** - Statistical analysis with growth/decline patterns  
💾 **Multi-Database** - 5 demo databases (Electronics, Airline, EdTech, EdNite, Liqo Retail)  
⚡ **Fast & Free** - Powered by Groq AI (26x faster) with Gemini fallback  
🎨 **Beautiful UI** - Dark/light theme, responsive design  
⌨️ **Keyboard Shortcuts** - Power user productivity features  

---

## 🎯 Live Demo

**Production:** [https://memova.vercel.app](https://memova.vercel.app) *(after deployment)*

**Example Questions:**
- "How many employees are there?"
- "Show me top 10 customers by revenue"
- "Give me insights to improve sales" *(triggers AI analyst)*
- "What products are low in stock?"
- "Compare revenue across regions"

---

## 🏗️ Tech Stack

**Frontend:**
- Next.js 16 (App Router, Turbopack)
- React 19 + TypeScript 5
- Tailwind CSS 4
- shadcn/ui components
- Framer Motion animations

**Backend:**
- FastAPI (Python 3.11+)
- SQLite databases
- Groq AI (`llama-3.3-70b-versatile`)
- Google Gemini (fallback)

**Infrastructure:**
- Vercel (hosting)
- GitHub (version control)

---

## 🚀 Quick Start

### Option 1: Deploy to Vercel (Easiest)

1. Click the "Deploy with Vercel" button above
2. Connect your GitHub account
3. Add environment variables:
   - `GOOGLE_API_KEY` - [Get free key](https://makersuite.google.com/app/apikey)
   - `GROQ_API_KEY` - [Get free key](https://console.groq.com/keys)
4. Deploy! ✨

### Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/memova.git
cd memova

# Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Set up environment
cp .env.example .env
# Edit .env and add your API keys

# Generate databases (if not already present)
python scripts/generate_all_companies.py

# Start backend (terminal 1)
python -m uvicorn api.main:app --reload --port 8000

# Start frontend (terminal 2)
cd frontend && npm run dev

# Open http://localhost:3000
```

---

## 📚 Documentation

- **[Deployment Guide](VERCEL_DEPLOYMENT.md)** - Step-by-step Vercel setup
- **[Full Documentation](docs/README.md)** - Complete system documentation
- **[API Reference](docs/05-api/endpoints.md)** - REST API documentation
- **[Architecture](docs/02-architecture/system-overview.md)** - System design

---

## 🗄️ Databases

### Included Demo Databases

1. **Electronics Company** (12 tables, 11K+ rows)
   - Employees, Products, Sales, Inventory, Customers
   
2. **Airline Company** (16 tables)
   - Aircraft, Pilots, Flights, Passengers, Revenue
   
3. **EdTech India** (15 tables)
   - Students, Courses, Instructors, Payments, Placements
   
4. **EdNite Test Results** (5 tables, 2,540 students)
   - Test scores, Questions, Performance analysis
   
5. **Liqo Retail Chain** (5 tables, 37,857 transactions)
   - North India retail stores, FY 2022-23 data

All databases are **bundled** in the deployment for instant access.

---

## 🧠 AI Features

### Standard Queries
```
Q: "How many employees?"
A: Generated SQL: SELECT COUNT(*) FROM employees
   Result: 150 employees
   Natural language summary provided
```

### Intelligent Analysis (v3.2.0)
```
Q: "My sales are declining, help me"
A: AI generates 5 custom exploratory queries:
   1. Revenue trend analysis
   2. Customer churn investigation
   3. Product performance comparison
   4. Inventory stockout risks
   5. Customer satisfaction metrics
   
   Provides 6-10 actionable recommendations
```

### Auto-Charting
- AI decides if visualization is helpful
- Detects optimal chart type (bar, line, pie, etc.)
- Statistical trend detection
- Growth/decline insights

---

## 🔑 Environment Variables

Create `.env` file:

```bash
# Required
GOOGLE_API_KEY=your-gemini-api-key
GROQ_API_KEY=your-groq-api-key

# Optional
LOG_LEVEL=INFO
```

**Get Free API Keys:**
- **Groq:** https://console.groq.com/keys (100K tokens/day)
- **Gemini:** https://makersuite.google.com/app/apikey (550 req/day with rotation)

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Test specific module
pytest tests/unit/test_query_engine.py -v
```

**Test Coverage:** 95.2% (94/94 tests passing)

---

## 📊 Performance

- **Query Response:** < 0.5s (with caching)
- **AI Generation:** 0.35s (Groq cached) / 1.5s (Gemini)
- **Prompt Caching:** 98% token reduction
- **Database Queries:** < 100ms

---

## 🛠️ Development

### Project Structure
```
/
├── api/              # FastAPI backend
├── frontend/         # Next.js UI
├── src/
│   ├── core/        # Query engine, AI clients
│   ├── data/        # Data generators
│   └── utils/       # Utilities
├── data/database/   # SQLite files
├── docs/            # Documentation
└── tests/           # Test suite
```

### Key Commands

```bash
# Development
make start          # Start web server
make stop           # Stop servers
make restart        # Restart + clear cache

# Data Generation
make generate       # Generate all databases

# Testing
make test           # Run test suite
make test-cov       # With coverage report

# Cleanup
make clean          # Remove generated files
```

---

## 🤝 Contributing

Contributions welcome! Please read our [Contributing Guide](docs/04-development/setup.md).

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🌟 Acknowledgments

- **Groq** - Lightning-fast AI inference
- **Google Gemini** - Reliable AI fallback
- **Vercel** - Seamless deployment
- **shadcn/ui** - Beautiful components
- **Next.js** - React framework

---

## 📧 Contact

**Project:** [github.com/YOUR_USERNAME/memova](https://github.com/YOUR_USERNAME/memova)  
**Issues:** [Report a bug](https://github.com/YOUR_USERNAME/memova/issues)  
**Discussions:** [Community forum](https://github.com/YOUR_USERNAME/memova/discussions)

---

**Built with ❤️ using Context Engineering methodology**

*Turn data into decisions, questions into insights.* 🚀
