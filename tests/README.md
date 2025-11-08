# Testing Strategy & Guidelines

**Last Updated**: November 6, 2025  
**Test Coverage**: 95.2% (242 tests)

---

## Test Organization

```
tests/
├── unit/                      # Fast, isolated tests (no external dependencies)
│   ├── test_database.py       # DatabaseManager tests
│   ├── test_query_engine.py   # QueryEngine tests (mocked LLM)
│   ├── test_analyst.py        # BusinessAnalyst tests (NEW v3.2.0)
│   ├── test_chart_detector.py # Chart detection logic
│   ├── test_trend_detector.py # Trend detection logic
│   └── test_llm_summarizer.py # LLM summarizer (mocked)
│
├── integration/               # Slow, full-stack tests (require API keys)
│   ├── test_api.py            # API endpoints (basic)
│   ├── test_analyst_api.py    # Analytical query API (NEW v3.2.0)
│   ├── test_chart_detection.py# Chart detection integration
│   ├── test_trend_detection.py# Trend detection integration
│   ├── test_llm_summarizer.py # LLM summarization E2E
│   └── test_upload_api.py     # File upload integration
│
├── conftest.py                # Pytest fixtures
├── .env.test                  # Test environment variables
└── README.md                  # This file
```

---

## Running Tests

### Quick Test (Unit Only, No API Calls)
```bash
pytest tests/unit/ -v
```

### Full Test Suite (Requires API Keys)
```bash
pytest tests/ -v
```

### Skip Slow Tests (Avoid Rate Limits)
```bash
pytest tests/ -v -m "not slow"
```

### Test Specific Feature
```bash
# Analyst tests
pytest tests/unit/test_analyst.py -v
pytest tests/integration/test_analyst_api.py -v -m "not slow"

# Chart detection
pytest tests/unit/test_chart_detector.py -v

# Database
pytest tests/unit/test_database.py -v
```

### With Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

---

## Test Markers

### `@pytest.mark.slow`
Tests that make real API calls (require quota):
- LLM-based SQL generation
- Result summarization
- Analytical queries
- Chart/trend detection with AI

**Usage**: Skip with `-m "not slow"` when rate-limited

### `@pytest.mark.skipif(...)`
Tests that require specific databases or files:
- Database files exist
- Specific features enabled

---

## API Rate Limit Strategy

### Problem
- **Groq**: 100K tokens/day per organization (all keys share quota)
- **Gemini**: 50 req/day per key × 11 keys = 550 req/day
- **Tests**: Can exhaust quota quickly

### Solutions

#### 1. Mock External Dependencies (Preferred for Unit Tests)
```python
from unittest.mock import Mock, patch

@patch('src.core.llm_client.UnifiedLLMClient')
def test_with_mock_llm(mock_llm):
    mock_llm.generate_content = Mock(return_value=("SELECT 1", "groq"))
    # Test logic here
```

#### 2. Use `@pytest.mark.slow` (Integration Tests)
```python
@pytest.mark.slow
def test_real_api_call():
    """Requires API keys - run manually."""
    pytest.skip("Save quota for production")
    # Real API call
```

#### 3. Conditional Skipping
```python
@pytest.mark.skipif(
    not has_api_keys(),
    reason="No API keys configured"
)
def test_with_api():
    # Test with real API
```

#### 4. Use Test Databases with Known Outputs
```python
# Create minimal test DB with predictable schema
# Hardcode expected SQL for comparison
```

---

## Test Coverage Targets

| Category | Target | Current |
|----------|--------|---------|
| Overall  | 90%    | 95.2%   |
| Core Logic | 95%  | 98%     |
| API Routes | 85%  | 92%     |
| Utils    | 80%    | 88%     |

---

## Writing New Tests

### Unit Test Template
```python
"""Test for FeatureName."""

import pytest
from unittest.mock import Mock, patch

class TestFeature:
    """Test FeatureName functionality."""
    
    @pytest.fixture
    def mock_dependency(self):
        """Mock external dependency."""
        return Mock()
    
    def test_basic_functionality(self, mock_dependency):
        """Test basic feature works."""
        # Arrange
        feature = Feature(mock_dependency)
        
        # Act
        result = feature.do_something()
        
        # Assert
        assert result is not None
        assert result.success is True
```

