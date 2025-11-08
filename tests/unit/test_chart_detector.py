"""
Unit tests for ChartDetector.

Tests chart detection heuristics:
- Time series detection
- Categorical breakdown detection
- Histogram detection
- Edge cases (empty results, single column, etc.)
"""

import pytest
from src.core.chart_detector import (
    ChartDetector,
    ChartConfig,
    ColumnMetadata,
    detect_charts_from_results
)


class TestColumnTypeInference:
    """Test column type inference logic."""
    
    def test_infer_numeric_type(self):
        """Should detect numeric columns."""
        columns = ["revenue"]
        rows = [[100.5], [200.0], [150.25]]
        
        detector = ChartDetector(columns, rows)
        assert len(detector.column_metadata) == 1
        assert detector.column_metadata[0].is_numeric()
    
    def test_infer_date_type(self):
        """Should detect date columns."""
        columns = ["order_date"]
        rows = [["2025-01-01"], ["2025-01-02"], ["2025-01-03"]]
        
        detector = ChartDetector(columns, rows)
        assert len(detector.column_metadata) == 1
        assert detector.column_metadata[0].is_temporal()
        assert detector.column_metadata[0].inferred_type == "date"
    
    def test_infer_datetime_type(self):
        """Should detect datetime columns."""
        columns = ["created_at"]
        rows = [
            ["2025-01-01T10:30:00"],
            ["2025-01-02T14:15:00"],
            ["2025-01-03T09:00:00"]
        ]
        
        detector = ChartDetector(columns, rows)
        assert len(detector.column_metadata) == 1
        assert detector.column_metadata[0].is_temporal()
        assert detector.column_metadata[0].inferred_type == "datetime"
    
    def test_infer_categorical_type(self):
        """Should detect categorical columns (low cardinality)."""
        columns = ["department"]
        rows = [["Engineering"], ["Sales"], ["Engineering"], ["Marketing"], ["Sales"]]
        
        detector = ChartDetector(columns, rows)
        assert len(detector.column_metadata) == 1
        assert detector.column_metadata[0].is_categorical()
    
    def test_infer_text_type(self):
        """Should default to text for high cardinality strings."""
        columns = ["description"]
        rows = [[f"Description {i}"] for i in range(100)]
        
        detector = ChartDetector(columns, rows)
        assert len(detector.column_metadata) == 1
        assert detector.column_metadata[0].inferred_type == "text"


class TestTimeSeriesDetection:
    """Test time series chart detection."""
    
    def test_detect_time_series_basic(self):
        """Should detect basic time series (date + numeric)."""
        columns = ["month", "revenue"]
        rows = [
            ["2025-01-01", 10000],
            ["2025-02-01", 15000],
            ["2025-03-01", 12000]
        ]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        assert len(charts) >= 1
        time_chart = next((c for c in charts if c.type == "line"), None)
        assert time_chart is not None
        assert time_chart.x_column == "month"
        assert "revenue" in time_chart.y_columns
        assert time_chart.confidence > 0.7
    
    def test_detect_time_series_multiple_metrics(self):
        """Should detect time series with multiple y-axis columns."""
        columns = ["date", "revenue", "profit", "orders"]
        rows = [
            ["2025-01-01", 10000, 2000, 50],
            ["2025-02-01", 15000, 3000, 75],
            ["2025-03-01", 12000, 2500, 60]
        ]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        time_chart = next((c for c in charts if c.type == "line"), None)
        assert time_chart is not None
        # Should include up to 3 metrics
        assert len(time_chart.y_columns) <= 3
        assert "revenue" in time_chart.y_columns
    
    def test_no_time_series_without_temporal(self):
        """Should not detect time series without temporal column."""
        columns = ["category", "count"]
        rows = [["A", 10], ["B", 20]]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        time_chart = next((c for c in charts if c.type == "line"), None)
        assert time_chart is None
    
    def test_no_time_series_without_numeric(self):
        """Should not detect time series without numeric column."""
        columns = ["date", "name"]
        rows = [["2025-01-01", "John"], ["2025-01-02", "Jane"]]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        time_chart = next((c for c in charts if c.type == "line"), None)
        assert time_chart is None


