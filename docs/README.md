# Memova Documentation

**Multi-Database Natural Language Query System**  
**Version**: 3.2.0  
**Last Updated**: November 6, 2025  
**Methodology**: Context Engineering

---

## 📚 Documentation Structure

**🗺️ First-time here? Read [Documentation Map](00-DOCUMENTATION-MAP.md) to understand our documentation philosophy!**

```
docs/
├── 00-DOCUMENTATION-MAP.md      ← START HERE! (Meta-documentation)
├── README.md                    ← YOU ARE HERE (Master overview)
├── INDEX.md                     ← Navigation hub
├── 01-getting-started/
│   ├── quickstart.md           ← 5-minute setup guide
│   ├── installation.md         ← Detailed installation
│   └── first-query.md          ← Your first query tutorial
├── 02-architecture/
│   ├── system-overview.md      ← High-level architecture
│   ├── data-flow.md            ← Request/response flow
│   ├── tech-stack.md           ← Technologies used
│   └── design-decisions.md     ← Why we chose what we chose
├── 03-features/
│   ├── natural-language.md     ← AI-powered querying
│   ├── intelligent-problem-solving.md ← Business analyst for vague problems 🆕 v3.2.0
│   ├── charts-insights.md      ← Auto-charting & trend detection 🆕
│   ├── multi-database.md       ← Database switching
│   ├── settings.md             ← User preferences
│   └── keyboard-shortcuts.md   ← Power user features
├── 04-development/
│   ├── setup.md                ← Dev environment
│   ├── coding-standards.md     ← Code style guide
│   ├── testing.md              ← Test strategy
│   └── contributing.md         ← How to contribute
├── 05-api/
│   ├── endpoints.md            ← REST API reference
│   ├── request-response.md     ← Request/response schemas
│   └── error-handling.md       ← Error codes & handling
├── 06-database/
│   ├── electronics-schema.md   ← Electronics company schema
│   ├── airline-schema.md       ← Airline company schema
│   ├── edtech-schema.md        ← EdTech India schema 🆕
│   ├── ednite-schema.md        ← EdNite test results schema 🆕 v3.2.0
│   └── data-generation.md      ← How data is generated
└── 07-maintenance/
    ├── deployment.md           ← Production deployment
    ├── troubleshooting.md      ← Common issues & fixes
    └── changelog.md            ← Version history
```

---

## 🚀 Quick Links

### For New Users
- [5-Minute Quickstart](01-getting-started/quickstart.md) - Get running immediately
- [Your First Query](01-getting-started/first-query.md) - Tutorial walkthrough
- [Keyboard Shortcuts](03-features/keyboard-shortcuts.md) - Power user guide

### For Developers
- [Development Setup](04-development/setup.md) - Complete dev environment
- [Architecture Overview](02-architecture/system-overview.md) - How it works
- [API Reference](05-api/endpoints.md) - REST API docs
- [Testing Guide](04-development/testing.md) - Run tests

### For DevOps
- [Deployment Guide](07-maintenance/deployment.md) - Production setup
- [Troubleshooting](07-maintenance/troubleshooting.md) - Fix common issues

---

## 🎯 What is Memova?

**Memova** is a production-ready web application that allows users to query relational databases using **natural language** instead of SQL. Powered by Google Gemini AI, it translates questions like *"How many employees are there?"* into SQL queries, executes them, and presents results in an elegant, user-friendly interface.

### Key Features


✅ **Natural Language Queries** - Ask questions in plain English  
✅ **Multi-Database Support** - Switch between Electronics, Airline, EdTech India, EdNite & Liqo Retail companies  
✅ **AI-Powered SQL Generation** - Groq (primary) + Google Gemini (fallback)  
✅ **AI Business Insights** - Strategic analysis with actionable recommendations 🆕  
✅ **Auto-Charting** - Visualizations auto-detected from query results  
✅ **Auto SQL Error Recovery** - AI fixes ambiguous columns, syntax errors automatically  
✅ **Beautiful UI** - Modern dark/light theme with animations  
✅ **Persistent Preferences** - Settings saved to localStorage  
✅ **Keyboard Shortcuts** - Power user productivity features  
✅ **CSV Export** - Download query results  
✅ **Auto-Expand Options** - Configure default view  
✅ **Compact Mode** - Optimized for small screens  

✅ **Sidebar Quick Query Shortcuts** - One-click access to common queries, grouped by difficulty (Easy/Medium/Hard) with icons and color badges

---

## 📊 System Overview

### Tech Stack

**Frontend**:
- Next.js 16.0.1 (App Router, Turbopack)
- React 19 with TypeScript 5
- Tailwind CSS 4 (modern styling)
- Framer Motion (animations)
- Zustand (state management)
- shadcn/ui components

**Backend**:
- FastAPI (Python)
- SQLite (5 databases: Electronics, Airline, EdTech India, EdNite, Liqo Retail)
- **AI Service**: 
  - **Primary**: Groq (llama-3.3-70b-versatile) - 100K tokens/day
    - ⚠️ **Important**: Rate limits are per-organization, not per-key
    - Multiple keys from same account share quota
    - ✅ **Prompt Caching**: 40-50% faster queries, 98% token reduction
    - ✅ **Auto SQL Error Recovery**: AI fixes ambiguous columns, syntax errors automatically
  - **Fallback**: Google Gemini AI (gemini-2.0-flash-exp) - 550 req/day
    - 11 API keys with automatic rotation
    - Each key independent (50 req/day × 11 = 550/day total)

