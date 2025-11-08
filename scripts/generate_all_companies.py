"""
Multi-Company Database Generator
Supports generating databases for multiple companies
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.generators import main as generate_electronics
from src.data.airline_generators import main as generate_airline
from src.data.edtech_generators import generate_all_edtech_data as generate_edtech
from src.data.converters import excel_to_sql
from src.data.schema import generate_schema_file, generate_sql_schema
from src.utils.config import Config

config = Config()


def print_banner(company_name):
    """Print banner for company"""
    print("\n" + "=" * 70)
    print(f"  📊 {company_name.upper()} - DATA PIPELINE")
    print("=" * 70)


def generate_all_data():
    """Generate data for all companies"""
    print("\n" + "=" * 70)
    print("  🏢 MULTI-COMPANY DATA GENERATION PIPELINE")
    print("=" * 70)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Company 1: Electronics
    print_banner("Electronics Company")
    print("\n📝 Step 1/3: Generating Excel Files...")
    generate_electronics()
    
    print("\n📝 Step 2/3: Converting to SQL Database...")
    excel_dir = os.path.join(config.EXCEL_OUTPUT_DIR, 'electronics_company')
    db_path = os.path.join(config.DATABASE_DIR, 'electronics_company.db')
    excel_to_sql(excel_dir=excel_dir, db_name=db_path)
    
    print("\n📝 Step 3/3: Generating Schema Documentation...")
    schema_md = os.path.join(config.DOCS_DIR, '06-database', 'electronics_schema.md')
    schema_sql = os.path.join(config.DOCS_DIR, '06-database', 'electronics_schema.sql')
    generate_schema_file(db_name=db_path, output_file=schema_md)
    generate_sql_schema(db_name=db_path, output_file=schema_sql)
    
    # Company 2: Airline
    print_banner("Airline Company")
    print("\n📝 Step 1/3: Generating Excel Files...")
    generate_airline()
    
    print("\n📝 Step 2/3: Converting to SQL Database...")
    excel_dir = os.path.join(config.EXCEL_OUTPUT_DIR, 'airline_company')
    db_path = os.path.join(config.DATABASE_DIR, 'airline_company.db')
    excel_to_sql(excel_dir=excel_dir, db_name=db_path)
    
    print("\n📝 Step 3/3: Generating Schema Documentation...")
    schema_md = os.path.join(config.DOCS_DIR, '06-database', 'airline_schema.md')
    schema_sql = os.path.join(config.DOCS_DIR, '06-database', 'airline_schema.sql')
    generate_schema_file(db_name=db_path, output_file=schema_md)
    generate_sql_schema(db_name=db_path, output_file=schema_sql)
    
    # Company 3: EdTech India
    print_banner("EdTech India Company")
    print("\n📝 Step 1/3: Generating Excel Files...")
    generate_edtech()
    
    print("\n📝 Step 2/3: Converting to SQL Database...")
    excel_dir = os.path.join(config.EXCEL_OUTPUT_DIR, 'edtech_company')
    db_path = os.path.join(config.DATABASE_DIR, 'edtech_company.db')
    excel_to_sql(excel_dir=excel_dir, db_name=db_path)
    
    print("\n📝 Step 3/3: Generating Schema Documentation...")
    schema_md = os.path.join(config.DOCS_DIR, '06-database', 'edtech_schema.md')
    schema_sql = os.path.join(config.DOCS_DIR, '06-database', 'edtech_schema.sql')
    generate_schema_file(db_name=db_path, output_file=schema_md)
    generate_sql_schema(db_name=db_path, output_file=schema_sql)
    
    # Final summary
    print("\n" + "=" * 70)
    print("  ✨ ALL COMPANIES PROCESSED SUCCESSFULLY!")
    print("=" * 70)
    print("\n  📊 Summary:")
    print("     Electronics Company:")
    print("       - data/excel/electronics_company/ (12 Excel files)")
    print("       - data/database/electronics_company.db")
    print("       - docs/06-database/electronics_schema.md")
    print("\n     Airline Company:")
    print("       - data/excel/airline_company/ (16 Excel files)")
    print("       - data/database/airline_company.db")
    print("       - docs/06-database/airline_schema.md")
    print("\n     EdTech India Company:")
    print("       - data/excel/edtech_company/ (15 Excel files)")
    print("       - data/database/edtech_company.db")
    print("       - docs/06-database/edtech_schema.md")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    generate_all_data()
