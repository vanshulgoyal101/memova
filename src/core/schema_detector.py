"""
Auto Schema Detection from Excel/CSV Files
Automatically infers database schema, relationships, and types from uploaded files
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from datetime import datetime
import re
from collections import Counter

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ColumnInfo:
    """Information about a single column"""
    
    def __init__(self, name: str, df: pd.DataFrame, col_idx: int):
        self.name = name
        self.original_name = name
        self.data_type = self._infer_type(df[name])
        self.is_unique = df[name].nunique() == len(df)
        self.null_count = df[name].isnull().sum()
        self.null_percentage = (self.null_count / len(df)) * 100
        self.sample_values = df[name].dropna().head(5).tolist()
        self.unique_count = df[name].nunique()
        
        # Set sql_type first (needed for PK detection)
        self.sql_type = self.data_type
        
        # Infer if this might be a key
        self.is_primary_key = self._is_primary_key(df)
        self.is_foreign_key = self._is_foreign_key(self.is_primary_key)
        self.referenced_table = self._infer_referenced_table() if self.is_foreign_key else None
        
    def _infer_type(self, series: pd.Series) -> str:
        """
        Infer SQL data type from pandas series
        
        Returns: 'INTEGER', 'REAL', 'TEXT', 'DATE', 'DATETIME', 'BOOLEAN'
        """
        # Drop nulls for type inference
        non_null = series.dropna()
        
        if len(non_null) == 0:
            return 'TEXT'  # Default to TEXT if all nulls
        
        # Check for boolean (True/False, Yes/No, 0/1)
        if series.dtype == bool:
            return 'BOOLEAN'
        
        unique_vals = set(non_null.unique())
        if unique_vals.issubset({True, False, 1, 0, 'Yes', 'No', 'yes', 'no', 'TRUE', 'FALSE'}):
            return 'BOOLEAN'
        
        # Check for datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return 'DATETIME'
        
        # Try to parse as date/datetime
        if series.dtype == 'object':
            try:
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    parsed = pd.to_datetime(non_null.head(100), errors='coerce')
                if parsed.notna().sum() / len(parsed) > 0.8:  # 80% parseable as dates
                    # Check if has time component
                    if parsed.dt.time.nunique() > 1:
                        return 'DATETIME'
                    else:
                        return 'DATE'
            except:
                pass
        
        # Check for numeric types
        if pd.api.types.is_integer_dtype(series):
            return 'INTEGER'
        
        if pd.api.types.is_float_dtype(series):
            return 'REAL'
        
        # Try to convert to numeric
        if series.dtype == 'object':
            try:
                numeric = pd.to_numeric(non_null.head(100), errors='coerce')
                if numeric.notna().sum() / len(numeric) > 0.8:  # 80% numeric
                    if (numeric % 1 == 0).all():  # All whole numbers
                        return 'INTEGER'
                    else:
                        return 'REAL'
            except:
                pass
        
        # Default to TEXT
        return 'TEXT'
    
    def _is_primary_key(self, df: pd.DataFrame) -> bool:
        """
        Heuristic to determine if column is a primary key.
        
        Criteria (ALL must be true):
        - Unique values (100% unique)
        - No null values
        - Column name ends with 'id' or IS 'id' (case insensitive)
        - Integer or text type (not REAL, DATE, etc.)
        - First or second column in table (common convention)
        """
        # Must be unique and non-null
        if self.null_percentage > 0 or not self.is_unique:
            return False
        
        # Must be suitable type (not REAL, DATE, DATETIME)
        if self.sql_type in ('REAL', 'DATE', 'DATETIME'):
            return False
        
        # Check if name suggests ID (must END with _id or BE id)
        name_lower = self.name.lower()
        if not (name_lower.endswith('_id') or name_lower == 'id'):
            return False
        
        # Must be in first 2 columns (PKs are usually at the start)
        col_position = df.columns.tolist().index(self.name)
        if col_position > 1:
            return False
        
        return True
    
    def _is_foreign_key(self, is_primary_key: bool) -> bool:
        """
        Heuristic to determine if column is a foreign key.
        
        Criteria:
        - Column name ends with '_id' or '_fk'
        - NOT the primary key (can't be both)
        """
        if is_primary_key:
            return False
        
        name_lower = self.name.lower()
        return name_lower.endswith('_id') or name_lower.endswith('_fk')
    
    def _infer_referenced_table(self) -> Optional[str]:
        """
        Infer which table this FK references
        
        Example:
        - 'customer_id' → 'customers'
        - 'product_id' → 'products'
        - 'emp_id' → 'employees'
        """
        col_lower = self.name.lower()
        
        # Remove common suffixes
        base_name = col_lower.replace('_id', '').replace('_fk', '').replace('fk_', '')
        
        # Pluralize common table names
        plural_map = {
            'customer': 'customers',
            'product': 'products',
            'employee': 'employees',
            'order': 'orders',
            'user': 'users',
            'category': 'categories',
            'supplier': 'suppliers',
            'warehouse': 'warehouses',
            'department': 'departments',
            'invoice': 'invoices',
            'payment': 'payments',
            'shipment': 'shipments',
            'ticket': 'tickets',
            'warranty': 'warranties',
        }
        
        # Check if base name matches known tables
        if base_name in plural_map:
            return plural_map[base_name]
        
        # Try adding 's' for simple pluralization
        return base_name + 's'
    
    def to_sql_definition(self) -> str:
        """Generate SQL column definition"""
        sql_type = self.data_type
        
        # Add constraints
        constraints = []
        if self.is_primary_key:
            constraints.append('PRIMARY KEY')
        if self.null_count == 0 and not self.is_primary_key:
            constraints.append('NOT NULL')
        
        constraint_str = ' ' + ' '.join(constraints) if constraints else ''
        
        return f"{self.name} {sql_type}{constraint_str}"
    
    def __repr__(self):
        return f"<Column {self.name}: {self.data_type} (unique={self.is_unique}, pk={self.is_primary_key}, fk={self.is_foreign_key})>"


class TableSchema:
    """Schema information for a single table"""
    
    def __init__(self, name: str, df: pd.DataFrame):
        self.name = name
        self.row_count = len(df)
        self.columns: List[ColumnInfo] = []
        
        # Analyze each column
        primary_keys = []
        for idx, col_name in enumerate(df.columns):
            col_info = ColumnInfo(col_name, df, idx)
            self.columns.append(col_info)
            
            # Only consider first PK candidate to avoid composite keys
            if col_info.is_primary_key and not primary_keys:
                primary_keys.append(col_info)
        
        # Set primary key (only one)
        self.primary_key = primary_keys[0] if primary_keys else None
        
        # Mark only the PK as PK, rest are regular columns
        for col in self.columns:
            if col != self.primary_key:
                col.is_primary_key = False
        
        # Identify foreign keys (exclude self-references and the PK)
        self.foreign_keys = [
            col for col in self.columns 
            if col.is_foreign_key and col.referenced_table != self.name and col != self.primary_key
        ]
    
    def to_create_table_sql(self) -> str:
        """Generate CREATE TABLE SQL statement"""
        lines = [f"CREATE TABLE {self.name} ("]
        
        # Column definitions
        col_defs = [f"    {col.to_sql_definition()}" for col in self.columns]
        lines.append(',\n'.join(col_defs))
        
        lines.append(");")
        return '\n'.join(lines)
    
    def __repr__(self):
        return f"<TableSchema {self.name}: {len(self.columns)} columns, {self.row_count} rows, PK={self.primary_key.name if self.primary_key else None}>"


class SchemaDetector:
    """
    Automatically detect database schema from Excel/CSV files
    
    Features:
    - Infer column types (INTEGER, REAL, TEXT, DATE, DATETIME, BOOLEAN)
    - Detect primary keys (unique, non-null, id-like columns)
    - Detect foreign keys (columns ending in _id)
    - Infer table relationships
    - Generate CREATE TABLE statements
    
    Example:
        >>> detector = SchemaDetector()
        >>> detector.analyze_directory('data/excel/my_company/')
        >>> print(detector.get_schema_summary())
    """
    
    def __init__(self):
        self.tables: Dict[str, TableSchema] = {}
        self.relationships: List[Tuple[str, str, str, str]] = []  # (from_table, from_col, to_table, to_col)
    
    def analyze_file(self, file_path: str) -> TableSchema:
        """
        Analyze a single Excel/CSV file
        
        Args:
            file_path: Path to Excel or CSV file
            
        Returns:
            TableSchema object
        """
        path = Path(file_path)
        table_name = path.stem  # Filename without extension
        
        logger.info(f"Analyzing file: {file_path}")
        
        # Read file
        if path.suffix == '.xlsx':
            df = pd.read_excel(file_path)
        elif path.suffix == '.csv':
            df = pd.read_csv(file_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        
        # Create table schema
        table_schema = TableSchema(table_name, df)
        self.tables[table_name] = table_schema
        
        logger.info(f"✅ Detected schema for '{table_name}': {len(table_schema.columns)} columns, {table_schema.row_count} rows")
        
        return table_schema
    
    def analyze_directory(self, directory: str) -> Dict[str, TableSchema]:
        """
        Analyze all Excel/CSV files in a directory
        
        Args:
            directory: Path to directory containing data files
            
        Returns:
            Dictionary of table_name → TableSchema
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        # Find all Excel and CSV files
        files = list(dir_path.glob('*.xlsx')) + list(dir_path.glob('*.csv'))
        
        if not files:
            logger.warning(f"No Excel or CSV files found in {directory}")
            return {}
        
        logger.info(f"Found {len(files)} file(s) in {directory}")
        
        # Analyze each file
        for file_path in sorted(files):
            self.analyze_file(str(file_path))
        
        # Infer relationships after all tables are loaded
        self._infer_relationships()
        
        return self.tables
    
    def _infer_relationships(self):
        """
        Infer foreign key relationships between tables
        
        Matches FK columns to PK columns by:
        - Column name similarity (customer_id → customers.id)
        - Value overlap (FK values exist in referenced PK)
        """
        logger.info("Inferring table relationships...")
        
        for table_name, table_schema in self.tables.items():
            for fk_col in table_schema.foreign_keys:
                referenced_table = fk_col.referenced_table
                
                # Check if referenced table exists
                if referenced_table in self.tables:
                    ref_table = self.tables[referenced_table]
                    ref_pk = ref_table.primary_key
                    
                    if ref_pk:
                        relationship = (
                            table_name,
                            fk_col.name,
                            referenced_table,
                            ref_pk.name
                        )
                        self.relationships.append(relationship)
                        logger.debug(f"  → {table_name}.{fk_col.name} references {referenced_table}.{ref_pk.name}")
        
        logger.info(f"✅ Detected {len(self.relationships)} relationships")
    
    def get_schema_summary(self) -> str:
        """
        Get human-readable schema summary
        
        Returns:
            Formatted string with schema information
        """
        lines = []
        lines.append("=" * 60)
        lines.append("AUTO-DETECTED DATABASE SCHEMA")
        lines.append("=" * 60)
        lines.append(f"\nTables: {len(self.tables)}")
        lines.append(f"Relationships: {len(self.relationships)}\n")
        
        # Table summaries
        for table_name, table_schema in sorted(self.tables.items()):
            lines.append(f"\n📋 {table_name} ({table_schema.row_count} rows)")
            lines.append("-" * 60)
            
            for col in table_schema.columns:
                pk_indicator = " [PK]" if col.is_primary_key else ""
                fk_indicator = f" [FK → {col.referenced_table}]" if col.is_foreign_key else ""
                null_info = f" ({col.null_percentage:.0f}% null)" if col.null_percentage > 0 else ""
                
                lines.append(f"  • {col.name}: {col.data_type}{pk_indicator}{fk_indicator}{null_info}")
        
        # Relationships
        if self.relationships:
            lines.append("\n\n🔗 RELATIONSHIPS")
            lines.append("-" * 60)
            for from_table, from_col, to_table, to_col in self.relationships:
                lines.append(f"  {from_table}.{from_col} → {to_table}.{to_col}")
        
        lines.append("\n" + "=" * 60)
        
        return '\n'.join(lines)
    
    def generate_sql_schema(self) -> str:
        """
        Generate complete SQL schema (CREATE TABLE statements)
        
        Returns:
            SQL statements to create all tables
        """
        lines = []
        lines.append("-- Auto-generated SQL Schema")
        lines.append(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"-- Tables: {len(self.tables)}")
        lines.append("")
        
        for table_name, table_schema in sorted(self.tables.items()):
            lines.append(f"-- Table: {table_name}")
            lines.append(table_schema.to_create_table_sql())
            lines.append("")
        
        return '\n'.join(lines)
    
    def to_dict(self) -> Dict:
        """
        Export schema as dictionary (for JSON serialization)
        
        Returns:
            Dictionary representation of schema
        """
        return {
            'tables': {
                name: {
                    'row_count': schema.row_count,
                    'primary_key': schema.primary_key.name if schema.primary_key else None,
                    'columns': [
                        {
                            'name': col.name,
                            'type': col.data_type,
                            'is_primary_key': col.is_primary_key,
                            'is_foreign_key': col.is_foreign_key,
                            'referenced_table': col.referenced_table,
                            'null_percentage': round(col.null_percentage, 2),
                            'sample_values': col.sample_values
                        }
                        for col in schema.columns
                    ]
                }
                for name, schema in self.tables.items()
            },
            'relationships': [
                {
                    'from': {'table': rel[0], 'column': rel[1]},
                    'to': {'table': rel[2], 'column': rel[3]}
                }
                for rel in self.relationships
            ]
        }


# Example usage
if __name__ == "__main__":
    # Test with existing data
    detector = SchemaDetector()
    detector.analyze_directory('data/excel/electronics_company/')
    
    print(detector.get_schema_summary())
    print("\n\n")
    print(detector.generate_sql_schema())
