"""
Convert Excel files to SQLite Database
Creates a comprehensive SQL database from generated Excel files
"""

import pandas as pd
import sqlite3
from sqlalchemy import create_engine, inspect
import os
from datetime import datetime

from src.utils.config import Config

# Load config
config = Config()


def excel_to_sql(excel_dir=None, db_name=None):
    """Convert all Excel files to SQL database"""
    
    # Use config defaults if not provided
    if excel_dir is None:
        excel_dir = config.EXCEL_OUTPUT_DIR
    if db_name is None:
        db_name = config.DATABASE_PATH
    """Convert all Excel files to SQL database"""
    
    print("🔄 Converting Excel files to SQL database...")
    print("-" * 60)
    
    # Remove existing database if it exists
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"🗑️  Removed existing database: {db_name}")
    
    # Create SQLAlchemy engine
    engine = create_engine(f'sqlite:///{db_name}', echo=False)
    
    # Get all Excel and CSV files
    data_files = [f for f in os.listdir(excel_dir) if f.endswith(('.xlsx', '.xls', '.csv'))]
    
    if not data_files:
        print(f"❌ No Excel or CSV files found in {excel_dir}/")
        return
    
    # Convert each file to a table
    for data_file in sorted(data_files):
        file_path = os.path.join(excel_dir, data_file)
        
        # Determine table name (remove file extension and sanitize)
        if data_file.endswith('.xlsx'):
            table_name = data_file.replace('.xlsx', '')
        elif data_file.endswith('.xls'):
            table_name = data_file.replace('.xls', '')
        else:  # .csv
            table_name = data_file.replace('.csv', '')
        
        # Sanitize table name: replace hyphens and other special chars with underscores
        # SQL table names should only contain letters, numbers, and underscores
        table_name = table_name.replace('-', '_').replace(' ', '_').replace('.', '_')
        # Remove any other non-alphanumeric characters except underscores
        table_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in table_name)
        # Ensure it starts with a letter or underscore (SQL requirement)
        if table_name and table_name[0].isdigit():
            table_name = 't_' + table_name
        
        try:
            # Read file based on extension
            if data_file.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            # Write to SQL database
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            
            print(f"✅ Converted: {data_file} → table '{table_name}' ({len(df)} rows)")
            
        except Exception as e:
            print(f"❌ Error converting {data_file}: {str(e)}")
    
    print("-" * 60)
    print(f"✨ Database created successfully: {db_name}")
    
    # Display database statistics
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📊 Database contains {len(tables)} tables:")
        for table in tables:
            # Use parameterized query with quoted table name for safety
            table_name = table[0]
            cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            count = cursor.fetchone()[0]
            print(f"   - {table_name}: {count} rows")
    
    return db_name, engine


def verify_database(db_name=None):
    """Verify database integrity and display sample queries"""
    
    # Use config default if not provided
    if db_name is None:
        db_name = config.DATABASE_PATH
    
    print("\n" + "=" * 60)
    print("🔍 Database Verification")
    print("=" * 60)
    
    with sqlite3.connect(db_name) as conn:
        # Example queries
        print("\n📋 Sample Queries:")
        
        # Query 1: Total sales
        print("\n1. Total Sales Revenue:")
        query = """
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value
        FROM sales_orders
        WHERE status = 'Completed'
        """
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
        
        # Query 2: Products by category
        print("\n2. Product Count by Category:")
        query = """
        SELECT 
            category,
            COUNT(*) as product_count,
            AVG(selling_price) as avg_price
        FROM products
        GROUP BY category
        ORDER BY product_count DESC
        LIMIT 5
        """
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
        
        # Query 3: Employee department distribution
        print("\n3. Employees by Department:")
        query = """
        SELECT 
            department,
            COUNT(*) as employee_count,
            AVG(salary) as avg_salary
        FROM employees
        WHERE status = 'Active'
        GROUP BY department
        ORDER BY employee_count DESC
        """
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
        
        # Query 4: Inventory status
        print("\n4. Inventory Stock Status:")
        query = """
        SELECT 
            warehouse_location,
            COUNT(*) as product_types,
            SUM(quantity_in_stock) as total_items,
            SUM(total_value) as total_value
        FROM inventory
        GROUP BY warehouse_location
        ORDER BY total_value DESC
        """
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    db_name, engine = excel_to_sql()
    verify_database(db_name)
    print("\n✅ Conversion complete!")
