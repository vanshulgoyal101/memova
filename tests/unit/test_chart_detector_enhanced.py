"""
Unit tests for enhanced chart detection features.

Tests:
- Multi-series line charts
- Stacked bar charts
- Area charts
- Combo charts
- New chart types integration

Author: Context Engineering
Created: 2025-11-07
"""

import pytest
from src.core.chart_detector import ChartDetector, ChartConfig


class TestMultiSeriesLineChart:
    """Test multi-series line chart detection."""
    
    def test_detects_multi_series_with_temporal_and_multiple_numeric(self):
        """Should detect multi-series line when 2+ numeric columns with temporal."""
        columns = ["date", "revenue", "cost", "profit"]
        rows = [
            ["2024-01-01", 10000, 6000, 4000],
            ["2024-01-02", 12000, 7000, 5000],
            ["2024-01-03", 11000, 6500, 4500],
        ]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_multi_series_line()
        
        assert chart is not None
        assert chart.type == "line"
        assert chart.x_column == "date"
        assert len(chart.y_columns) == 3  # revenue, cost, profit
        assert "revenue" in chart.y_columns
        assert "cost" in chart.y_columns
        assert "profit" in chart.y_columns
    
    def test_limits_to_5_series(self):
        """Should limit multi-series to max 5 series."""
        columns = ["date", "col1", "col2", "col3", "col4", "col5", "col6", "col7"]
        rows = [
            ["2024-01-01", 1, 2, 3, 4, 5, 6, 7],
            ["2024-01-02", 2, 3, 4, 5, 6, 7, 8],
        ]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_multi_series_line()
        
        assert chart is not None
        assert len(chart.y_columns) <= 5
    
    def test_returns_none_with_single_numeric(self):
        """Should return None if only 1 numeric column."""
        columns = ["date", "revenue"]
        rows = [
            ["2024-01-01", 10000],
            ["2024-01-02", 12000],
        ]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_multi_series_line()
        
        # Should return None because we need 2+ numeric for multi-series
        assert chart is None
    
    def test_returns_none_without_temporal(self):
        """Should return None without temporal column."""
        columns = ["category", "value1", "value2"]
        rows = [
            ["A", 100, 200],
            ["B", 150, 250],
        ]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_multi_series_line()
        
        assert chart is None


class TestStackedBarChart:
    """Test stacked bar chart detection."""
    
    def test_detects_stacked_bar_with_categorical_and_multiple_numeric(self):
        """Should detect stacked bar with categorical + 2+ numeric."""
        columns = ["region", "product_a", "product_b", "product_c"]
        rows = [
            ["North", 1000, 2000, 1500],
            ["South", 1200, 1800, 1600],
            ["East", 900, 2100, 1400],
        ]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_stacked_bar()
        
        assert chart is not None
        assert chart.type == "stacked_bar"
        assert chart.x_column == "region"
        assert len(chart.y_columns) >= 2
        assert "product_a" in chart.y_columns
        assert "product_b" in chart.y_columns
    
    def test_limits_to_5_stacks(self):
        """Should limit stacked bar to max 5 stacks."""
        columns = ["category", "s1", "s2", "s3", "s4", "s5", "s6", "s7"]
        rows = [
            ["A", 1, 2, 3, 4, 5, 6, 7],
            ["B", 2, 3, 4, 5, 6, 7, 8],
        ]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_stacked_bar()
        
        assert chart is not None
        assert len(chart.y_columns) <= 5
    
    def test_returns_none_with_single_numeric(self):
        """Should return None with only 1 numeric column."""
        columns = ["region", "sales"]
        rows = [
            ["North", 1000],
            ["South", 1200],
        ]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_stacked_bar()
        
        assert chart is None
    
    def test_confidence_higher_with_fewer_categories(self):
        """Should have higher confidence with fewer categories."""
        # 3 categories
        columns1 = ["region", "value1", "value2"]
        rows1 = [["A", 100, 200], ["B", 150, 250], ["C", 120, 220]]
        detector1 = ChartDetector(columns1, rows1)
        chart1 = detector1._detect_stacked_bar()
        
        # 15 categories
        columns2 = ["region", "value1", "value2"]
        rows2 = [[f"Cat{i}", 100, 200] for i in range(15)]
        detector2 = ChartDetector(columns2, rows2)
        chart2 = detector2._detect_stacked_bar()
        
        assert chart1 is not None and chart2 is not None
        assert chart1.confidence > chart2.confidence


