#!/bin/bash
# Railway deployment startup script - Simplified

set -e

echo "🚂 Starting Memova on Railway..."
echo "PORT: ${PORT:-8000}"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Install and build frontend
echo "📦 Installing and building frontend..."
cd frontend
npm ci
npm run build

# Start backend only (Railway will proxy to it)
echo "🚀 Starting FastAPI backend on port ${PORT:-8000}..."
cd ..
exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}