class TestCategoricalBreakdown:
    """Test categorical breakdown chart detection."""
    
    def test_detect_pie_chart_few_categories(self):
        """Should detect pie chart for few categories (<=6)."""
        columns = ["department", "employee_count"]
        rows = [
            ["Engineering", 50],
            ["Sales", 30],
            ["Marketing", 20],
            ["HR", 10]
        ]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        cat_chart = next((c for c in charts if c.type in ("pie", "bar")), None)
        assert cat_chart is not None
        assert cat_chart.x_column == "department"
        assert "employee_count" in cat_chart.y_columns
        # Should prefer pie for few categories
        assert cat_chart.type == "pie"
    
    def test_detect_bar_chart_many_categories(self):
        """Should detect bar chart for many categories (>6)."""
        columns = ["product", "sales"]
        rows = [[f"Product_{i}", i * 100] for i in range(10)]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        cat_chart = next((c for c in charts if c.type in ("pie", "bar")), None)
        assert cat_chart is not None
        # Should prefer bar for many categories
        assert cat_chart.type == "bar"
    
    def test_no_categorical_without_category_column(self):
        """Should not detect categorical chart without categorical column."""
        columns = ["value1", "value2"]
        rows = [[i, i * 2] for i in range(100)]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        cat_chart = next((c for c in charts if c.type in ("pie", "bar")), None)
        assert cat_chart is None


class TestHistogramDetection:
    """Test histogram detection."""
    
    def test_detect_histogram_single_numeric(self):
        """Should detect histogram for single numeric column."""
        columns = ["age"]
        rows = [[i] for i in range(18, 65)]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        hist_chart = next((c for c in charts if c.type == "histogram"), None)
        assert hist_chart is not None
        assert hist_chart.x_column == "age"
    
    def test_no_histogram_for_multiple_columns(self):
        """Should not create histogram when multiple columns present."""
        columns = ["age", "name"]
        rows = [[25, "John"], [30, "Jane"]]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        hist_chart = next((c for c in charts if c.type == "histogram"), None)
        assert hist_chart is None
    
    def test_no_histogram_for_few_values(self):
        """Should not create histogram for very few distinct values."""
        columns = ["rating"]
        rows = [[1], [2], [3], [1]]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        hist_chart = next((c for c in charts if c.type == "histogram"), None)
        assert hist_chart is None


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_result_set(self):
        """Should handle empty result set gracefully."""
        columns = ["id", "name"]
        rows = []
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        assert charts == []
    
    def test_single_column(self):
        """Should handle single column result."""
        columns = ["count"]
        rows = [[42]]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        # Single value should not generate charts (histogram needs > 5 distinct values)
        assert len(charts) == 0
    
    def test_null_values(self):
        """Should handle null values in data."""
        columns = ["date", "value"]
        rows = [
            ["2025-01-01", 100],
            ["2025-01-02", None],
            ["2025-01-03", 200]
        ]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        # Should still detect chart
        assert len(charts) > 0
    
    def test_large_result_set(self):
        """Should handle large result sets efficiently."""
        columns = ["date", "value"]
        rows = [[f"2025-01-{str(i % 28 + 1).zfill(2)}", i] for i in range(5000)]
        
        detector = ChartDetector(columns, rows, max_sample=1000)
        charts = detector.detect_charts()
        
        # Should still detect chart but limit analysis
        assert len(charts) > 0
        # Chart data should be limited to max_sample
        if charts:
            assert len(charts[0].data) <= 1000


class TestConvenienceFunction:
    """Test the convenience function."""
    
    def test_detect_charts_from_results(self):
        """Should return JSON-serializable chart configs."""
        columns = ["month", "revenue"]
        rows = [
            ["2025-01-01", 10000],
            ["2025-02-01", 15000]
        ]
        
        charts = detect_charts_from_results(columns, rows)
        
        assert isinstance(charts, list)
        if charts:
            assert isinstance(charts[0], dict)
            assert "type" in charts[0]
            assert "data" in charts[0]
            assert "x_column" in charts[0]


class TestChartPrioritization:
    """Test chart confidence scoring and prioritization."""
    
    def test_charts_sorted_by_confidence(self):
        """Should sort charts by confidence score."""
        columns = ["date", "category", "value"]
        rows = [
            ["2025-01-01", "A", 100],
            ["2025-01-02", "B", 200],
            ["2025-01-03", "A", 150]
        ]
        
        detector = ChartDetector(columns, rows)
        charts = detector.detect_charts()
        
        # Should return multiple charts, sorted by confidence
        if len(charts) > 1:
            for i in range(len(charts) - 1):
                assert charts[i].confidence >= charts[i + 1].confidence
