"""
Pydantic Models for API Request/Response
All data validation schemas for FastAPI endpoints
"""

from pydantic import BaseModel
from typing import List, Optional, Any, Dict, Literal


# Type aliases
ChartType = Literal["line", "bar", "horizontal_bar", "pie", "doughnut", "histogram", "area", "stacked_area", "stacked_bar", "grouped_bar", "combo", "scatter", "bubble", "none"]
TrendType = Literal["growth", "decline", "flat", "outlier", "distribution", "seasonality"]
QueryStatusType = Literal["pending", "executing", "completed", "failed"]
SeriesType = Literal["line", "bar", "area"]  # For combo charts


# Request Models

class AskRequest(BaseModel):
    """Request model for /ask endpoint with AI-generated answer"""
    question: str
    company_id: str  # 'electronics' or 'airline'
    section_ids: List[str] = []


class QueryRequest(BaseModel):
    """Request model for /query endpoint (raw results)"""
    question: str
    database: str


# Response Models

class ChartSeries(BaseModel):
    """Series configuration for multi-series charts"""
    name: str  # Display name (e.g., "Revenue", "Cost")
    column: str  # Data column name
    type: Optional[SeriesType] = None  # "line", "bar", "area" - for combo charts
    color: Optional[str] = None  # Hex color code
    yAxisId: Optional[str] = None  # For dual-axis charts (left/right)


class ChartConfig(BaseModel):
    """Chart configuration for visualizing query results"""
    id: str
    type: ChartType
    title: str
    x_column: str
    # Backwards-compatible: y_columns remains for older detectors
    y_columns: Optional[List[str]] = None
    # New richer series model for multi-series / stacked / combo charts
    series: Optional[List[ChartSeries]] = None
    data: List[Dict[str, Any]]
    x_type: str  # "date", "category", "numeric"
    confidence: float  # 0.0 - 1.0
    # Optional metadata
    granularity: Optional[str] = None  # "daily", "weekly", "monthly"
    chart_group: Optional[int] = None  # For grouping related charts
    stacked: Optional[bool] = None  # For stacked bar/area charts
    dual_axis: Optional[bool] = None  # If chart uses two Y axes
    layout_hint: Optional[str] = None  # "single", "horizontal", "vertical", "grid"


class TrendInsight(BaseModel):
    """Trend insight detected from query results"""
    id: str
    type: TrendType
    title: str
    description: str
    confidence: float  # 0.0 - 1.0
    metrics: Dict[str, Any]
    columns: List[str]


class BusinessAnalysis(BaseModel):
    """Business analysis result for strategic questions"""
    analysis_text: str  # Full markdown analysis with insights + recommendations
    insights: List[str]  # Key insights (3-5 bullets)
    recommendations: List[str]  # Actionable steps (5-7 items)
    data_points: List[Dict[str, Any]]  # Key metrics extracted
    queries_used: List[str]  # Exploratory queries that gathered data
    success: bool = True


class QueryStepModel(BaseModel):
    """Single query step in a multi-query plan"""
    id: str
    description: str
    sql: str
    depends_on: List[str]
    status: QueryStatusType
    row_count: Optional[int] = None
    execution_time_ms: Optional[float] = None
    error: Optional[str] = None
    results: Optional[Dict[str, Any]] = None  # Intermediate data: {columns: [...], rows: [...]}


class QueryPlanModel(BaseModel):
    """Multi-query execution plan"""
    queries: List[QueryStepModel]
    final_query_id: str
    question: Optional[str] = None
    total_execution_time_ms: Optional[float] = None
    is_complete: bool = False
    has_errors: bool = False


class AskResponse(BaseModel):
    """Response model for /ask endpoint with natural language answer"""
    answer_text: str  # AI-generated natural language summary
    sql: Optional[str] = None  # SQL query (if data query)
    columns: Optional[List[str]] = None  # Result columns (if data query)
    rows: Optional[List[List[Any]]] = None  # Result rows (if data query)
    charts: Optional[List[ChartConfig]] = None  # Auto-detected charts
    trends: Optional[List[TrendInsight]] = None  # Auto-detected trends
    analysis: Optional[BusinessAnalysis] = None  # Business analysis (if analytical query)
    query_type: str = "data"  # "data" or "analytical"
    query_plan: Optional[QueryPlanModel] = None  # Multi-query plan (if used)
    timings: Optional[Dict[str, float]] = None
    meta: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """Response model for /query endpoint (legacy)"""
    success: bool
    sql: str
    columns: List[str]
    rows: List[List[Any]]
    row_count: int
    execution_time: float
    charts: Optional[List[ChartConfig]] = None  # Auto-detected charts
    trends: Optional[List[TrendInsight]] = None  # Auto-detected trends
    query_plan: Optional[QueryPlanModel] = None  # Multi-query plan (if used)
    error: Optional[str] = None


# Database Information Models

class DatabaseInfo(BaseModel):
    """Database metadata"""
    id: str
    name: str
    path: str
    exists: bool
    size_mb: Optional[float] = None
    table_count: Optional[int] = None


class SchemaInfo(BaseModel):
    """Database schema information"""
    tables: List[Dict[str, Any]]  # Changed from Dict to List for compatibility
    table_count: int


class ExampleQuery(BaseModel):
    """Example query for database"""
    id: int = 0
    title: str = ""  # Added title field
    question: str
    category: str
    complexity: str  # Changed from difficulty to complexity


# Upload Models

class UploadResponse(BaseModel):
    """Response model for /upload endpoint"""
    upload_id: str
    database_name: str
    database_path: str
    detected_schema: Dict[str, Any]  # Renamed from 'schema' to avoid shadowing
    table_count: int
    total_rows: int
    relationships: int
    message: str


class UploadedDatabase(BaseModel):
    """Information about an uploaded database"""
    id: str
    name: str
    upload_date: str
    table_count: int
    total_rows: int
    size_mb: float
