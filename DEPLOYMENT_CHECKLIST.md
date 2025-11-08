# Memova - Vercel Deployment Checklist

Use this checklist to ensure smooth deployment to Vercel.

## Pre-Deployment Checklist

### 1. Repository Setup
- [ ] Git repository initialized
- [ ] All files committed
- [ ] `.gitignore` updated to include databases
- [ ] `.vercelignore` created
- [ ] Database files in `data/database/` directory
- [ ] No sensitive data in repository

### 2. Configuration Files
- [ ] `vercel.json` created
- [ ] `runtime.txt` specifies Python 3.11
- [ ] `requirements.txt` has all dependencies
- [ ] `api/index.py` entry point created
- [ ] `frontend/package.json` has correct build scripts

### 3. Environment Variables Ready
- [ ] `GOOGLE_API_KEY` obtained
- [ ] `GROQ_API_KEY` obtained
- [ ] API keys tested locally
- [ ] `.env.example` updated with template

### 4. Local Testing
- [ ] Backend runs: `python -m uvicorn api.main:app --reload`
- [ ] Frontend builds: `cd frontend && npm run build`
- [ ] Frontend runs: `cd frontend && npm start`
- [ ] API endpoints work: `curl http://localhost:8000/api/health`
- [ ] Database queries execute successfully
- [ ] All 5 databases accessible

### 5. Code Quality
- [ ] Tests passing: `pytest`
- [ ] No console errors in browser
- [ ] No linting errors
- [ ] Documentation up to date

---

## Deployment Steps

### Step 1: Push to GitHub
```bash
# Check git status
git status

# Add all files (ensures databases are included)
git add .

# Commit
git commit -m "feat: ready for Vercel deployment"

# Create repo and push
gh repo create memova --public --source=. --remote=origin --push
```

**Verify on GitHub:**
- [ ] Repository created
- [ ] All files pushed
- [ ] Database files visible in `data/database/`
- [ ] README displays correctly

### Step 2: Deploy to Vercel

#### Via Vercel CLI
```bash
# Install Vercel CLI (if needed)
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

#### Via Vercel Dashboard
1. [ ] Go to https://vercel.com
2. [ ] Click "New Project"
3. [ ] Import GitHub repository
4. [ ] Select `memova`
5. [ ] Configure project (should auto-detect)
6. [ ] Add environment variables (next step)
7. [ ] Click "Deploy"

### Step 3: Configure Environment Variables

In Vercel Dashboard → Settings → Environment Variables:

**Add these:**
- [ ] `GOOGLE_API_KEY` = your-gemini-key
- [ ] `GROQ_API_KEY` = your-groq-key
- [ ] `LOG_LEVEL` = INFO (optional)

**Apply to:**
- [ ] Production
- [ ] Preview
- [ ] Development

### Step 4: Verify Deployment

- [ ] Deployment completed successfully
- [ ] No build errors in logs
- [ ] Production URL accessible

---

## Post-Deployment Testing

### API Tests
```bash
# Replace with your actual URL
VERCEL_URL="https://memova.vercel.app"

# Test health endpoint
curl $VERCEL_URL/api/health

# Expected: {"status": "healthy", ...}
```

**Manual API Tests:**
- [ ] `/api/health` returns 200
- [ ] `/api/databases` lists 5 databases
- [ ] `/api/schema?database=electronics` returns schema
- [ ] `/api/examples?database=electronics` returns examples

### Frontend Tests
Open `https://memova.vercel.app` and test:

- [ ] Page loads without errors
- [ ] Theme toggle works (light/dark)
- [ ] Database selector shows 5 options
- [ ] Sidebar quick queries visible
- [ ] Settings dialog opens

### Query Tests
Try these questions:

- [ ] "How many employees?" (simple count)
- [ ] "Show top 10 customers" (complex query)
- [ ] "Give me insights to improve sales" (analytical)
- [ ] Check SQL tab shows generated query
- [ ] Check Data tab shows results
- [ ] Check Answer shows natural language summary

### Chart & Insights Tests
- [ ] Charts render when applicable
- [ ] Trends show up for time-series data
- [ ] Business analysis appears for analytical questions

### Mobile Tests
- [ ] Responsive design on mobile
- [ ] Sidebar collapses on small screens
- [ ] Touch interactions work

---

## Troubleshooting

### Build Fails

**Check:**
- [ ] View build logs in Vercel dashboard
- [ ] Verify `requirements.txt` has all dependencies
- [ ] Ensure `runtime.txt` exists
- [ ] Check Python version compatibility

**Common issues:**
```bash
# Missing dependency
# → Add to requirements.txt

# Python version mismatch
# → Update runtime.txt to python-3.11

# Frontend build error
# → Run locally: cd frontend && npm run build
```

### API Returns 500

**Check:**
- [ ] Environment variables set in Vercel
- [ ] Database files deployed (check in Vercel file browser)
- [ ] View Function logs in Vercel dashboard
- [ ] API key quota not exceeded

### Database Not Found

**Check:**
- [ ] `.gitignore` allows `.db` files
- [ ] `.vercelignore` doesn't exclude `data/database/`
- [ ] Files visible in GitHub repo
- [ ] Correct path in code: `data/database/*.db`

**Debug:**
```bash
# Check if files are in repo
git ls-files | grep .db

# Should show:
# data/database/electronics_company.db
# data/database/airline_company.db
# etc.
```

### CORS Errors

**Check:**
- [ ] `vercel.json` has CORS headers
- [ ] `api/main.py` has CORS middleware
- [ ] Frontend uses correct API URL

### Frontend Can't Reach API

**Check:**
- [ ] `vercel.json` routes `/api/*` correctly
- [ ] `frontend/src/lib/api.ts` uses relative URLs
- [ ] No hardcoded `localhost` in production code

---

## Performance Monitoring

After deployment:

- [ ] Enable Vercel Analytics (free)
- [ ] Monitor function execution times
- [ ] Track error rates
- [ ] Check bandwidth usage

**Dashboard:** https://vercel.com/dashboard/analytics

---

## Custom Domain (Optional)

1. [ ] Purchase domain (Namecheap, Google Domains, etc.)
2. [ ] Add domain in Vercel Dashboard → Domains
3. [ ] Update DNS records:
   ```
   Type: CNAME
   Name: @ (or www)
   Value: cname.vercel-dns.com
   ```
4. [ ] Wait for DNS propagation (5-30 minutes)
5. [ ] Verify HTTPS certificate issued

---

## Success Criteria

Your deployment is successful when:

✅ All API endpoints respond  
✅ All 5 databases queryable  
✅ Natural language queries work  
✅ AI insights generate correctly  
✅ Charts render properly  
✅ Mobile responsive  
✅ No console errors  
✅ Fast loading (< 2s)  
✅ Theme switching works  
✅ CSV export works  

---

## Next Steps

After successful deployment:

1. [ ] Share URL with test users
2. [ ] Gather feedback
3. [ ] Monitor for errors
4. [ ] Iterate on features
5. [ ] Update documentation
6. [ ] Consider custom domain
7. [ ] Add to portfolio

---

**Deployment Date:** _______________  
**Production URL:** _______________  
**Notes:** _______________

---

🎉 **Congratulations on deploying Memova!**
