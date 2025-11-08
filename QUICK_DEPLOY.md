# ⚡ Quick Deployment Reference

## 🎯 Goal
Deploy Memova to GitHub → Vercel in ~10 minutes

---

## 📋 Quick Steps

### 1️⃣ GitHub (3 min)
```bash
# Run the helper script
./push_to_github.sh

# OR manually:
# 1. Create repo: https://github.com/new (name: memova)
# 2. git remote add origin https://github.com/YOUR_USERNAME/memova.git
# 3. git branch -M main
# 4. git push -u origin main
```

### 2️⃣ Vercel (7 min)
1. **Go to**: https://vercel.com/new
2. **Import**: YOUR_USERNAME/memova
3. **Framework**: Next.js (auto-detected)
4. **Add env vars**:
   ```
   GROQ_API_KEY=gsk_...
   GOOGLE_API_KEY=AIza...
   ```
5. **Click**: Deploy
6. **Wait**: 2-3 minutes
7. **Done**: App live at `memova.vercel.app`

---

## 🔑 Get API Keys

**Groq** (Primary, 26x faster):
- Dashboard: https://console.groq.com/keys
- Click "Create API Key"
- Copy: `gsk_...`

**Gemini** (Fallback):
- Dashboard: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy: `AIza...`

---

## ✅ Test Deployed App

1. Open: `https://your-app.vercel.app`
2. Select: "Electronics Company"
3. Ask: "How many employees?"
4. Expect: Answer + SQL + Table

---

## 🐛 Common Issues

| Issue | Fix |
|-------|-----|
| Build fails | Check `frontend/package.json` dependencies |
| 404 on API calls | Add `GROQ_API_KEY` env var in Vercel |
| Database not found | Verify `*.db` files in `data/database/` |
| Timeout errors | Normal for analytical queries (30-60s) |

---

## 📱 Commands

```bash
# Deploy to GitHub
./push_to_github.sh

# Update deployment (after changes)
git add -A
git commit -m "your message"
git push  # Vercel auto-deploys!

# View deployment logs
vercel logs YOUR_APP_URL

# Local development
make start
```

---

## 📚 Full Docs

- **Step-by-step**: `DEPLOY_NOW.md`
- **Vercel guide**: `VERCEL_DEPLOYMENT.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`

---

**Ready?** Run: `./push_to_github.sh`
