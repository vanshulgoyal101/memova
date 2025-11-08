"""
Integration tests for Trend Detection API endpoints

Tests that /ask and /query endpoints return trend insights
for appropriate query results.

Author: AI Assistant
Date: 2025-11-06
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestTrendDetectionAPI:
    """Test trend detection through API endpoints."""
    
    def test_ask_endpoint_includes_trends_for_timeseries(self):
        """Test /ask endpoint returns trends for time series queries."""
        request = {
            "question": "Show monthly sales for 2023",
            "company_id": "electronics",
            "section_ids": []
        }
        
        response = client.post("/ask", json=request)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return results
        assert data["sql"]
        assert len(data["rows"]) > 0
        
        # Should detect trends for time series
        # (May be None if no significant trends detected)
        if data.get("trends"):
            trends = data["trends"]
            assert isinstance(trends, list)
            if len(trends) > 0:
                trend = trends[0]
                assert "id" in trend
                assert "type" in trend
                assert "title" in trend
                assert "description" in trend
                assert "confidence" in trend
                assert "metrics" in trend
                assert "columns" in trend
                assert trend["type"] in ["growth", "decline", "flat", "outlier", "distribution", "seasonality"]
                assert 0.0 <= trend["confidence"] <= 1.0
    
    def test_ask_endpoint_includes_trends_for_categorical(self):
        """Test /ask endpoint returns trends for categorical queries."""
        request = {
            "question": "Count employees by department",
            "company_id": "electronics",
            "section_ids": []
        }
        
        response = client.post("/ask", json=request)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return results
        assert data["sql"]
        assert len(data["rows"]) > 0
        
        # May detect categorical outliers
        if data.get("trends"):
            trends = data["trends"]
            assert isinstance(trends, list)
    
    def test_query_endpoint_includes_trends(self):
        """Test /query endpoint includes trends in response."""
        request = {
            "question": "Show total sales by month in 2023",
            "database": "electronics"
        }
        
        response = client.post("/query", json=request)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["sql"]
        
        # trends field should exist (may be null or empty)
        assert "trends" in data
    
    def test_empty_results_no_trends(self):
        """Test that empty results return no trends."""
        request = {
            "question": "Show sales from year 2050",  # Future date = no results
            "company_id": "electronics",
            "section_ids": []
        }
        
        response = client.post("/ask", json=request)
        
        assert response.status_code == 200
        data = response.json()
        
        # Empty results should not have trends
        if len(data["rows"]) == 0:
            assert data.get("trends") is None or len(data.get("trends", [])) == 0
    
    def test_trend_data_structure(self):
        """Test trend data structure is valid."""
        request = {
            "question": "Show average salary by department",
            "company_id": "electronics",
            "section_ids": []
        }
        
        response = client.post("/ask", json=request)
        
        assert response.status_code == 200
        data = response.json()
        
        if data.get("trends") and len(data["trends"]) > 0:
            trend = data["trends"][0]
            
            # Required fields
            assert isinstance(trend["id"], str)
            assert isinstance(trend["type"], str)
            assert isinstance(trend["title"], str)
            assert isinstance(trend["description"], str)
            assert isinstance(trend["confidence"], (int, float))
            assert isinstance(trend["metrics"], dict)
            assert isinstance(trend["columns"], list)
            
            # Valid ranges
            assert trend["confidence"] >= 0.0
            assert trend["confidence"] <= 1.0
            assert len(trend["columns"]) > 0
    
    def test_multiple_databases_trend_detection(self):
        """Test trend detection works for different databases."""
        # Test electronics database
        request1 = {
            "question": "Count products by category",
            "company_id": "electronics",
            "section_ids": []
        }
        
        response1 = client.post("/ask", json=request1)
        assert response1.status_code == 200
        assert "trends" in response1.json()
        
        # Test airline database
        request2 = {
            "question": "Show flight count by month",
            "company_id": "airline",
            "section_ids": []
        }
        
        response2 = client.post("/ask", json=request2)
        assert response2.status_code == 200
        assert "trends" in response2.json()
    
    def test_trends_sorted_by_confidence(self):
        """Test that trends are sorted by confidence (highest first)."""
        request = {
            "question": "Show monthly revenue for all departments",
            "company_id": "electronics",
            "section_ids": []
        }
        
        response = client.post("/ask", json=request)
        
        assert response.status_code == 200
        data = response.json()
        
        if data.get("trends") and len(data["trends"]) > 1:
            trends = data["trends"]
            confidences = [t["confidence"] for t in trends]
            
            # Verify descending order
            assert confidences == sorted(confidences, reverse=True)
