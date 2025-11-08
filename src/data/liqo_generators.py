"""
Liqo Retail Data Generator
Processes Raw_Data_FY_2022-23.xlsx and generates normalized database

Business Context:
- Liqo is a retail electronics/home appliances chain in North India
- 5 store locations: Kharar, Chandigarh, Ramgarh, Panchkula, Solan
- FY 2022-23 data: 37,857 transactions across 12 months
- Product categories: AC, Refrigerator, LED TV, Washing Machine, Accessories, etc.
- Both B2B and B2C sales
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
import sqlite3
import hashlib
import logging

logger = logging.getLogger(__name__)


class LiqoDataGenerator:
    """Generate normalized database from Liqo raw sales data"""
    
    def __init__(self, excel_path: str):
        self.excel_path = Path(excel_path)
        self.df = None
        
    def load_data(self):
        """Load Excel data"""
        logger.info(f"Loading data from {self.excel_path}")
        self.df = pd.read_excel(self.excel_path, sheet_name='FY_2022-23')
        
        # Clean column names
        self.df.columns = [col.strip() for col in self.df.columns]
        
        # Convert dates
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        logger.info(f"Loaded {len(self.df)} transactions")
        
    def generate_database(self, db_path: str):
        """Generate normalized SQLite database"""
        logger.info(f"Generating database at {db_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create tables
        self._create_tables(cursor)
        
        # Insert data
        self._insert_locations(cursor)
        self._insert_customers(cursor)
        self._insert_products(cursor)
        self._insert_sales_transactions(cursor)
        self._insert_salespeople(cursor)
        
        conn.commit()
        conn.close()
        
        logger.info(f"Database created successfully: {db_path}")
        
    def _create_tables(self, cursor):
        """Create database schema"""
        
        # Locations table
        cursor.execute("""
        CREATE TABLE locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_name TEXT NOT NULL UNIQUE,
            state TEXT,
            material_centre TEXT
        )
        """)
        
        # Customers table
        cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            address TEXT,
            state TEXT,
            gst_number TEXT,
            customer_type TEXT -- B2B or B2C
        )
        """)
        
        # Salespeople table
        cursor.execute("""
        CREATE TABLE salespeople (
            salesperson_id INTEGER PRIMARY KEY AUTOINCREMENT,
            salesperson_name TEXT NOT NULL UNIQUE
        )
        """)
        
        # Products table
        cursor.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            full_description TEXT,
            item_group TEXT,
            brand TEXT,
            model TEXT,
            source TEXT,
            main_category TEXT,
            sub_category TEXT,
            capacity TEXT,
            type1 TEXT
        )
        """)
        
        # Sales transactions table
        cursor.execute("""
        CREATE TABLE sales_transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            customer_id INTEGER,
            salesperson_id INTEGER,
            product_id INTEGER,
            voucher_number TEXT NOT NULL,
            transaction_date DATE NOT NULL,
            month TEXT,
            fiscal_year TEXT,
            quantity REAL NOT NULL,
            item_amount REAL NOT NULL,
            taxable_amount REAL NOT NULL,
            transaction_type TEXT, -- Cash, Credit, etc.
            FOREIGN KEY (location_id) REFERENCES locations(location_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (salesperson_id) REFERENCES salespeople(salesperson_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX idx_transactions_date ON sales_transactions(transaction_date)")
        cursor.execute("CREATE INDEX idx_transactions_location ON sales_transactions(location_id)")
        cursor.execute("CREATE INDEX idx_transactions_customer ON sales_transactions(customer_id)")
        cursor.execute("CREATE INDEX idx_transactions_product ON sales_transactions(product_id)")
        cursor.execute("CREATE INDEX idx_products_category ON products(main_category)")
        cursor.execute("CREATE INDEX idx_products_brand ON products(brand)")
        
    def _insert_locations(self, cursor):
        """Insert unique locations"""
        # Group by location and take first occurrence
        locations_df = self.df.groupby('Location').first().reset_index()[['Location', 'State', 'Material Centre']]
        
        for _, row in locations_df.iterrows():
            cursor.execute("""
                INSERT INTO locations (location_name, state, material_centre)
                VALUES (?, ?, ?)
            """, (row['Location'], row['State'], row['Material Centre']))
            
        logger.info(f"Inserted {len(locations_df)} locations")
        
    def _insert_salespeople(self, cursor):
        """Insert unique salespeople"""
        # Filter out null values
        salespeople = self.df['Ref/Sales Person'].dropna().unique()
        
        for person in salespeople:
            cursor.execute("""
                INSERT INTO salespeople (salesperson_name)
                VALUES (?)
            """, (person,))
            
        logger.info(f"Inserted {len(salespeople)} salespeople")
        
    def _insert_customers(self, cursor):
        """Insert unique customers"""
        # Group by customer name and take first occurrence for details
        customers_df = self.df.groupby('Customer Name').first().reset_index()
        
        for _, row in customers_df.iterrows():
            cursor.execute("""
                INSERT INTO customers (customer_name, address, state, gst_number, customer_type)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row['Customer Name'],
                row['Address'] if pd.notna(row['Address']) else None,
                row['State'],
                row['GST No.'] if pd.notna(row['GST No.']) else None,
                row['B-Type']
            ))
            
        logger.info(f"Inserted {len(customers_df)} customers")
        
    def _insert_products(self, cursor):
        """Insert unique products"""
        # Group by item name and take first occurrence for details
        products_df = self.df.groupby('Item Name').first().reset_index()
        
        for _, row in products_df.iterrows():
            cursor.execute("""
                INSERT INTO products (
                    item_name, full_description, item_group, brand, model, source,
                    main_category, sub_category, capacity, type1
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['Item Name'],
                row['Full Item Desc.'],
                row['Itemgroup'] if pd.notna(row['Itemgroup']) else None,
                row['Brand'] if pd.notna(row['Brand']) else None,
                row['Model'] if pd.notna(row['Model']) else None,
                row['Source'] if pd.notna(row['Source']) else None,
                row['Main Category'] if pd.notna(row['Main Category']) else None,
                row['Sub Category'] if pd.notna(row['Sub Category']) else None,
                row['Capacity'] if pd.notna(row['Capacity']) else None,
                row['Type1'] if pd.notna(row['Type1']) else None
            ))
            
        logger.info(f"Inserted {len(products_df)} products")
        
    def _insert_sales_transactions(self, cursor):
        """Insert all sales transactions with foreign keys"""
        
        # Get lookup dictionaries
        locations = {row[1]: row[0] for row in cursor.execute("SELECT location_id, location_name FROM locations").fetchall()}
        customers = {row[1]: row[0] for row in cursor.execute("SELECT customer_id, customer_name FROM customers").fetchall()}
        salespeople = {row[1]: row[0] for row in cursor.execute("SELECT salesperson_id, salesperson_name FROM salespeople").fetchall()}
        products = {row[1]: row[0] for row in cursor.execute("SELECT product_id, item_name FROM products").fetchall()}
        
        transaction_count = 0
        
        for _, row in self.df.iterrows():
            location_id = locations.get(row['Location'])
            customer_id = customers.get(row['Customer Name'])
            salesperson_id = salespeople.get(row['Ref/Sales Person']) if pd.notna(row['Ref/Sales Person']) else None
            product_id = products.get(row['Item Name'])
            
            cursor.execute("""
                INSERT INTO sales_transactions (
                    location_id, customer_id, salesperson_id, product_id,
                    voucher_number, transaction_date, month, fiscal_year,
                    quantity, item_amount, taxable_amount, transaction_type
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                location_id, customer_id, salesperson_id, product_id,
                row['Vch/Bill No'],
                row['Date'].strftime('%Y-%m-%d'),
                row['Month'],
                row['FY'],
                row['Qty'],
                row['Item_Amount'],
                row['Taxable_Amount'],
                row['Type']
            ))
            
            transaction_count += 1
            
            if transaction_count % 5000 == 0:
                logger.info(f"Inserted {transaction_count} transactions...")
                
        logger.info(f"Inserted {transaction_count} total transactions")


def generate_liqo_data():
    """Main function to generate Liqo database"""
    from src.utils.config import Config
    from src.utils.logger import setup_logger
    
    logger = setup_logger(__name__)
    
    excel_path = Config.DATA_DIR / 'excel' / 'liqo' / 'Raw_Data_FY_2022-23.xlsx'
    db_path = Config.DATABASE_DIR / 'liqo_company.db'
    
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    # Remove existing database
    if db_path.exists():
        logger.info(f"Removing existing database: {db_path}")
        db_path.unlink()
    
    # Generate database
    generator = LiqoDataGenerator(str(excel_path))
    generator.load_data()
    generator.generate_database(str(db_path))
    
    logger.info(f"✅ Liqo database created: {db_path}")
    logger.info(f"   - 37,857 transactions")
    logger.info(f"   - FY 2022-23 (Apr 2022 - Mar 2023)")
    logger.info(f"   - 5 locations, 7,914 customers, 10,768 products")
    
    return str(db_path)


if __name__ == "__main__":
    generate_liqo_data()
