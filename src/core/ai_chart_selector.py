"""
AI-powered chart type selection engine.

Uses LLM to intelligently select the best chart type based on:
- Data characteristics (types, distributions, cardinality)
- Question context
- Visualization best practices

Author: Context Engineering
Created: 2025-11-06
"""

from typing import List, Dict, Optional, Any, Literal
import logging
from dataclasses import dataclass, asdict

from src.core.chart_detector import ChartConfig, ChartType, ColumnMetadata
from src.utils.llm import _get_client

logger = logging.getLogger(__name__)


@dataclass
class ChartRecommendation:
    """AI recommendation for chart type."""
    
    chart_type: ChartType
    reasoning: str
    confidence: float
    x_column: str
    y_columns: List[str]
    title: str


class AIChartSelector:
    """
    Uses LLM to select optimal chart type for query results.
    
    Provides intelligent chart recommendations based on:
    - Data shape and types
    - Statistical properties
    - Question context
    - Visualization best practices
    """
    
    def __init__(self):
        """Initialize AI chart selector."""
        self.llm = _get_client()
    
    def select_chart(
        self,
        columns: List[str],
        rows: List[List[Any]],
        column_metadata: List[ColumnMetadata],
        question: Optional[str] = None,
        max_analyze: int = 100
    ) -> Optional[ChartConfig]:
        """
        Use AI to select the best chart type for the data.
        
        Args:
            columns: Column names
            rows: Data rows
            column_metadata: Analyzed column metadata
            question: User's original question (optional context)
            max_analyze: Max rows to send to LLM (default 100)
            
        Returns:
            ChartConfig or None if no chart recommended
        """
        if not rows or not columns:
            logger.info("Empty dataset - no chart to recommend")
            return None
        
        # Build context for LLM
        data_summary = self._build_data_summary(
            columns, 
            rows[:max_analyze],
            column_metadata
        )
        
        # Create prompt for LLM
        prompt = self._build_chart_selection_prompt(
            data_summary,
            question
        )
        
        try:
            # Call LLM (returns tuple: (response_text, provider))
            response_text, provider = self.llm.generate_content(prompt)
            logger.info(f"Chart selection using {provider}")
            
            # Parse recommendation
            recommendation = self._parse_recommendation(response_text)
            
            if not recommendation:
                logger.warning("LLM did not provide a valid recommendation")
                return None
            
            # Check if AI decided no chart is needed
            if recommendation.chart_type == "none":
                logger.info(f"AI decided no chart needed: {recommendation.reasoning}")
                return None
            
            # Build ChartConfig from recommendation
            chart = self._build_chart_config(
                recommendation,
                columns,
                rows,
                column_metadata
            )
            
            if chart:
                logger.info(
                    f"AI recommended {chart.type} chart: {chart.title} "
                    f"(confidence: {chart.confidence:.0%}, reasoning: {recommendation.reasoning[:100]})"
                )
            
            return chart
            
            return chart
            
        except Exception as e:
            logger.error(f"AI chart selection failed: {e}")
            return None
    
    def _build_data_summary(
        self,
        columns: List[str],
        rows: List[List[Any]],
        column_metadata: List[ColumnMetadata]
    ) -> str:
        """Build concise data summary for LLM."""
        summary_parts = []
        
        # Dataset shape
        summary_parts.append(f"Dataset: {len(rows)} rows × {len(columns)} columns")
        
        # Column details
        summary_parts.append("\nColumns:")
        for col_meta in column_metadata:
            col_desc = (
                f"  - {col_meta.name}: {col_meta.inferred_type} "
                f"({col_meta.distinct_count} distinct values"
            )
            if col_meta.null_count > 0:
                col_desc += f", {col_meta.null_count} nulls"
            col_desc += ")"
            
            # Add sample values
            sample_str = ", ".join(str(v) for v in col_meta.sample_values[:5])
            col_desc += f"\n    Samples: {sample_str}"
            
            summary_parts.append(col_desc)
        
        # Sample data (first 5 rows)
        summary_parts.append("\nSample Data:")
        for i, row in enumerate(rows[:5]):
            row_dict = dict(zip(columns, row))
            summary_parts.append(f"  Row {i+1}: {row_dict}")
        
        return "\n".join(summary_parts)
    
    def _build_chart_selection_prompt(
        self,
        data_summary: str,
        question: Optional[str]
    ) -> str:
        """Build prompt for LLM chart selection."""
        prompt = f"""You are a data visualization expert. Analyze this query result and determine if a chart would be helpful.

{data_summary}

{"User's Question: " + question if question else ""}

**Decision Process:**
1. First, decide if this data should be visualized at all
2. If yes, select the BEST chart type

**When NOT to visualize (use `none`):**
- Single row/value results (e.g., "How many products?" → just a number)
- Text-heavy data (employee names, descriptions)
- Simple lookup results (e.g., "What is X's salary?" → one value)
- Already clear from the data table

**When TO visualize:**
- Comparisons between categories
- Trends over time
- Distributions or patterns
- Part-to-whole relationships

**Available Chart Types:**
- `line`: Time series, trends over time (requires temporal x-axis)
- `bar`: Vertical bar for comparing categories (standard, up to 20 items)
- `horizontal_bar`: Horizontal bars (better for long labels, many items, or rankings)
- `pie`: Part-to-whole, percentages (best for 3-6 categories only)
- `doughnut`: Modern alternative to pie (better for 4-8 categories)
- `histogram`: Numeric distribution (single numeric column)
- `area`: Filled line chart for cumulative/volume data
- `stacked_bar`: Part-to-whole over categories (multiple series)
- `stacked_area`: Cumulative trends over time
- `grouped_bar`: Side-by-side comparison of multiple metrics
- `combo`: Mixed bar + line (different scale metrics)
- `scatter`: Correlation between two numeric variables
- `none`: No visualization needed - data is clear from table

**Best Practices:**
- Pie/Doughnut: Only 3-8 categories showing proportions
- Horizontal Bar: Use when labels are long (>15 chars) or there are many items (>10)
- Scatter: Use for "X vs Y" questions to show correlation
- Combo: Use when comparing metrics with different scales (e.g., sales $ and units)
- None: Use for single values, text data, or when table is clearer
- Bar charts: Better for comparing categories or when values don't sum to 100%
- Line charts: Require temporal x-axis (dates/times)
- Consider if the user's question really needs a chart

**Your Response Format (JSON):**
{{
  "chart_type": "bar|pie|line|histogram|none",
  "reasoning": "Brief explanation why this chart type is best (or why no chart is needed)",
  "x_column": "column name for x-axis (or empty string if none)",
  "y_columns": ["column name(s) for y-axis (or empty array if none)"],
  "title": "Descriptive chart title (or empty string if none)"
}}

**Critical Rules:**
1. Simple counts/single values → use `none`
2. Comparing categories WITHOUT proportions → use `bar` not `pie`
3. Showing top/bottom rankings → use `bar` not `pie`
4. If >7 categories → NEVER use `pie`, use `bar`
5. Trends over time → use `line`
6. When in doubt, use `none` - let the data table speak for itself

Respond ONLY with valid JSON, no other text."""

        return prompt
    
    def _parse_recommendation(self, response_text: str) -> Optional[ChartRecommendation]:
        """Parse LLM response into ChartRecommendation."""
        try:
            # Extract JSON from response
            import json
            import re
            
            # Try to find JSON in response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if not json_match:
                logger.warning(f"No JSON found in LLM response: {response_text[:200]}")
                return None
            
            data = json.loads(json_match.group())
            
            # Validate required fields
            required = ["chart_type", "reasoning", "x_column", "y_columns", "title"]
            if not all(k in data for k in required):
                logger.warning(f"Missing required fields in recommendation: {data}")
                return None
            
            # Validate chart_type
            valid_types = ["line", "bar", "pie", "histogram", "none"]
            if data["chart_type"] not in valid_types:
                logger.warning(f"Invalid chart type: {data['chart_type']}")
                return None
            
            # If no chart needed, allow empty fields
            if data["chart_type"] == "none":
                return ChartRecommendation(
                    chart_type="none",
                    reasoning=data.get("reasoning", "No visualization needed"),
                    confidence=0.9,
                    x_column="",
                    y_columns=[],
                    title=""
                )
            
            # For actual charts, validate columns exist
            if not data.get("x_column") or not data.get("y_columns"):
                logger.warning(f"Missing column information for chart type {data['chart_type']}: {data}")
                return None
            
            # Build recommendation
            return ChartRecommendation(
                chart_type=data["chart_type"],
                reasoning=data["reasoning"],
                confidence=0.9,  # High confidence in AI decision
                x_column=data["x_column"],
                y_columns=data["y_columns"] if isinstance(data["y_columns"], list) else [data["y_columns"]],
                title=data["title"]
            )
            
        except Exception as e:
            logger.error(f"Failed to parse recommendation: {e}\nResponse: {response_text[:500]}")
            return None
    
    def _build_chart_config(
        self,
        recommendation: ChartRecommendation,
        columns: List[str],
        rows: List[List[Any]],
        column_metadata: List[ColumnMetadata]
    ) -> Optional[ChartConfig]:
        """Build ChartConfig from AI recommendation."""
        
        if recommendation.chart_type == "none":
            return None
        
        # Find column indices
        try:
            x_idx = columns.index(recommendation.x_column)
            y_indices = [columns.index(y) for y in recommendation.y_columns]
        except ValueError as e:
            logger.error(f"Column not found: {e}")
            return None
        
        # Build data array
        data = []
        for row in rows:
            point = {recommendation.x_column: row[x_idx]}
            for y_col, y_idx in zip(recommendation.y_columns, y_indices):
                point[y_col] = row[y_idx]
            data.append(point)
        
        # Determine x_type
        x_meta = next((m for m in column_metadata if m.name == recommendation.x_column), None)
        if x_meta:
            if x_meta.is_temporal():
                x_type = "date"
            elif x_meta.is_numeric():
                x_type = "numeric"
            else:
                x_type = "category"
        else:
            x_type = "category"
        
        return ChartConfig(
            id="chart_ai_selected",
            type=recommendation.chart_type,
            title=recommendation.title,
            x_column=recommendation.x_column,
            y_columns=recommendation.y_columns,
            data=data,
            x_type=x_type,
            confidence=recommendation.confidence
        )
