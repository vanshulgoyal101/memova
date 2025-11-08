# Memova - Vercel Deployment Guide

## 📦 Repository Structure for Vercel

This repository is configured for **Vercel deployment** with the following structure:

```
/
├── api/                    # Python backend (FastAPI)
│   ├── main.py            # FastAPI app
│   ├── index.py           # Vercel entry point
│   ├── routes.py          # API endpoints
│   └── models.py          # Pydantic models
├── frontend/              # Next.js frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── src/                   # Core Python business logic
│   ├── core/              # Query engine, SQL generator, AI clients
│   ├── data/              # Data generators
│   └── utils/             # Utilities
├── data/
│   └── database/          # SQLite databases (bundled in deployment)
│       ├── electronics_company.db
│       ├── airline_company.db
│       ├── edtech_company.db
│       ├── ednite_company.db
│       └── liqo_company.db
├── vercel.json            # Vercel configuration
├── .vercelignore          # Files to exclude from deployment
├── runtime.txt            # Python version
└── requirements.txt       # Python dependencies
```

---

## 🚀 Deployment Steps

### 1️⃣ **Push to GitHub**

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Memova ready for Vercel"

# Create GitHub repo (use GitHub CLI or web interface)
gh repo create memova --public --source=. --remote=origin --push

# Or manually:
# 1. Create repo on github.com
# 2. git remote add origin https://github.com/YOUR_USERNAME/memova.git
# 3. git push -u origin main
```

### 2️⃣ **Deploy to Vercel**

#### Option A: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name? memova
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

#### Option B: Vercel Dashboard (Easier)
1. Go to [vercel.com](https://vercel.com)
2. Click **"New Project"**
3. Import your GitHub repo `memova`
4. Vercel auto-detects Next.js + Python
5. Add environment variables (see below)
6. Click **"Deploy"**

### 3️⃣ **Configure Environment Variables**

In Vercel Dashboard → Your Project → Settings → Environment Variables:

**Required:**
```
GOOGLE_API_KEY=your-google-gemini-api-key-here
GROQ_API_KEY=your-groq-api-key-here
```

**Optional:**
```
LOG_LEVEL=INFO
NEXT_PUBLIC_API_BASE=https://your-project.vercel.app
```

**Get API Keys:**
- Google Gemini: https://makersuite.google.com/app/apikey
- Groq: https://console.groq.com/keys

---

## 🗄️ Database Handling

**SQLite databases are bundled** in the deployment:
- ✅ Files included in Git repo
- ✅ Deployed with application
- ✅ Read-only access (perfect for demo)
- ✅ Fast local file access

**Size:** ~20-50MB (well within Vercel limits)

---

## 🔧 Configuration Files

### `vercel.json`
- Routes API requests to Python backend
- Routes frontend requests to Next.js
- Sets CORS headers
- Defines environment variables

### `.vercelignore`
- Excludes unnecessary files (tests, docs, scripts)
- Reduces deployment size
- Keeps databases and core code

### `runtime.txt`
- Specifies Python 3.11
- Required for Vercel Python runtime

### `api/index.py`
- Entry point for serverless Python functions
- Re-exports FastAPI app

---

## 🧪 Testing Deployment

### Local Testing (Before Deploy)
```bash
# Test frontend
cd frontend
npm run build
npm start

# Test backend (separate terminal)
python -m uvicorn api.main:app --reload --port 8000

# Visit http://localhost:3000
```

### Production Testing (After Deploy)
```bash
# Your app will be at:
https://memova.vercel.app

# Test deployment
curl https://memova.vercel.app/api/health

# Open browser to https://memova.vercel.app
```

---

## 📊 Vercel Free Tier Limits

✅ **Perfect for this project:**
- Bandwidth: 100 GB/month
- Serverless Function Execution: 100 GB-hrs/month
- Builds: 6,000 minutes/month
- Deployments: Unlimited

Your app uses minimal resources:
- DB queries: Fast (local SQLite)
- AI calls: Throttled by API limits (not Vercel)
- Bandwidth: Low (static frontend)

---

## 🔄 Continuous Deployment

After initial setup, Vercel auto-deploys on:
- ✅ Every `git push` to `main` branch
- ✅ Every pull request (preview deployments)
- ✅ Manual triggers from dashboard

**Workflow:**
```bash
# Make changes
git add .
git commit -m "Add new feature"
git push

# Vercel automatically:
# 1. Detects push
# 2. Builds project
# 3. Runs tests
# 4. Deploys to production
# 5. Sends notification
```

---

## 🐛 Troubleshooting

### Build Fails?
```bash
# Check Vercel build logs
vercel logs

# Test build locally
cd frontend && npm run build
```

### API Not Working?
- Check environment variables in Vercel dashboard
- Verify API routes in `vercel.json`
- Check Python logs in Vercel dashboard

### Database Not Found?
- Ensure `.gitignore` doesn't exclude `.db` files
- Check `.vercelignore` doesn't exclude `data/database/`
- Verify files are in Git repo: `git ls-files | grep .db`

### CORS Errors?
- Verify CORS headers in `vercel.json`
- Check API `main.py` has CORS middleware
- Ensure frontend uses correct API URL

---

## 📝 Next Steps

After successful deployment:

1. ✅ **Test all features** on production URL
2. ✅ **Set up custom domain** (optional)
   - Vercel Dashboard → Domains → Add
   - Example: `memova.com` → CNAME to `cname.vercel-dns.com`
3. ✅ **Enable analytics** (Vercel Analytics - free)
4. ✅ **Monitor performance** (Vercel Dashboard)
5. ✅ **Share with users** 🎉

---

## 🌟 Production Checklist

Before sharing publicly:

- [ ] All API keys set in Vercel environment
- [ ] Frontend builds successfully
- [ ] Backend responds to `/api/health`
- [ ] All 5 databases accessible
- [ ] Example queries work
- [ ] Charts render correctly
- [ ] AI insights generate properly
- [ ] Mobile responsive design tested
- [ ] Error handling works
- [ ] Rate limiting respects API quotas

---

**Ready to deploy?** Follow Step 1 above! 🚀
