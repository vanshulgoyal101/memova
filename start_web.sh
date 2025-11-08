#!/bin/bash

# Memova - Frontend Startup Script
# Starts both the FastAPI backend and opens the frontend in browser

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Memova - AI-Powered Database Query System        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if virtual environment is activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo -e "${GREEN}Activating .venv...${NC}"
    source .venv/bin/activate
fi

# Check if databases exist
if [ ! -f "data/database/electronics_company.db" ] || [ ! -f "data/database/airline_company.db" ]; then
    echo -e "${YELLOW}⚠️  Databases not found!${NC}"
    echo -e "${GREEN}Generating databases first...${NC}"
    python scripts/generate_all_companies.py
    echo ""
fi

# Start FastAPI backend in background
echo -e "${GREEN}🚀 Starting FastAPI backend on http://localhost:8000${NC}"
cd "$(dirname "$0")"
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo -e "${YELLOW}⏳ Waiting for backend to start...${NC}"
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend is running!${NC}"
else
    echo -e "${YELLOW}⚠️  Backend might still be starting...${NC}"
fi

# Start frontend server on port 3000
echo -e "${GREEN}🌐 Starting Next.js frontend on http://localhost:3000${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 3

# Open frontend in browser
echo -e "${GREEN}🌐 Opening frontend in browser...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "http://localhost:3000"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "http://localhost:3000" 2>/dev/null || echo "Please open http://localhost:3000 in your browser"
else
    echo "Please open http://localhost:3000 in your browser"
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  System is ready!                                 ║${NC}"
echo -e "${BLUE}╠════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║  Backend API: http://localhost:8000               ║${NC}"
echo -e "${BLUE}║  Frontend:    http://localhost:3000               ║${NC}"
echo -e "${BLUE}║  API Docs:    http://localhost:8000/docs          ║${NC}"
echo -e "${BLUE}╠════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║  Press Ctrl+C to stop both servers                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Keep script running and forward signals to both processes
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM

# Wait for backend process
wait $BACKEND_PID $FRONTEND_PID