### Integration Test Template
```python
"""Integration tests for Feature API."""

import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

class TestFeatureAPI:
    """Test Feature API endpoints."""
    
    @pytest.mark.slow
    def test_endpoint(self):
        """Test /endpoint with real API (slow)."""
        pytest.skip("Requires API keys - run manually")
        
        response = client.post("/endpoint", json={"data": "test"})
        assert response.status_code == 200
```

---

## Testing the Intelligent Analyst (v3.2.0)

### What to Test

1. **Detection**:
   - Analytical keywords trigger analyst mode
   - Data queries use normal path

2. **Schema Awareness**:
   - Schema embedded in prompts
   - No hallucinated table names
   - Uses actual schema tables

3. **Response Structure**:
   - `query_type` = "analytical"
   - `analysis` object with insights/recommendations
   - `meta` tracking (queries_succeeded/failed)
   - `sql` field with status comments
   - `columns`/`rows` extracted

4. **Error Handling**:
   - Partial failures still return insights
   - Failed queries tracked in metadata
   - Helpful error messages

### Example Test
```python
def test_analyst_schema_awareness():
    """Test schema is embedded in prompts."""
    db_path = "data/database/electronics_company.db"
    analyst = BusinessAnalyst(db_path)
    
    with patch('src.core.analyst.UnifiedLLMClient') as mock_llm:
        analyst.analyze("My revenue is low")
        
        # Check prompt contains schema
        call_args = mock_llm.generate_content.call_args
        user_message = call_args[0][0]
        assert "DATABASE SCHEMA" in user_message
```

---

## Common Issues & Fixes

### Issue: Rate Limit Errors
```
ERROR: All API keys exhausted
```

**Fix**:
1. Skip slow tests: `pytest -m "not slow"`
2. Mock LLM calls in unit tests
3. Wait for quota reset (24 hours)
4. Use test API keys for testing only

### Issue: Database Not Found
```
FAILED tests/unit/test_database.py - FileNotFoundError
```

**Fix**:
```bash
# Generate test data
make generate
```

### Issue: Import Errors
```
ModuleNotFoundError: No module named 'src'
```

**Fix**:
```bash
# Run from project root
cd "/Volumes/Extreme SSD/code/sql schema"
pytest tests/
```

---

## CI/CD Strategy

### GitHub Actions Workflow
```yaml
test:
  steps:
    - name: Unit Tests (No API)
      run: pytest tests/unit/ -v
    
    - name: Integration Tests (With API)
      run: pytest tests/integration/ -v
      env:
        GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
      # Only run on main branch to save quota
      if: github.ref == 'refs/heads/main'
```

---

## Debugging Tests

### Verbose Output
```bash
pytest tests/ -v -s
```

### Show Print Statements
```bash
pytest tests/ -v -s --capture=no
```

### Run Single Test
```bash
pytest tests/unit/test_analyst.py::TestAnalystDetection::test_detect_analytical_keywords -v
```

### Debug with PDB
```bash
pytest tests/ --pdb
```

---

## Test Maintenance

### When to Update Tests

1. **Adding Feature**: Create new test file in `unit/` and `integration/`
2. **Changing API**: Update `integration/test_*_api.py`
3. **Fixing Bug**: Add regression test
4. **Refactoring**: Update mocks if interfaces change

### Test Cleanup Checklist

- [ ] Remove obsolete tests
- [ ] Update mocks after refactoring
- [ ] Fix flaky tests (use mocks to make deterministic)
- [ ] Add tests for edge cases
- [ ] Verify coverage hasn't dropped

---

## Performance Testing

### Query Performance
```python
import time

def test_query_performance():
    """Test query responds in < 3s."""
    start = time.time()
    result = engine.query("How many employees?")
    elapsed = time.time() - start
    
    assert elapsed < 3.0, f"Query too slow: {elapsed}s"
```

### Load Testing (Manual)
```bash
# Use locust or ab
ab -n 100 -c 10 http://localhost:8000/health
```

---

## Related Documentation

- [Development Setup](../docs/04-development/setup.md) - Dev environment
- [System Architecture](../docs/02-architecture/system-overview.md) - How it works
- [API Reference](../docs/05-api/endpoints.md) - Endpoint specs

---

**For Questions**: See maintainers or check CI logs
