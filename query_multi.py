#!/usr/bin/env python3
"""
Multi-Company Query Interface
Query multiple databases with AI
"""

import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.cli.query_cli import QueryCLI
from src.utils.config import Config
import os

config = Config()


def select_company():
    """Let user select which company database to query"""
    databases = {
        '1': ('Electronics Company', str(config.DATABASE_DIR / 'electronics_company.db')),
        '2': ('Airline Company', str(config.DATABASE_DIR / 'airline_company.db'))
    }
    
    print("\n" + "=" * 70)
    print("  🗄️  SELECT DATABASE TO QUERY")
    print("=" * 70)
    print("\n  Available Databases:")
    for key, (name, path) in databases.items():
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"    {key}. {name} {exists}")
    print("\n" + "=" * 70)
    
    choice = input("\n  Select database (1-2) or 'q' to quit: ").strip()
    
    if choice.lower() == 'q':
        print("\n  👋 Goodbye!\n")
        sys.exit(0)
    
    if choice in databases:
        name, db_path = databases[choice]
        if not os.path.exists(db_path):
            print(f"\n  ❌ Error: Database not found: {db_path}")
            print(f"  Run: python scripts/generate_all_companies.py\n")
            sys.exit(1)
        return name, db_path
    else:
        print("\n  ❌ Invalid choice. Please select 1 or 2.\n")
        return select_company()


def main():
    """Main entry point"""
    # Check if database argument provided
    if len(sys.argv) > 1 and sys.argv[1] in ['electronics', 'airline']:
        company = sys.argv[1]
        db_path = str(config.DATABASE_DIR / f'{company}_company.db')
        company_name = f'{company.title()} Company'
        
        # Remove the company argument so rest can be question
        sys.argv.pop(1)
    else:
        # Interactive selection
        company_name, db_path = select_company()
    
    print(f"\n  📊 Selected: {company_name}")
    print(f"  🗄️  Database: {db_path}\n")
    
    # Create CLI with selected database
    cli = QueryCLI(db_path=db_path)
    
    # Check if question provided
    if len(sys.argv) > 1:
        # Single question mode
        question = " ".join(sys.argv[1:])
        cli.single_query(question)
    else:
        # Interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()
