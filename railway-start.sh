#!/bin/bash
# Railway deployment startup script

set -e

echo "🚂 Starting Memova on Railway..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
npm run build
cd ..

# Start both servers
echo "🚀 Starting servers..."
# Start backend in background
python -m uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} &
BACKEND_PID=$!

# Start frontend
cd frontend
PORT=3000 npm start &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
