# Token Usage Monitoring - Quick Reference

**Date**: November 6, 2025  
**Purpose**: Monitor token usage to verify prompt caching is working  

---

## Current Status

### Groq Rate Limits (as of testing)
- **Org 1**: 99,537 / 100,000 tokens used (99.5%)
- **Org 2**: 99,153 / 100,000 tokens used (99.1%)
- **Status**: Rate limited until midnight UTC reset

### Token Logging Added
✅ Added comprehensive token logging to `src/core/groq_client.py`:
```python
logger.info(f"🔢 Groq tokens: {total} total ({prompt} prompt + {completion} completion)")
```

### Test Script Created
✅ Created `test_token_caching.py` - comprehensive caching verification

---

## How to Test Token Usage

### Run the Test Script
```bash
cd "/Volumes/Extreme SSD/code/sql schema"
.venv/bin/python3 test_token_caching.py
```

### What to Look For

**In the logs:**
1. Lines with `🔢 Groq tokens:` showing token counts
2. Lines with `✅ Cache hit:` showing cached tokens
3. Token reduction from first to second analytical query

**Expected Results (WITH caching):**

**Test 1: Simple Data Query**
```
🔢 Groq tokens: 1556 total (1548 prompt + 8 completion)
```

**Test 2: First Analytical Query (Cold - No Cache)**
```
Call 1: 🔢 Groq tokens: 2600 total (2550 prompt + 50 completion)  # Schema cached
Call 2: 🔢 Groq tokens: 250 total (200 prompt + 50 completion)    # Cache hit
Call 3: 🔢 Groq tokens: 500 total (450 prompt + 50 completion)    # Cache hit
Total: ~3,350 tokens
```

**Test 3: Second Analytical Query (Warm - Cache Hit)**
```
Call 1: 🔢 Groq tokens: 100 total (50 prompt + 50 completion)     # Cache hit
Call 2: 🔢 Groq tokens: 250 total (200 prompt + 50 completion)    # Cache hit
Call 3: 🔢 Groq tokens: 500 total (450 prompt + 50 completion)    # Cache hit
Total: ~850 tokens (75% reduction!)
```

---

## Token Budget Analysis

### Before Caching Fix
- **Per analytical query**: ~5,700 tokens (3 calls × ~1,900 avg)
- **Daily capacity**: 100,000 / 5,700 = **17 analyses/day**

### After Caching Fix (Expected)
- **First query (cold)**: ~3,350 tokens
- **Subsequent (warm)**: ~850 tokens each
- **Daily capacity (warm)**: 100,000 / 850 = **117 analyses/day**
- **Improvement**: **7x increase in capacity**

### Mixed Usage Pattern
```
1 cold + 99 warm queries:
  3,350 + (99 × 850) = 87,500 tokens
  = 100 analytical queries/day
```

---

## Interpreting Results

### ✅ Caching is Working If:
- Token counts drop significantly (50-75%) from cold to warm
- Warm queries use ~850 tokens total
- You see `✅ Cache hit:` in logs
- Performance improves 20-40% on warm queries

### ⚠️ Caching May Not Be Working If:
- Token counts stay around 1,500-2,500 per call
- No significant reduction from cold to warm
- Each call shows ~2,500 prompt tokens
- No cache hit messages in logs

### 🔍 Debugging Steps

1. **Check System Message Consistency**
   ```python
   # In analyst.py - should be same for all calls
   self.system_message = f"{schema}\n\nYou are an expert business analyst..."
   ```

2. **Verify Groq Client Usage**
   ```python
   # All calls should pass system_message parameter
   llm_client.generate_content(user_msg, system_message=self.system_message)
   ```

3. **Check Token Logs**
   ```bash
   # Grep for token usage in test output
   python test_token_caching.py 2>&1 | grep "🔢 Groq tokens"
   ```

---

## Current Token Usage (From Error Messages)

When hitting rate limits, error messages show:
```
Used 99537, Requested 1546  # Org 1
Used 99153, Requested 1546  # Org 2
```

This tells us:
- **Request size**: ~1,546 tokens per call
- **With caching**: Should drop to ~50-500 tokens

---

## Next Steps

### When Groq Limits Reset (Midnight UTC)
1. Run `test_token_caching.py`
2. Verify token counts in logs
3. Confirm 75% reduction on warm queries
4. Document actual token savings

### If Caching Not Working
1. Check `analyst.py` - verify `self.system_message` is shared
2. Check all 3 methods use same system message
3. Verify no string concatenation modifying system message
4. Test with simple queries first

### To Increase Capacity Now
- Create Groq accounts with different emails
- Get API keys from each account (different organizations)
- Add to `.env` file
- System will rotate across organizations

---

## Files Modified

- ✅ `src/core/groq_client.py` - Added token usage logging
- ✅ `src/core/analyst.py` - Shared system message for caching
- ✅ `test_token_caching.py` - Comprehensive caching test

---

## Commands

### Quick Token Check
```bash
# Run simple query and check tokens
cd "/Volumes/Extreme SSD/code/sql schema"
.venv/bin/python3 -c "
from src.core.query_engine import QueryEngine
engine = QueryEngine(db_path='data/database/electronics_company.db')
result = engine.ask('How many products?')
" 2>&1 | grep "🔢 Groq tokens"
```

### Full Caching Test
```bash
# Run comprehensive test
.venv/bin/python3 test_token_caching.py
```

### Monitor Daily Usage
```bash
# Extract token usage from error messages
.venv/bin/python3 test_token_caching.py 2>&1 | grep -E "Used [0-9]+, Requested"
```

---

**Note**: Groq rate limits reset at **00:00 UTC** daily. Plan testing accordingly.
