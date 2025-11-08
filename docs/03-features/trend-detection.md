# Trend Detection (AI Insights)

**Feature**: Automatically detect trends and generate natural language insights from query results  
**Status**: ✅ Production Ready  
**Added**: v1.3.0 (2025-11-06)

---

## Purpose

Provide users with automatic AI-powered insights about their data, including:
- **Growth/Decline Trends**: "Sales increased 23% month-over-month"
- **Outliers**: "March revenue (€150K) is 3x the average"
- **Seasonality**: "Peak sales occur in Q4 (November-December)"
- **Comparisons**: "Department A has 40% more employees than average"

---

## How It Works

1. **User asks a question** → Backend executes query
2. **TrendDetector analyzes results** → Statistical analysis + pattern detection
3. **LLM generates insights** → Natural language summaries via Groq/Gemini
4. **Frontend displays insights** → Highlighted cards above charts/tables

---

## Detection Strategies

### 1. Time Series Trends
**Pattern**: Sequential date/datetime data with numeric values

**Statistics Calculated**:
- **Growth Rate**: % change between first and last values
- **Trend Direction**: Increasing, decreasing, or flat (±5% threshold)
- **Volatility**: Standard deviation / mean (coefficient of variation)
- **Peak/Trough**: Maximum and minimum values with dates

**Example Insights**:
- "Sales grew by 34% from Jan 2023 (€45K) to Dec 2023 (€60K)"
- "Revenue peaked in November (€150K), 2.5x the average"
- "High volatility detected: monthly sales vary by ±45%"

---

### 2. Categorical Outliers
**Pattern**: Categorical data with numeric aggregates

**Statistics Calculated**:
- **Mean & Median**: Central tendency
- **Standard Deviation**: Spread
- **Z-Score**: Standard deviations from mean (outlier threshold: |z| > 2)
- **Top/Bottom**: Highest and lowest values

**Example Insights**:
- "Electronics department (150 employees) is 60% above average (94)"
- "Product category 'Laptops' accounts for 45% of total sales"
- "3 departments are outliers: Engineering (+2.1σ), Marketing (-1.8σ), Sales (+2.4σ)"

---

### 3. Distributions
**Pattern**: Single numeric column with many values

**Statistics Calculated**:
- **Quartiles**: Q1, Median (Q2), Q3
- **Interquartile Range (IQR)**: Q3 - Q1
- **Outliers**: Values < Q1 - 1.5×IQR or > Q3 + 1.5×IQR
- **Skewness**: Left/right skew detection

**Example Insights**:
- "Employee ages range from 22 to 67 (median: 34)"
- "75% of orders are under €500, but 12 orders exceed €2,000"
- "Salary distribution is right-skewed (high earners pull mean up)"

---

### 4. Seasonality Detection
**Pattern**: Time series with repeating patterns

**Statistics Calculated**:
- **Monthly/Quarterly Peaks**: Identify high-frequency periods
- **Day-of-Week Patterns**: Weekday vs. weekend trends
- **Year-over-Year Growth**: Same period comparison

**Example Insights**:
- "Sales peak in Q4 (Nov-Dec), 2x higher than Q1-Q3 average"
- "Weekday orders (avg 450/day) exceed weekend orders (280/day)"
- "November 2024 sales (+18%) outpaced November 2023"

---

## Architecture

### Backend Components

**1. TrendDetector Class** (`src/core/trend_detector.py`)
```python
class TrendDetector:
    def __init__(self, columns: List[str], rows: List[List[Any]]):
        self.columns = columns
        self.rows = rows
        self.df = pd.DataFrame(rows, columns=columns)
    
    def detect_trends(self) -> List[TrendInsight]:
        """Detect all applicable trends from data."""
        insights = []
        insights.extend(self._detect_time_series_trends())
        insights.extend(self._detect_categorical_outliers())
        insights.extend(self._detect_distributions())
        return sorted(insights, key=lambda x: x.confidence, reverse=True)
    
    def _detect_time_series_trends(self) -> List[TrendInsight]:
        """Detect growth/decline in temporal data."""
        pass
    
    def _detect_categorical_outliers(self) -> List[TrendInsight]:
        """Detect outliers in categorical breakdowns."""
        pass
    
    def _detect_distributions(self) -> List[TrendInsight]:
        """Analyze numeric distributions."""
        pass
```

**2. TrendInsight Dataclass**
```python
@dataclass
class TrendInsight:
    id: str                # Unique ID
    type: str             # "growth", "outlier", "seasonality", "distribution"
    title: str            # Short headline
    description: str      # AI-generated natural language insight
    confidence: float     # 0.0-1.0
    metrics: Dict[str, Any]  # Supporting statistics
    columns: List[str]    # Relevant columns
```

