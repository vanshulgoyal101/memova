# Testing Guide

## Test Organization

The test suite is organized into **fast tests** and **slow tests** to optimize CI/CD performance and avoid API rate limits.

### Fast Tests (63 tests)
**Run with**: `pytest -m "not slow"`

These tests:
- ✅ Execute in ~25 seconds
- ✅ No external API calls (mocked or unit tests)
- ✅ Always pass consistently
- ✅ Safe for CI/CD pipelines
- ✅ 100% pass rate expected

**When to use**: Development, CI/CD, pre-commit hooks

### Slow Tests (14 tests)
**Run with**: `pytest -m slow`

These tests:
- ⚠️ Make real Groq/Gemini API calls
- ⚠️ May hit rate limits (Groq: 100k tokens/day, Gemini: 50 req/day)
- ⚠️ Take longer to execute (~2-3 minutes)
- ⚠️ May fail due to quota exhaustion (expected behavior)
- ✅ Validate end-to-end integration

**When to use**: Weekly integration testing, pre-deployment validation

**Slow test categories**:
- `tests/integration/test_api.py` (7 tests) - Full API query execution
- `tests/integration/test_llm_summarizer.py` (4 tests) - LLM answer generation
- `tests/unit/test_query_engine.py` (3 tests) - SQL generation with real AI

## Running Tests

### Development Workflow
```bash
# Fast iteration during coding
pytest -m "not slow" -q

# Detailed output for debugging
pytest -m "not slow" -v

# Single test file
pytest tests/unit/test_database.py -v
```

### Pre-Deployment Validation
```bash
# Run all tests (fast + slow)
pytest tests/ -v

# Fast tests only (should always pass)
pytest -m "not slow" -v

# Slow tests only (verify integration)
pytest -m slow -v --tb=short
```

### Coverage Reporting
```bash
# Full coverage with HTML report
make test-cov

# Coverage for fast tests only
pytest -m "not slow" --cov=src --cov-report=html
```

## Test Metrics

- **Total Tests**: 77
  - Fast: 63 (82%)
  - Slow: 14 (18%)
- **Expected Pass Rate**:
  - Fast: 100% (63/63)
  - Slow: Variable (depends on API quotas)
  - Combined: ~90-95% (quota-dependent)
- **Execution Time**:
  - Fast: ~25 seconds
  - Slow: ~120-180 seconds (with API delays)
  - Total: ~3-4 minutes

## Continuous Integration

**Recommended CI/CD strategy**:

```yaml
# .github/workflows/tests.yml
- name: Run fast tests
  run: pytest -m "not slow" --cov=src

- name: Run slow tests (weekly only)
  if: github.event.schedule == 'weekly'
  run: pytest -m slow --tb=short
  continue-on-error: true  # Don't fail build on quota errors
```

## Troubleshooting

### All Slow Tests Failing
**Symptom**: `pytest -m slow` shows rate limit errors

**Cause**: API quota exhausted (expected after multiple runs)

**Solution**:
- Wait 24 hours for quota reset
- Or run fast tests only: `pytest -m "not slow"`

### Fast Tests Failing
**Symptom**: `pytest -m "not slow"` shows failures

**Cause**: Code regression or broken mocks

**Action**: **Investigate immediately** - fast tests should always pass

### Coverage Drop
**Symptom**: Coverage < 80%

**Action**: Add unit tests (fast) for new code

## Adding New Tests

### Mark AI-Dependent Tests as Slow
```python
import pytest

class TestNewFeature:
    @pytest.mark.slow  # Uses real Groq/Gemini API
    def test_ai_query_generation(self):
        """Test SQL generation with real AI"""
        result = query_engine.query("How many employees?")
        assert result['success'] is True
```

### Keep Non-AI Tests Fast
```python
from unittest.mock import patch

class TestNewFeature:
    def test_database_connection(self):
        """Test DB connection (no AI needed)"""
        db = DatabaseManager("data/database/test.db")
        assert db.connection is not None  # Fast, always passes
```

## Test Breakdown by File

### Fast Tests Only
- `tests/unit/test_database.py` (8 tests)
- `tests/integration/test_data_generation.py` (17 tests)
- `tests/unit/test_llm_summarizer.py` (4 tests)
- `tests/integration/test_api.py` (31 tests - non-query endpoints)
- `tests/integration/test_llm_summarizer.py` (3 tests - basic format)

### Mixed (Fast + Slow)
- `tests/integration/test_api.py` (38 total: 31 fast, 7 slow)
- `tests/integration/test_llm_summarizer.py` (7 total: 3 fast, 4 slow)
- `tests/unit/test_query_engine.py` (17 total: 14 fast, 3 slow)

## Performance Benchmarks

### Groq AI (Primary)
- SQL Generation: ~0.3s
- Result Summarization: ~0.5s
- Total Query Time: ~0.8s

### Gemini AI (Fallback)
- SQL Generation: ~1.5s
- Result Summarization: ~1.0s
- Total Query Time: ~2.5s

**Speed Improvement**: 3-5x faster with Groq

---

**Last Updated**: 2025-11-06  
**Groq Migration**: Phase 10 Complete  
**Test Organization**: Fast/Slow Split Implemented
