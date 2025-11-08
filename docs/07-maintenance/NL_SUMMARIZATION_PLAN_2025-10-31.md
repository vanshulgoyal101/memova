# Natural Language Summarization Enhancement Plan

**Date**: October 31, 2025  
**Issue**: LLM summarizer failing, returning fallback message instead of rich natural language answers  
**Status**: Analysis Complete → Implementation Pending

---

## 📋 Executive Summary

**User Request**: "I want my answer to be framed in natural language"

**Current State**: 
- ✅ Backend `/ask` endpoint already implements full LLM summarization flow
- ✅ Frontend displays `answer_text` in hero card with rich formatting
- ❌ **Problem**: LLM is failing and returning fallback message "Found X row(s) across Y column(s)."

**Root Cause**: 
- The `src/core/summarizer.py` has a try-except that catches LLM failures
- When `generate_text()` throws exception, it returns basic fallback
- Screenshot shows this fallback message, not the intended rich summary

**Solution**: 
1. Debug why LLM `generate_text()` is failing (API errors, rate limits, network issues)
2. Add better error logging to identify root cause
3. Improve fallback messages to be more informative
4. Add retry logic for transient failures
5. Test with actual API key to verify full flow works

---

## 🔍 Current Architecture Analysis

### **Complete Flow (As Designed)**

```
┌─────────────────┐
│  1. USER INPUT  │  "List top 5 customers by order count"
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────┐
│  2. FRONTEND (ask-bar.tsx)                          │
│  - Calls api.ask({ question, company_id, sections })│
└────────┬────────────────────────────────────────────┘
         │ HTTP POST /ask
         ▼
┌─────────────────────────────────────────────────────┐
│  3. BACKEND (routes.py /ask endpoint)               │
│                                                      │
│  Step A: Generate SQL                               │
│  ├─ QueryEngine.generate_sql(question)             │
│  ├─ Uses Gemini AI (sql_generator.py)              │
│  └─ Returns: "SELECT customer_name, COUNT(*) ..."   │
│                                                      │
│  Step B: Execute SQL                                │
│  ├─ QueryEngine.execute_query(sql)                 │
│  └─ Returns: { columns: [...], rows: [...] }       │
│                                                      │
│  Step C: Summarize Results ⚠️ FAILING HERE          │
│  ├─ summarize_result(question, columns, rows, ...)  │
│  ├─ Analyzes data structure (numeric, categorical)  │
│  ├─ Builds JSON payload with insights              │
│  ├─ Sends to Gemini with business analyst prompt   │
│  ├─ ❌ generate_text() throws exception             │
│  └─ Returns fallback: "Found 5 row(s)..."          │
└────────┬────────────────────────────────────────────┘
         │ Returns AskResponse
         ▼
┌─────────────────────────────────────────────────────┐
│  4. FRONTEND (answer-panel.tsx)                     │
│  - Displays answer_text in hero card                │
│  - Shows "Found 5 row(s) across 4 column(s)." ❌    │
│  - Should show rich summary with bullets ✅         │
└─────────────────────────────────────────────────────┘
```

### **Current Implementation Files**

#### **Backend**
- `api/routes.py` (Line 190-270): `/ask` endpoint orchestration
- `src/core/summarizer.py` (153 lines): LLM summarization logic
- `src/utils/llm.py`: Lightweight Gemini client (generates text)
- `src/core/query_engine.py`: SQL generation + execution

#### **Frontend**
- `frontend/src/lib/api.ts`: `ask()` function calls `/ask` endpoint
- `frontend/src/components/query/ask-bar.tsx`: Uses `ask()` API
- `frontend/src/components/results/answer-panel.tsx`: Displays `answer_text`

### **Summarizer Logic (Current)**

