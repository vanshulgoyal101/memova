"""
FastAPI Backend for Multi-Database Query System
Modern REST API with CORS support for frontend integration

Refactored Structure:
- api/main.py: App initialization and middleware (this file)
- api/models.py: Pydantic request/response models
- api/routes.py: All endpoint handlers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.routes import router
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Database Query API",
    description="AI-powered natural language database queries",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(router)

logger.info("FastAPI app initialized successfully")
