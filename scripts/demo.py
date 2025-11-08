#!/usr/bin/env python3
"""
Quick demonstration of the AI query system
Shows 3 example queries with results
"""

import sys
from pathlib import Path

from query_engine import QueryEngine
from cli import QueryCLI
from logger import setup_logger
from exceptions import AppException

logger = setup_logger(__name__)


def main():
    """Run demo queries"""
    print("\n" + "=" * 70)
    print("  🎯 DEMO: Natural Language to SQL with Google Gemini")
    print("=" * 70 + "\n")
    
    # Check if database exists
    db_path = Path("electronics_company.db")
    if not db_path.exists():
        print("⚠️  Database not found! Running data generation first...\n")
        try:
            import main as data_gen
            data_gen.main()
            print("\n")
        except Exception as e:
            print(f"❌ Error generating data: {e}\n")
            sys.exit(1)
    
    # Initialize
    try:
        engine = QueryEngine()
        cli = QueryCLI()
        cli.engine = engine  # Reuse engine
        
        print(f"✅ Connected to Google AI Studio")
        print(f"📦 Using model: {engine.model_name}")
        print(f"🗄️  Database: {engine.db_manager.db_path}\n")
        
    except AppException as e:
        print(f"❌ {e}\n")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error")
        print(f"❌ Unexpected error: {e}\n")
        sys.exit(1)
    
    # Demo questions
    questions = [
        "How many employees do we have?",
        "What are the top 5 products by price?",
        "Show me the total revenue from all sales",
    ]
    
    for i, question in enumerate(questions, 1):
        print("=" * 70)
        print(f"DEMO QUERY {i}/{len(questions)}")
        print("=" * 70 + "\n")
        
        result = engine.ask(question)
        
        if result['success']:
            print(f"🤔 Question: {question}")
            print(f"📝 SQL: {result['sql']}\n")
        
        cli.print_results(result)
        
        if i < len(questions):
            input("Press Enter to continue...\n")
    
    print("=" * 70)
    print("  ✨ Demo Complete!")
    print("=" * 70)
    print("\n  To start interactive mode, run:")
    print("    python llm_query.py\n")


if __name__ == "__main__":
    main()
