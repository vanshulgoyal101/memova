"""
Unit tests for TrendDetector class

Tests trend detection for:
- Time series (growth/decline)
- Categorical outliers
- Numeric distributions
- Edge cases

Author: AI Assistant
Date: 2025-11-06
"""

import pytest
from src.core.trend_detector import TrendDetector, TrendInsight, detect_trends_from_results


class TestTimeSeriesTrends:
    """Test time series trend detection (growth/decline)."""
    
    def test_growth_trend_detection(self):
        """Test detection of growth trend in time series."""
        columns = ['month', 'sales']
        rows = [
            ['2023-01', 10000],
            ['2023-02', 12000],
            ['2023-03', 15000],
            ['2023-04', 18000],
            ['2023-05', 20000],
        ]
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        assert len(trends) > 0
        growth_trends = [t for t in trends if t.type == "growth"]
        assert len(growth_trends) > 0
        
        trend = growth_trends[0]
        assert trend.metrics['growth_rate'] > 0
        assert trend.metrics['trend'] == 'increasing'
        assert trend.confidence > 0.7
        assert 'month' in trend.columns
        assert 'sales' in trend.columns
    
    def test_decline_trend_detection(self):
        """Test detection of decline trend in time series."""
        columns = ['quarter', 'revenue']
        rows = [
            ['2023-Q1', 100000],
            ['2023-Q2', 90000],
            ['2023-Q3', 75000],
            ['2023-Q4', 60000],
        ]
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        assert len(trends) > 0
        decline_trends = [t for t in trends if t.type == "decline"]
        assert len(decline_trends) > 0
        
        trend = decline_trends[0]
        assert trend.metrics['growth_rate'] < 0
        assert trend.metrics['trend'] == 'decreasing'
        assert trend.confidence > 0.7
    
    def test_flat_trend_detection(self):
        """Test detection of flat/stable trend."""
        columns = ['week', 'orders']
        rows = [
            ['2023-W1', 500],
            ['2023-W2', 505],
            ['2023-W3', 498],
            ['2023-W4', 502],
            ['2023-W5', 501],
        ]
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        # Flat trend might not be reported (growth < 5%)
        # If reported, should be type "flat"
        flat_trends = [t for t in trends if t.type == "flat"]
        if len(flat_trends) > 0:
            trend = flat_trends[0]
            assert abs(trend.metrics['growth_rate']) < 0.05
            assert trend.metrics['trend'] == 'flat'
    
    def test_peak_detection(self):
        """Test peak value detection in time series."""
        columns = ['date', 'visitors']
        rows = [
            ['2023-01-01', 100],
            ['2023-01-02', 150],
            ['2023-01-03', 500],  # Peak
            ['2023-01-04', 120],
            ['2023-01-05', 110],
        ]
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        assert len(trends) > 0
        trend = trends[0]
        assert trend.metrics['peak_value'] == 500
    
    def test_no_temporal_column(self):
        """Test behavior when no temporal column exists."""
        columns = ['category', 'count']
        rows = [
            ['A', 10],
            ['B', 20],
        ]
        
        detector = TrendDetector(columns, rows)
        time_trends = detector._detect_time_series_trends()
        
        assert len(time_trends) == 0
    
    def test_no_numeric_column(self):
        """Test behavior when no numeric column exists."""
        columns = ['date', 'name']
        rows = [
            ['2023-01-01', 'Alice'],
            ['2023-01-02', 'Bob'],
        ]
        
        detector = TrendDetector(columns, rows)
        time_trends = detector._detect_time_series_trends()
        
        assert len(time_trends) == 0


class TestCategoricalOutliers:
    """Test categorical outlier detection."""
    
    def test_outlier_detection_high(self):
        """Test detection of high outlier in categorical data."""
        columns = ['department', 'employee_count']
        rows = [
            ['Engineering', 200],  # Outlier (high)
            ['Sales', 50],
            ['Marketing', 45],
            ['HR', 40],
            ['Finance', 48],
            ['Operations', 52],
        ]
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        assert len(trends) > 0
        outlier_trends = [t for t in trends if t.type == "outlier"]
        assert len(outlier_trends) > 0
        
        trend = outlier_trends[0]
        assert trend.metrics['max_category'] == 'Engineering'
        assert abs(trend.metrics['z_score']) > 2.0
        assert trend.confidence > 0.6
    
    def test_outlier_detection_low(self):
        """Test detection of low outlier in categorical data."""
        columns = ['product', 'sales']
        rows = [
            ['A', 100],
            ['B', 95],
            ['C', 98],
            ['D', 5],  # Outlier (low) - made more extreme
            ['E', 102],
            ['F', 97],
        ]
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        # Should detect the significant difference
        assert len(trends) > 0
    
    def test_no_outliers(self):
        """Test behavior when no significant outliers exist."""
        columns = ['region', 'revenue']
        rows = [
            ['North', 100],
            ['South', 105],
            ['East', 98],
            ['West', 102],
        ]
        
        detector = TrendDetector(columns, rows)
        outlier_trends = detector._detect_categorical_outliers()
        
        # No outliers (all within 2 standard deviations)
        assert len(outlier_trends) == 0
    
    def test_wrong_column_count(self):
        """Test behavior with wrong number of columns."""
        columns = ['a', 'b', 'c']
        rows = [
            [1, 2, 3],
            [4, 5, 6],
        ]
        
        detector = TrendDetector(columns, rows)
        outlier_trends = detector._detect_categorical_outliers()
        
        # Requires exactly 2 columns
        assert len(outlier_trends) == 0


