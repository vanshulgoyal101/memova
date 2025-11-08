"""
Intelligent result summarizer with data structure understanding
Analyzes rows/columns to generate context-aware natural language summaries
"""

import json
import math
import logging
from typing import Any, Dict, List

from src.utils.llm import generate_text

logger = logging.getLogger(__name__)


def _is_time_col(name: str) -> bool:
    """
    Detect time-related columns by name pattern
    
    Args:
        name: Column name
        
    Returns:
        True if column appears to be time-related
    """
    n = name.lower()
    return any(k in n for k in ("date", "day", "month", "year", "created", "updated", "ts", "timestamp"))


def summarize_result(
    question: str,
    columns: List[str],
    rows: List[List[Any]],
    company_id: str,
    section_ids: List[str],
    exec_ms: float,
    currency_symbol: str = "$",
    max_cells: int = 4000,
) -> str:
    """
    Generate natural language summary of SQL query results
    
    Intelligently analyzes the data structure:
    - Downsamples large datasets (head + tail)
    - Computes numeric aggregates for quantitative insights
    - Detects time columns for trend analysis
    - Identifies categorical columns for grouping insights
    
    Args:
        question: Original user question
        columns: Column names from query
        rows: Result rows
        company_id: Database identifier
        section_ids: Filtered sections
        exec_ms: Query execution time in milliseconds
        currency_symbol: Currency symbol for the database ($ for USD, ₹ for INR)
        max_cells: Maximum cells to include in sample
        
    Returns:
        Natural language summary (paragraph + bullets)
    """
    logger.info(f"Summarizing {len(rows)} rows for question: {question[:50]}...")
    row_count, col_count = len(rows), len(columns)
    
    # Handle empty results
    if row_count == 0:
        logger.debug("No rows to summarize")
        return "No matching records for this question."
    
    # Downsample large datasets (head + tail with ellipsis separator)
    cells = row_count * col_count
    truncated = cells > max_cells
    sample_rows = rows
    
    if truncated:
        head = rows[:min(50, row_count)]
        tail = rows[max(0, row_count - 50):]
        # Add ellipsis separator if significant gap
        sample_rows = head + ([["…"] * col_count] if row_count > 100 else []) + tail
    
    # Compute numeric aggregates for quantitative columns
    numeric_summary: Dict[str, Dict[str, float]] = {}
    for j, name in enumerate(columns):
        nums = []
        for r in rows:
            v = r[j]
            if isinstance(v, (int, float)) and not (isinstance(v, float) and math.isnan(v)):
                nums.append(float(v))
        
        if nums:
            s = sum(nums)
            c = len(nums)
            numeric_summary[name] = {
                "count": c,
                "sum": s,
                "mean": s / max(1, c),
                "min": min(nums),
                "max": max(nums)
            }
    
    # Detect categorical columns (low cardinality strings)
    cat_candidates: Dict[str, List[str]] = {}
    for j, name in enumerate(columns):
        vals = set()
        for r in rows[:1000]:  # Sample first 1000 rows
            v = r[j]
            if isinstance(v, str):
                vals.add(v)
        
        # Consider low-cardinality columns (2-30 unique values)
        if 1 < len(vals) <= 30:
            cat_candidates[name] = sorted(list(vals))[:30]
    
    # Detect time-related columns
    time_cols = [c for c in columns if _is_time_col(c)]
    
    # Build compact JSON payload for LLM
    payload = {
        "question": question,
        "scope": {
            "company_id": company_id,
            "section_ids": section_ids
        },
        "shape": {
            "rows": row_count,
            "cols": col_count,
            "truncated": truncated
        },
        "columns": columns,
        "sample_rows": sample_rows,
        "numeric_summary": numeric_summary,
        "category_candidates": cat_candidates,
        "time_columns": time_cols,
        "execution_ms": exec_ms,
    }
    
    # Tight prompt for crisp business summary
    system = (
        "You are a senior data analyst. Produce a crisp business summary of tabular SQL results.\n"
        "- Start with ONE sentence answering the question directly.\n"
        "- Then 3–6 bullet points with key insights: ranks, totals, trends, extremes, notable categories.\n"
        f"- Use exact figures if small; otherwise round sensibly. Include units if obvious (%, {currency_symbol}).\n"
        "- If time columns exist, comment on trend (MoM/DoD) when clear.\n"
        "- If data was truncated, add a final caveat line.\n"
        "- No code, no SQL, no tables. Keep under ~130 words.\n\n"
        "CRITICAL - NUMBER FORMATTING:\n"
        f"- For currency amounts ≥1000: Format with abbreviations (e.g., {currency_symbol}1.2K, {currency_symbol}5.6M, {currency_symbol}1.2B)\n"
        f"- For currency amounts <1000: Use exact value with symbol (e.g., {currency_symbol}57, {currency_symbol}211)\n"
        "- For counts/quantities: Use whole numbers with commas (e.g., 1,234 units, 5,678 orders)\n"
        "- For percentages: Show 1-2 decimals (e.g., 23.5%, 0.8%)\n"
        "- Examples: '$5.2M revenue', '1,234 units sold', '$57 per item'\n\n"
        "CRITICAL - NO HALLUCINATIONS:\n"
        "- ONLY use numbers that appear in the 'numeric_summary' or 'sample_rows' provided\n"
        "- If no numeric data exists in results, DO NOT make up numbers\n"
        "- If asked about sales/revenue but only names returned, mention 'product names only' in summary\n"
        "- Be honest about data limitations"
    )
    
    user = (
        "QUESTION:\n" + question + "\n\n"
        "RESULT JSON:\n" + json.dumps(payload, ensure_ascii=False, default=str)
    )
    
    # Generate summary with fallback
    try:
        txt = generate_text(system, user)
        return txt if txt.strip() else f"Found {row_count} row(s) across {col_count} column(s)."
    except Exception as e:
        # Log detailed error for debugging
        logger.error(f"LLM summarization failed: {type(e).__name__}: {str(e)}")
        logger.debug(f"Payload size: {len(json.dumps(payload, default=str))} chars, {row_count} rows")
        logger.debug(f"Question: {question[:100]}...")
        
        # Enhanced fallback with data preview
        return _create_fallback_message(question, columns, rows, row_count, col_count)


