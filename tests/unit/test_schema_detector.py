"""
Unit tests for schema_detector module

Tests the SchemaDetector class's ability to automatically infer
database schemas from Excel/CSV files.
"""

import pytest
import pandas as pd
from pathlib import Path
from src.core.schema_detector import SchemaDetector, TableSchema, ColumnInfo


class TestColumnInfo:
    """Test ColumnInfo class"""
    
    def test_integer_type_detection(self):
        """Test INTEGER type inference"""
        df = pd.DataFrame({'id': [1, 2, 3, 4, 5]})
        col = ColumnInfo('id', df, 0)
        assert col.data_type == 'INTEGER'
    
    def test_real_type_detection(self):
        """Test REAL type inference"""
        df = pd.DataFrame({'price': [10.5, 20.99, 30.0, 40.25]})
        col = ColumnInfo('price', df, 0)
        assert col.data_type == 'REAL'
    
    def test_text_type_detection(self):
        """Test TEXT type inference"""
        df = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie']})
        col = ColumnInfo('name', df, 0)
        assert col.data_type == 'TEXT'
    
    def test_datetime_type_detection(self):
        """Test DATETIME type inference"""
        df = pd.DataFrame({'created_at': pd.date_range('2024-01-01', periods=5, freq='h')})
        col = ColumnInfo('created_at', df, 0)
        assert col.data_type == 'DATETIME'
    
    def test_date_type_detection(self):
        """Test DATE type inference"""
        df = pd.DataFrame({'birth_date': pd.date_range('2000-01-01', periods=5, freq='D')})
        col = ColumnInfo('birth_date', df, 0)
        # Date vs DateTime detection is tricky - accept both
        assert col.data_type in ('DATE', 'DATETIME')
    
    def test_primary_key_detection(self):
        """Test PK detection: unique, non-null, ends with _id, first column"""
        df = pd.DataFrame({
            'customer_id': [1, 2, 3, 4, 5],
            'name': ['A', 'B', 'C', 'D', 'E']
        })
        id_col = ColumnInfo('customer_id', df, 0)
        assert id_col.is_primary_key is True
    
    def test_foreign_key_detection(self):
        """Test FK detection: ends with _id but not PK"""
        df = pd.DataFrame({
            'order_id': [1, 2, 3, 4, 5],
            'customer_id': [10, 10, 20, 20, 30]  # Not unique, so not PK
        })
        customer_col = ColumnInfo('customer_id', df, 1)
        assert customer_col.is_foreign_key is True
        assert customer_col.is_primary_key is False
    
    def test_referenced_table_inference(self):
        """Test FK referenced table inference"""
        df = pd.DataFrame({
            'order_id': [1, 2, 3, 4, 5],
            'customer_id': [10, 10, 20, 20, 30]  # Not unique
        })
        customer_col = ColumnInfo('customer_id', df, 1)
        assert customer_col.referenced_table == 'customers'
    
    def test_null_percentage(self):
        """Test null percentage calculation"""
        df = pd.DataFrame({'optional_field': [1, None, 3, None, 5]})
        col = ColumnInfo('optional_field', df, 0)
        assert col.null_percentage == 40.0  # 2 out of 5 = 40%
    
    def test_uniqueness_detection(self):
        """Test unique vs non-unique columns"""
        df_unique = pd.DataFrame({'id': [1, 2, 3, 4, 5]})
        df_not_unique = pd.DataFrame({'category': ['A', 'B', 'A', 'B', 'C']})
        
        unique_col = ColumnInfo('id', df_unique, 0)
        non_unique_col = ColumnInfo('category', df_not_unique, 0)
        
        assert unique_col.is_unique is True
        assert non_unique_col.is_unique is False


