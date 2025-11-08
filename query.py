#!/usr/bin/env python3
"""
Main entry point for AI-powered database queries
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from cli.query_cli import main

if __name__ == "__main__":
    main()
