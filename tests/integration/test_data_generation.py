"""
Integration Tests for Data Generation and Conversion
Tests Excel generation, data quality, and SQL conversion
"""

import pytest
from pathlib import Path
import sys
import pandas as pd
import sqlite3

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data.generators import (
    generate_employees,
    generate_sales_orders,
    generate_products,
    generate_customers,
    generate_inventory,
    generate_suppliers
)
from src.data.converters import verify_database


class TestDataGenerators:
    """Test data generation functions"""
    
    def test_generate_employees(self):
        """Test employee data generation"""
        df = generate_employees(num_rows=50)
        
        assert len(df) == 50
        assert 'employee_id' in df.columns
        assert 'first_name' in df.columns
        assert 'last_name' in df.columns
        assert 'email' in df.columns
        assert 'department' in df.columns
        assert 'salary' in df.columns
        
        # Check no nulls in required fields
        assert df['first_name'].notna().all()
        assert df['last_name'].notna().all()
        assert df['email'].notna().all()
    
    def test_generate_sales_orders(self):
        """Test sales orders generation"""
        df = generate_sales_orders(num_rows=100)
        
        assert len(df) == 100
        assert 'order_id' in df.columns
        assert 'customer_id' in df.columns
        assert 'product_id' in df.columns
        assert 'order_date' in df.columns
        assert 'quantity' in df.columns
        assert 'total_amount' in df.columns
    
    def test_generate_products(self):
        """Test products generation"""
        df = generate_products(num_rows=75)
        
        assert len(df) == 75
        assert 'product_id' in df.columns
        assert 'product_name' in df.columns
        assert 'category' in df.columns
        assert 'selling_price' in df.columns
        
        # Check price is positive
        assert (df['selling_price'] > 0).all()
    
    def test_generate_customers(self):
        """Test customers generation"""
        df = generate_customers(num_rows=80)
        
        assert len(df) == 80
        assert 'customer_id' in df.columns
        assert 'first_name' in df.columns
        assert 'email' in df.columns
        
        # Check email format
        assert df['email'].str.contains('@').all()
    
    def test_generate_inventory(self):
        """Test inventory generation"""
        df = generate_inventory(num_rows=60)
        
        assert len(df) == 60
        assert 'inventory_id' in df.columns
        assert 'product_id' in df.columns
        assert 'quantity_in_stock' in df.columns
        
        # Check quantities are non-negative
        assert (df['quantity_in_stock'] >= 0).all()
    
    def test_generate_suppliers(self):
        """Test suppliers generation"""
        df = generate_suppliers(num_rows=20)
        
        assert len(df) == 20
        assert 'supplier_id' in df.columns
        assert 'supplier_name' in df.columns
        assert 'email' in df.columns
        
        # Check email format
        assert df['email'].str.contains('@').all()


class TestDataQuality:
    """Test data quality and integrity"""
    
    def test_employees_data_quality(self):
        """Test employees data quality"""
        df = generate_employees(num_rows=100)
        
        # Check unique IDs
        assert df['employee_id'].is_unique
        
        # Check salary range
        assert df['salary'].min() > 0
        assert df['salary'].max() <= 500000
        
        # Check department is not null
        assert df['department'].notna().all()
    
    def test_products_data_quality(self):
        """Test products data quality"""
        df = generate_products(num_rows=100)
        
        # Check unique product IDs
        assert df['product_id'].is_unique
        
        # Check price ranges
        assert df['selling_price'].min() > 0
        assert df['selling_price'].max() <= 50000
    
    def test_sales_orders_data_quality(self):
        """Test sales orders data quality"""
        df = generate_sales_orders(num_rows=100)
        
        # Check quantities are positive
        assert (df['quantity'] > 0).all()
        
        # Check total amounts are positive
        assert (df['total_amount'] > 0).all()
        
        # Check dates are not null
        assert df['order_date'].notna().all()


class TestDatabaseVerification:
    """Test database verification"""
    
    def test_verify_electronics_database(self, electronics_db_path):
        """Test verifying electronics database"""
        if not Path(electronics_db_path).exists():
            pytest.skip("Electronics database not found")
        
        # This should not raise an exception
        verify_database(str(electronics_db_path))
    
    def test_database_integrity(self, electronics_db_path):
        """Test database integrity"""
        if not Path(electronics_db_path).exists():
            pytest.skip("Electronics database not found")
        
        conn = sqlite3.connect(electronics_db_path)
        cursor = conn.cursor()
        
        # Check some tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert len(tables) > 0
        
        # Check tables have data
        for table in tables[:5]:  # Check first 5 tables
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            assert count > 0, f"Table {table} is empty"
        
        conn.close()


class TestExcelGeneration:
    """Test Excel file generation"""
    
    def test_excel_export(self, tmp_path):
        """Test exporting data to Excel"""
        df = generate_employees(num_rows=30)
        
        excel_file = tmp_path / "test_employees.xlsx"
        df.to_excel(excel_file, index=False)
        
        assert excel_file.exists()
        
        # Read it back
        df_read = pd.read_excel(excel_file)
        assert len(df_read) == 30
        assert list(df_read.columns) == list(df.columns)
    
    def test_multiple_sheets(self, tmp_path):
        """Test creating Excel with multiple sheets"""
        excel_file = tmp_path / "test_multi.xlsx"
        
        with pd.ExcelWriter(excel_file) as writer:
            generate_employees(num_rows=20).to_excel(writer, sheet_name='Employees', index=False)
            generate_products(num_rows=15).to_excel(writer, sheet_name='Products', index=False)
        
        assert excel_file.exists()
        
        # Read sheets
        xl_file = pd.ExcelFile(excel_file)
        assert 'Employees' in xl_file.sheet_names
        assert 'Products' in xl_file.sheet_names
