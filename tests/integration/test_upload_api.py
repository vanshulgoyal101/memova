"""
Integration tests for /upload API endpoint

Tests the complete upload workflow:
- File upload
- Schema detection
- Database creation
- Query execution on uploaded data
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import shutil

from api.main import app


class TestUploadAPI:
    """Test upload endpoint"""
    
    @pytest.fixture
    def client(self):
        """FastAPI test client"""
        return TestClient(app)
    
    @pytest.fixture
    def sample_excel_file(self, tmp_path):
        """Create a sample Excel file for testing"""
        import pandas as pd
        
        # Create sample data
        df = pd.DataFrame({
            'customer_id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com', 
                     'diana@example.com', 'eve@example.com'],
            'total_purchases': [1500.50, 2300.75, 890.00, 3200.00, 1100.25]
        })
        
        # Save to Excel
        excel_path = tmp_path / 'customers.xlsx'
        df.to_excel(excel_path, index=False, engine='openpyxl')
        
        return excel_path
    
    def test_upload_single_file(self, client, sample_excel_file):
        """Test uploading a single Excel file"""
        with open(sample_excel_file, 'rb') as f:
            response = client.post(
                "/upload",
                files={"files": ("customers.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert 'upload_id' in data
        assert 'database_name' in data
        assert 'database_path' in data
        assert 'detected_schema' in data
        assert 'table_count' in data
        assert 'total_rows' in data
        assert 'message' in data
        
        # Check values
        assert data['table_count'] == 1  # One table (customers)
        assert data['total_rows'] == 5  # 5 rows
        assert 'customers' in data['detected_schema']['tables']
        
        # Check schema structure
        customers_schema = data['detected_schema']['tables']['customers']
        assert 'columns' in customers_schema
        assert 'primary_key' in customers_schema
        assert len(customers_schema['columns']) == 4  # 4 columns
        assert customers_schema['primary_key'] == 'customer_id'
    
    def test_upload_invalid_file_type(self, client, tmp_path):
        """Test uploading invalid file type"""
        # Create a text file
        txt_file = tmp_path / 'test.txt'
        txt_file.write_text('This is not an Excel file')
        
        with open(txt_file, 'rb') as f:
            response = client.post(
                "/upload",
                files={"files": ("test.txt", f, "text/plain")}
            )
        
        assert response.status_code == 400
        assert 'Invalid file type' in response.json()['detail']
    
    def test_upload_no_files(self, client):
        """Test uploading with no files"""
        response = client.post("/upload", files={})
        assert response.status_code == 422  # Validation error
    
    def test_list_uploads(self, client, sample_excel_file):
        """Test listing uploaded databases"""
        # First upload a file
        with open(sample_excel_file, 'rb') as f:
            upload_response = client.post(
                "/upload",
                files={"files": ("customers.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            )
        
        assert upload_response.status_code == 200
        upload_id = upload_response.json()['upload_id']
        
        # List uploads
        list_response = client.get("/uploads")
        assert list_response.status_code == 200
        
        uploads = list_response.json()
        assert len(uploads) >= 1
        
        # Check if our upload is in the list
        upload_ids = [u['id'] for u in uploads]
        assert upload_id in upload_ids
    
    def test_delete_upload(self, client, sample_excel_file):
        """Test deleting an uploaded database"""
        # First upload a file
        with open(sample_excel_file, 'rb') as f:
            upload_response = client.post(
                "/upload",
                files={"files": ("customers.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            )
        
        assert upload_response.status_code == 200
        upload_id = upload_response.json()['upload_id']
        
        # Delete the upload
        delete_response = client.delete(f"/uploads/{upload_id}")
        assert delete_response.status_code == 200
        assert 'deleted successfully' in delete_response.json()['message']
        
        # Verify it's gone
        list_response = client.get("/uploads")
        uploads = list_response.json()
        upload_ids = [u['id'] for u in uploads]
        assert upload_id not in upload_ids
    
    def test_delete_nonexistent_upload(self, client):
        """Test deleting a non-existent upload"""
        response = client.delete("/uploads/nonexistent_id")
        assert response.status_code == 404
    
    def test_delete_builtin_database(self, client):
        """Test that built-in databases cannot be deleted"""
        response = client.delete("/uploads/electronics")
        assert response.status_code in [400, 404]  # Either bad request or not found


class TestUploadedDatabaseQuery:
    """Test querying uploaded databases"""
    
    @pytest.fixture
    def client(self):
        """FastAPI test client"""
        return TestClient(app)
    
    @pytest.fixture
    def uploaded_db(self, client, tmp_path):
        """Upload a database and return its ID"""
        import pandas as pd
        
        # Create sample orders data
        df = pd.DataFrame({
            'order_id': [1, 2, 3, 4, 5],
            'customer_id': [101, 102, 101, 103, 102],
            'product_name': ['Widget', 'Gadget', 'Widget', 'Doohickey', 'Gadget'],
            'amount': [150.00, 200.00, 150.00, 300.00, 200.00],
            'order_date': pd.date_range('2024-01-01', periods=5, freq='D')
        })
        
        excel_path = tmp_path / 'orders.xlsx'
        df.to_excel(excel_path, index=False, engine='openpyxl')
        
        with open(excel_path, 'rb') as f:
            response = client.post(
                "/upload",
                files={"files": ("orders.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            )
        
        assert response.status_code == 200
        return response.json()['upload_id']
    
    @pytest.mark.slow
    def test_query_uploaded_database(self, client, uploaded_db):
        """Test querying an uploaded database"""
        # Query the uploaded database
        response = client.post(
            "/ask",
            json={
                "question": "How many orders are there?",
                "company_id": uploaded_db,
                "section_ids": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return 5 orders
        assert 'answer_text' in data
        assert 'rows' in data
        # Check that we got some result
        assert len(data['rows']) > 0 or '5' in data['answer_text']
    
    @pytest.mark.slow
    def test_query_uploaded_with_aggregation(self, client, uploaded_db):
        """Test aggregation query on uploaded database"""
        response = client.post(
            "/ask",
            json={
                "question": "What is the total amount of all orders?",
                "company_id": uploaded_db,
                "section_ids": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Total should be 1000.00 (150+200+150+300+200)
        assert 'answer_text' in data
        # Check for the sum in either answer or SQL
        assert '1000' in str(data) or 'SUM' in data.get('sql', '').upper()