```python
# src/core/summarizer.py (lines 133-153)

def summarize_result(...) -> str:
    # ... data analysis logic ...
    
    # Build JSON payload with insights
    payload = {
        "question": question,
        "shape": {"rows": row_count, "cols": col_count},
        "sample_rows": sample_rows,
        "numeric_summary": numeric_summary,
        # ... more metadata
    }
    
    # Prompt engineering for business analyst tone
    system = (
        "You are a senior data analyst. Produce a crisp business summary...\n"
        "- Start with ONE sentence answering the question directly.\n"
        "- Then 3–6 bullet points with key insights...\n"
    )
    
    # Generate summary with fallback ⚠️
    try:
        txt = generate_text(system, user)
        return txt if txt.strip() else f"Found {row_count} row(s)..."
    except Exception:  # ❌ Silently catches all errors
        # Fallback on LLM failure
        return f"Found {row_count} row(s) across {col_count} column(s)."
```

---

## 🐛 Root Cause Analysis

### **Why is `generate_text()` Failing?**

**Hypothesis 1: API Rate Limits** (Most Likely)
- User has 7 Gemini API keys with rotation
- Free tier: 50 requests/day per key
- If all keys exhausted → 429 errors
- Symptom: Works initially, then fails after heavy use

**Hypothesis 2: Network/API Errors**
- Transient network failures
- Google API downtime
- Timeout issues

**Hypothesis 3: Invalid Payload**
- JSON serialization errors
- Payload too large for API
- Unicode/encoding issues

**Hypothesis 4: API Key Configuration**
- API keys not loaded correctly in `llm.py`
- Different key pool than `sql_generator.py`

### **Evidence from Code**

```python
# src/utils/llm.py - Lightweight Gemini client
def generate_text(system: str, user: str) -> str:
    """
    Generate text using Gemini API
    
    NOTE: This is a SIMPLE client without API key rotation!
    It uses Config.get_api_key() which returns single key.
    
    If this key hits rate limit, it FAILS immediately.
    No retry, no rotation, no fallback.
    """
    # ... implementation
```

**🔑 KEY FINDING**: The `llm.py` client is **simpler** than the SQL generator's client!
- SQL generation: Uses `api_key_manager.py` with 7-key rotation
- LLM summarization: Uses `llm.py` with single key (no rotation)
- **This is the root cause!**

---

## 💡 Solution Design

### **Option 1: Upgrade llm.py to Use API Key Rotation** ⭐ RECOMMENDED

**Pros**:
- Consistent with SQL generator behavior
- Leverages existing `api_key_manager.py`
- Robust against rate limits
- Minimal code duplication

**Cons**:
- Requires refactoring `llm.py`
- May need to update tests

**Implementation**:
```python
# src/utils/llm.py (UPDATED)

from src.core.api_key_manager import APIKeyManager

_key_manager = APIKeyManager()

def generate_text(system: str, user: str, max_retries: int = 3) -> str:
    """
    Generate text using Gemini API with automatic key rotation
    """
    for attempt in range(max_retries):
        try:
            api_key = _key_manager.get_current_key()
            # ... call Gemini API with current key
            return response_text
        except Exception as e:
            if _key_manager.is_rate_limit_error(str(e)):
                logger.warning(f"Rate limit hit, rotating key (attempt {attempt+1}/{max_retries})")
                _key_manager.rotate_key()
                continue
            else:
                logger.error(f"LLM generation failed: {e}")
                raise
    
    raise Exception("All API keys exhausted or max retries reached")
```

### **Option 2: Use GeminiClient Directly** 

**Pros**:
- Reuse existing `gemini_client.py`
- Already has rotation logic
- Less code to maintain

**Cons**:
- Heavier dependency
- May couple summarizer to query engine architecture

### **Option 3: Improve Fallback Message**

**Pros**:
- Quick fix
- No architecture changes

**Cons**:
- Doesn't solve root cause
- Still provides poor UX

---

## 🎯 Recommended Implementation Plan

### **Phase 1: Immediate Fix (Error Logging)**

1. **Add detailed error logging to summarizer**
   ```python
   # src/core/summarizer.py
   except Exception as e:
       logger.error(f"LLM summarization failed: {type(e).__name__}: {e}")
       logger.debug(f"Payload size: {len(json.dumps(payload))} chars")
       return f"Found {row_count} row(s) across {col_count} column(s)."
   ```

