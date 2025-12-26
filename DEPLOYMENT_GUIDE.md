# Deployment Guide - Render.com 🚀

Step-by-step guide to deploy the Email Classification API to Render.

---

## Prerequisites

- GitHub account
- Render.com account (free tier available)
- Project pushed to GitHub

---

## Step 1: Prepare Repository

### 1.1 Push to GitHub

```bash
cd /Users/saifshaik/Downloads/Projects/mails_classification

# Initialize git if not already done
git init
git add .
git commit -m "Production-ready email classifier with 100% test accuracy"

# Add remote and push
git remote add origin https://github.com/yourusername/email-classifier.git
git branch -M main
git push -u origin main
```

### 1.2 Verify Essential Files

Ensure these files are in your repository:
```
├── api_server.py
├── predict_hierarchical.py
├── requirements.txt
├── training_data.csv
├── models/
│   ├── abuse_detector.joblib
│   ├── abuse_tfidf.joblib
│   ├── spam_detector.joblib
│   ├── spam_tfidf.joblib
│   ├── intent_classifier.joblib
│   ├── intent_tfidf.joblib
│   └── intent_label_encoder.joblib
├── README.md
└── .gitignore
```

---

## Step 2: Create .gitignore

Create `.gitignore` file to exclude unnecessary files:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
myenv/
venv/
env/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
server.log

# Data
archive/
external_data/
llm_augmented/
*.CSV

# Temporary
frontend.html
start_server.sh
```

---

## Step 3: Create requirements.txt

Create clean production `requirements.txt`:

```txt
flask==3.0.0
flask-cors==4.0.0
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.26.2
joblib==1.3.2
gunicorn==21.2.0
```

---

## Step 4: Create Render Configuration

### Option A: Using render.yaml (Recommended)

Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: email-classifier-api
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 api_server:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: API_KEYS
        value: sk-emailclassifier-2024-prod,sk-test-key-12345
      - key: FLASK_ENV
        value: production
      - key: CONFIDENCE_THRESHOLD
        value: 0.70
```

### Option B: Manual Render Dashboard Setup

If not using `render.yaml`, you'll configure these settings manually in Render dashboard (see Step 5).

---

## Step 5: Deploy to Render

### 5.1 Create New Web Service

1. Go to [https://render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the repository: `email-classifier`

### 5.2 Configure Service

**Basic Settings:**
- **Name:** `email-classifier-api`
- **Region:** Oregon (US West) or nearest to your users
- **Branch:** `main`
- **Runtime:** Python 3

**Build Settings:**
- **Build Command:** 
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command:**
  ```bash
  gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 api_server:app
  ```

### 5.3 Environment Variables

Add these in Render dashboard under "Environment":

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `API_KEYS` | `sk-emailclassifier-2024-prod,sk-test-key-12345` |
| `FLASK_ENV` | `production` |
| `CONFIDENCE_THRESHOLD` | `0.70` |

### 5.4 Advanced Settings

- **Health Check Path:** `/health`
- **Auto-Deploy:** Yes (deploy on git push)
- **Plan:** Free (or upgrade as needed)

### 5.5 Deploy

Click **"Create Web Service"**

Render will:
1. Clone your repository
2. Install dependencies
3. Start the gunicorn server
4. Assign a public URL: `https://email-classifier-api.onrender.com`

---

## Step 6: Verify Deployment

### 6.1 Check Deployment Status

Monitor the deployment logs in Render dashboard. Look for:
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 1
```

### 6.2 Test Health Endpoint

```bash
curl https://email-classifier-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-12-25T18:00:00.000000"
}
```

### 6.3 Test Classification

```bash
curl -X POST https://email-classifier-api.onrender.com/classify \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-emailclassifier-2024-prod" \
  -d '{
    "subject": "Budget approved!",
    "body": "My boss finally approved the purchase. Send the contract today!"
  }'
