# 🌐 Web Interface Guide

## Modern Frontend for Multi-Database Query System

A beautiful, minimalistic web interface for querying your databases with natural language using AI.

## 🚀 Quick Start

### Option 1: One-Command Start (Recommended)
```bash
./start_web.sh
```

This script will:
- ✅ Activate virtual environment
- ✅ Check/generate databases if needed
- ✅ Start FastAPI backend on port 8000
- ✅ Open frontend in your browser

### Option 2: Manual Start

#### 1. Start the Backend
```bash
# From project root
python -m uvicorn api.main:app --reload --port 8000
```

#### 2. Open the Frontend
Simply open `frontend/index.html` in your web browser, or:
```bash
# macOS
open frontend/index.html

# Linux
xdg-open frontend/index.html

# Or manually navigate to:
# file:///path/to/sql schema/frontend/index.html
```

## 🎨 Features

### Modern UI Design
- **Minimalistic**: Clean, distraction-free interface
- **Responsive**: Works on desktop, tablet, and mobile
- **Elegant**: Smooth animations and transitions
- **Production-Ready**: Professional gradient design

### Key Functionality

#### 1. Database Selection
- View available databases with status indicators
- See table count and file size
- One-click switching between databases
- Visual feedback for selected database

#### 2. Natural Language Queries
- Type questions in plain English
- Real-time query execution
- See generated SQL code
- View results in formatted tables

#### 3. Example Queries
- Pre-built queries for each database
- Categorized by complexity (simple, medium, complex)
- One-click to use examples
- Learn SQL patterns

#### 4. Results Display
- Clean table formatting
- Shows row count and execution time
- Displays generated SQL
- Handles large result sets (shows first 100 rows)

#### 5. System Statistics
- Live database metrics in header
- Total tables and rows
- Real-time updates

## 📱 User Interface

### Header Section
```
🗄️ Multi-Database Query System
AI-powered natural language database queries

[2 Databases] [28 Tables] [7,520 Rows]
```

### Database Selector
```
┌─────────────────────────────────────┐
│ Electronics Company        ✓ Available│
│ 12 tables • 0.48 MB                  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Airline Company           ✓ Available│
│ 16 tables • 1.4 MB                   │
└─────────────────────────────────────┘
```

### Query Input
```
Ask a Question
┌──────────────────────────────────────┐
│ How many aircraft are in the fleet?  │ [🚀 Query] [✨ New Query]
└──────────────────────────────────────┘
```

### Example Queries
```
💡 Example Queries

┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Fleet Size       │ │ Top Pilots       │ │ Revenue Analysis │
│ simple          │ │ medium           │ │ complex          │
│ Operations      │ │ Personnel        │ │ Finance          │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

### Results Display
```
📝 Generated SQL
┌──────────────────────────────────────────────────────┐
│ SELECT count(*) FROM aircraft                        │
└──────────────────────────────────────────────────────┘

✅ Results: 350 rows • 2.5ms
┌──────────┐
│ count(*) │
├──────────┤
│   350    │
└──────────┘
```

## 🛠️ Technology Stack

### Backend (FastAPI)
- **Framework**: FastAPI 0.109+
- **Server**: Uvicorn (ASGI)
- **API**: RESTful JSON API
- **CORS**: Enabled for local development
- **Documentation**: Auto-generated at `/docs`

### Frontend (Vanilla React)
- **UI Library**: React 18 (CDN)
- **Styling**: Tailwind CSS 3 (CDN)
- **Icons**: Unicode emojis
- **Fonts**: Google Fonts (Inter)
- **No Build Step**: Pure HTML/JS

## 📡 API Endpoints

### GET `/`
Health check and API info
```json
{
  "name": "Multi-Database Query API",
  "version": "1.0.0",
  "status": "online",
  "databases": ["electronics", "airline"]
}
```

### GET `/databases`
List available databases
```json
[
  {
    "id": "electronics",
    "name": "Electronics Company",
    "path": "/path/to/electronics_company.db",
    "exists": true,
    "size_mb": 0.48,
    "table_count": 12
  }
]
```

### GET `/databases/{db_id}/schema`
Get database schema
```json
{
  "tables": [
    {
      "name": "aircraft",
      "columns": [...]
    }
  ],
  "table_count": 16
}
```

### GET `/databases/{db_id}/examples`
Get example queries
```json
[
  {
    "id": 1,
    "title": "Fleet Size",
    "question": "How many aircraft?",
    "category": "Fleet",
    "complexity": "simple"
  }
]
```

### POST `/query`
Execute natural language query
```json
Request:
{
  "question": "How many aircraft?",
  "database": "airline"
}

