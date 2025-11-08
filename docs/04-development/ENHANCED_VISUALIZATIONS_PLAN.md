# Enhanced Visualization System - Development Plan

**Date**: November 7, 2025  
**Version**: 3.4.0  
**Objective**: Fix currency formatting, improve daily granularity, and enhance visualization capabilities

---

## 🎯 Problems Identified

### 1. Currency Formatting Issue
**Problem**: Liqo data shows dollar signs ($) instead of rupee signs (₹)
**Impact**: Confusing for users, data appears to be in wrong currency
**Root Cause**: LLM summarizer uses hardcoded "$" in prompt (line 140 of summarizer.py)

### 2. Daily Granularity Issue
**Problem**: The "daily sales" query returns data but the graph shows non-daily spacing
**Root Cause**: SQL query is correct (GROUP BY transaction_date), but:
- Data has gaps (no transactions on some days)
- Chart rendering doesn't handle sparse time series
- Line chart connects points without filling gaps

**Evidence from test**:
```sql
-- Correct SQL
SELECT transaction_date, SUM(item_amount) as daily_total 
FROM sales_transactions 
GROUP BY transaction_date 
ORDER BY transaction_date DESC

-- Returns: ['2023-03-31', 6963335.51], ['2023-03-30', 3821154.0], ['2023-03-29', 4481257.28]
-- ✅ Daily data exists
-- ❌ But visual shows irregular spacing because missing dates not filled
```

### 3. Limited Visualization Capabilities
**Current State**:
- Single chart per query
- Max 3 series in line charts
- No multi-chart layouts
- No comparative visualizations
- No stacked/grouped charts

**Desired State**:
- Multiple charts per query when beneficial
- Multi-series line charts (unlimited)
- Stacked bar charts
- Grouped bar charts
- Area charts for cumulative trends
- Combo charts (line + bar)
- Side-by-side chart comparisons

---

## 📋 Detailed Development Plan

### Phase 1: Currency Formatting Fix (30 min)
**Priority**: HIGH
**Complexity**: LOW

#### 1.1 Add Database Metadata
**File**: `api/routes.py`
- Add `currency` field to DATABASES dict
- Electronics: "USD" ($)
- Airline: "USD" ($)
- EdTech: "INR" (₹)
- EdNite: "INR" (₹)
- Liqo: "INR" (₹)

#### 1.2 Update LLM Summarizer
**File**: `src/utils/llm.py`
- Accept `database_id` parameter in `summarize_results()`
- Detect currency from database metadata
- Pass currency symbol to prompt

**File**: `src/core/summarizer.py`
- Update prompt template (line 140)
- Replace hardcoded "$" with dynamic `{currency}`
- Example: "Use exact figures. Include units if obvious (%, {currency})."

#### 1.3 Update API Routes
**File**: `api/routes.py`
- Pass `database_id` to summarizer in `/ask` endpoint
- Ensure currency context flows through

#### 1.4 Frontend Display (Optional Enhancement)
**File**: `frontend/src/components/results/answer-panel.tsx`
- Add currency formatting helper
- Format numbers in tables based on database
- Example: `formatCurrency(value, currency)`

---

### Phase 2: Daily Granularity Fix (1 hour)
**Priority**: HIGH
**Complexity**: MEDIUM

#### 2.1 Backend: Gap Filling in Results
**File**: `src/core/chart_detector.py` (new method)
- Add `_fill_date_gaps()` method to ChartDetector
- Detect date range (min/max) in time series data
- Generate complete date sequence
- Fill missing dates with null/zero values
- Preserves all columns, only fills gaps

**Algorithm**:
```python
def _fill_date_gaps(data: List[Dict], date_column: str) -> List[Dict]:
    """Fill gaps in time series data with null values"""
    # 1. Parse dates, find min/max
    # 2. Generate complete date range (daily/monthly based on data)
    # 3. Create lookup dict of existing data
    # 4. For each date in range:
    #    - If date exists: use actual data
    #    - If date missing: insert row with nulls
    # 5. Return filled dataset
```

#### 2.2 Apply Gap Filling to Line Charts
**File**: `src/core/chart_detector.py`
- In `_detect_line_chart()` method
- After identifying time series, call `_fill_date_gaps()`
- Only apply to line charts (not bar/pie)

