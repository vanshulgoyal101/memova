#!/usr/bin/env python3
"""
Generate all data: Excel files, SQL database, and schema documentation
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from data.generators import main as generate_excel
from data.converters import excel_to_sql, verify_database
from data.schema import generate_schema_file, generate_sql_schema
from utils.logger import setup_logger
from datetime import datetime

logger = setup_logger(__name__)


def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 70)
    print("  📊 ELECTRONICS APPLIANCE COMPANY - DATA GENERATION PIPELINE")
    print("=" * 70)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")


def print_summary(start_time):
    """Print final summary"""
    duration = (datetime.now() - start_time).total_seconds()
    
    print("\n" + "=" * 70)
    print("  ✨ PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"  Duration: {duration:.2f} seconds")
    print("\n  📁 Generated Files:")
    print("     - data/excel/ (12 Excel files)")
    print("     - data/database/electronics_company.db (SQLite database)")
    print("     - docs/database_schema.md (Documentation)")
    print("     - docs/database_schema.sql (SQL DDL)")
    print("\n  🚀 Next Steps:")
    print("     1. Review Excel files in data/excel/")
    print("     2. Query the database: python query.py")
    print("     3. Read schema documentation: docs/database_schema.md")
    print("=" * 70 + "\n")


def main():
    """Main execution pipeline"""
    start_time = datetime.now()
    
    try:
        print_banner()
        
        # Step 1: Generate Excel files
        print("STEP 1/3: Generating Excel Files")
        print("-" * 70)
        generate_excel()
        
        # Step 2: Convert to SQL
        print("\n\nSTEP 2/3: Converting to SQL Database")
        print("-" * 70)
        excel_to_sql()
        verify_database()
        
        # Step 3: Generate schema documentation
        print("\n\nSTEP 3/3: Generating Schema Documentation")
        print("-" * 70)
        generate_schema_file()
        generate_sql_schema()
        
        print_summary(start_time)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user\n")
        sys.exit(1)
    except Exception as e:
        logger.exception("Pipeline failed")
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
