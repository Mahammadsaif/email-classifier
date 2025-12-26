# Render Deployment Checklist

## ✅ What We Have (Ready)
- [x] Dockerfile (production-ready)
- [x] Docker image built and tested (945MB)
- [x] requirements.txt with gunicorn
- [x] API server with health check
- [x] Model files (7 .joblib files, 1.6MB total)
- [x] 100% accuracy on 150 test cases

## 📋 What We Need to Deploy

### Option A: Docker Hub Route (Recommended for now)
1. Docker Hub account (free)
2. Push image to Docker Hub
3. Create Render web service
4. Configure environment variables on Render

### Option B: GitHub Route (For later when you push to company repo)
1. GitHub repository (you'll do this later)
2. Create Render web service from GitHub
3. Configure environment variables on Render

---

## Next Steps (Using Docker Hub - NO GITHUB NEEDED)

### Step 1: Create Docker Hub Account
Go to: https://hub.docker.com/signup
- Sign up (free account)
- Note your username

### Step 2: I'll guide you to:
1. Tag and push Docker image to Docker Hub
2. Create Render account
3. Deploy from Docker Hub
4. Test production API
5. Get production URL for your Vercel app

---

## Production URL Format
After deployment, you'll get:
`https://email-classifier-api.onrender.com`

Your Vercel app will call:
```javascript
fetch('https://email-classifier-api.onrender.com/classify', {
  method: 'POST',
  headers: {
    'X-API-Key': 'sk-emailclassifier-2024-prod',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ subject: "...", body: "..." })
})
```

---

## ⚠️ Important Notes

1. **Free Tier Limits (Render)**:
   - Spins down after 15 mins of inactivity
   - First request takes ~30s (cold start)
   - Upgrade to $7/month for always-on

2. **API Key**: Already configured in code
   - Production: `sk-emailclassifier-2024-prod`
   - Test: `sk-test-key-12345`

3. **Model Size**: 945MB image fits Render free tier

---

## Ready to Deploy?

**Do you have a Docker Hub account?**
- YES → I'll guide you to push image and deploy
- NO → Create one now (free): https://hub.docker.com/signup

After that, deployment takes ~10 minutes total.
