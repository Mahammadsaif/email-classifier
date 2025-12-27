# GitHub + Render Deployment Guide

## 📋 Quick Summary
- GitHub Profile: https://github.com/Mahammadsaif
- Repository Name: `email-classifier` (private)
- Current Status: Code committed locally, ready to push

---

## STEP 1: Create GitHub Repository (Do this NOW)

### 1.1 Go to GitHub and create new repo
**Open this link:** https://github.com/new

### 1.2 Fill in repository details:
- **Repository name:** `email-classifier`
- **Description:** "5-class email classifier API (HOT/WARM/COLD/SPAM/ABUSE) using 3-stage hierarchical SVM - Production ready with 100% test accuracy"
- **Visibility:** ✅ **Private** (checked)
- **DO NOT** initialize with:
  - ❌ README (we already have one)
  - ❌ .gitignore (we already have one)
  - ❌ License

### 1.3 Click "Create repository"

---

## STEP 2: Push Code to GitHub (Run these commands)

After creating the repo, GitHub will show you commands. We'll use these:

```bash
# Add GitHub remote
git remote add origin https://github.com/Mahammadsaif/email-classifier.git

# Push code to GitHub
git push -u origin main
```

**Note:** GitHub will ask for authentication:
- **Username:** Mahammadsaif
- **Password:** Use a Personal Access Token (NOT your GitHub password)
  
If you don't have a token:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Copy the token and use it as password

---

## STEP 3: Deploy to Render

### 3.1 Create Render Account
1. Go to: https://dashboard.render.com/register
2. Sign up with GitHub (easiest - auto-connects repos)
3. Authorize Render to access your GitHub

### 3.2 Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Click **"Build and deploy from a Git repository"**
3. Click **"Connect account"** (if not connected)
4. Find `email-classifier` repo → Click **"Connect"**

### 3.3 Configure Service Settings

Fill in these details:

**Basic Settings:**
- **Name:** `email-classifier-api` (or any name you want)
- **Region:** `Oregon (US West)` (or closest to you)
- **Branch:** `main`
- **Runtime:** `Docker`

**Build & Deploy:**
- **Dockerfile Path:** Leave blank (Render auto-detects `./Dockerfile`)
- **Docker Build Context:** `.` (current directory)

**Instance Type:**
- **Free** (for testing) - spins down after 15 mins inactivity
- OR **Starter ($7/month)** - always on, better for production

### 3.4 Environment Variables

Click **"Advanced"** → Add Environment Variables:

| Key | Value |
|-----|-------|
| `EMAIL_CLASSIFIER_API_KEY` | `sk-emailclassifier-2024-prod` |
| `PORT` | `5001` |

### 3.5 Health Check Settings

- **Health Check Path:** `/health`
- **Health Check Interval:** 30 seconds

### 3.6 Deploy!

Click **"Create Web Service"**

Render will:
1. Clone your GitHub repo
2. Build Docker image (takes ~5-10 mins)
3. Deploy container
4. Give you a public URL

---

## STEP 4: Test Production API

### 4.1 Get Your URL
After deployment succeeds, you'll get:
```
https://email-classifier-api.onrender.com
```
(Or similar - Render will show your exact URL)

### 4.2 Test Health Endpoint
```bash
curl https://email-classifier-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-26T..."
}
```

### 4.3 Test Classification Endpoint
```bash
curl -X POST https://email-classifier-api.onrender.com/classify \
  -H "X-API-Key: sk-emailclassifier-2024-prod" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "URGENT: Server down!",
    "body": "Our production server crashed. Need immediate help!"
  }'
```

Expected response:
```json
{
  "label": "HOT",
  "confidence": 0.95,
  "action": "URGENT - Respond immediately",
  "stage": "intent_classification",
  "needs_review": false
}
```

---

## STEP 5: Connect to Your Vercel App

Update your Vercel frontend to use the production URL:

```javascript
// In your Vercel app
const CLASSIFIER_API = 'https://email-classifier-api.onrender.com';

async function classifyEmail(subject, body) {
  const response = await fetch(`${CLASSIFIER_API}/classify`, {
    method: 'POST',
    headers: {
      'X-API-Key': 'sk-emailclassifier-2024-prod',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ subject, body })
  });
  
  return await response.json();
}
```

---

## 🎉 Deployment Complete!

### What You Have:
✅ Private GitHub repo with version control
✅ Automated deployments (git push → auto-deploy on Render)
✅ Production API at `https://email-classifier-api.onrender.com`
✅ Health monitoring
✅ Secure API key authentication

### Next Steps:
1. Share production URL with your team
2. Update Vercel app to use production endpoint
3. Test with real emails
4. Monitor logs on Render dashboard

### Future Updates:
```bash
# Make code changes locally
git add .
git commit -m "Update model or API"
git push origin main

# Render automatically detects push and redeploys!
```

---

## 📊 Render Dashboard Features

After deployment, you can:
- View logs: Real-time application logs
- Monitor metrics: CPU, memory, request counts
- View events: Deployment history
- Restart service: Manual restart if needed
- Environment variables: Update API keys without redeployment

---

## ⚠️ Important Notes

### Free Tier Limitations:
- Spins down after 15 mins of inactivity
- First request after spin-down takes ~30s (cold start)
- 750 hours/month free (enough for testing)

### Upgrade to Starter ($7/month) for:
- Always-on service (no cold starts)
- Faster build times
- More memory (512MB → 2GB)
- Better for production use

### Security:
- API key is required for all requests
- Private GitHub repo (code not public)
- HTTPS only (Render auto-provides SSL)

---

## 🆘 Troubleshooting

### Build fails on Render:
- Check logs in Render dashboard
- Verify Dockerfile is correct
- Ensure all model files are committed to git

### API returns 500 error:
- Check Render logs for Python errors
- Verify environment variables are set
- Test health endpoint first

### Slow response times:
- Free tier spins down - upgrade to Starter
- Check logs for model loading issues
- Consider caching loaded models

---

Ready to start? Begin with **STEP 1** above! 🚀
