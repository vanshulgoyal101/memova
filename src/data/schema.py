"""
Generate Database Schema Documentation
Creates comprehensive schema file documenting database structure
"""

import sqlite3
from datetime import datetime
import os

from src.utils.config import Config

# Load config
config = Config()


def get_table_info(cursor, table_name):
    """Get detailed information about a table"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()


def get_foreign_keys(cursor, table_name):
    """Get foreign key relationships for a table"""
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    return cursor.fetchall()


def generate_schema_file(db_name=None, output_file=None):
    """Generate comprehensive schema documentation"""
    
    # Use config defaults if not provided
    if db_name is None:
        db_name = config.DATABASE_PATH
    if output_file is None:
        output_file = str(config.DOCS_DIR / 'database_schema.md')
    """Generate comprehensive schema documentation"""
    
    print("🔄 Generating database schema documentation...")
    print("-" * 60)
    
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [table[0] for table in cursor.fetchall()]
        
        # Start building schema document
        schema_doc = []
        schema_doc.append("# 📊 Electronics Appliance Company - Database Schema")
        schema_doc.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        schema_doc.append(f"\n**Database:** {db_name}")
        schema_doc.append(f"\n**Total Tables:** {len(tables)}")
        schema_doc.append("\n---\n")
        
        # Table of Contents
        schema_doc.append("## 📑 Table of Contents\n")
        for i, table in enumerate(tables, 1):
            schema_doc.append(f"{i}. [{table.replace('_', ' ').title()}](#{table})")
        schema_doc.append("\n---\n")
        
        # Database Overview
        schema_doc.append("## 🎯 Database Overview\n")
        schema_doc.append("This database contains comprehensive data for an electronics appliance selling company, including:\n")
        schema_doc.append("- **HR & Payroll**: Employee management and compensation data")
        schema_doc.append("- **Sales & Orders**: Customer orders and sales transactions")
        schema_doc.append("- **Inventory**: Product stock and warehouse management")
        schema_doc.append("- **Finance**: Financial transactions and accounting")
        schema_doc.append("- **Customer Service**: Support tickets and warranty claims")
        schema_doc.append("- **Marketing**: Campaign tracking and analytics")
        schema_doc.append("- **Logistics**: Shipping and delivery information")
        schema_doc.append("\n---\n")
        
        # Entity Relationship Overview
        schema_doc.append("## 🔗 Key Relationships\n")
        schema_doc.append("```")
        schema_doc.append("employees ──→ sales_orders (employee_id)")
        schema_doc.append("employees ──→ payroll (employee_id)")
        schema_doc.append("employees ──→ customer_service_tickets (assigned_employee_id)")
        schema_doc.append("")
        schema_doc.append("customers ──→ sales_orders (customer_id)")
        schema_doc.append("customers ──→ customer_service_tickets (customer_id)")
        schema_doc.append("customers ──→ warranties (customer_id)")
        schema_doc.append("")
        schema_doc.append("products ──→ sales_orders (product_id)")
        schema_doc.append("products ──→ inventory (product_id)")
        schema_doc.append("products ──→ customer_service_tickets (product_id)")
        schema_doc.append("products ──→ warranties (product_id)")
        schema_doc.append("products ──→ suppliers (supplier_id)")
        schema_doc.append("")
        schema_doc.append("sales_orders ──→ shipments (order_id)")
        schema_doc.append("```")
        schema_doc.append("\n---\n")
        
        # Detailed table schemas
        schema_doc.append("## 📋 Detailed Table Schemas\n")
        
        # Table descriptions
        table_descriptions = {
            'employees': 'Employee records including personal information, department, position, and compensation details.',
            'products': 'Product catalog with specifications, pricing, warranty, and supplier information.',
            'customers': 'Customer database with contact information, registration details, and loyalty data.',
            'sales_orders': 'Sales transaction records including order details, pricing, and delivery information.',
            'inventory': 'Stock management data for products across different warehouse locations.',
            'suppliers': 'Supplier information including contact details and business terms.',
            'financial_transactions': 'Financial records including revenue, expenses, and various business transactions.',
            'payroll': 'Employee payroll information including salary, taxes, deductions, and payment details.',
            'customer_service_tickets': 'Customer support tickets tracking issues, resolutions, and satisfaction.',
            'marketing_campaigns': 'Marketing campaign data with budget, performance metrics, and ROI analysis.',
            'shipments': 'Shipment tracking information including carrier details and delivery status.',
            'warranties': 'Product warranty registrations and claim tracking information.'
        }
        
        for table in tables:
            # Get table info
            columns = get_table_info(cursor, table)
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cursor.fetchone()[0]
            
            # Table header
            schema_doc.append(f"### <a id='{table}'></a>{table.replace('_', ' ').title()}")
            schema_doc.append(f"\n**Description:** {table_descriptions.get(table, 'No description available.')}")
            schema_doc.append(f"\n**Row Count:** {row_count:,}")
            schema_doc.append(f"\n**Column Count:** {len(columns)}\n")
            
            # Column details table
            schema_doc.append("| Column Name | Data Type | Nullable | Default | Primary Key | Description |")
            schema_doc.append("|-------------|-----------|----------|---------|-------------|-------------|")
            
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                nullable = "No" if not_null else "Yes"
                default = str(default_val) if default_val is not None else "NULL"
                is_pk = "✓" if pk else ""
                
                # Generate description based on column name
                description = generate_column_description(col_name, table)
                
                schema_doc.append(f"| `{col_name}` | {col_type} | {nullable} | {default} | {is_pk} | {description} |")
            
            schema_doc.append("")
            
            # Sample data
            cursor.execute(f"SELECT * FROM {table} LIMIT 3")
            sample_rows = cursor.fetchall()
            
            if sample_rows:
                schema_doc.append("**Sample Data:**")
                schema_doc.append("```")
                # Get column names
                col_names = [col[1] for col in columns]
                
                # Print first 5 columns only for readability
                display_cols = col_names[:5]
                schema_doc.append(" | ".join(display_cols))
                schema_doc.append("-" * (len(" | ".join(display_cols)) + 10))
                
                for row in sample_rows:
                    display_values = [str(row[i])[:20] for i in range(min(5, len(row)))]
                    schema_doc.append(" | ".join(display_values))
                
                if len(col_names) > 5:
                    schema_doc.append(f"\n... and {len(col_names) - 5} more columns")
                
                schema_doc.append("```\n")
            
            schema_doc.append("---\n")
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(schema_doc))
        
        print(f"✅ Schema documentation generated: {output_file}")
        print(f"📄 Document contains {len(schema_doc)} lines")
        print(f"📊 Documented {len(tables)} tables")
        
    print("-" * 60)
    print("✨ Schema generation complete!")
    
    return output_file


def generate_column_description(col_name, table_name):
    """Generate human-readable description for columns"""
    
    # Common column descriptions
    descriptions = {
        'id': 'Unique identifier',
        'employee_id': 'Employee unique identifier',
        'customer_id': 'Customer unique identifier',
        'product_id': 'Product unique identifier',
        'order_id': 'Order unique identifier',
        'first_name': 'First name',
        'last_name': 'Last name',
        'email': 'Email address',
        'phone': 'Phone number',
        'address': 'Street address',
        'city': 'City name',
        'state': 'State code',
        'zip_code': 'ZIP/Postal code',
        'created_date': 'Record creation date',
        'updated_date': 'Last update date',
        'status': 'Current status',
        'total_amount': 'Total amount',
        'quantity': 'Quantity',
        'price': 'Price',
        'date': 'Date',
        'description': 'Description',
        'name': 'Name',
    }
    
    # Check exact match first
    if col_name in descriptions:
        return descriptions[col_name]
    
    # Check partial matches
    for key, desc in descriptions.items():
        if key in col_name.lower():
            return desc
    
    # Generate from column name
    return col_name.replace('_', ' ').title()


def generate_sql_schema(db_name=None, output_file=None):
    """Generate SQL CREATE TABLE statements"""
    
    # Use config defaults if not provided
    if db_name is None:
        db_name = config.DATABASE_PATH
    if output_file is None:
        output_file = str(config.DOCS_DIR / 'database_schema.sql')
    
    print("\n🔄 Generating SQL schema file...")
    
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [table[0] for table in cursor.fetchall()]
        
        sql_statements = []
        sql_statements.append("-- Electronics Appliance Company Database Schema")
        sql_statements.append(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sql_statements.append(f"-- Total Tables: {len(tables)}")
        sql_statements.append("\n")
        
        for table in tables:
            # Get CREATE TABLE statement
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}';")
            create_statement = cursor.fetchone()[0]
            
            sql_statements.append(f"-- Table: {table}")
            sql_statements.append(create_statement + ";")
            sql_statements.append("\n")
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_statements))
        
        print(f"✅ SQL schema file generated: {output_file}")
    
    return output_file


if __name__ == "__main__":
    # Generate markdown documentation
    schema_md = generate_schema_file()
    
    # Generate SQL schema
    schema_sql = generate_sql_schema()
    
    print("\n📁 Generated Files:")
    print(f"   - {schema_md} (Documentation)")
    print(f"   - {schema_sql} (SQL DDL)")
