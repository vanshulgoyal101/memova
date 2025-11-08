# Adding Your New Groq API Key

You mentioned creating a new Groq API key from a different account. Here's how to add it:

## Step 1: Edit .env File

```bash
cd "/Volumes/Extreme SSD/code/sql schema"
nano .env  # or use your preferred editor
```

## Step 2: Add New Key

Find the `GROQ_API_KEY` lines and add your new key:

```bash
# Groq API Keys (rate limits are per-organization)
# Primary Groq keys (from first account/organization)
GROQ_API_KEY=gsk_L9iNyFztQaUIc9IZpWgdWGdyb3FYKkQnFWCTqIl...  # Key 1
#GROQ_API_KEY=gsk_XwOMAzJFAi7OHbVPUXsJWGdyb3FYIXjCZzRkVGS...  # Key 2
#GROQ_API_KEY=gsk_VG0wWJjx8OGLs76xHm2eWGdyb3FYWq5k7yWd3vp...  # Key 3
#GROQ_API_KEY=gsk_GGQqH6g8pGu8uN9ZR4YhWGdyb3FYMsZ4xPpKLnB...  # Key 4

# NEW: Keys from second account/organization (separate quota!)
GROQ_API_KEY=YOUR_NEW_KEY_HERE  # Key 5 (from different account)
```

**Important:**
- The new key should be from a **different email/account** than the first 4 keys
- This gives you an additional 100K tokens/day quota (separate organization)
- Keys from the same organization share the 100K/day limit

## Step 3: Verify

Restart the backend and check logs:

```bash
make restart
# Look for: "INFO - Loaded 5 Groq API key(s) for rotation"
```

## Step 4: Test

```bash
python3 << 'EOF'
from src.core.query_engine import QueryEngine

engine = QueryEngine(db_path='data/database/electronics_company.db')
result = engine.ask("How many employees?")
print(f"Success: {result['success']}")
print(f"SQL: {result['sql']}")
EOF
```

## Expected Behavior

With 5 keys across 2 organizations:
- **First 4 keys**: Share 100K tokens/day (organization 1)
- **New key (5th)**: Separate 100K tokens/day (organization 2)
- **Total capacity**: 200K tokens/day
- **With caching**: Effective ~4000-5000 queries/day

## Quota Monitoring

Check current usage at: https://console.groq.com/settings/billing

Each organization shows its own usage separately.