class TestAreaChart:
    """Test area chart detection."""
    
    def test_detects_area_chart_with_temporal_and_numeric(self):
        """Should detect area chart with temporal + numeric."""
        columns = ["month", "cumulative_sales"]
        rows = [
            ["2024-01", 1000],
            ["2024-02", 2200],
            ["2024-03", 3500],
        ]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_area_chart()
        
        assert chart is not None
        assert chart.type == "area"
        assert chart.x_column == "month"
        assert "cumulative_sales" in chart.y_columns
    
    def test_handles_multiple_series(self):
        """Should handle multiple series for stacked area."""
        columns = ["date", "category_a", "category_b", "category_c"]
        rows = [
            ["2024-01-01", 100, 200, 150],
            ["2024-01-02", 120, 210, 160],
        ]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_area_chart()
        
        assert chart is not None
        assert len(chart.y_columns) == 3
    
    def test_returns_none_without_temporal(self):
        """Should return None without temporal column."""
        columns = ["category", "value"]
        rows = [["A", 100], ["B", 200]]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_area_chart()
        
        assert chart is None


class TestComboChart:
    """Test combo chart (line + bar) detection."""
    
    def test_detects_combo_chart_with_two_numeric(self):
        """Should detect combo chart with temporal + 2 numeric."""
        columns = ["date", "revenue", "growth_rate"]
        rows = [
            ["2024-01-01", 10000, 0.05],
            ["2024-01-02", 12000, 0.20],
            ["2024-01-03", 11000, -0.08],
        ]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_combo_chart()
        
        assert chart is not None
        assert chart.type == "combo"
        assert chart.x_column == "date"
        assert len(chart.y_columns) == 2
        assert "revenue" in chart.y_columns
        assert "growth_rate" in chart.y_columns
    
    def test_returns_none_with_single_numeric(self):
        """Should return None with only 1 numeric."""
        columns = ["date", "value"]
        rows = [["2024-01-01", 100], ["2024-01-02", 120]]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_combo_chart()
        
        assert chart is None
    
    def test_returns_none_without_temporal(self):
        """Should return None without temporal column."""
        columns = ["category", "value1", "value2"]
        rows = [["A", 100, 200]]
        
        detector = ChartDetector(columns, rows)
        chart = detector._detect_combo_chart()
        
        assert chart is None


class TestEnhancedDetection:
    """Test enhanced detection with all new chart types."""
    
    def test_detects_multiple_chart_types(self):
        """Should detect multiple chart types from same data."""
        columns = ["date", "revenue", "cost", "profit"]
        rows = [
            ["2024-01-01", 10000, 6000, 4000],
            ["2024-01-02", 12000, 7000, 5000],
            ["2024-01-03", 11000, 6500, 4500],
        ]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts(use_ai=False)
        
        # Should detect at least one chart
        assert len(charts) > 0
        # Should include some enhanced chart types
        chart_types = [c.type for c in charts]
        assert any(t in chart_types for t in ["line", "area", "combo"])
    
    def test_sorts_by_confidence(self):
        """Should sort detected charts by confidence (highest first)."""
        columns = ["date", "value1", "value2", "value3"]
        rows = [
            ["2024-01-01", 100, 200, 300],
            ["2024-01-02", 120, 210, 310],
        ]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts(use_ai=False)
        
        if len(charts) > 1:
            # Verify sorted by confidence descending
            for i in range(len(charts) - 1):
                assert charts[i].confidence >= charts[i + 1].confidence
    
    def test_backward_compatibility_with_y_columns(self):
        """All charts should still include y_columns for backward compatibility."""
        columns = ["date", "value1", "value2"]
        rows = [
            ["2024-01-01", 100, 200],
            ["2024-01-02", 120, 210],
        ]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts(use_ai=False)
        
        # All charts should have y_columns
        for chart in charts:
            assert hasattr(chart, 'y_columns')
            assert isinstance(chart.y_columns, list)
            assert len(chart.y_columns) > 0
