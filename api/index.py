"""
Vercel serverless function entry point
This file is required for Vercel to properly route Python backend
"""

from api.main import app

# Vercel expects a handler named 'app' or default export
# FastAPI app is already named 'app' in main.py, so we just re-export it
