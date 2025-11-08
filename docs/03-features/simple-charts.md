# Simple Charts (Auto-charting)

**Feature**: Generate simple visualizations automatically from query results  
**Status**: ✅ Production Ready  
**Added**: v1.2.0 (2025-11-06)

---

## Purpose

Provide users with a quick way to visualize query results. The system automatically detects chartable patterns in the returned result set (time series, categorical aggregates, numeric distributions) and renders an appropriate chart (line, bar, pie, histogram) in the UI with minimal configuration.

---

## How It Works

1. **User asks a question** → Backend executes query
2. **ChartDetector analyzes results** → Applies heuristics to detect patterns
3. **Chart metadata generated** → Type, columns, data, confidence score
4. **Frontend ChartPanel renders** → Uses Recharts library to display visualization

### Chart Detection Heuristics

The backend `ChartDetector` class (`src/core/chart_detector.py`) uses these heuristics:

#### 1. Time Series (Line Chart)
- **Pattern**: DATE/DATETIME column + numeric column(s)
- **Example**: "Show sales by month", "Employee hires over time"
- **Chart**: Line chart with time on X-axis, metrics on Y-axis
- **Confidence**: 0.9 (high) if no null dates

#### 2. Categorical Breakdown (Bar/Pie Chart)
- **Pattern**: Categorical column + numeric aggregate
- **Example**: "Count employees by department", "Sales by product category"
- **Chart**: Pie (≤10 categories) or Bar (>10 categories)
- **Confidence**: 0.85 (few categories) or 0.65 (many)

#### 3. Numeric Distribution (Histogram)
- **Pattern**: Single numeric column with many distinct values (≥5)
- **Example**: "Show employee ages", "Distribution of order amounts"
- **Chart**: Histogram with bins
- **Confidence**: 0.7

#### 4. Fallback
- If no patterns match, no chart is suggested
- Results still display in table format

---

## API Integration

Both `/ask` and `/query` endpoints include chart metadata when detected.

### Response Format

```json
{
  "answer_text": "Found 8 departments with employee counts...",
  "sql": "SELECT department, COUNT(*) ...",
  "columns": ["department", "employee_count"],
  "rows": [["Engineering", 50], ["Sales", 30], ...],
  "charts": [
    {
      "id": "chart_categorical",
      "type": "bar",
      "title": "employee_count by department",
      "x_column": "department",
      "y_columns": ["employee_count"],
      "data": [
        {"department": "Engineering", "employee_count": 50},
        {"department": "Sales", "employee_count": 30}
      ],
      "x_type": "category",
      "confidence": 0.85
    }
  ],
  "timings": {"genMs": 1200, "execMs": 15}
}
```

### Empty Results
When results are empty or unsuitable for charting:
```json
{
  "charts": null
}
```

---

## Frontend Implementation

### ChartPanel Component

Location: `frontend/src/components/results/chart-panel.tsx`

**Features**:
- Renders line, bar, pie, and histogram charts
- Uses Recharts library for responsive, accessible visualizations
- Shows chart type badge and confidence score
- Automatically selects appropriate chart from heuristics
- Colorblind-friendly palette (5 distinct colors)

**Accessibility**:
- ARIA labels for axes and tooltips
- Keyboard navigable tooltips
- High contrast colors (respects light/dark theme)

### Integration in AnswerPanel

Charts appear between the "Answer" card and collapsible SQL/data sections:
1. Natural language answer (hero)
2. **Chart visualization** ← NEW
3. Collapsible SQL query
4. Collapsible raw data table

---

## Examples

### Categorical Breakdown (Bar Chart)
**Question**: "Show employee count by department"  
**Result**: Bar chart with departments on X-axis, counts on Y-axis  
**Confidence**: 85%

### Time Series (Line Chart)
**Question**: "Show sales over time"  
**Result**: Line chart with months on X-axis, total sales on Y-axis  
**Confidence**: 90%

### Pie Chart (Few Categories)
**Question**: "Product count by category"  
**Result**: Pie chart with 6 slices for product categories  
**Confidence**: 85%

### Histogram (Distribution)
**Question**: "Show age distribution"  
**Result**: Histogram with age bins on X-axis, frequency on Y-axis  
**Confidence**: 70%

---

## Testing

### Unit Tests
Location: `tests/unit/test_chart_detector.py`  
**Coverage**: 21/21 tests passing (100%)

Test categories:
- Column type inference (numeric, date, datetime, categorical, text)
- Time series detection
- Categorical breakdown detection
- Histogram detection
- Edge cases (empty results, null values, large datasets)

### Integration Tests
Location: `tests/integration/test_chart_detection.py`  
**Coverage**: 6/6 tests passing (100%)

Test categories:
- Charts included in `/ask` endpoint
- Charts included in `/query` endpoint
- Empty results handling
- Chart data structure validation
- Multi-database support

---

## Limitations

- **Max 1000 rows** analyzed for performance (samples larger datasets)
- **Top chart only** shown (highest confidence, can show multiple in future)
- **No custom binning** for histograms (frontend could add this)
- **No multi-series grouping** (e.g., stacked bars) yet
- **Server-side detection only** (no client-side override UI yet)

---

## Performance

- **Chart detection**: <10ms for typical result sets
- **Frontend rendering**: <100ms with Recharts
- **No LLM calls** required (pure heuristic, fast and deterministic)

---

## Future Enhancements

- [ ] User-selectable chart type (override heuristics)
- [ ] Custom axis labels and titles
- [ ] Download chart as PNG/SVG
- [ ] Multi-series charts (grouped/stacked bars)
- [ ] Drill-down interactions (click bar → filter table)
- [ ] Sparklines in table cells
- [ ] Dashboard mode (show multiple charts side-by-side)

---

## Related Documentation

- [Natural Language Querying](natural-language.md) - How queries are processed
- [API Reference](../05-api/endpoints.md) - `/ask` and `/query` endpoint details
- [Architecture](../02-architecture/system-overview.md) - How ChartDetector fits in

---

**Last Updated**: 2025-11-06  
**Implementation**: Backend (21 unit tests) + Frontend (ChartPanel component) + Integration (6 tests)