**3. LLM Integration** (`src/core/summarizer.py`)
- Use existing `summarize_result()` function
- Add `generate_trend_insight()` method for natural language generation
- Prompt engineering: "Given these statistics: {...}, generate a 1-sentence business insight."

---

### API Integration

**Updated AskResponse** (`api/models.py`):
```python
class AskResponse(BaseModel):
    success: bool
    answer: str
    sql: str
    columns: List[str]
    rows: List[List[Any]]
    row_count: int
    gen_ms: int
    exec_ms: int
    charts: Optional[List[ChartConfig]] = None
    trends: Optional[List[TrendInsight]] = None  # ← NEW
```

**Updated /ask Endpoint** (`api/routes.py`):
```python
@router.post("/ask")
async def ask_question(request: AskRequest) -> AskResponse:
    # ... existing query execution ...
    
    # Detect charts
    charts = detect_charts_from_results(columns, rows)
    
    # Detect trends ← NEW
    trends = detect_trends_from_results(columns, rows)
    
    return AskResponse(
        # ... existing fields ...
        charts=charts,
        trends=trends
    )
```

---

### Frontend Components

**1. InsightsPanel Component** (`frontend/src/components/results/insights-panel.tsx`)
```tsx
interface InsightsPanelProps {
  trends: TrendInsight[];
}

export function InsightsPanel({ trends }: InsightsPanelProps) {
  if (!trends?.length) return null;
  
  return (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TrendingUp className="h-5 w-5" />
          AI Insights
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {trends.map((trend) => (
            <Alert key={trend.id} variant={getAlertVariant(trend.type)}>
              <AlertTitle>{trend.title}</AlertTitle>
              <AlertDescription>{trend.description}</AlertDescription>
              <Badge variant="outline" className="mt-2">
                {(trend.confidence * 100).toFixed(0)}% confidence
              </Badge>
            </Alert>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
```

**2. Integration in AnswerPanel**
```tsx
// frontend/src/components/results/answer-panel.tsx
import { InsightsPanel } from './insights-panel';

export function AnswerPanel({ result }: AnswerPanelProps) {
  return (
    <div className="space-y-4">
      {/* Hero Answer Card */}
      <Card>...</Card>
      
      {/* AI Insights ← NEW */}
      {res.trends && <InsightsPanel trends={res.trends} />}
      
      {/* Charts */}
      {res.charts && <ChartPanel charts={res.charts} />}
      
      {/* SQL + Table */}
      ...
    </div>
  );
}
```

---

## Testing Strategy

### Unit Tests (`tests/unit/test_trend_detector.py`)

**Test Coverage**:
1. **Time Series Trends**
   - Growth detection (positive trend)
   - Decline detection (negative trend)
   - Flat trend (±5% change)
   - Peak/trough identification
   - Volatility calculation

2. **Categorical Outliers**
   - Z-score calculation
   - Outlier detection (|z| > 2)
   - Top/bottom identification
   - Percentage contributions

3. **Distributions**
   - Quartile calculation
   - IQR outlier detection
   - Skewness detection
   - Range analysis

4. **Edge Cases**
   - Empty results
   - Single row
   - All null values
   - Non-numeric data

**Target**: 20+ unit tests, 90%+ coverage

---

### Integration Tests (`tests/integration/test_trend_detection.py`)

**Test Coverage**:
1. `/ask` endpoint returns trends for time series queries
2. `/ask` endpoint returns trends for categorical queries
3. `/query` endpoint includes trends in response
4. Empty results return no trends
5. Trend data structure validation
6. Multiple databases compatibility

**Target**: 6+ integration tests

---

## Performance Targets

- **Statistical Analysis**: < 50ms (pure Python/pandas)
- **LLM Insight Generation**: < 1.5s (parallel with result summarization)
- **Total Overhead**: < 100ms (excluding LLM, which is parallelizable)

**Optimization**:
- Cache trend detection results for identical queries
- Limit LLM calls to top 3 highest-confidence trends
- Use sampling for large datasets (>1000 rows → analyze first 1000)

---

## Limitations

### Known Constraints

1. **Sample Size**: Requires ≥5 rows for meaningful statistics
2. **Data Quality**: Null values reduce confidence scores
3. **LLM Dependency**: Insights require Groq/Gemini API (fallback to raw stats)
4. **Temporal Granularity**: Monthly/yearly trends work best; hourly data may show noise
5. **Language**: Currently English-only for insights