Response:
{
  "success": true,
  "sql": "SELECT count(*) FROM aircraft",
  "columns": ["count(*)"],
  "rows": [[350]],
  "row_count": 1,
  "execution_time": 0.0025
}
```

### GET `/stats`
System statistics
```json
{
  "total_databases": 2,
  "databases": {
    "electronics": {
      "name": "Electronics Company",
      "tables": 12,
      "total_rows": 2070,
      "size_mb": 0.48
    },
    "airline": {
      "name": "Airline Company", 
      "tables": 16,
      "total_rows": 5450,
      "size_mb": 1.4
    }
  }
}
```

## 🎯 Usage Examples

### Simple Query
```
Question: "How many aircraft are in the fleet?"

Generated SQL:
SELECT count(*) FROM aircraft

Result: 350 aircraft
```

### Complex Query
```
Question: "Show me the top 5 pilots with most flight hours"

Generated SQL:
SELECT first_name, last_name 
FROM Pilots 
ORDER BY total_flight_hours DESC 
LIMIT 5

Results:
Kara Richards
Dave Stevens
Stephanie Brown
Michael Pittman
James Davis
```

### JOIN Query
```
Question: "Show flights with their aircraft type"

Generated SQL:
SELECT F.flight_number, A.aircraft_type, F.passengers_booked 
FROM Flights AS F 
JOIN Aircraft AS A ON F.aircraft_id = A.aircraft_id

Results: 400 rows with flight details
```

## 🐛 Troubleshooting

### Backend Not Starting
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>

# Restart backend
python -m uvicorn api.main:app --reload --port 8000
```

### Frontend Not Loading Data
1. **Check Backend**: Visit http://localhost:8000/health
2. **Check Console**: Open browser DevTools (F12) and check for errors
3. **CORS Issues**: Make sure backend CORS is configured for your origin

### Database Not Found
```bash
# Generate databases
python scripts/generate_all_companies.py

# Verify databases exist
ls -lh data/database/
```

### API Connection Error
- Ensure backend is running on port 8000
- Check firewall settings
- Verify `API_BASE_URL` in frontend matches backend

## 🔧 Configuration

### Change Backend Port
```bash
# In start_web.sh or manual command
uvicorn api.main:app --port 8080  # Use port 8080

# Update frontend/index.html
const API_BASE_URL = 'http://localhost:8080';
```

### Add Custom Database
1. Add to `api/main.py`:
```python
DATABASES = {
    'electronics': {...},
    'airline': {...},
    'hospital': {  # New database
        'name': 'Hospital System',
        'path': str(Config.DATABASE_DIR / 'hospital_company.db'),
        'description': 'Patient and medical records'
    }
}
```

2. Add example queries for new database

### Customize UI Colors
Edit `frontend/index.html`:
```css
.gradient-bg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Change to your preferred gradient */
}
```

## 📊 Performance

### Metrics
- **API Response Time**: ~1-2s (SQL generation)
- **Query Execution**: 2-10ms (database query)
- **Frontend Load**: <500ms
- **Memory Usage**: ~50MB (backend)

### Optimization Tips
1. **Limit Results**: Frontend shows first 100 rows
2. **Caching**: Backend can cache schema info
3. **Compression**: Enable gzip for API responses
4. **CDN**: Host static assets on CDN for production

## 🚢 Deployment

### Development
```bash
./start_web.sh
```

### Production

#### Option 1: Traditional Server
```bash
# Install dependencies
pip install -r requirements.txt

# Start with production server
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### Option 2: Docker
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Option 3: Cloud Platform
- **Heroku**: `heroku create` + git push
- **Railway**: Connect GitHub repo
- **Vercel**: Deploy as serverless function
- **AWS**: EC2 + nginx reverse proxy

### Frontend Hosting
- **GitHub Pages**: Push `frontend/` folder
- **Netlify**: Drag & drop `frontend/` folder
- **Vercel**: Deploy static site
- **S3 + CloudFront**: AWS hosting

## 🎓 Best Practices

### Security
- [ ] Add API authentication (JWT tokens)
- [ ] Rate limiting for API endpoints
- [ ] Input validation and sanitization
- [ ] HTTPS in production
- [ ] Environment variables for secrets

### Performance
- [ ] Enable gzip compression
- [ ] Add response caching
- [ ] Database connection pooling
- [ ] Minify frontend assets for production

### User Experience
- [ ] Add query history
- [ ] Save favorite queries
- [ ] Export results to CSV/JSON
- [ ] Dark mode toggle
- [ ] Keyboard shortcuts

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **Tailwind CSS**: https://tailwindcss.com
- **Google Gemini**: https://ai.google.dev

## 🤝 Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review browser console for errors
3. Check backend logs
4. Verify databases are generated

---

**Built with ❤️ for elegant, production-ready database querying**