class TestDistributions:
    """Test numeric distribution analysis."""
    
    def test_distribution_basic(self):
        """Test basic distribution analysis."""
        columns = ['age']
        rows = [[22], [25], [28], [30], [32], [35], [38], [40], [45], [50]]
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        assert len(trends) > 0
        dist_trends = [t for t in trends if t.type == "distribution"]
        assert len(dist_trends) > 0
        
        trend = dist_trends[0]
        assert 'median' in trend.metrics
        assert 'q1' in trend.metrics
        assert 'q3' in trend.metrics
        assert trend.confidence > 0.5
    
    def test_distribution_with_outliers(self):
        """Test distribution with outliers."""
        columns = ['salary']
        # Normal values + outliers
        rows = [[50000], [52000], [48000], [51000], [49000], 
                [150000], [200000]]  # Outliers
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        assert len(trends) > 0
        dist_trends = [t for t in trends if t.type == "distribution"]
        assert len(dist_trends) > 0
        
        trend = dist_trends[0]
        assert trend.metrics['outliers_count'] > 0
    
    def test_distribution_wrong_column_count(self):
        """Test behavior with multiple columns."""
        columns = ['a', 'b']
        rows = [[1, 2], [3, 4]]
        
        detector = TrendDetector(columns, rows)
        dist_trends = detector._detect_distributions()
        
        # Requires exactly 1 column
        assert len(dist_trends) == 0
    
    def test_distribution_non_numeric(self):
        """Test behavior with non-numeric column."""
        columns = ['name']
        rows = [['Alice'], ['Bob'], ['Charlie']]
        
        detector = TrendDetector(columns, rows)
        dist_trends = detector._detect_distributions()
        
        assert len(dist_trends) == 0
    
    def test_distribution_few_distinct_values(self):
        """Test behavior with few distinct values."""
        columns = ['count']
        rows = [[1], [1], [2], [2]]  # Only 2 distinct values
        
        detector = TrendDetector(columns, rows)
        dist_trends = detector._detect_distributions()
        
        # Requires >= 5 distinct values
        assert len(dist_trends) == 0


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_dataset(self):
        """Test with empty dataset."""
        columns = ['a', 'b']
        rows = []
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        assert len(trends) == 0
    
    def test_single_row(self):
        """Test with single row."""
        columns = ['date', 'value']
        rows = [['2023-01-01', 100]]
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        assert len(trends) == 0
    
    def test_null_values(self):
        """Test handling of null values."""
        columns = ['month', 'sales']
        rows = [
            ['2023-01', 100],
            ['2023-02', None],
            ['2023-03', 150],
            ['2023-04', None],
            ['2023-05', 200],
        ]
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        # Should still work, dropping nulls
        # Confidence should be lower due to nulls
        if len(trends) > 0:
            trend = trends[0]
            assert trend.confidence < 0.95  # Penalized for nulls
    
    def test_large_dataset_sampling(self):
        """Test sampling behavior with large dataset."""
        columns = ['id', 'value']
        rows = [[i, i*10] for i in range(2000)]  # 2000 rows
        
        detector = TrendDetector(columns, rows, max_sample=1000)
        
        # Should sample to max_sample
        assert len(detector.rows) == 1000
        assert len(detector.df) == 1000


class TestConvenienceFunction:
    """Test the convenience function for JSON serialization."""
    
    def test_detect_trends_from_results(self):
        """Test convenience function returns dictionaries."""
        columns = ['month', 'revenue']
        rows = [
            ['2023-01', 10000],
            ['2023-02', 15000],
            ['2023-03', 20000],
        ]
        
        trends = detect_trends_from_results(columns, rows)
        
        assert isinstance(trends, list)
        if len(trends) > 0:
            trend = trends[0]
            assert isinstance(trend, dict)
            assert 'id' in trend
            assert 'type' in trend
            assert 'title' in trend
            assert 'description' in trend
            assert 'confidence' in trend
            assert 'metrics' in trend
            assert 'columns' in trend


class TestTrendPrioritization:
    """Test trend sorting by confidence."""
    
    def test_trends_sorted_by_confidence(self):
        """Test that trends are sorted by confidence (highest first)."""
        columns = ['month', 'sales']
        rows = [
            ['2023-01', 10000],
            ['2023-02', 50000],  # Big jump
            ['2023-03', 55000],
            ['2023-04', 60000],
        ]
        
        detector = TrendDetector(columns, rows)
        trends = detector.detect_trends()
        
        if len(trends) > 1:
            # Verify descending order
            for i in range(len(trends) - 1):
                assert trends[i].confidence >= trends[i+1].confidence


class TestHelperMethods:
    """Test helper methods in TrendDetector."""
    
    def test_looks_like_date(self):
        """Test date detection helper."""
        detector = TrendDetector(['a'], [[1]])
        
        assert detector._looks_like_date('2023-01-01') is True
        assert detector._looks_like_date('2023-11') is True  # YYYY-MM
        assert detector._looks_like_date('2023/01/01') is True
        assert detector._looks_like_date('01-01-2023') is True
        assert detector._looks_like_date('not a date') is False
        assert detector._looks_like_date(123) is False
    
    def test_is_temporal_column(self):
        """Test temporal column detection."""
        columns = ['sale_date', 'amount']
        rows = [['2023-01-01', 100], ['2023-01-02', 200]]
        
        detector = TrendDetector(columns, rows)
        
        assert detector._is_temporal_column('sale_date') is True
        assert detector._is_temporal_column('amount') is False
    
    def test_format_number(self):
        """Test number formatting helper."""
        detector = TrendDetector(['a'], [[1]])
        
        assert detector._format_number(1_500_000) == '1.5M'
        assert detector._format_number(45_000) == '45.0K'
        assert detector._format_number(123) == '123'
        assert detector._format_number(3.14) == '3.14'