#### 2.3 Frontend: Handle Null Values
**File**: `frontend/src/components/results/chart-panel.tsx`
- Recharts already handles nulls gracefully
- Ensure connectNulls={false} to show gaps visually
- Or use interpolation for smoother lines

#### 2.4 Add Granularity Detection
**File**: `src/core/chart_detector.py`
- Detect if data is daily/weekly/monthly
- Based on date format and gaps between points
- Add `granularity` field to ChartConfig
- Frontend can show "(Daily)" or "(Monthly)" in title

---

### Phase 3: Enhanced Multi-Chart System (3 hours)
**Priority**: MEDIUM
**Complexity**: HIGH

#### 3.1 Update Chart Detection Architecture

**File**: `api/models.py`
- Update `ChartConfig` to support multi-series
- Add `series` field: List of {name, column, color}
- Add `chart_group` field for multi-chart layouts
- Add `layout` field: "single", "horizontal", "vertical", "grid"

```python
class ChartSeries(BaseModel):
    name: str
    column: str
    color: Optional[str] = None
    type: Optional[str] = None  # "line", "bar", "area" for combo charts

class ChartConfig(BaseModel):
    id: str
    type: ChartType  # Add "area", "stacked_bar", "grouped_bar", "combo"
    title: str
    x_column: str
    series: List[ChartSeries]  # NEW: replaces y_columns
    data: List[Dict[str, Any]]
    x_type: str
    confidence: float
    granularity: Optional[str] = None  # "daily", "weekly", "monthly"
    chart_group: Optional[int] = None  # For multi-chart layouts
```

#### 3.2 Enhance Chart Detector Logic

**File**: `src/core/chart_detector.py`
- Add `max_charts` parameter (default: 3)
- Detect multiple patterns in same dataset:
  - Example: Time series + categorical breakdown
  - Return List[ChartConfig] instead of List[ChartConfig]

**New Methods**:
```python
def detect_multiple_charts(self) -> List[ChartConfig]:
    """Detect multiple complementary visualizations"""
    charts = []
    
    # 1. Primary chart (existing logic)
    primary = self._detect_primary_chart()
    if primary:
        charts.append(primary)
    
    # 2. Secondary chart (if data supports)
    # Example: If primary is line chart, add bar for categories
    secondary = self._detect_secondary_chart(primary)
    if secondary:
        charts.append(secondary)
    
    return charts[:self.max_charts]
```

#### 3.3 Add Multi-Series Support

**File**: `src/core/chart_detector.py`
- Detect multiple numeric columns suitable for comparison
- Create multi-series line charts
- Example: Revenue + Cost + Profit on same time axis
- Limit: 5 series max (configurable)

```python
def _detect_multi_series_line(self) -> Optional[ChartConfig]:
    """Detect if multiple numeric columns should be on same line chart"""
    time_col = self._find_temporal_column()
    if not time_col:
        return None
    
    numeric_cols = [c for c in self.columns if self._is_numeric_column(c)]
    if len(numeric_cols) <= 1:
        return None
    
    # Create series config
    series = [
        ChartSeries(name=col, column=col, type="line")
        for col in numeric_cols[:5]  # Max 5 series
    ]
    
    return ChartConfig(
        id=f"chart_multi_line_{uuid4()}",
        type="line",
        title="Multi-Series Trend Analysis",
        x_column=time_col,
        series=series,
        data=self.rows,
        ...
    )
```

#### 3.4 Add Stacked/Grouped Bar Charts

**File**: `src/core/chart_detector.py`
- Detect when categorical data has multiple metrics
- Example: Sales by location WITH breakdown by product category
- Create stacked or grouped bar based on question context

```python
def _detect_stacked_bar(self) -> Optional[ChartConfig]:
    """Detect stacked bar chart opportunity"""
    # Look for: 1 categorical column + 2+ numeric columns
    # Or: 2 categorical columns + 1 numeric (second cat becomes stack)
    ...
```

#### 3.5 Add Area Charts

**File**: `src/core/chart_detector.py`
- For cumulative trends
- Stacked area for part-to-whole over time
- Example: "Revenue by category over time"

#### 3.6 Add Combo Charts (Line + Bar)

**File**: `src/core/chart_detector.py`
- For mixed metrics on same chart
- Example: Revenue (bar) + Growth % (line)
- Detect when one metric is absolute, other is rate/percentage

#### 3.7 Update AI Chart Selector

