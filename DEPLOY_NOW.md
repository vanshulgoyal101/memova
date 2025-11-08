# 🚀 Deploy Memova to GitHub + Vercel

**Quick deployment guide - Follow these steps in order**

---

## ✅ Prerequisites

- [x] Git repository initialized ✓
- [x] Initial commit created ✓
- [x] .env excluded from git ✓
- [ ] GitHub account (create at https://github.com/signup)
- [ ] Vercel account (create at https://vercel.com/signup)

---

## 📋 Step 1: Create GitHub Repository (2 minutes)

1. **Go to**: https://github.com/new

2. **Fill in**:
   ```
   Repository name: memova
   Description: AI-powered natural language database query system
   Visibility: ⚪ Public
   
   ❌ DO NOT check "Add a README file"
   ❌ DO NOT add .gitignore
   ❌ DO NOT add license
   ```

3. **Click**: "Create repository"

4. **Copy** the repository URL (shown on the next page):
   ```
   https://github.com/YOUR_USERNAME/memova.git
   ```

---

## 📤 Step 2: Push to GitHub (1 minute)

**Replace `YOUR_USERNAME` with your actual GitHub username**, then run these commands:

```bash
cd "/Volumes/Extreme SSD/code/sql schema"

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/memova.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**Expected output**:
```
Enumerating objects: 450, done.
Counting objects: 100% (450/450), done.
...
To https://github.com/YOUR_USERNAME/memova.git
 * [new branch]      main -> main
```

**Verify**: Open `https://github.com/YOUR_USERNAME/memova` in your browser - you should see all your code!

---

## ☁️ Step 3: Deploy to Vercel (5 minutes)

### 3.1 Import Repository

1. **Go to**: https://vercel.com/new

2. **Sign in** with GitHub (if not already signed in)

3. **Import Git Repository**:
   - Click "Import Git Repository"
   - Select `YOUR_USERNAME/memova`
   - Click "Import"

### 3.2 Configure Project

**Framework Preset**: Next.js ✓ (auto-detected)

**Root Directory**: `./` (leave as default)

**Build Settings**:
```
Build Command: cd frontend && npm run build
Output Directory: frontend/.next
Install Command: cd frontend && npm install
```

**Advanced Settings** → **Root Directory**: `frontend`

### 3.3 Add Environment Variables

Click **"Environment Variables"** and add:

```bash
# Required: AI Provider Keys
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Optional: Custom API URL (leave empty for auto-detection)
NEXT_PUBLIC_API_BASE=
```

**Where to find your API keys**:
- **Groq**: https://console.groq.com/keys
- **Gemini**: https://makersuite.google.com/app/apikey

### 3.4 Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes (Vercel will build and deploy)
3. ✅ Success! You'll see: "Congratulations! Your project has been deployed."

### 3.5 Get Your URL

Your app is now live at:
```
https://memova-xxxxx.vercel.app
```

Click **"Visit"** to open your deployed app!

---

## 🧪 Step 4: Test Deployment

1. **Open** your Vercel URL

2. **Test query**:
   ```
   Company: Electronics Company
   Query: How many employees are there?
   ```

3. **Expected**: Natural language answer + SQL query + data table

4. **Try analytical query**:
   ```
   Company: Airline Company
   Query: Analyze seasonal trends in passenger bookings
   ```

5. **Expected**: Business insights + multiple charts + recommendations

---

## 🎯 Step 5: Custom Domain (Optional)

### If you own a domain (e.g., memova.com):

1. Go to: https://vercel.com/YOUR_USERNAME/memova/settings/domains

2. Add custom domain: `memova.com`

3. Follow DNS instructions:
   ```
   Type: CNAME
   Name: @
   Value: cname.vercel-dns.com
   ```

4. Wait 1-2 minutes for DNS propagation

5. ✅ Your app is now at `https://memova.com`!

---

## 🔄 Future Updates

After making changes locally:

```bash
cd "/Volumes/Extreme SSD/code/sql schema"

# Stage changes
git add -A

# Commit
git commit -m "feat: your change description"

# Push to GitHub
git push

# Vercel auto-deploys! No manual step needed
```

Vercel automatically redeploys on every push to `main` branch.

---

## 🐛 Troubleshooting

### Build fails with "Module not found"
- **Fix**: Make sure `frontend/package.json` has all dependencies
- Run locally: `cd frontend && npm install && npm run build`

### API calls return 404
- **Fix**: Check environment variables in Vercel dashboard
- Make sure `GROQ_API_KEY` and `GOOGLE_API_KEY` are set

### Database not found
- **Fix**: Check that `.db` files are in `data/database/` directory
- Verify `.gitignore` doesn't exclude `*.db` files

### Rate limit errors
- **Fix**: You've hit Groq's free tier limit (100K tokens/day)
- System automatically falls back to Gemini
- Upgrade Groq tier at: https://console.groq.com/settings/billing

---

## 📊 Deployment Summary

| Step | Time | Status |
|------|------|--------|
| 1. Create GitHub repo | 2 min | ⏳ Pending |
| 2. Push to GitHub | 1 min | ⏳ Pending |
| 3. Deploy to Vercel | 5 min | ⏳ Pending |
| **Total** | **~8 min** | |

---

## 🎉 Success Checklist

- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] Vercel project created
- [ ] Environment variables added
- [ ] Deployment successful
- [ ] App accessible at Vercel URL
- [ ] Test query works
- [ ] Analytical query works

---

## 🔗 Quick Links

- **GitHub Repo**: `https://github.com/YOUR_USERNAME/memova`
- **Vercel Dashboard**: `https://vercel.com/dashboard`
- **Live App**: `https://memova-xxxxx.vercel.app`
- **Groq Console**: https://console.groq.com
- **Gemini API**: https://makersuite.google.com

---

**Need help?** Check:
- Full deployment guide: `VERCEL_DEPLOYMENT.md`
- Deployment checklist: `DEPLOYMENT_CHECKLIST.md`
- Start guide: `START_HERE.md`

---

**Version**: 1.0  
**Last Updated**: 2025-11-08  
**Product**: Memova v3.2.0
