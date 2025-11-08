"""
Chart detection engine for automatic visualization.

Analyzes SQL query results and detects chartable patterns:
- Time series (line charts)
- Categorical aggregations (bar/pie charts)
- Numeric distributions (histograms)

Uses AI-powered selection by default, falls back to heuristics if AI unavailable.

Author: Context Engineering
Created: 2025-11-06
Updated: 2025-11-07 (Added date gap filling for time series)
"""

from typing import List, Dict, Optional, Any, Literal
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import re
import logging

logger = logging.getLogger(__name__)

ChartType = Literal[
    "line",           # Time series trends
    "bar",            # Vertical bar chart
    "horizontal_bar", # Horizontal bar (better for long labels)
    "pie",            # Pie chart (≤ 6 categories)
    "doughnut",       # Doughnut chart (≤ 8 categories, more modern)
    "histogram",      # Distribution
    "area",           # Filled area chart
    "stacked_bar",    # Stacked vertical bars
    "stacked_area",   # Stacked area chart
    "grouped_bar",    # Grouped vertical bars
    "combo",          # Mixed bar + line
    "scatter",        # Scatter plot for correlations
    "bubble",         # Bubble chart (3 dimensions)
    "heatmap",        # Heatmap for matrix data
    "none"            # No chart recommended
]


@dataclass
class ColumnMetadata:
    """Metadata for a single column in the result set."""
    
    name: str
    index: int
    inferred_type: str  # "date", "datetime", "numeric", "categorical", "text"
    sample_values: List[Any]
    distinct_count: int
    null_count: int
    
    def is_temporal(self) -> bool:
        """Check if column is date/datetime."""
        return self.inferred_type in ("date", "datetime")
    
    def is_numeric(self) -> bool:
        """Check if column is numeric."""
        return self.inferred_type == "numeric"
    
    def is_categorical(self) -> bool:
        """Check if column is categorical (low cardinality)."""
        return self.inferred_type == "categorical"


@dataclass
class ChartConfig:
    """Configuration for a single chart."""
    
    id: str
    type: ChartType
    title: str
    x_column: str
    y_columns: List[str]
    data: List[Dict[str, Any]]
    x_type: str  # "date", "category", "numeric"
    confidence: float  # 0.0 - 1.0 (how confident we are in this chart suggestion)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return asdict(self)