**File**: `src/core/ai_chart_selector.py`
- Update prompt to support multi-chart decisions
- Ask: "Should this data have multiple charts?"
- If yes: "What chart types and layout?"
- Return structured multi-chart config

**Enhanced Prompt**:
```
Given this query result, decide on visualizations:

1. Should we visualize this data? (yes/no)
2. If yes, how many charts? (1-3)
3. For each chart:
   - Type: line/bar/pie/area/stacked_bar/grouped_bar/combo
   - Purpose: What insight does it show?
   - Series: Which columns to include?
4. Layout: single/horizontal/vertical/grid

Consider:
- Does data support multiple perspectives?
- Would comparison charts add value?
- Is time series + categorical breakdown useful?
- Keep it intuitive, not cluttered
```

---

### Phase 4: Frontend Rendering (2 hours)
**Priority**: MEDIUM
**Complexity**: MEDIUM

#### 4.1 Update Chart Panel Component

**File**: `frontend/src/components/results/chart-panel.tsx`
- Support multi-chart layouts
- Add layout modes: single, horizontal (2-col), vertical (2-row), grid (2x2)
- Responsive: stack vertically on mobile

```typescript
interface ChartPanelProps {
  charts: ChartConfig[];
  layout: 'single' | 'horizontal' | 'vertical' | 'grid';
}

// Layout examples:
// single: 1 chart, full width
// horizontal: 2 charts, 50% width each
// vertical: 2 charts, stacked, 100% width each
// grid: 4 charts, 50% width, 50% height
```

#### 4.2 Add Multi-Series Line Chart

**File**: `frontend/src/components/results/chart-panel.tsx`
- Use Recharts multi-line support
- Color each series differently
- Add legend
- Ensure Y-axis scales appropriately

```typescript
<LineChart data={chart.data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey={chart.x_column} />
  <YAxis />
  <Tooltip />
  <Legend />
  {chart.series.map((s, i) => (
    <Line 
      key={s.column}
      type="monotone"
      dataKey={s.column}
      stroke={s.color || COLORS[i]}
      name={s.name}
    />
  ))}
</LineChart>
```

#### 4.3 Add Stacked Bar Chart

**File**: `frontend/src/components/results/chart-panel.tsx`
- Use Recharts BarChart with multiple Bar components
- Set stackId for stacking

```typescript
<BarChart data={chart.data}>
  {chart.series.map((s, i) => (
    <Bar 
      dataKey={s.column}
      stackId="a"  // Same stackId = stacked
      fill={s.color || COLORS[i]}
    />
  ))}
</BarChart>
```

#### 4.4 Add Area Chart

**File**: `frontend/src/components/results/chart-panel.tsx`
- Use Recharts AreaChart
- Support stacked area (part-to-whole)
- Add gradient fills for visual appeal

#### 4.5 Add Combo Chart (Line + Bar)

**File**: `frontend/src/components/results/chart-panel.tsx`
- Use Recharts ComposedChart
- Mix Line and Bar components
- Use different Y-axes if scales differ

```typescript
<ComposedChart data={chart.data}>
  <Bar dataKey="revenue" fill="#8884d8" />
  <Line dataKey="growth_pct" stroke="#ff7300" yAxisId="right" />
  <YAxis />
  <YAxis yAxisId="right" orientation="right" />
</ComposedChart>
```

#### 4.6 Update Chart Panel Layout

**File**: `frontend/src/components/results/chart-panel.tsx`
- Add grid/flex layout based on `layout` prop
- Ensure charts resize gracefully
- Add spacing between charts
- Mobile: always stack vertically

---

### Phase 5: Testing (1 hour)
**Priority**: HIGH
**Complexity**: LOW

#### 5.1 Unit Tests - Currency Formatting
**File**: `tests/unit/test_currency_formatting.py` (NEW)
- Test USD formatting for electronics/airline
- Test INR formatting for edtech/ednite/liqo
- Test summarizer receives correct currency

#### 5.2 Unit Tests - Date Gap Filling
**File**: `tests/unit/test_chart_detector.py` (UPDATE)
- Test `_fill_date_gaps()` with sparse data
- Test daily granularity detection
- Test weekly/monthly detection
- Test edge cases (single point, no gaps)

#### 5.3 Unit Tests - Multi-Chart Detection
**File**: `tests/unit/test_chart_detector.py` (UPDATE)
- Test multi-series line chart detection
- Test stacked bar detection
- Test area chart detection
- Test combo chart detection
- Test layout decisions