def _create_fallback_message(
    question: str,
    columns: List[str],
    rows: List[List[Any]],
    row_count: int,
    col_count: int
) -> str:
    """
    Create an informative fallback message when LLM summarization fails
    
    Provides context-aware messages with data preview to help users
    understand results even without AI summary.
    
    Args:
        question: Original user question
        columns: Column names
        rows: Result rows
        row_count: Total number of rows
        col_count: Total number of columns
        
    Returns:
        Informative fallback message with preview
    """
    # Handle empty results
    if row_count == 0:
        return "No matching records found for your query."
    
    # Single row - show all values
    if row_count == 1:
        preview_items = []
        for i in range(min(col_count, 5)):  # Show up to 5 columns
            value = rows[0][i]
            if value is not None:
                preview_items.append(f"{columns[i]}: {value}")
        
        preview = ", ".join(preview_items)
        if col_count > 5:
            preview += f"... (+{col_count - 5} more fields)"
        
        return (
            f"Found 1 record.\n\n"
            f"{preview}\n\n"
            f"Note: AI summary unavailable. View full details below."
        )
    
    # Multiple rows - show sample from first row
    preview_items = []
    for i in range(min(col_count, 3)):  # Show up to 3 columns for brevity
        value = rows[0][i]
        if value is not None:
            # Truncate long values
            value_str = str(value)
            if len(value_str) > 50:
                value_str = value_str[:47] + "..."
            preview_items.append(f"{columns[i]}: {value_str}")
    
    preview = ", ".join(preview_items)
    if col_count > 3:
        preview += "..."
    
    return (
        f"Found {row_count} records across {col_count} columns.\n\n"
        f"Sample: {preview}\n\n"
        f"Note: AI summary temporarily unavailable. View complete results below."
    )