class ChartDetector:
    """
    Detects chartable patterns in query results.
    
    Uses AI-powered chart selection by default for intelligent recommendations.
    Falls back to heuristic-based detection if AI unavailable.
    
    Usage:
        detector = ChartDetector(columns, rows, question="Compare top vs bottom products")
        charts = detector.detect_charts(use_ai=True)
    """
    
    def __init__(
        self, 
        columns: List[str], 
        rows: List[List[Any]], 
        question: Optional[str] = None,
        max_sample: int = 1000
    ):
        """
        Initialize chart detector.
        
        Args:
            columns: List of column names
            rows: List of rows (each row is a list of values)
            question: User's original question (provides context for AI)
            max_sample: Maximum rows to analyze (default 1000)
        """
        self.columns = columns
        self.rows = rows[:max_sample]  # Limit analysis to max_sample rows
        self.row_count = len(self.rows)
        self.question = question
        self.column_metadata: List[ColumnMetadata] = []
        
        if self.row_count > 0:
            self._analyze_columns()
    
    def _analyze_columns(self) -> None:
        """Analyze each column to infer types and metadata."""
        for idx, col_name in enumerate(self.columns):
            values = [row[idx] for row in self.rows if row[idx] is not None]
            null_count = self.row_count - len(values)
            
            # Sample up to 100 values for analysis
            sample_values = values[:100]
            distinct_count = len(set(values))
            
            # Infer type
            inferred_type = self._infer_column_type(values, distinct_count)
            
            self.column_metadata.append(ColumnMetadata(
                name=col_name,
                index=idx,
                inferred_type=inferred_type,
                sample_values=sample_values,
                distinct_count=distinct_count,
                null_count=null_count
            ))
    
    def _infer_column_type(self, values: List[Any], distinct_count: int) -> str:
        """
        Infer column type from sample values.
        
        Returns: "date", "datetime", "numeric", "categorical", "text"
        """
        if not values:
            return "text"
        
        sample = values[:50]
        sample_size = len(sample)
        
        # Check for numeric
        numeric_count = sum(1 for v in sample if isinstance(v, (int, float)))
        if numeric_count / sample_size > 0.9:
            return "numeric"
        
        # Check for date/datetime (must check before categorical)
        date_count = 0
        datetime_count = 0
        for v in sample:
            if isinstance(v, str):
                if self._looks_like_datetime(v):
                    datetime_count += 1
                    date_count += 1
                elif self._looks_like_date(v):
                    date_count += 1
        
        if date_count / sample_size > 0.8:
            # Distinguish date vs datetime
            if datetime_count / sample_size > 0.5:
                return "datetime"
            return "date"
        
        # Check for categorical (low cardinality)
        # More lenient for small datasets
        max_categories = max(20, int(len(values) * 0.3))
        if distinct_count <= min(max_categories, 50):
            return "categorical"
        
        return "text"
    
    def _looks_like_date(self, value: str) -> bool:
        """Check if string looks like a date."""
        if not isinstance(value, str):
            return False
        
        # Common date patterns
        patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{4}-\d{2}$',        # YYYY-MM (month aggregations)
            r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
            r'^\d{4}/\d{2}$',        # YYYY/MM (month aggregations)
            r'^\d{2}-\d{2}-\d{4}$',  # DD-MM-YYYY
            r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
        ]
        
        return any(re.match(pattern, value.strip()) for pattern in patterns)
    
    def _looks_like_datetime(self, value: str) -> bool:
        """Check if string looks like a datetime."""
        if not isinstance(value, str):
            return False
        
        # Contains time component (ISO format or space-separated)
        value = value.strip()
        return ('T' in value and ':' in value) or (' ' in value and ':' in value and len(value) > 10)
    
    def detect_charts(self, use_ai: bool = True) -> List[ChartConfig]:
        """
        Detect all possible charts from the result set.
        
        Args:
            use_ai: Use AI-powered chart selection (default True)
        
        Returns:
            List of ChartConfig objects (may be empty if no charts detected)
        """
        if self.row_count == 0:
            logger.info("Empty result set - no charts to detect")
            return []
        
        # Try AI-powered selection first (if enabled)
        if use_ai:
            try:
                from src.core.ai_chart_selector import AIChartSelector
                
                selector = AIChartSelector()
                ai_chart = selector.select_chart(
                    columns=self.columns,
                    rows=self.rows,
                    column_metadata=self.column_metadata,
                    question=self.question
                )
                
                if ai_chart:
                    logger.info(f"AI selected {ai_chart.type} chart (confidence: {ai_chart.confidence:.0%})")
                    return [ai_chart]
                else:
                    logger.info("AI recommended no chart, falling back to heuristics")
            except Exception as e:
                logger.warning(f"AI chart selection failed, falling back to heuristics: {e}")
        
        # Fallback: Use heuristic-based detection
        logger.info("Using heuristic-based chart detection")
        charts = []
        
        # Heuristic 1: Time Series (line chart)
        time_series = self._detect_time_series()
        if time_series:
            charts.append(time_series)
        
        # Heuristic 2: Multi-Series Line Chart
        multi_series = self._detect_multi_series_line()
        if multi_series:
            charts.append(multi_series)
        
        # Heuristic 3: Stacked Bar Chart
        stacked_bar = self._detect_stacked_bar()
        if stacked_bar:
            charts.append(stacked_bar)
        
        # Heuristic 4: Area Chart
        area_chart = self._detect_area_chart()
        if area_chart:
            charts.append(area_chart)
        
        # Heuristic 5: Combo Chart
        combo_chart = self._detect_combo_chart()
        if combo_chart:
            charts.append(combo_chart)
        
        # Heuristic 6: Categorical Breakdown (bar/pie chart)
        categorical = self._detect_categorical_breakdown()
        if categorical:
            charts.append(categorical)
        
        # Heuristic 7: Numeric Distribution (histogram)
        histogram = self._detect_histogram()
        if histogram:
            charts.append(histogram)
        
        # Sort by confidence (highest first)
        charts.sort(key=lambda c: c.confidence, reverse=True)
        
        logger.info(f"Detected {len(charts)} chart(s) from {self.row_count} rows")
        return charts
    
    def _fill_date_gaps(
        self, 
        data: List[Dict[str, Any]], 
        date_column: str,
        value_columns: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Fill gaps in time series data with null values for smooth plotting.
        
        Detects date granularity (daily/weekly/monthly) and fills missing dates.
        
        Args:
            data: List of data points
            date_column: Name of the date column
            value_columns: Names of value columns to preserve
            
        Returns:
            Data with gaps filled (missing dates have null values)
        """
        if not data or len(data) < 2:
            return data
        
        # Parse dates and determine format
        date_values = []
        date_format = None
        
        for point in data:
            date_str = point.get(date_column)
            if not date_str:
                continue
            
            try:
                # Try different date formats
                if re.match(r'^\d{4}-\d{2}-\d{2}$', str(date_str)):
                    date_obj = datetime.strptime(str(date_str), '%Y-%m-%d')
                    date_format = '%Y-%m-%d'
                elif re.match(r'^\d{4}-\d{2}$', str(date_str)):
                    date_obj = datetime.strptime(str(date_str), '%Y-%m')
                    date_format = '%Y-%m'
                elif re.match(r'^\d{4}/\d{2}/\d{2}$', str(date_str)):
                    date_obj = datetime.strptime(str(date_str), '%Y/%m/%d')
                    date_format = '%Y/%m/%d'
                elif re.match(r'^\d{4}/\d{2}$', str(date_str)):
                    date_obj = datetime.strptime(str(date_str), '%Y/%m')
                    date_format = '%Y/%m'
                else:
                    # Try ISO format
                    date_obj = datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
                    date_format = 'iso'
                
                date_values.append((date_obj, point))
            except (ValueError, TypeError):
                logger.warning(f"Could not parse date: {date_str}")
                continue
        
        if len(date_values) < 2:
            return data
        
        # Sort by date
        date_values.sort(key=lambda x: x[0])
        
        # Detect granularity (daily, weekly, monthly)
        first_date, _ = date_values[0]
        second_date, _ = date_values[1]
        gap_days = (second_date - first_date).days
        
        if gap_days <= 1:
            delta = timedelta(days=1)
            granularity = "daily"
        elif gap_days <= 7:
            delta = timedelta(days=7)
            granularity = "weekly"
        elif gap_days <= 31:
            # Monthly - handled differently
            granularity = "monthly"
            delta = None
        else:
            # Large gaps - don't fill
            logger.info(f"Date gaps too large ({gap_days} days), skipping gap filling")
            return data
        
        # Fill gaps
        filled_data = []
        current_date = date_values[0][0]
        end_date = date_values[-1][0]
        
        # Create lookup dict of existing data
        data_lookup = {date_obj: point for date_obj, point in date_values}
        
        while current_date <= end_date:
            if current_date in data_lookup:
                # Existing data point
                filled_data.append(data_lookup[current_date])
            else:
                # Missing data point - create null entry
                null_point = {date_column: current_date.strftime(date_format) if date_format != 'iso' else current_date.isoformat()}
                for col in value_columns:
                    null_point[col] = None
                filled_data.append(null_point)
            
            # Move to next date
            if granularity == "monthly":
                # Handle month increment
                month = current_date.month
                year = current_date.year
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1
                current_date = current_date.replace(year=year, month=month, day=1)
            else:
                current_date += delta
        
        logger.info(f"Filled {len(filled_data) - len(data)} date gaps ({granularity} granularity)")
        return filled_data
    
    def _detect_time_series(self) -> Optional[ChartConfig]:
        """
        Detect time series pattern: temporal column + numeric column(s).
        
        Fills date gaps for smooth daily/weekly/monthly visualizations.
        
        Returns:
            ChartConfig for line chart or None
        """
        temporal_cols = [col for col in self.column_metadata if col.is_temporal()]
        numeric_cols = [col for col in self.column_metadata if col.is_numeric()]
        
        if not temporal_cols or not numeric_cols:
            return None
        
        # Use first temporal column as x-axis
        x_col = temporal_cols[0]
        
        # Use all numeric columns as y-axes (multi-series)
        y_cols = numeric_cols[:3]  # Limit to 3 series for readability
        
        # Build data array
        data = []
        for row in self.rows:
            point = {x_col.name: row[x_col.index]}
            for y_col in y_cols:
                point[y_col.name] = row[y_col.index]
            data.append(point)
        
        # Fill date gaps for smooth time series
        data = self._fill_date_gaps(data, x_col.name, [c.name for c in y_cols])
        
        # Confidence based on data quality
        confidence = 0.9 if x_col.null_count == 0 else 0.7
        
        return ChartConfig(
            id="chart_timeseries",
            type="line",
            title=f"{', '.join(c.name for c in y_cols)} over {x_col.name}",
            x_column=x_col.name,
            y_columns=[c.name for c in y_cols],
            data=data,
            x_type="date",
            confidence=confidence
        )
    
    def _detect_categorical_breakdown(self) -> Optional[ChartConfig]:
        """
        Detect categorical breakdown: categorical column + numeric aggregate.
        
        For readability, limits bar charts to top 15 items when there are many categories.
        
        Returns:
            ChartConfig for bar or pie chart or None
        """
        categorical_cols = [col for col in self.column_metadata if col.is_categorical()]
        numeric_cols = [col for col in self.column_metadata if col.is_numeric()]
        
        if not categorical_cols or not numeric_cols:
            return None
        
        # Use first categorical as x, first numeric as y
        x_col = categorical_cols[0]
        y_col = numeric_cols[0]
        
        # Build data array
        data = []
        for row in self.rows:
            data.append({
                x_col.name: row[x_col.index],
                y_col.name: row[y_col.index]
            })
        
        # For readability: limit bar charts to top 15 items when there are many categories
        MAX_BAR_ITEMS = 15
        original_count = len(data)
        
        if len(data) > MAX_BAR_ITEMS:
            # Sort by numeric value (descending) and take top N
            data = sorted(data, key=lambda x: x[y_col.name] or 0, reverse=True)[:MAX_BAR_ITEMS]
            logger.info(f"Limited chart from {original_count} to {MAX_BAR_ITEMS} items (showing top values)")
        
        # Smart chart type selection based on data characteristics
        num_items = len(data)
        
        # Check if labels are long (average > 15 chars)
        avg_label_length = sum(len(str(row[x_col.name])) for row in data) / num_items if data else 0
        
        if num_items <= 6:
            # Small datasets: doughnut chart (modern, clean)
            chart_type: ChartType = "doughnut"
            confidence = 0.9
        elif num_items <= 10 and avg_label_length < 15:
            # Medium datasets with short labels: vertical bar
            chart_type = "bar"
            confidence = 0.85
        elif num_items > 10 or avg_label_length >= 15:
            # Many items or long labels: horizontal bar (easier to read)
            chart_type = "horizontal_bar"
            confidence = 0.8
        else:
            # Default: vertical bar
            chart_type = "bar"
            confidence = 0.75
        
        # Add note to title if data was filtered
        title_suffix = f" (Top {MAX_BAR_ITEMS})" if original_count > MAX_BAR_ITEMS else ""
        
        return ChartConfig(
            id="chart_categorical",
            type=chart_type,
            title=f"{y_col.name} by {x_col.name}{title_suffix}",
            x_column=x_col.name,
            y_columns=[y_col.name],
            data=data,
            x_type="category",
            confidence=confidence
        )
    
    def _detect_multi_series_line(self) -> Optional[ChartConfig]:
        """
        Detect multi-series line chart: temporal column + 2+ numeric columns.
        
        For questions like "Compare revenue, cost, and profit over time".
        Limits to 5 series max for readability.
        
        Returns:
            ChartConfig with series field or None
        """
        temporal_cols = [col for col in self.column_metadata if col.is_temporal()]
        numeric_cols = [col for col in self.column_metadata if col.is_numeric()]
        
        # Need at least 2 numeric columns for multi-series
        if not temporal_cols or len(numeric_cols) < 2:
            return None
        
        # Use first temporal column as x-axis
        x_col = temporal_cols[0]
        
        # Use up to 5 numeric columns as series
        y_cols = numeric_cols[:5]
        
        # Build data array
        data = []
        for row in self.rows:
            point = {x_col.name: row[x_col.index]}
            for y_col in y_cols:
                point[y_col.name] = row[y_col.index]
            data.append(point)
        
        # Fill date gaps for smooth time series
        data = self._fill_date_gaps(data, x_col.name, [c.name for c in y_cols])
        
        # Confidence based on data quality
        confidence = 0.85 if x_col.null_count == 0 else 0.7
        
        return ChartConfig(
            id="chart_multi_series_line",
            type="line",
            title=f"Multi-Series Comparison over {x_col.name}",
            x_column=x_col.name,
            y_columns=[c.name for c in y_cols],  # Keep for backward compatibility
            data=data,
            x_type="date",
            confidence=confidence
        )
    
    def _detect_stacked_bar(self) -> Optional[ChartConfig]:
        """
        Detect stacked bar chart: categorical column + 2+ numeric columns.
        
        For questions like "Show revenue by location with breakdown by category".
        Useful for part-to-whole comparisons.
        
        Returns:
            ChartConfig with stacked=True or None
        """
        categorical_cols = [col for col in self.column_metadata if col.is_categorical()]
        numeric_cols = [col for col in self.column_metadata if col.is_numeric()]
        
        # Need at least 2 numeric columns for stacking
        if not categorical_cols or len(numeric_cols) < 2:
            return None
        
        # Use first categorical as x
        x_col = categorical_cols[0]
        # Use all numeric columns (up to 5) as stacked layers
        y_cols = numeric_cols[:5]
        
        # Build data array
        data = []
        for row in self.rows:
            point = {x_col.name: row[x_col.index]}
            for y_col in y_cols:
                point[y_col.name] = row[y_col.index]
            data.append(point)
        
        # Confidence based on category count (stacked works best with fewer categories)
        confidence = 0.8 if x_col.distinct_count <= 10 else 0.6
        
        return ChartConfig(
            id="chart_stacked_bar",
            type="stacked_bar",
            title=f"Stacked {', '.join(c.name for c in y_cols)} by {x_col.name}",
            x_column=x_col.name,
            y_columns=[c.name for c in y_cols],
            data=data,
            x_type="category",
            confidence=confidence
        )
    
    def _detect_area_chart(self) -> Optional[ChartConfig]:
        """
        Detect area chart: temporal column + numeric column(s) for cumulative trends.
        
        For questions like "Show cumulative revenue over time" or 
        "Stacked area chart of sales by category".
        
        Returns:
            ChartConfig with type="area" or None
        """
        temporal_cols = [col for col in self.column_metadata if col.is_temporal()]
        numeric_cols = [col for col in self.column_metadata if col.is_numeric()]
        
        if not temporal_cols or not numeric_cols:
            return None
        
        # Use first temporal column as x-axis
        x_col = temporal_cols[0]
        
        # Use numeric columns (up to 5) as area series
        y_cols = numeric_cols[:5]
        
        # Build data array
        data = []
        for row in self.rows:
            point = {x_col.name: row[x_col.index]}
            for y_col in y_cols:
                point[y_col.name] = row[y_col.index]
            data.append(point)
        
        # Fill date gaps
        data = self._fill_date_gaps(data, x_col.name, [c.name for c in y_cols])
        
        # Determine if stacked based on number of series
        stacked = len(y_cols) > 1
        
        # Confidence slightly lower than line (area charts less common)
        confidence = 0.75 if x_col.null_count == 0 else 0.6
        
        return ChartConfig(
            id="chart_area",
            type="area",
            title=f"{'Stacked ' if stacked else ''}{', '.join(c.name for c in y_cols)} over {x_col.name}",
            x_column=x_col.name,
            y_columns=[c.name for c in y_cols],
            data=data,
            x_type="date",
            confidence=confidence
        )
    
    def _detect_combo_chart(self) -> Optional[ChartConfig]:
        """
        Detect combo chart (line + bar): temporal + numeric columns with different scales.
        
        For questions like "Show revenue (bar) and growth rate (line)" or
        "Sales volume and profit margin over time".
        
        Detects when metrics have significantly different scales or units
        (e.g., absolute values vs percentages).
        
        Returns:
            ChartConfig with type="combo" or None
        """
        temporal_cols = [col for col in self.column_metadata if col.is_temporal()]
        numeric_cols = [col for col in self.column_metadata if col.is_numeric()]
        
        # Need at least 2 numeric columns
        if not temporal_cols or len(numeric_cols) < 2:
            return None
        
        # Use first temporal column as x-axis
        x_col = temporal_cols[0]
        
        # Use first 2 numeric columns (one for bar, one for line)
        y_cols = numeric_cols[:2]
        
        # Build data array
        data = []
        for row in self.rows:
            point = {x_col.name: row[x_col.index]}
            for y_col in y_cols:
                point[y_col.name] = row[y_col.index]
            data.append(point)
        
        # Fill date gaps
        data = self._fill_date_gaps(data, x_col.name, [c.name for c in y_cols])
        
        # Check if scales differ significantly (for dual axis decision)
        # Calculate average magnitude of each column
        col1_values = [row[y_cols[0].index] for row in self.rows if row[y_cols[0].index] is not None]
        col2_values = [row[y_cols[1].index] for row in self.rows if row[y_cols[1].index] is not None]
        
        if col1_values and col2_values:
            avg1 = sum(abs(v) for v in col1_values) / len(col1_values)
            avg2 = sum(abs(v) for v in col2_values) / len(col2_values)
            
            # If one is 10x or more different, suggest dual axis
            scale_ratio = max(avg1, avg2) / (min(avg1, avg2) + 0.001)  # Avoid div by zero
            dual_axis = scale_ratio > 10
        else:
            dual_axis = False
        
        # Confidence moderate (combo charts are more complex)
        confidence = 0.7
        
        return ChartConfig(
            id="chart_combo",
            type="combo",
            title=f"{y_cols[0].name} & {y_cols[1].name} over {x_col.name}",
            x_column=x_col.name,
            y_columns=[c.name for c in y_cols],
            data=data,
            x_type="date",
            confidence=confidence
        )
    
    def _detect_histogram(self) -> Optional[ChartConfig]:
        """
        Detect numeric distribution pattern: single numeric column.
        
        Returns:
            ChartConfig for histogram or None
        """
        numeric_cols = [col for col in self.column_metadata if col.is_numeric()]
        
        # Only create histogram if we have a single numeric column with many values
        if len(self.columns) != 1 or not numeric_cols:
            return None
        
        col = numeric_cols[0]
        
        # Skip if too few distinct values
        if col.distinct_count < 5:
            return None
        
        # Build histogram bins (simple approach: raw values)
        # Frontend can bin them as needed
        data = [
            {"value": row[col.index], "count": 1}
            for row in self.rows if row[col.index] is not None
        ]
        
        return ChartConfig(
            id="chart_histogram",
            type="histogram",
            title=f"Distribution of {col.name}",
            x_column=col.name,
            y_columns=["count"],
            data=data,
            x_type="numeric",
            confidence=0.7
        )


def detect_charts_from_results(
    columns: List[str], 
    rows: List[List[Any]],
    question: Optional[str] = None,
    use_ai: bool = True,
    currency_symbol: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Convenience function to detect charts from query results.
    
    Args:
        columns: Column names
        rows: Result rows
        question: User's original question (for AI context)
        use_ai: Use AI-powered chart selection (default True)
        
    Returns:
        List of chart config dicts (JSON-serializable)
    """
    detector = ChartDetector(columns, rows, question=question)
    charts = detector.detect_charts(use_ai=use_ai)
    chart_dicts = [chart.to_dict() for chart in charts]
    # Attach currency symbol metadata if provided so frontend can format tooltips
    if currency_symbol:
        for cd in chart_dicts:
            cd['currency_symbol'] = currency_symbol
    return chart_dicts