#### 5.4 Integration Tests - Full Flow
**File**: `tests/integration/test_enhanced_visualizations.py` (NEW)
- Test API returns multiple charts
- Test currency in answer matches database
- Test daily granularity in time series
- Test multi-series data structure

#### 5.5 Frontend Manual Testing
- Test each chart type renders correctly
- Test multi-chart layouts (horizontal, vertical, grid)
- Test responsive behavior (mobile)
- Test currency symbols display correctly

---

### Phase 6: Documentation (30 min)
**Priority**: MEDIUM
**Complexity**: LOW

#### 6.1 Update Charts Documentation
**File**: `docs/03-features/charts-insights.md`
- Add multi-chart section
- Add multi-series examples
- Add stacked/grouped bar examples
- Add area chart examples
- Add combo chart examples
- Update chart types table

#### 6.2 Update API Documentation
**File**: `docs/05-api/endpoints.md`
- Document new ChartConfig structure
- Document ChartSeries model
- Document layout field
- Show multi-chart response examples

#### 6.3 Update Schema Documentation
**File**: `docs/06-database/liqo_schema.md`
- Add note about rupee currency
- Update example queries to show ₹ symbols
- Add daily granularity examples

#### 6.4 Create Changelog Entry
**File**: `docs/07-maintenance/CHANGELOG.md`
- v3.4.0 release notes
- Currency formatting fix
- Daily granularity improvement
- Enhanced visualization system
- Multi-chart support
- New chart types (area, stacked, grouped, combo)

---

## 🎯 Implementation Priority

### Sprint 1 (High Priority) - 2 hours
1. ✅ Currency formatting fix (30 min)
2. ✅ Daily granularity fix (1 hour)
3. ✅ Basic testing (30 min)

### Sprint 2 (Medium Priority) - 3 hours
1. Multi-chart architecture (1 hour)
2. Multi-series line charts (30 min)
3. Stacked bar charts (30 min)
4. Frontend multi-chart rendering (1 hour)

### Sprint 3 (Nice-to-Have) - 2 hours
1. Area charts (30 min)
2. Combo charts (30 min)
3. AI-powered multi-chart selection (30 min)
4. Complete documentation (30 min)

---

## 📊 Expected Outcomes

### Currency Formatting
- ✅ Liqo queries show ₹ instead of $
- ✅ Other databases continue showing $ correctly
- ✅ Consistent across answer text, tables, and tooltips

### Daily Granularity
- ✅ Line charts show proper daily spacing
- ✅ Missing days filled with nulls or zeros
- ✅ Chart titles indicate granularity "(Daily)"
- ✅ No more irregular time axis spacing

### Enhanced Visualizations
- ✅ Multiple charts when beneficial (max 3)
- ✅ Multi-series line charts (up to 5 series)
- ✅ Stacked bar charts for part-to-whole over categories
- ✅ Grouped bar charts for side-by-side comparisons
- ✅ Area charts for cumulative trends
- ✅ Combo charts for mixed metrics
- ✅ Intelligent layout (horizontal/vertical/grid)
- ✅ Responsive design (mobile stacks vertically)
- ✅ Not cluttered - AI decides when multi-chart adds value

---

## 🔍 Technical Considerations

### Performance
- Gap filling: O(n log n) for sorting, minimal overhead
- Multi-chart detection: Still <100ms total
- Frontend rendering: Recharts handles multiple charts well
- Limit: Max 3 charts per query to avoid overload

### Backward Compatibility
- Single-chart queries still work
- `y_columns` deprecated but supported via migration
- Frontend gracefully handles old ChartConfig format

### Edge Cases
- No numeric data → No charts (existing behavior)
- All nulls after gap filling → Chart shows empty
- Too many series (>5) → Trim to top 5 by variance
- Mobile layout → Always vertical stacking

---

## 🚀 Rollout Plan

1. **Develop in feature branch**: `feature/enhanced-visualizations`
2. **Test thoroughly**: All unit + integration tests passing
3. **Deploy to dev environment**: Verify with real queries
4. **User testing**: Get feedback on multi-chart UX
5. **Merge to main**: After approval
6. **Deploy to production**: With rollback plan
7. **Monitor**: Track chart rendering performance, user engagement

---

**Status**: Ready for implementation  
**Estimated Time**: 7 hours total (3 sprints)  
**Version Target**: 3.4.0  
**Release Date**: TBD