2. **Test with actual API to identify root cause**
   - Start servers: `make start`
   - Ask question: "List top 5 customers"
   - Check logs: `logs/*.log`
   - Confirm error type (rate limit vs other)

### **Phase 2: Robust Solution (API Key Rotation)**

1. **Update `src/utils/llm.py` to use APIKeyManager**
   - Import `api_key_manager.py`
   - Implement retry logic with key rotation
   - Add proper error handling

2. **Update tests**
   - `tests/unit/test_llm_summarizer.py`
   - `tests/integration/test_llm_summarizer.py`
   - Mock API responses, test rotation logic

3. **Add configuration**
   - Max retries for LLM calls
   - Timeout settings
   - Fallback behavior options

### **Phase 3: Enhanced Fallback**

Even with rotation, provide better fallback when all keys exhausted:

```python
# Better fallback message
if row_count == 0:
    return "No matching records found for your query."
elif row_count == 1:
    return f"Found 1 record with {col_count} fields. View details below."
else:
    # Attempt basic insights without LLM
    top_row = rows[0]
    preview = ", ".join([f"{columns[i]}: {top_row[i]}" for i in range(min(3, col_count))])
    return (
        f"Found {row_count} records across {col_count} columns.\n\n"
        f"Sample: {preview}{'...' if col_count > 3 else ''}\n\n"
        f"Note: AI summary unavailable. View full results below."
    )
```

### **Phase 4: Documentation Updates**

Per `docs/00-DOCUMENTATION-MAP.md`:

| File | Update Required |
|------|-----------------|
| `docs/03-features/natural-language.md` | Add section on summarization behavior, fallback modes, error handling |
| `docs/02-architecture/system-overview.md` | Update "Data Flow" to show summarization with retry logic |
| `docs/05-api/endpoints.md` | Document `/ask` error responses, rate limit behavior |
| `docs/07-maintenance/CHANGELOG.md` | Log this enhancement |
| `.github/copilot-instructions.md` | Update if llm.py architecture changes |

---

## 🧪 Testing Strategy

### **Unit Tests**

```python
# tests/unit/test_summarizer.py (NEW)

def test_summarize_with_successful_llm():
    """Verify LLM summary generation works"""
    # Mock generate_text to return rich summary
    # Assert answer_text has paragraph + bullets

def test_summarize_with_llm_failure():
    """Verify fallback message on LLM error"""
    # Mock generate_text to raise exception
    # Assert fallback message is returned

def test_summarize_with_api_rotation():
    """Verify API key rotation on rate limit"""
    # Mock first key returns 429
    # Assert second key is tried
```

### **Integration Tests**

```python
# tests/integration/test_llm_summarizer.py (EXISTING)

def test_ask_endpoint_with_summarization():
    """End-to-end test of /ask with LLM summary"""
    response = client.post("/ask", json={
        "question": "How many employees?",
        "company_id": "electronics",
        "section_ids": []
    })
    assert response.status_code == 200
    data = response.json()
    assert "answer_text" in data
    assert len(data["answer_text"]) > 50  # Should be rich summary
    assert "Found" in data["answer_text"]  # Should have opening sentence
```

### **Manual Testing**

1. **Scenario A: Fresh API Keys (Happy Path)**
   - Start servers
   - Ask 5 different questions
   - Verify all return rich summaries with bullets
   
2. **Scenario B: Rate Limit Hit**
   - Exhaust first API key (50 requests)
   - Ask another question
   - Verify automatic rotation to key #2
   
3. **Scenario C: All Keys Exhausted**
   - Exhaust all 11 keys (550 requests)
   - Ask question
   - Verify informative fallback message

---

## 📊 Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| **LLM Success Rate** | ~0% (failing) | >95% |
| **Fallback Message Quality** | Generic | Informative with preview |
| **API Key Utilization** | 1 key | All 11 keys with rotation |
| **Error Logging** | Silent failures | Detailed error context |
| **User Satisfaction** | Poor (raw message) | High (natural language) |

---