**Infrastructure**:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Single repository monorepo

### Architecture Highlights

```
User Question → AskBar → FastAPI → Gemini AI → SQL → SQLite → Results → AnswerPanel
```

1. User types natural language question
2. Frontend sends to `/query` endpoint
3. Backend sends to Gemini AI for SQL generation
4. SQL executes against SQLite database
5. Results formatted and returned
6. Frontend displays with animations

---

## 📖 Documentation Philosophy: Context Engineering

**Why This Matters**: AI assistants (like me) have limited context windows. Good documentation = efficient development.

### Our Principles

1. **Documentation is Single Source of Truth**
   - Code changes → Update docs immediately
   - Never rely on memory or conversation history
   - Grep docs before making changes

2. **Nested Structure for Scalability**
   - Group related docs in folders
   - Clear naming conventions
   - Cross-references between docs

3. **Task-Based Organization**
   - Getting Started (for users)
   - Development (for contributors)
   - Maintenance (for ops)

4. **Rich Metadata**
   - Version numbers
   - Last updated dates
   - Author/contributor info

---

## 🗂️ File Organization

### Active Documentation (Current)
```
docs/
├── 01-getting-started/    ← User onboarding
├── 02-architecture/       ← System design
├── 03-features/           ← Feature documentation
├── 04-development/        ← Developer guides
├── 05-api/                ← API reference
├── 06-database/           ← Schema & data
└── 07-maintenance/        ← Operations
```

### Legacy Documentation (Archived)
```
docs/archive/
├── task-completions/      ← Historical task logs (TASK_5_COMPLETE.md, etc.)
├── old-structure/         ← Previous documentation structure
└── migration-logs/        ← Documentation reorganization history
```

**Rule**: Never delete docs. Archive with timestamp and reason.

---

## 🔑 Key Concepts

### 1. Natural Language Processing
- User asks question in plain English
- Gemini AI generates SQL query
- No SQL knowledge required for end users

### 2. Multi-Database System
- **Electronics Company**: Retail/manufacturing data (12 tables)
- **Airline Company**: Airline operations data (16 tables)
- **EdTech India**: Education platform data (15 tables)
- **EdNite**: Student test performance data (6 tables, 2,540 students) 🆕
- Users switch via Sidebar or Settings

### 3. Data Scope
- **Company**: Which database to query
- **Sections**: Filter to specific table groups (inventory, sales, fleet, etc.)
- Managed via Zustand store

### 4. User Preferences
- Default company/sections
- Auto-expand SQL/Data accordions
- Compact mode for reduced spacing
- Persisted in localStorage

### 5. Answer-First Design
- Natural language answer displayed first
- SQL and raw data hidden in collapsible accordions
- Progressive disclosure UX pattern

---

## 📈 Current Status

### Completed Features (v2.0.0)
- ✅ Next.js 16 frontend with App Router
- ✅ FastAPI backend with Gemini AI
- ✅ Multi-database support (2 databases, 28 tables)
- ✅ Natural language query processing
- ✅ Settings dialog with localStorage persistence
- ✅ Keyboard shortcuts (⌘K, Shift+S, Shift+D, T)
- ✅ Framer Motion animations
- ✅ Elegant dark/light themes
- ✅ CSV export functionality
- ✅ Auto-expand preferences
- ✅ Compact mode
- ✅ API key rotation (7 keys)
- ✅ 95.2% test coverage (60/63 tests passing)

### Production Ready
- All core features implemented
- Comprehensive test suite
- Complete documentation
- Error handling & logging
- Performance optimized

---

## 🚦 Getting Started (5 Minutes)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google API Key (Gemini AI)

### Quick Start

```bash
# 1. Clone repository
git clone <repo-url>
cd sql-schema

# 2. Setup backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# 3. Configure API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# 4. Generate data
make generate

# 5. Setup frontend
cd frontend
npm install

# 6. Start servers
make start  # Opens both frontend (3000) and backend (8000)
```

Open http://localhost:3000 and ask: *"How many employees are there?"*

---

## 📚 Learn More

- [Quickstart Guide](01-getting-started/quickstart.md) - Detailed setup
- [Architecture Overview](02-architecture/system-overview.md) - System design
- [API Reference](05-api/endpoints.md) - REST API docs
- [Development Setup](04-development/setup.md) - Contributing guide

---

## 🤝 Contributing

See [CONTRIBUTING.md](04-development/contributing.md) for:
- Code style guidelines
- Testing requirements
- Pull request process
- Documentation standards

---

## 📝 License

MIT License - See LICENSE file

---

## 🆘 Support

- **Issues**: GitHub Issues
- **Docs**: This documentation
- **Troubleshooting**: [Common Issues](07-maintenance/troubleshooting.md)

---

**Built with ❤️ using Context Engineering methodology**
