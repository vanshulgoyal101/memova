#!/usr/bin/env python3
"""
Main script to generate Excel files, convert to SQL, and create schema
Electronics Appliance Company Data Pipeline
"""

import os
import sys
from datetime import datetime

# Import our modules
from generate_data import main as generate_excel
from convert_to_sql import excel_to_sql, verify_database
from generate_schema import generate_schema_file, generate_sql_schema


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
    print("     - excel_files/ (12 Excel files)")
    print("     - electronics_company.db (SQLite database)")
    print("     - database_schema.md (Documentation)")
    print("     - database_schema.sql (SQL DDL)")
    print("\n  🚀 Next Steps:")
    print("     1. Review Excel files in excel_files/ directory")
    print("     2. Query the database: sqlite3 electronics_company.db")
    print("     3. Read schema documentation: database_schema.md")
    print("=" * 70 + "\n")


def main():
    """Main execution pipeline"""
    start_time = datetime.now()
    
    try:
        # Print banner
        print_banner()
        
        # Step 1: Generate Excel files
        print("STEP 1/3: Generating Excel Files")
        print("-" * 70)
        datasets = generate_excel()
        print("\n")
        
        # Step 2: Convert to SQL database
        print("STEP 2/3: Converting to SQL Database")
        print("-" * 70)
        db_name, engine = excel_to_sql()
        verify_database(db_name)
        print("\n")
        
        # Step 3: Generate schema documentation
        print("STEP 3/3: Generating Schema Documentation")
        print("-" * 70)
        schema_md = generate_schema_file(db_name)
        schema_sql = generate_sql_schema(db_name)
        print("\n")
        
        # Print summary
        print_summary(start_time)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
