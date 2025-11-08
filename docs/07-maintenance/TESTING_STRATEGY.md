# Testing Strategy for API Rate Limit Mitigation

**Date**: October 31, 2025  
**Issue**: Google Gemini API rate limits prevent tests from running (50 req/day free tier)  
**Current**: 77 tests total, many fail due to rate limits  
**Goal**: 100% tests passing with proper mocking

---

## Problem Analysis

### Root Cause
- Google Gemini API has 50 requests/day limit per API key (free tier)
- Project uses 11 API keys, but tests exhaust all within minutes
- Integration tests call real API during test runs
- No mocking strategy for AI-powered features

### Affected Tests
1. `tests/integration/test_llm_summarizer.py` - 4 tests calling `/ask` endpoint  
2. `tests/unit/test_query_engine.py` - 9 integration tests calling `QueryEngine.ask()`  
3. `tests/integration/test_api.py` - 8 tests calling `/query` endpoint

---

## Solution: Multi-Layer Mocking Strategy

### Layer 1: Mock `generate_text` Function
**Location**: `src.utils.llm.generate_text` and `src.core.summarizer.generate_text`  
**Why**: This is the lowest-level function that calls Google Gemini API  
**How**: Use `unittest.mock.patch` to intercept and return mock responses

### Layer 2: Mock `QueryEngine.generate_sql`  
**Location**: `src.core.query_engine.QueryEngine.generate_sql`  
**Why**: For tests that need SQL generation without AI  
**How**: Use `patch.object()` to return pre-defined SQL based on question patterns

### Layer 3: Mark Real API Tests
**Marker**: `@pytest.mark.requires_api`  
**Why**: Allow selective running of tests (skip API tests by default)  
**How**: Use pytest markers defined in `conftest.py`

---

## Implementation Plan

### Step 1: Fix `tests/integration/test_llm_summarizer.py` ✅
**Status**: DONE  
**Changes**:
- Mock `src.core.summarizer.generate_text` 
- Return context-aware mock summaries based on question
- Fixed response format assertions (genMs/execMs)

### Step 2: Create Reusable Mock Fixtures
**File**: `tests/conftest.py`  
**Add**:
```python
@pytest.fixture
def mock_gemini_api():
    """Mock all Gemini API calls"""
    def mock_generate_text(system_prompt, user_prompt, **kwargs):
        # Context-aware mock responses
        pass
    
    with patch('src.utils.llm.generate_text', side_effect=mock_generate_text), \
         patch('src.core.summarizer.generate_text', side_effect=mock_generate_text):
        yield

@pytest.fixture
def mock_sql_generation():
    """Mock SQL generation without AI"""
    def mock_gen_sql(question):
        # Pattern-based SQL generation
        pass
    
    with patch.object(QueryEngine, 'generate_sql', side_effect=mock_gen_sql):
        yield
```

### Step 3: Update Unit Tests
**File**: `tests/unit/test_query_engine.py`  
**Strategy**: Use `mock_sql_generation` fixture for all integration tests  
**Status**: TO DO

### Step 4: Update Integration Tests  
**File**: `tests/integration/test_api.py`  
**Strategy**: Use `mock_gemini_api` fixture  
**Status**: TO DO

### Step 5: Add pytest Markers
**File**: `tests/conftest.py`  
**Add**: `requires_api` marker already defined ✅  
**Usage**: Mark tests that intentionally hit real API

---

## Testing Commands

```bash
# Run all tests (with mocks, no API calls)
make test

# Run only tests that don't require API
make test-no-api

# Run with real API (for manual verification)
pytest -m requires_api

# Run with coverage
make test-cov
```

---

## Documentation Updates Needed

1. ✅ `.github/copilot-instructions.md` - Document mocking strategy
2. ⏳ `docs/04-development/setup.md` - Add testing best practices
3. ⏳ `docs/README.md` - Update test count after fixes
4. ⏳ `tests/README.md` - Create testing guide (NEW FILE)

---

## Expected Outcome

- **Before**: 58 passed, 9 failed, 10 errors (rate limits)
- **After**: 77 passed, 0 failed, 0 errors (all mocked)
- **Coverage**: Maintain 80%+ coverage
- **Speed**: Tests complete in <60 seconds (no network calls)

---

## Rollback Plan

If mocking breaks functionality:
1. Revert `tests/unit/test_query_engine.py` changes
2. Revert `tests/conftest.py` changes  
3. Keep `tests/integration/test_llm_summarizer.py` (already working)
4. Document partial success in this file