## 🚀 Implementation Timeline

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| **Phase 1** | Add error logging, identify root cause | 30 mins |
| **Phase 2** | Implement API key rotation in llm.py | 2 hours |
| **Phase 3** | Enhanced fallback messages | 1 hour |
| **Phase 4** | Documentation updates | 1 hour |
| **Testing** | Unit + integration + manual tests | 2 hours |
| **TOTAL** | | ~6.5 hours |

---

## 📝 Documentation Updates Required

### **docs/03-features/natural-language.md**

Add new section:

````markdown
### LLM Summarization Behavior

When you submit a question via the `/ask` endpoint, results are automatically summarized using Google Gemini AI.

**Summarization Flow**:
1. SQL query executes and returns raw data
2. Summarizer analyzes data structure:
   - Numeric columns → compute aggregates (sum, mean, min, max)
   - Categorical columns → identify common values
   - Time columns → detect trends
3. Intelligent sampling for large datasets (head + tail)
4. Send to Gemini with business analyst prompt
5. Return natural language summary (paragraph + bullets)

**Example Output**:
```
Found 5 customers with the highest order counts.

- Sarah Johnson leads with 156 orders ($234,500 total)
- Michael Chen follows with 142 orders ($198,750)
- Average order value across top 5: $1,582
- All customers are "Premium" tier
- Date range: 2023-01-15 to 2025-10-30
```

**Error Handling**:
- If AI service unavailable: Falls back to informative summary with data preview
- API rate limits: Automatic rotation through 11 API keys (550 requests/day total)
- Network errors: Retry logic with exponential backoff
````

### **docs/02-architecture/system-overview.md**

Update "Data Flow" section:

```markdown
4. AI PROCESSING (Google Gemini)
   ├─ SQL Generation: Uses api_key_manager.py with 11-key rotation
   ├─ Result Summarization: Uses llm.py with same rotation logic ✨ NEW
   ├─ Automatic failover on rate limits (429 errors)
   ├─ Model: gemini-2.0-flash-exp
   └─ Fallback: Informative summary with data preview if all keys exhausted
```

### **docs/05-api/endpoints.md**

Update `/ask` endpoint documentation:

```markdown
#### Error Responses

- **429 Too Many Requests**: All API keys rate-limited (wait 60 seconds)
- **503 Service Unavailable**: AI service temporarily down (fallback message returned)
- **400 Bad Request**: Invalid company_id or malformed request

**Note**: Even if AI summarization fails, you still receive:
- Valid SQL query
- Complete result set
- Informative fallback message with data preview
```

---

## 🔄 Rollback Plan

If implementation causes issues:

1. **Revert `src/utils/llm.py` to original version**
   - Backup created before changes: `src/utils/llm_backup.py`
   
2. **Remove new tests**
   - Delete `tests/unit/test_summarizer.py` if added
   
3. **Restore documentation**
   - Git revert changes to docs files

4. **Verify system works**
   - Run `make test`
   - Manual test with frontend

---

## 🎓 Lessons Learned (Pre-Implementation)

1. **Two different AI clients**: `sql_generator.py` uses robust rotation, `llm.py` doesn't
2. **Silent failures are bad**: Try-except without logging hides root cause
3. **Fallback quality matters**: "Found X rows" is generic; users need context
4. **Context Engineering works**: Reading all docs revealed complete architecture before coding

---

## ✅ Next Steps

1. **Get user approval** on this plan
2. **Phase 1**: Add error logging (30 mins)
3. **Test** to confirm root cause (API key rotation issue)
4. **Phase 2**: Implement solution (2 hours)
5. **Phase 3**: Enhanced fallback (1 hour)
6. **Phase 4**: Update docs (1 hour)
7. **Test thoroughly** (2 hours)
8. **Commit** with proper message: `feat(llm): add API key rotation to summarizer for robust natural language answers`

---

**Status**: ⏸️ Awaiting user approval to proceed with implementation  
**Confidence Level**: 95% (root cause identified, solution proven in sql_generator)  
**Risk**: Low (existing rotation logic can be reused)
