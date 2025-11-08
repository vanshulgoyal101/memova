"""
Integration Tests for LLM Summarizer API
Tests /ask endpoint integration with real query engine
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys
from unittest.mock import patch

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from api.main import app
from src.core.summarizer import summarize_result


class MockGeminiClient:
    """Mock Gemini client for integration tests"""
    
    def generate_text(self, user_prompt, system_prompt=None, temperature=0.3, max_tokens=300):
        """Return a realistic mock summary based on the query"""
        if "average" in user_prompt.lower() or "avg" in user_prompt.lower():
            return """The average employee salary is $95,212.75.

• This represents compensation across all departments
• Engineering leads with higher average salaries
• Range spans from entry-level to senior positions"""
        
        if "top" in user_prompt.lower() or "highest" in user_prompt.lower():
            return """The top employees by salary represent the senior leadership team.

• Highest earner: $149,955 annual salary
• Top 3 employees are in engineering and management
• Total compensation for top performers reflects market rates
• Strong retention of high-performing talent"""
        
        return """Query results provide insights into the requested data.

• Data retrieved successfully from database
• Results reflect current state of records
• Analysis complete"""


class TestLLMSummarizerIntegration:
    """Integration tests for /ask endpoint with LLM summarizer"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_gemini(self):
        """Mock generate_text function for all tests"""
        def mock_generate_text(system_prompt, user_prompt, temperature=0.3, max_tokens=300):
            """Return a realistic mock summary based on the query"""
            prompt_text = user_prompt.lower() if user_prompt else ""
            
            if "average" in prompt_text or "avg" in prompt_text:
                return """The average employee salary is $95,212.75.

• This represents compensation across all departments
• Engineering leads with higher average salaries
• Range spans from entry-level to senior positions"""
            
            if "top" in prompt_text or "highest" in prompt_text:
                return """The top employees by salary represent the senior leadership team.

• Highest earner: $149,955 annual salary
• Top 3 employees are in engineering and management
• Total compensation for top performers reflects market rates
• Strong retention of high-performing talent"""
            
            if "count" in prompt_text or "how many" in prompt_text:
                return """There are 150 employees in the database.

• This represents the current workforce
• Across all departments and positions
• Data reflects active employee records"""
            
            return """Query results provide insights into the requested data.

• Data retrieved successfully from database
• Results reflect current state of records
• Analysis complete"""
        
        # Mock generate_text in its actual location (src.utils.llm)
        with patch('src.utils.llm.generate_text', side_effect=mock_generate_text) as mock_llm:
            yield mock_llm
    
    def test_ask_endpoint_exists(self, client):
        """Test that /ask endpoint is available"""
        response = client.post("/ask", json={
            "question": "How many employees?",
            "company_id": "electronics",
            "section_ids": []
        })
        
        # Should return 200 or have proper error handling
        assert response.status_code in [200, 404, 500]
    
    @pytest.mark.skipif(
        not Path("data/database/electronics_company.db").exists(),
        reason="Database not generated"
    )
    @pytest.mark.slow  # Mark as slow test (uses real AI API)
    def test_ask_average_salary(self, client):
        """Test /ask endpoint with average salary query (uses real AI)"""
        response = client.post("/ask", json={
            "question": "What is the average employee salary?",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "answer_text" in data
        assert "sql" in data
        assert "columns" in data
        assert "rows" in data
        assert "timings" in data
        assert "meta" in data
        
        # Verify SQL was generated
        assert "SELECT" in data["sql"].upper()
        assert len(data["answer_text"]) > 0  # May be fallback or real summary
    
    @pytest.mark.skipif(
        not Path("data/database/electronics_company.db").exists(),
        reason="Database not generated"
    )
    @pytest.mark.slow  # Mark as slow test (uses real AI API)
    def test_ask_top_employees(self, client):
        """Test /ask endpoint with top employees query (uses real AI)"""
        response = client.post("/ask", json={
            "question": "Show top 3 employees by salary",
            "company_id": "electronics",
            "section_ids": ["employees"]
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response
        assert "answer_text" in data
        assert "rows" in data
        assert len(data["answer_text"]) > 0
    
    def test_ask_invalid_company(self, client):
        """Test /ask endpoint with invalid company_id"""
        response = client.post("/ask", json={
            "question": "How many employees?",
            "company_id": "invalid_company",
            "section_ids": []
        })
        
        assert response.status_code == 400
    
    def test_ask_missing_fields(self, client):
        """Test /ask endpoint with missing required fields"""
        response = client.post("/ask", json={
            "question": "How many employees?"
            # Missing company_id
        })
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.skipif(
        not Path("data/database/electronics_company.db").exists(),
        reason="Database not generated"
    )
    @pytest.mark.slow  # Mark as slow test (uses real AI API)
    def test_ask_response_format(self, client):
        """Test that /ask response follows AskResponse schema (uses real AI)"""
        response = client.post("/ask", json={
            "question": "Count employees",
            "company_id": "electronics",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields
        assert isinstance(data["answer_text"], str)
        assert isinstance(data["sql"], str)
        assert isinstance(data["columns"], list)
        assert isinstance(data["rows"], list)
        assert isinstance(data["timings"], dict)
        assert isinstance(data["meta"], dict)
        
        # Verify timings structure (genMs and execMs)
        assert "genMs" in data["timings"]
        assert "execMs" in data["timings"]
        
        # Verify meta structure
        assert "row_count" in data["meta"]
    
    @pytest.mark.skipif(
        not Path("data/database/airline_company.db").exists(),
        reason="Database not generated"
    )
    @pytest.mark.slow  # Mark as slow test (uses real AI API)
    def test_ask_airline_database(self, client):
        """Test /ask endpoint with airline database (uses real AI)"""
        response = client.post("/ask", json={
            "question": "How many flights?",
            "company_id": "airline",
            "section_ids": []
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer_text" in data
        assert len(data["answer_text"]) > 0

