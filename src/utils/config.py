"""
Configuration management for the application
Loads and validates environment variables
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Application configuration"""
    
    # Load environment variables
    load_dotenv()
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent  # Project root
    DATA_DIR = BASE_DIR / "data"
    DATABASE_DIR = DATA_DIR / "database"
    EXCEL_DIR = DATA_DIR / "excel"
    LOGS_DIR = BASE_DIR / "logs"
    DOCS_DIR = BASE_DIR / "docs"
    
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATABASE_DIR / "electronics_company.db"))
    EXCEL_OUTPUT_DIR = os.getenv("EXCEL_OUTPUT_DIR", str(EXCEL_DIR))
    LOG_FILE = os.getenv("LOG_FILE", str(LOGS_DIR / "app.log"))
    
    # API Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Load all API keys from .env file for rotation
    @classmethod
    def get_all_api_keys(cls) -> list[str]:
        """
        Extract all Google API keys from .env file
        Reads both active and commented keys for rotation
        """
        keys = []
        env_file = cls.BASE_DIR / ".env"
        
        if not env_file.exists():
            # Fallback to current key if .env doesn't exist
            if cls.GOOGLE_API_KEY:
                return [cls.GOOGLE_API_KEY]
            return []
        
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Match lines like: GOOGLE_API_KEY=AIza... or # GOOGLE_API_KEY=AIza...
                    if 'GOOGLE_API_KEY=' in line and 'AIza' in line:
                        # Extract the key value
                        if '=' in line:
                            key = line.split('=', 1)[1].strip()
                            # Remove any trailing comments
                            key = key.split('#')[0].strip()
                            if key and key.startswith('AIza'):
                                keys.append(key)
        except Exception as e:
            # Fallback to current key on error
            if cls.GOOGLE_API_KEY:
                return [cls.GOOGLE_API_KEY]
            return []
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keys = []
        for key in keys:
            if key not in seen:
                seen.add(key)
                unique_keys.append(key)
        
        return unique_keys
    
    @classmethod
    def get_all_groq_api_keys(cls) -> list[str]:
        """
        Extract all Groq API keys from .env file for rotation
        Reads both active and commented keys
        """
        keys = []
        env_file = cls.BASE_DIR / ".env"
        
        if not env_file.exists():
            # Fallback to current key if .env doesn't exist
            if cls.GROQ_API_KEY:
                return [cls.GROQ_API_KEY]
            return []
        
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Match lines like: GROQ_API_KEY=gsk_... or # GROQ_API_KEY=gsk_...
                    if 'GROQ_API_KEY=' in line and 'gsk_' in line:
                        # Extract the key value
                        if '=' in line:
                            key = line.split('=', 1)[1].strip()
                            # Remove any trailing comments
                            key = key.split('#')[0].strip()
                            if key and key.startswith('gsk_'):
                                keys.append(key)
        except Exception as e:
            # Fallback to current key on error
            if cls.GROQ_API_KEY:
                return [cls.GROQ_API_KEY]
            return []
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keys = []
        for key in keys:
            if key not in seen:
                seen.add(key)
                unique_keys.append(key)
        
        return unique_keys
    
    @classmethod
    def get_groq_api_key(cls) -> Optional[str]:
        """
        Get Groq API key from environment
        
        Returns:
            Groq API key or None if not set
        """
        return cls.GROQ_API_KEY
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Data Generation
    DEFAULT_EMPLOYEE_COUNT = int(os.getenv("DEFAULT_EMPLOYEE_COUNT", "150"))
    DEFAULT_PRODUCT_COUNT = int(os.getenv("DEFAULT_PRODUCT_COUNT", "120"))
    DEFAULT_CUSTOMER_COUNT = int(os.getenv("DEFAULT_CUSTOMER_COUNT", "200"))
    DEFAULT_SALES_COUNT = int(os.getenv("DEFAULT_SALES_COUNT", "300"))
    
    # Query Engine
    MAX_QUERY_RESULTS = int(os.getenv("MAX_QUERY_RESULTS", "1000"))
    QUERY_TIMEOUT_SECONDS = int(os.getenv("QUERY_TIMEOUT_SECONDS", "30"))
    DEFAULT_RESULT_LIMIT = int(os.getenv("DEFAULT_RESULT_LIMIT", "100"))
    MAX_SQL_ERROR_RETRIES = int(os.getenv("MAX_SQL_ERROR_RETRIES", "2"))  # AI-powered retry attempts
    
    @classmethod
    def validate(cls) -> list[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        # Check if at least one API provider is configured
        has_groq = cls.GROQ_API_KEY and cls.GROQ_API_KEY != "your-groq-api-key-here"
        has_gemini = cls.GOOGLE_API_KEY and cls.GOOGLE_API_KEY != "your-api-key-here"
        
        if not has_groq and not has_gemini:
            errors.append(
                "No API keys configured. Set either GROQ_API_KEY or GOOGLE_API_KEY in .env\n"
                "Groq (recommended): https://console.groq.com/ (14,400 req/day free)\n"
                "Gemini: https://makersuite.google.com/app/apikey (50 req/day free)"
            )
        
        if cls.LOG_LEVEL not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            errors.append(f"Invalid LOG_LEVEL: {cls.LOG_LEVEL}")
        
        return errors
    
    @classmethod
    def get_db_path(cls) -> Path:
        """Get full database path"""
        return cls.BASE_DIR / cls.DATABASE_PATH
    
    @classmethod
    def get_excel_dir(cls) -> Path:
        """Get full Excel output directory path"""
        return cls.BASE_DIR / cls.EXCEL_OUTPUT_DIR
    
    @classmethod
    def get_log_path(cls) -> Path:
        """Get full log file path"""
        return cls.BASE_DIR / cls.LOG_FILE
