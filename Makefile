# Makefile for Electronics Company Data Management System

.PHONY: help install setup generate query test clean docs all start stop restart

# Default target
help:
	@echo "📊 Electronics Company Data Management System"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make setup      - Setup virtual environment and install deps"
	@echo "  make generate   - Generate all data (Excel + SQL + Schema)"
	@echo "  make query      - Start interactive query mode"
	@echo "  make test       - Run all tests (fast + slow, ~3-4 min)"
	@echo "  make test-fast  - Run fast tests only (~25s, no API calls)"
	@echo "  make test-slow  - Run slow integration tests (real API calls)"
	@echo "  make test-cov   - Run with coverage report"
	@echo "  make clean      - Clean generated files"
	@echo "  make docs       - View schema documentation"
	@echo "  make all        - Full setup + generation"
	@echo ""
	@echo "Web Server Commands:"
	@echo "  make start      - Start web server (frontend + backend)"
	@echo "  make stop       - Stop web server"
	@echo "  make restart    - Restart web server and clear cache"
	@echo ""

# Install dependencies
install:
	pip install -r requirements.txt

# Setup virtual environment
setup:
	python3 -m venv .venv
	@echo "✅ Virtual environment created"
	@echo "Activate with: source .venv/bin/activate"
	@echo "Then run: make install"

# Generate all data
generate:
	@python generate.py

# Start interactive query mode
query:
	@python query.py

# Run tests
test:
	@if [ -d ".venv" ]; then \
		source .venv/bin/activate && python -m pytest -v; \
	else \
		python -m pytest -v; \
	fi

# Run fast tests only (no API calls, ~25s)
test-fast:
	@if [ -d ".venv" ]; then \
		source .venv/bin/activate && python -m pytest -m "not slow" -q; \
	else \
		python -m pytest -m "not slow" -q; \
	fi

# Run slow integration tests (real API calls, ~2-3 min)
test-slow:
	@if [ -d ".venv" ]; then \
		source .venv/bin/activate && python -m pytest -m slow -v; \
	else \
		python -m pytest -m slow -v; \
	fi

# Run tests with coverage
test-cov:
	@if [ -d ".venv" ]; then \
		source .venv/bin/activate && python -m pytest --cov=src --cov-report=html --cov-report=term; \
	else \
		python -m pytest --cov=src --cov-report=html --cov-report=term; \
	fi

# Run tests without API calls (skip integration tests requiring API)
# DEPRECATED: Use 'make test-fast' instead
test-no-api:
	@echo "⚠️  This command is deprecated. Use 'make test-fast' instead."
	@if [ -d ".venv" ]; then \
		source .venv/bin/activate && python -m pytest -m "not slow" -q; \
	else \
		python -m pytest -m "not slow" -q; \
	fi

# Clean generated files
clean:
	rm -rf data/excel/*.xlsx
	rm -rf data/database/*.db
	rm -rf logs/*.log
	@echo "✅ Cleaned generated files"

# Clean everything including cache
clean-all: clean
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/*/__pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	@echo "✅ Cleaned all cache and generated files"

# View schema documentation
docs:
	@if [ -f docs/database_schema.md ]; then \
		cat docs/database_schema.md; \
	else \
		echo "❌ Schema not generated yet. Run 'make generate' first."; \
	fi

# Full setup and generation
all: install generate
	@echo ""
	@echo "✅ Setup complete!"
	@echo "Try: make query"

# Start web server (frontend + backend)
start:
	@echo "🚀 Starting web server..."
	@./start_web.sh

# Stop web server
stop:
	@echo "🛑 Stopping web server..."
	@pkill -f "uvicorn api.main:app" 2>/dev/null || true
	@pkill -f "python -m uvicorn api.main" 2>/dev/null || true
	@pkill -f "next dev" 2>/dev/null || true
	@pkill -f "http.server 3000" 2>/dev/null || true
	@echo "✅ Web server stopped"

# Restart web server and clear cache
restart: stop
	@echo ""
	@echo "🧹 Clearing cache..."
	@rm -rf __pycache__ 2>/dev/null || true
	@rm -rf api/__pycache__ 2>/dev/null || true
	@rm -rf src/__pycache__ 2>/dev/null || true
	@rm -rf src/*/__pycache__ 2>/dev/null || true
	@rm -rf tests/__pycache__ 2>/dev/null || true
	@rm -rf tests/*/__pycache__ 2>/dev/null || true
	@rm -rf .pytest_cache 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cache cleared"
	@echo ""
	@echo "🚀 Restarting web server..."
	@sleep 1
	@./start_web.sh