### Future Enhancements (Post-MVP)

- Multi-metric correlations ("Sales correlate with ad spend, r=0.87")
- Forecasting ("Projected Q1 2024 revenue: €180K ±15%")
- Anomaly alerts ("Unusual spike detected in recent data")
- User feedback loop (thumbs up/down on insights)
- Custom thresholds (user-defined outlier sensitivity)

---

## Examples

### Example 1: Time Series Growth
**Query**: "Show monthly sales for 2023"

**Results**:
| month     | total_sales |
|-----------|-------------|
| 2023-01   | 45000       |
| 2023-02   | 48000       |
| ...       | ...         |
| 2023-12   | 60000       |

**Detected Trends**:
```json
[
  {
    "id": "trend_1",
    "type": "growth",
    "title": "Strong Sales Growth",
    "description": "Sales increased by 33% from January (€45K) to December (€60K), averaging €52K per month.",
    "confidence": 0.92,
    "metrics": {
      "growth_rate": 0.33,
      "start_value": 45000,
      "end_value": 60000,
      "average": 52000,
      "trend": "increasing"
    },
    "columns": ["month", "total_sales"]
  }
]
```

---

### Example 2: Categorical Outliers
**Query**: "Count employees by department"

**Results**:
| department | employee_count |
|------------|----------------|
| Engineering| 150            |
| Sales      | 120            |
| Marketing  | 45             |
| HR         | 12             |

**Detected Trends**:
```json
[
  {
    "id": "trend_1",
    "type": "outlier",
    "title": "Engineering Department Stands Out",
    "description": "Engineering (150 employees) is 60% above the average department size (82), accounting for 46% of total headcount.",
    "confidence": 0.88,
    "metrics": {
      "mean": 81.75,
      "z_score": 2.1,
      "percentage": 0.46,
      "outlier": true
    },
    "columns": ["department", "employee_count"]
  }
]
```

---

### Example 3: Distribution Analysis
**Query**: "Show all employee ages"

**Results**:
| age |
|-----|
| 22  |
| 25  |
| 28  |
| ...100 rows... |
| 67  |

**Detected Trends**:
```json
[
  {
    "id": "trend_1",
    "type": "distribution",
    "title": "Age Distribution Summary",
    "description": "Employee ages range from 22 to 67 with a median of 34. Most employees (50%) are between 28 and 42 years old.",
    "confidence": 0.75,
    "metrics": {
      "min": 22,
      "q1": 28,
      "median": 34,
      "q3": 42,
      "max": 67,
      "iqr": 14,
      "outliers_count": 3
    },
    "columns": ["age"]
  }
]
```

---

## Implementation Checklist

### Phase 1: Backend Core ✅
- [x] Create `src/core/trend_detector.py` (TrendDetector class - 562 lines)
- [x] Create `tests/unit/test_trend_detector.py` (24 tests)
- [x] Run tests: `pytest tests/unit/test_trend_detector.py -v`
- [x] Verify: 24/24 passing ✅

### Phase 2: LLM Integration (Future Enhancement)
- [ ] Add `generate_trend_insight()` to `src/core/summarizer.py`
- [ ] Test LLM insight generation manually
- [ ] Verify prompts produce quality insights
- *Note: Currently using template-based descriptions; LLM enhancement planned for v1.4*

### Phase 3: API Integration ✅
- [x] Update `api/models.py` (add TrendInsight model, trends field)
- [x] Update `api/routes.py` (wire into /ask and /query)
- [x] Create `tests/integration/test_trend_detection.py` (7 tests)
- [x] Run integration tests: `pytest tests/integration/test_trend_detection.py -v`
- [x] Verify: 7/7 passing ✅

### Phase 4: Frontend UI ✅
- [x] Update `frontend/src/lib/api.ts` (add TrendInsight TypeScript types)
- [x] Create `frontend/src/components/ui/alert.tsx` (shadcn/ui component)
- [x] Create `frontend/src/components/results/insights-panel.tsx`
- [x] Update `frontend/src/components/results/answer-panel.tsx` (add InsightsPanel)
- [x] Test in browser: verify insights display correctly ✅

### Phase 5: Documentation ✅
- [x] Update this file with production details
- [x] Update `docs/INDEX.md` (add Trend Detection link)
- [x] Update `.github/copilot-instructions.md` (add to Recent Enhancements)
- [x] Create completion summary document

---

**Version**: 1.3.0  
**Last Updated**: 2025-11-06  
**Status**: ✅ Production Ready  
**Test Coverage**: 31/31 tests passing (24 unit + 7 integration)
