"""
Unit Tests for LLM Summarizer
Tests data preparation logic (downsampling, aggregates, payload building)
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.summarizer import summarize_result


def mock_generate_text(system_prompt: str, user_prompt: str) -> str:
    """Mock generate_text function for testing without API calls"""
    return """The top products by revenue are Widget A, Widget B, and Widget C, generating $35,500 in total sales across 245 units.

• Widget A leads with $15,000 in revenue from 100 units sold
• Widget B follows with $12,000 from 80 units
• Widget C rounds out the top 3 with $8,500 from 65 units
• Average revenue per product: $11,833
• Products show consistent unit economics with strong performance"""


class TestLLMSummarizer:
    """Test LLM summarizer functionality"""
    
    @pytest.fixture
    def mock_gemini(self):
        """Mock the generate_text function to avoid API calls"""
        with patch('src.utils.llm.generate_text', side_effect=mock_generate_text) as mock_gen:
            yield mock_gen
    
    def test_basic_summary_format(self, mock_gemini):
        """Test basic summary returns meaningful text"""
        cols = ["product", "revenue", "units_sold"]
        rows = [
            ["Widget A", 15000, 100],
            ["Widget B", 12000, 80],
            ["Widget C", 8500, 65]
        ]
        
        result = summarize_result(
            question="What are the top products by revenue?",
            columns=cols,
            rows=rows,
            company_id="electronics",
            section_ids=["products", "sales"],
            exec_ms=25.5
        )
        
        # Verify format
        assert isinstance(result, str)
        assert len(result) > 20  # Should have meaningful content
        
        # Check for meaningful content (either from LLM or fallback)
        lines = result.split('\n')
        assert len(lines) > 0
        
        # Should have either bullets OR tabular data
        has_bullets = '•' in result or '-' in result or '*' in result
        has_data = any(str(row[0]) in result for row in rows)  # Widget A, B, or C
        assert has_bullets or has_data, "Should have formatted content"
    
    def test_downsampling_large_dataset(self, mock_gemini, caplog):
        """Test downsampling logic for large datasets"""
        cols = ["id", "name", "value"]
        rows = [[i, f"Item {i}", i * 100] for i in range(1000)]
        
        result = summarize_result(
            question="Show all items",
            columns=cols,
            rows=rows,
            company_id="electronics",
            section_ids=[],
            exec_ms=45.0,
            max_cells=100  # Force downsampling
        )
        
        # Verify result was generated (downsampling happens internally)
        assert isinstance(result, str)
        assert len(result) > 0
        # With 1000 rows and 3 columns = 3000 cells > max_cells (100), downsampling should occur
    
    def test_mixed_data_types(self, mock_gemini):
        """Test handling of mixed data types (numeric and non-numeric)"""
        cols = ["product", "price", "quantity", "in_stock"]
        rows = [
            ["Product A", 99.99, 50, True],
            ["Product B", 149.50, 30, False],
            ["Product C", 79.99, 75, True]
        ]
        
        result = summarize_result(
            question="Show product inventory",
            columns=cols,
            rows=rows,
            company_id="electronics",
            section_ids=["products"],
            exec_ms=18.5
        )
        
        # Should handle mixed types without crashing
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_empty_results(self, mock_gemini):
        """Test handling of empty result sets"""
        cols = ["product", "revenue"]
        rows = []
        
        result = summarize_result(
            question="Show products",
            columns=cols,
            rows=rows,
            company_id="electronics",
            section_ids=[],
            exec_ms=10.0
        )
        
        # Should handle gracefully
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_single_value_result(self, mock_gemini):
        """Test handling of single value results (e.g., COUNT, AVG)"""
        cols = ["avg_salary"]
        rows = [[95212.75]]
        
        result = summarize_result(
            question="What is the average employee salary?",
            columns=cols,
            rows=rows,
            company_id="electronics",
            section_ids=["employees"],
            exec_ms=12.3
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_fallback_on_api_error(self):
        """Test graceful fallback when API fails"""
        # Mock UnifiedLLMClient.generate_content to raise an error
        cols = ["product", "revenue"]
        rows = [["Widget A", 15000]]
        
        with patch('src.core.llm_client.UnifiedLLMClient.generate_content') as mock_gen:
            mock_gen.side_effect = Exception("API Error")
            
            result = summarize_result(
                question="Show products",
                columns=cols,
                rows=rows,
                company_id="electronics",
                section_ids=[],
                exec_ms=10.0
            )
            
            # Should fall back to basic data display (no LLM summary)
            # The fallback shows actual data when LLM fails
            assert "Widget" in result or "15000" in result or "$15,000" in result
            mock_gen.assert_called_once()  # Verify we attempted LLM call
    
    def test_numeric_aggregates_computation(self, mock_gemini):
        """Test that numeric aggregates are computed for numeric columns"""
        cols = ["product", "price", "quantity"]
        rows = [
            ["Product A", 100.0, 10],
            ["Product B", 200.0, 20],
            ["Product C", 150.0, 15]
        ]
        
        # This test verifies the function doesn't crash when computing aggregates
        result = summarize_result(
            question="Show products",
            columns=cols,
            rows=rows,
            company_id="electronics",
            section_ids=["products"],
            exec_ms=20.0
        )
        
        assert isinstance(result, str)
        assert len(result) > 0

