#!/bin/bash

# QueryPilot - Quick Setup Script
# This script helps you get started with QueryPilot quickly

set -e

#!/bin/bash
# Memova - Quick Setup Script
# This script helps you get started with Memova quickly

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Memova - Quick Setup"
echo "============================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - GOOGLE_API_KEY (get from https://makersuite.google.com/app/apikey)"
    echo "   - GROQ_API_KEY (get from https://console.groq.com/keys)"
    echo ""
    read -p "Press Enter after you've added your API keys..."
else
    echo "✅ .env file already exists"
fi

# Check if databases exist
if [ ! -f "data/database/electronics_company.db" ]; then
    echo ""
    echo "📊 Databases not found. Generating demo databases..."
    echo "This will take ~2-3 minutes..."
    python scripts/generate_all_companies.py
    echo "✅ Databases generated"
else
    echo "✅ Databases already exist"
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Python dependencies installed"

# Install frontend dependencies
echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install > /dev/null 2>&1
echo "✅ Frontend dependencies installed"
cd ..

echo ""
echo "✨ Setup complete! You can now:"
echo ""
echo "  Option 1: Use Make commands (recommended)"
echo "    make start     # Start both frontend and backend"
echo "    make stop      # Stop servers"
echo ""
echo "  Option 2: Manual start"
echo "    Terminal 1: python -m uvicorn api.main:app --reload --port 8000"
echo "    Terminal 2: cd frontend && npm run dev"
echo ""
echo "  Then open: http://localhost:3000"
echo ""
echo "🎉 Happy querying!"