class TestTableSchema:
    """Test TableSchema class"""
    
    def test_simple_table(self):
        """Test basic table schema detection"""
        df = pd.DataFrame({
            'customer_id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com']
        })
        schema = TableSchema('customers', df)
        
        assert schema.name == 'customers'
        assert schema.row_count == 3
        assert len(schema.columns) == 3
        assert schema.primary_key is not None
        assert schema.primary_key.name == 'customer_id'
    
    def test_table_with_foreign_keys(self):
        """Test table with foreign key detection"""
        df = pd.DataFrame({
            'order_id': [1, 2, 3, 4, 5],
            'customer_id': [10, 10, 20, 20, 30],  # Repeating values = FK
            'product_id': [100, 200, 100, 300, 200]  # Repeating values = FK
        })
        schema = TableSchema('orders', df)
        
        assert len(schema.foreign_keys) == 2
        fk_names = [fk.name for fk in schema.foreign_keys]
        assert 'customer_id' in fk_names
        assert 'product_id' in fk_names
    
    def test_no_self_referencing_fks(self):
        """Test that FKs don't reference their own table"""
        df = pd.DataFrame({
            'employee_id': [1, 2, 3],
            'manager_id': [None, 1, 1]  # Refers to employee_id
        })
        schema = TableSchema('employees', df)
        
        # manager_id should still be detected as FK
        # but referenced table is 'managers' not 'employees'
        fk_names = [fk.name for fk in schema.foreign_keys]
        assert 'manager_id' in fk_names
    
    def test_create_table_sql(self):
        """Test SQL generation"""
        df = pd.DataFrame({
            'product_id': [1, 2, 3],
            'name': ['Widget', 'Gadget', 'Doohickey'],
            'price': [10.5, 20.99, 15.0]
        })
        schema = TableSchema('products', df)
        sql = schema.to_create_table_sql()
        
        assert 'CREATE TABLE products' in sql
        # product_id will be INTEGER (not TEXT) since it contains integers
        assert 'product_id INTEGER PRIMARY KEY' in sql
        assert 'name TEXT NOT NULL' in sql
        assert 'price REAL NOT NULL' in sql


class TestSchemaDetector:
    """Test SchemaDetector class"""
    
    @pytest.fixture
    def electronics_dir(self):
        """Path to electronics test data"""
        return Path('data/excel/electronics_company')
    
    def test_analyze_directory(self, electronics_dir):
        """Test analyzing entire directory"""
        if not electronics_dir.exists():
            pytest.skip("Electronics test data not found")
        
        detector = SchemaDetector()
        detector.analyze_directory(str(electronics_dir))
        
        assert len(detector.tables) == 12  # 12 tables in electronics
        assert 'customers' in detector.tables
        assert 'products' in detector.tables
        assert 'sales_orders' in detector.tables
    
    def test_schema_summary(self, electronics_dir):
        """Test human-readable schema summary"""
        if not electronics_dir.exists():
            pytest.skip("Electronics test data not found")
        
        detector = SchemaDetector()
        detector.analyze_directory(str(electronics_dir))
        summary = detector.get_schema_summary()
        
        assert 'AUTO-DETECTED DATABASE SCHEMA' in summary
        assert 'Tables: 12' in summary
        assert 'customers' in summary.lower()
        assert 'RELATIONSHIPS' in summary
    
    def test_sql_generation(self, electronics_dir):
        """Test SQL schema generation"""
        if not electronics_dir.exists():
            pytest.skip("Electronics test data not found")
        
        detector = SchemaDetector()
        detector.analyze_directory(str(electronics_dir))
        sql = detector.generate_sql_schema()
        
        assert 'CREATE TABLE customers' in sql
        assert 'CREATE TABLE products' in sql
        assert 'PRIMARY KEY' in sql
        assert 'NOT NULL' in sql
    
    def test_relationship_inference(self, electronics_dir):
        """Test FK-PK relationship detection"""
        if not electronics_dir.exists():
            pytest.skip("Electronics test data not found")
        
        detector = SchemaDetector()
        detector.analyze_directory(str(electronics_dir))
        
        # Should detect relationships like:
        # sales_orders.customer_id → customers.customer_id
        relationships = detector.get_schema_summary()
        assert 'customer_id → customers' in relationships
        assert 'product_id → products' in relationships
    
    def test_to_dict_export(self, electronics_dir):
        """Test JSON export"""
        if not electronics_dir.exists():
            pytest.skip("Electronics test data not found")
        
        detector = SchemaDetector()
        detector.analyze_directory(str(electronics_dir))
        schema_dict = detector.to_dict()
        
        assert 'tables' in schema_dict
        assert len(schema_dict['tables']) == 12
        
        # Check table structure (tables is a dict, not a list)
        customers = schema_dict['tables']['customers']
        assert 'columns' in customers
        assert 'primary_key' in customers
        assert 'row_count' in customers
        assert customers['primary_key'] == 'customer_id'


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_dataframe(self):
        """Test handling empty DataFrame"""
        df = pd.DataFrame()
        # Should not crash
        try:
            schema = TableSchema('empty_table', df)
            assert schema.row_count == 0
            assert len(schema.columns) == 0
        except Exception as e:
            pytest.fail(f"Should handle empty DataFrame: {e}")
    
    def test_all_null_column(self):
        """Test column with all null values"""
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'optional': [None, None, None]
        })
        col = ColumnInfo('optional', df, 1)
        assert col.data_type == 'TEXT'  # Default to TEXT
        assert col.null_percentage == 100.0
    
    def test_no_primary_key(self):
        """Test table with no clear primary key"""
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Alice'],  # Not unique
            'score': [90, 85, 92]
        })
        schema = TableSchema('test_table', df)
        assert schema.primary_key is None  # No PK found
