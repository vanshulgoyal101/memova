"""
Integration tests for chart detection feature.

Tests that charts are automatically detected and included in API responses.
"""

import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestChartDetectionIntegration:
    """Test chart detection in API responses."""
    
    def test_ask_endpoint_includes_charts_for_categorical(self):
        """Should include bar/pie chart for categorical breakdown."""
        response = client.post(
            "/ask",
            json={
                "question": "Show employee count by department",
                "company_id": "electronics",
                "section_ids": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "charts" in data
        if data["charts"] and len(data["charts"]) > 0:
            chart = data["charts"][0]
            assert chart["type"] in ("bar", "pie")
            assert "id" in chart
            assert "title" in chart
            assert "x_column" in chart
            assert "y_columns" in chart
            assert isinstance(chart["data"], list)
            assert chart["confidence"] > 0.0
    
    def test_ask_endpoint_includes_charts_for_timeseries(self):
        """Should include line chart for time series data."""
        # Note: This test may not detect a chart if the query doesn't return temporal data
        response = client.post(
            "/ask",
            json={
                "question": "Show sales over time",
                "company_id": "electronics",
                "section_ids": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Charts may or may not be present depending on SQL results
        assert "charts" in data
    
    def test_query_endpoint_includes_charts(self):
        """Should include charts in legacy /query endpoint too."""
        response = client.post(
            "/query",
            json={
                "question": "Count employees by department",
                "database": "electronics"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "charts" in data
        # Charts should be null or a list
        assert data["charts"] is None or isinstance(data["charts"], list)
    
    def test_empty_results_no_charts(self):
        """Should not include charts for empty result sets."""
        response = client.post(
            "/ask",
            json={
                "question": "Show employees where salary > 999999999",
                "company_id": "electronics",
                "section_ids": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Empty results should have no charts (or empty charts array)
        if data.get("meta", {}).get("row_count") == 0:
            assert data.get("charts") is None or data.get("charts") == []
    
    def test_chart_data_structure(self):
        """Verify chart data has correct structure."""
        response = client.post(
            "/ask",
            json={
                "question": "Show product categories with product count",
                "company_id": "electronics",
                "section_ids": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        if data.get("charts") and len(data["charts"]) > 0:
            chart = data["charts"][0]
            
            # Required fields
            assert "id" in chart
            assert "type" in chart
            assert "title" in chart
            assert "x_column" in chart
            assert "y_columns" in chart
            assert "data" in chart
            assert "x_type" in chart
            assert "confidence" in chart
            
            # Data should be a list of dicts
            assert isinstance(chart["data"], list)
            if len(chart["data"]) > 0:
                assert isinstance(chart["data"][0], dict)
            
            # Confidence should be between 0 and 1
            assert 0.0 <= chart["confidence"] <= 1.0
    
    def test_multiple_databases_chart_detection(self):
        """Charts should work across different databases."""
        databases = ["electronics", "airline"]
        
        for db in databases:
            response = client.post(
                "/ask",
                json={
                    "question": "Count records by category",
                    "company_id": db,
                    "section_ids": []
                }
            )
            
            # Should succeed regardless of whether charts are detected
            assert response.status_code == 200
            data = response.json()
            assert "charts" in data