```

Expected response:
```json
{
  "label": "HOT",
  "confidence": 95.5,
  "action": "IMMEDIATE FOLLOW-UP REQUIRED - High interest lead, contact within 24 hours",
  "stage": "intent_classification",
  "needs_review": false
}
```

---

## Step 7: Production Configuration

### 7.1 Custom Domain (Optional)

In Render dashboard:
1. Go to **Settings** → **Custom Domain**
2. Add your domain: `api.salescentri.com`
3. Update DNS records as instructed
4. Render will provision SSL certificate automatically

### 7.2 Scaling

**Free Tier Limitations:**
- Spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds

**To Upgrade:**
1. Go to **Settings** → **Plan**
2. Select **Starter** ($7/month) or **Standard** ($25/month)
3. Benefits: Always-on, faster, more memory

### 7.3 Environment-Specific API Keys

For production, update `API_KEYS` environment variable:
```
API_KEYS=sk-prod-salescentri-2024,sk-backup-key-2024
```

### 7.4 Monitoring

Enable monitoring in Render:
- **Metrics:** CPU, Memory, Response times
- **Logs:** Real-time access to application logs
- **Alerts:** Set up email/Slack notifications

---

## Step 8: CI/CD Workflow

### 8.1 Automatic Deployments

Render automatically deploys when you push to `main`:

```bash
# Make changes locally
vim api_server.py

# Commit and push
git add .
git commit -m "Update API endpoint"
git push origin main

# Render auto-deploys in ~2-3 minutes
```

### 8.2 Manual Deploy

In Render dashboard:
- Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## Step 9: API Integration

### 9.1 Update Client Applications

Replace localhost URLs with production URL:

**Before:**
```javascript
const API_URL = "http://localhost:5001/classify";
```

**After:**
```javascript
const API_URL = "https://email-classifier-api.onrender.com/classify";
```

### 9.2 Share API Documentation

Share with your team:
- **API URL:** `https://email-classifier-api.onrender.com`
- **API Key:** `sk-emailclassifier-2024-prod`
- **Documentation:** Link to README.md in repository

---

## Troubleshooting

### Issue: Build Fails

**Check:**
- `requirements.txt` has correct package names
- Python version is 3.9 or higher
- All model files are committed to git

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt
python api_server.py
```

### Issue: Health Check Fails

**Check:**
- `/health` endpoint responds
- Models are loaded correctly
- No import errors

**Solution:**
Check Render logs for error messages.

### Issue: 401 Unauthorized

**Check:**
- `X-API-Key` header is included
- API key matches environment variable

**Solution:**
```bash
curl -H "X-API-Key: sk-emailclassifier-2024-prod" \
  https://email-classifier-api.onrender.com/health
```

### Issue: Slow First Request

**Cause:** Free tier spins down after inactivity

**Solution:**
- Upgrade to paid tier for always-on service
- Or: Set up periodic health check ping (every 10 minutes)

---

## Cost Estimate

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0/month | 750 hours/month, spins down after inactivity |
| **Starter** | $7/month | Always-on, 1 instance, SSL |
| **Standard** | $25/month | Always-on, faster, more memory |

**Recommended:** Start with **Free**, upgrade to **Starter** for production.

---

## Security Checklist

- [ ] API keys stored in environment variables (not code)
- [ ] `.env` file in `.gitignore`
- [ ] HTTPS enabled (automatic on Render)
- [ ] CORS configured for allowed origins only
- [ ] Rate limiting implemented (if needed)
- [ ] Regular security updates for dependencies

---

## Maintenance

### Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade flask

# Regenerate requirements
pip freeze > requirements.txt

# Commit and push (triggers auto-deploy)
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Monitor Performance

Check Render dashboard weekly:
- Response times
- Error rates
- Memory usage
- Request volume

---

## Rollback

If deployment fails:

1. Go to Render dashboard → **Events**
2. Find previous successful deployment
3. Click **"Rollback to this version"**

---

## Support

**Render Documentation:** https://render.com/docs
**Support:** help@render.com

**Project Support:**
- GitHub Issues: `https://github.com/yourusername/email-classifier/issues`
- Team Contact: SalesCentri Engineering

---

**Deployment Date:** December 25, 2025  
**Last Updated:** December 25, 2025  
**Status:** Production Ready ✅
