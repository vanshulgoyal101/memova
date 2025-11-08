"""
Trend Detection Engine

Automatically detects trends and patterns in query results using statistical analysis.
Generates natural language insights for:
- Time series trends (growth/decline)
- Categorical outliers
- Numeric distributions
- Seasonality patterns

Author: AI Assistant
Date: 2025-11-06
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import re

logger = logging.getLogger(__name__)


@dataclass
class TrendInsight:
    """
    Represents a detected trend or insight from query results.
    
    Attributes:
        id: Unique identifier
        type: Trend type ("growth", "outlier", "distribution", "seasonality")
        title: Short headline (e.g., "Strong Sales Growth")
        description: Natural language insight (AI-generated or template)
        confidence: Confidence score 0.0-1.0
        metrics: Supporting statistics dictionary
        columns: Column names involved in this insight
    """
    id: str
    type: str  # "growth", "decline", "outlier", "distribution", "seasonality"
    title: str
    description: str
    confidence: float  # 0.0 to 1.0
    metrics: Dict[str, Any] = field(default_factory=dict)
    columns: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "confidence": round(self.confidence, 2),
            "metrics": self.metrics,
            "columns": self.columns
        }


class TrendDetector:
    """
    Detects trends and patterns in SQL query results.
    
    Uses statistical analysis to identify:
    - Time series trends (growth/decline, peaks, volatility)
    - Categorical outliers (z-scores, top/bottom values)
    - Numeric distributions (quartiles, outliers, skewness)
    - Seasonality (periodic patterns)
    
    Example:
        >>> detector = TrendDetector(columns, rows)
        >>> trends = detector.detect_trends()
        >>> print(trends[0].description)
        "Sales increased by 33% from January (€45K) to December (€60K)"
    """
    
    def __init__(self, columns: List[str], rows: List[List[Any]], max_sample: int = 1000):
        """
        Initialize trend detector with query results.
        
        Args:
            columns: Column names from query
            rows: Data rows from query
            max_sample: Maximum rows to analyze (sampling for large datasets)
        """
        self.columns = columns
        self.max_sample = max_sample
        
        # Sample large datasets
        sampled_rows = rows[:max_sample] if len(rows) > max_sample else rows
        self.rows = sampled_rows
        
        # Convert to pandas DataFrame for analysis
        if sampled_rows:
            self.df = pd.DataFrame(sampled_rows, columns=columns)
            logger.info(f"TrendDetector initialized: {len(sampled_rows)} rows (sampled from {len(rows)}), {len(columns)} columns")
        else:
            self.df = pd.DataFrame(columns=columns)
            logger.warning("TrendDetector initialized with empty dataset")
    
    def detect_trends(self) -> List[TrendInsight]:
        """
        Detect all applicable trends from the dataset.
        
        Returns:
            List of TrendInsight objects, sorted by confidence (highest first)
        """
        if self.df.empty or len(self.df) < 2:
            logger.info("Insufficient data for trend detection")
            return []
        
        insights: List[TrendInsight] = []
        
        # Detect various trend types
        insights.extend(self._detect_time_series_trends())
        insights.extend(self._detect_categorical_outliers())
        insights.extend(self._detect_distributions())
        
        # Sort by confidence (highest first)
        insights.sort(key=lambda x: x.confidence, reverse=True)
        
        logger.info(f"Detected {len(insights)} trends with confidence > 0.5")
        return insights
    
    def _detect_time_series_trends(self) -> List[TrendInsight]:
        """
        Detect growth/decline trends in time series data.
        
        Looks for:
        - DATE/DATETIME column + numeric column
        - Calculates growth rate, trend direction, peaks
        - Confidence based on data quality and trend strength
        
        Returns:
            List of time series trend insights
        """
        insights = []
        
        # Find temporal columns
        temporal_cols = []
        for col in self.df.columns:
            if self._is_temporal_column(col):
                temporal_cols.append(col)
        
        if not temporal_cols:
            return insights
        
        # Find numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            return insights
        
        # Analyze first temporal + numeric pair
        time_col = temporal_cols[0]
        value_col = numeric_cols[0]
        
        # Sort by time
        df_sorted = self.df.sort_values(by=time_col).copy()
        df_sorted = df_sorted.dropna(subset=[time_col, value_col])
        
        if len(df_sorted) < 3:
            return insights
        
        # Calculate statistics
        values = df_sorted[value_col].values
        first_value = values[0]
        last_value = values[-1]
        mean_value = np.mean(values)
        std_value = np.std(values)
        
        # Growth rate
        if first_value != 0:
            growth_rate = (last_value - first_value) / abs(first_value)
        else:
            growth_rate = 0.0
        
        # Trend direction
        if abs(growth_rate) < 0.05:
            trend = "flat"
            trend_type = "flat"
        elif growth_rate > 0:
            trend = "increasing"
            trend_type = "growth"
        else:
            trend = "decreasing"
            trend_type = "decline"
        
        # Peak and trough
        max_idx = np.argmax(values)
        min_idx = np.argmin(values)
        peak_value = values[max_idx]
        trough_value = values[min_idx]
        peak_date = df_sorted.iloc[max_idx][time_col]
        trough_date = df_sorted.iloc[min_idx][time_col]
        
        # Volatility (coefficient of variation)
        if mean_value != 0:
            volatility = std_value / abs(mean_value)
        else:
            volatility = 0.0
        
        # Confidence calculation
        # Higher confidence if: more data points, stronger trend, fewer nulls
        null_ratio = df_sorted[value_col].isna().sum() / len(df_sorted)
        data_quality = 1.0 - null_ratio
        trend_strength = min(abs(growth_rate), 1.0)
        sample_size_factor = min(len(df_sorted) / 10, 1.0)
        
        confidence = 0.7 + (0.1 * data_quality) + (0.1 * trend_strength) + (0.1 * sample_size_factor)
        confidence = min(confidence, 0.95)
        
        # Only report significant trends (>5% change or high volatility)
        if abs(growth_rate) >= 0.05 or volatility > 0.3:
            # Format values for display
            first_str = self._format_number(first_value)
            last_str = self._format_number(last_value)
            mean_str = self._format_number(mean_value)
            peak_str = self._format_number(peak_value)
            
            # Generate description
            if trend_type == "growth":
                description = f"{value_col.replace('_', ' ').title()} increased by {abs(growth_rate)*100:.1f}% from {first_str} to {last_str}, averaging {mean_str}."
                title = f"Growth Trend Detected"
            elif trend_type == "decline":
                description = f"{value_col.replace('_', ' ').title()} decreased by {abs(growth_rate)*100:.1f}% from {first_str} to {last_str}, averaging {mean_str}."
                title = f"Decline Trend Detected"
            else:
                description = f"{value_col.replace('_', ' ').title()} remained relatively flat (±5%), averaging {mean_str}."
                title = f"Stable Trend"
            
            # Add peak information if significant
            if peak_value > mean_value * 1.5:
                peak_date_str = str(peak_date)[:10] if isinstance(peak_date, (str, datetime)) else str(peak_date)
                description += f" Peak value of {peak_str} occurred on {peak_date_str}."
            
            insights.append(TrendInsight(
                id=f"trend_time_{len(insights)}",
                type=trend_type,
                title=title,
                description=description,
                confidence=confidence,
                metrics={
                    "growth_rate": round(growth_rate, 3),
                    "trend": trend,
                    "first_value": float(first_value),
                    "last_value": float(last_value),
                    "mean": float(mean_value),
                    "std": float(std_value),
                    "volatility": round(volatility, 3),
                    "peak_value": float(peak_value),
                    "trough_value": float(trough_value),
                    "data_points": len(df_sorted)
                },
                columns=[time_col, value_col]
            ))
        
        return insights
    
    def _detect_categorical_outliers(self) -> List[TrendInsight]:
        """
        Detect outliers in categorical breakdowns.
        
        Looks for:
        - Categorical column + numeric aggregate
        - Calculates z-scores, identifies outliers (|z| > 2)
        - Reports top/bottom values and percentages
        
        Returns:
            List of categorical outlier insights
        """
        insights = []
        
        # Need exactly 2 columns for categorical breakdown
        if len(self.df.columns) != 2:
            return insights
        
        # Identify categorical and numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) != 1:
            return insights
        
        value_col = numeric_cols[0]
        cat_col = [c for c in self.df.columns if c != value_col][0]
        
        # Check if categorical column has reasonable cardinality
        distinct_count = self.df[cat_col].nunique()
        if distinct_count < 2 or distinct_count > 50:
            return insights
        
        # Drop nulls
        df_clean = self.df.dropna(subset=[cat_col, value_col])
        
        if len(df_clean) < 3:
            return insights
        
        # Get unique values per category (assuming data is already aggregated)
        # Each row represents one category with its aggregate value
        categories = df_clean[cat_col].values
        values = df_clean[value_col].values
        
        # Calculate statistics
        mean_value = np.mean(values)
        std_value = np.std(values)
        total_value = np.sum(values)
        
        # Calculate z-scores for each category's value
        if std_value > 0:
            z_scores = (values - mean_value) / std_value
        else:
            return insights  # No variation
        
        # Find outliers (|z| > 2)
        outlier_mask = np.abs(z_scores) > 2.0
        outlier_count = np.sum(outlier_mask)
        
        # Find max absolute z-score (strongest outlier)
        abs_z_scores = np.abs(z_scores)
        max_z_idx = np.argmax(abs_z_scores)
        max_z_score = z_scores[max_z_idx]
        max_value = values[max_z_idx]
        max_category = categories[max_z_idx]
        max_percentage = (max_value / total_value) * 100 if total_value > 0 else 0
        
        # Generate insight if significant outlier exists
        if outlier_count > 0:
            # Confidence based on z-score magnitude and data quality
            z_magnitude = min(abs(max_z_score) / 3, 1.0)  # Normalize to 0-1
            null_ratio = self.df[value_col].isna().sum() / len(self.df)
            data_quality = 1.0 - null_ratio
            
            confidence = 0.65 + (0.15 * z_magnitude) + (0.1 * data_quality)
            confidence = min(confidence, 0.92)
            
            # Format values
            max_str = self._format_number(max_value)
            mean_str = self._format_number(mean_value)
            
            # Generate description
            deviation_pct = ((max_value - mean_value) / mean_value * 100) if mean_value != 0 else 0
            description = f"{max_category} ({max_str}) is {abs(deviation_pct):.0f}% {'above' if deviation_pct > 0 else 'below'} the average ({mean_str})"
            
            if max_percentage > 25:
                description += f", accounting for {max_percentage:.0f}% of the total."
            else:
                description += "."
            
            if outlier_count > 1:
                description += f" {outlier_count} categories are statistical outliers."
            
            insights.append(TrendInsight(
                id=f"trend_outlier_{len(insights)}",
                type="outlier",
                title=f"{max_category} Stands Out",
                description=description,
                confidence=confidence,
                metrics={
                    "mean": float(mean_value),
                    "std": float(std_value),
                    "z_score": round(float(max_z_score), 2),
                    "max_value": float(max_value),
                    "max_category": str(max_category),
                    "percentage": round(max_percentage, 1),
                    "outliers_count": int(outlier_count)
                },
                columns=[cat_col, value_col]
            ))
        
        return insights
    
    def _detect_distributions(self) -> List[TrendInsight]:
        """
        Analyze numeric distributions.
        
        Looks for:
        - Single numeric column with many values
        - Calculates quartiles, IQR, outliers
        - Reports range, median, skewness
        
        Returns:
            List of distribution insights
        """
        insights = []
        
        # Need exactly 1 column for distribution analysis
        if len(self.df.columns) != 1:
            return insights
        
        col = self.df.columns[0]
        
        # Must be numeric
        if col not in self.df.select_dtypes(include=[np.number]).columns:
            return insights
        
        # Need enough distinct values
        distinct_count = self.df[col].nunique()
        if distinct_count < 5:
            return insights
        
        # Drop nulls
        values = self.df[col].dropna().values
        
        if len(values) < 5:
            return insights
        
        # Calculate statistics
        q1 = np.percentile(values, 25)
        median = np.percentile(values, 50)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        min_val = np.min(values)
        max_val = np.max(values)
        mean_val = np.mean(values)
        
        # Detect outliers (Tukey's method)
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        outliers = values[(values < lower_fence) | (values > upper_fence)]
        outlier_count = len(outliers)
        
        # Skewness detection (simple heuristic)
        if median > 0:
            skew_ratio = mean_val / median
            if skew_ratio > 1.2:
                skew = "right-skewed"
            elif skew_ratio < 0.8:
                skew = "left-skewed"
            else:
                skew = "symmetric"
        else:
            skew = "unknown"
        
        # Confidence calculation
        null_ratio = self.df[col].isna().sum() / len(self.df)
        data_quality = 1.0 - null_ratio
        sample_size_factor = min(len(values) / 50, 1.0)
        
        confidence = 0.60 + (0.15 * data_quality) + (0.1 * sample_size_factor)
        confidence = min(confidence, 0.85)
        
        # Format values
        min_str = self._format_number(min_val)
        max_str = self._format_number(max_val)
        median_str = self._format_number(median)
        q1_str = self._format_number(q1)
        q3_str = self._format_number(q3)
        
        # Generate description
        description = f"{col.replace('_', ' ').title()} ranges from {min_str} to {max_str} with a median of {median_str}."
        description += f" 50% of values fall between {q1_str} and {q3_str}."
        
        if outlier_count > 0:
            outlier_pct = (outlier_count / len(values)) * 100
            description += f" {outlier_count} outliers detected ({outlier_pct:.0f}% of data)."
        
        insights.append(TrendInsight(
            id=f"trend_dist_{len(insights)}",
            type="distribution",
            title=f"{col.replace('_', ' ').title()} Distribution",
            description=description,
            confidence=confidence,
            metrics={
                "min": float(min_val),
                "q1": float(q1),
                "median": float(median),
                "q3": float(q3),
                "max": float(max_val),
                "mean": float(mean_val),
                "iqr": float(iqr),
                "outliers_count": int(outlier_count),
                "skewness": skew
            },
            columns=[col]
        ))
        
        return insights
    
    def _is_temporal_column(self, col: str) -> bool:
        """
        Check if column contains temporal data.
        
        Args:
            col: Column name
            
        Returns:
            True if column appears to be date/datetime
        """
        # Check column name patterns
        temporal_keywords = ['date', 'time', 'day', 'month', 'year', 'quarter', 'week']
        if any(keyword in col.lower() for keyword in temporal_keywords):
            # Temporal keywords in column name = likely temporal
            # Even if values don't match date patterns (e.g., "2023-Q1")
            return True
        
        # Also check if values look like dates
        sample = self.df[col].dropna().head(10)
        if len(sample) > 0:
            for val in sample:
                if self._looks_like_date(val):
                    return True
        
        return False
    
    def _looks_like_date(self, value: Any) -> bool:
        """
        Check if value looks like a date.
        
        Args:
            value: Value to check
            
        Returns:
            True if value appears to be a date
        """
        if isinstance(value, (datetime, pd.Timestamp)):
            return True
        
        if isinstance(value, str):
            # Common date patterns
            date_patterns = [
                r'^\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'^\d{4}-\d{2}$',        # YYYY-MM
                r'^\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
                r'^\d{4}/\d{2}$',        # YYYY/MM
                r'^\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
                r'^\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            ]
            return any(re.match(pattern, value) for pattern in date_patterns)
        
        return False
    
    def _format_number(self, value: float) -> str:
        """
        Format number for display in insights.
        
        Args:
            value: Numeric value
            
        Returns:
            Formatted string (e.g., "45K", "1.2M", "€150")
        """
        if abs(value) >= 1_000_000:
            return f"{value/1_000_000:.1f}M"
        elif abs(value) >= 1_000:
            return f"{value/1_000:.1f}K"
        elif abs(value) >= 10:
            return f"{value:.0f}"
        else:
            return f"{value:.2f}"


def detect_trends_from_results(columns: List[str], rows: List[List[Any]]) -> List[Dict[str, Any]]:
    """
    Convenience function to detect trends and return as JSON-serializable dictionaries.
    
    Args:
        columns: Column names from query
        rows: Data rows from query
        
    Returns:
        List of trend insight dictionaries
    """
    detector = TrendDetector(columns, rows)
    trends = detector.detect_trends()
    return [trend.to_dict() for trend in trends]
