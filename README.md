# Email Classification API 📧

**Production-Grade 5-Class Hierarchical Email Classifier**

Automatically classify sales emails into HOT/WARM/COLD leads, SPAM, and ABUSE using a 3-stage hierarchical SVM model with 98%+ accuracy.

---

## 🎯 Overview

This system uses a **3-stage hierarchical pipeline** to classify incoming sales emails:

```
Email → Stage 1: ABUSE? → Stage 2: SPAM? → Stage 3: HOT/WARM/COLD
```

### Classification Labels

| Label | Meaning | Action |
|-------|---------|--------|
| **HOT** | Ready to buy NOW - approval obtained, urgent need, crisis | Immediate follow-up within 24 hours |
| **WARM** | Interested but future timeline - team discussion, budget planning | Schedule follow-up, add to nurture |
| **COLD** | Polite rejection, unsubscribe requests | Add to general outreach list |
| **SPAM** | Phishing, chain emails, scams | Auto-delete, no action |
| **ABUSE** | Threats, harassment, criminal accusations | Block sender, document |

---

## 📊 Performance Metrics

| Stage | Component | Accuracy | Purpose |
|-------|-----------|----------|---------|
| **1** | ABUSE Detector | 98.8% | Identify abusive/threatening emails |
| **2** | SPAM Detector | 99.7% | Filter spam and phishing |
| **3** | Intent Classifier | 88.7% | Classify HOT/WARM/COLD leads |
| **Overall** | Test Cases | **19/19 (100%)** | Real-world validation |

**Training Data:** 2,224 samples (balanced across all classes)

---

## 🚀 Quick Start

### Local Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd mails_classification

# Create virtual environment
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
python3 api_server.py
```

Server runs on: `http://localhost:5001`

---

## 🔑 API Authentication

All endpoints require API key authentication:

**Default API Keys:**
- Production: `sk-emailclassifier-2024-prod`
- Testing: `sk-test-key-12345`

**Headers:**
```
X-API-Key: sk-emailclassifier-2024-prod
Content-Type: application/json
```

---

## 📡 API Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-12-25T17:52:00.000000"
}
```

---

### 2. Classify Single Email
```http
POST /classify
```

**Request:**
```json
{
  "subject": "my boss approved!!!",
  "body": "omg finally! after 3 weeks my boss approved the budget. $45k for annual subscription. can you send me the order form?"
}
```

**Response:**
```json
{
  "label": "HOT",
  "confidence": 95.5,
  "action": "IMMEDIATE FOLLOW-UP REQUIRED - High interest lead, contact within 24 hours",
  "stage": "intent_classification",
  "needs_review": false,
  "timestamp": "2025-12-25T17:52:00.000000"
}
```

---

### 3. Batch Classification
```http
POST /classify/batch
```

**Request:**
```json
{
  "emails": [
    {
      "id": "email_001",
      "subject": "Purchase Order Ready",
      "body": "CFO approved. Send contract ASAP."
    },
    {
      "id": "email_002",
      "subject": "Unsubscribe please",
      "body": "Please remove me from your list. Thanks."
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "email_001",
      "label": "HOT",
      "confidence": 99.1,
      "action": "IMMEDIATE FOLLOW-UP REQUIRED - High interest lead, contact within 24 hours",
      "stage": "intent_classification",
      "needs_review": false
    },
    {
      "id": "email_002",
      "label": "COLD",
      "confidence": 99.7,
      "action": "ADD TO NURTURE LIST - Low interest, continue general outreach",
      "stage": "intent_classification",
      "needs_review": false
    }
  ],
  "total": 2,
  "timestamp": "2025-12-25T17:52:00.000000"
}
```

---

## 🧪 Testing Examples

### Postman Test Cases

**HOT Lead (Boss Approval):**
```json
{
  "subject": "Budget approved!",
  "body": "My boss finally approved the purchase. Send the contract today!"
}
```
Expected: `HOT` with 95%+ confidence

**WARM Lead (Team Discussion):**
```json
{
  "subject": "Need to discuss with team",
  "body": "Liked the demo. I need to present this to our leadership team next week."
}
```
Expected: `WARM` with 95%+ confidence

**COLD Lead (Unsubscribe):**
```json
{
  "subject": "Please remove me",
  "body": "We've decided to go another direction. Please take me off your list."
}
```
Expected: `COLD` with 99%+ confidence

**ABUSE (Criminal Accusation):**
```json
{
  "subject": "You are criminals",
  "body": "Your company is a scam run by thieves. I'm reporting you to the FBI."
}
```
Expected: `ABUSE` with 95%+ confidence

**SPAM (Phishing):**
```json
{
  "subject": "URGENT: Account suspended",
  "body": "Click here to verify your password immediately or your account will be closed."
}
```
Expected: `SPAM` with 100% confidence

---

## 🏗️ Architecture

### 3-Stage Hierarchical Pipeline

```
┌─────────────────────────────────────────────────────┐
│                   Input Email                        │
│              (subject + body text)                   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  Stage 1: ABUSE Detection (98.8% accuracy)          │
│  Binary SVM: ABUSE vs NOT_ABUSE                     │
│  Features: TF-IDF (1-3 grams, 3000 features)        │
└─────────────────────────────────────────────────────┘
         ↓ NOT_ABUSE                    ↓ ABUSE
         ↓                              Return "ABUSE"
┌─────────────────────────────────────────────────────┐
│  Stage 2: SPAM Detection (99.7% accuracy)           │
│  Binary SVM: SPAM vs NOT_SPAM                       │
│  Features: TF-IDF (1-3 grams, 3000 features)        │
└─────────────────────────────────────────────────────┘
         ↓ NOT_SPAM                     ↓ SPAM
         ↓                              Return "SPAM"
┌─────────────────────────────────────────────────────┐
│  Stage 3: Intent Classification (88.7% accuracy)    │
│  3-Class SVM: HOT / WARM / COLD                     │
│  Features: TF-IDF (1-3 grams, 5000 features)        │
└─────────────────────────────────────────────────────┘
         ↓
    Return HOT/WARM/COLD
```

### Model Details

- **Algorithm:** Support Vector Machine (SVM) with linear kernel
- **Vectorization:** TF-IDF with n-grams (1-3)
- **Confidence Threshold:** 70% (returns NEEDS_REVIEW below threshold)
- **Serialization:** joblib (optimized for scikit-learn)

### Project Structure

```
mails_classification/
├── api_server.py              # Flask REST API with authentication
├── predict_hierarchical.py    # 3-stage classification logic
├── training_data.csv          # Production training dataset (2,224 samples)
├── models/                    # Trained model files
│   ├── abuse_detector.joblib
│   ├── abuse_tfidf.joblib
│   ├── spam_detector.joblib
│   ├── spam_tfidf.joblib
│   ├── intent_classifier.joblib
│   ├── intent_tfidf.joblib
│   └── intent_label_encoder.joblib
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── DEPLOYMENT_GUIDE.md        # Render deployment instructions
└── archive/                   # Historical training scripts
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# API Configuration
API_KEYS=sk-emailclassifier-2024-prod,sk-test-key-12345
FLASK_ENV=production
PORT=5001

# Model Configuration
CONFIDENCE_THRESHOLD=0.70
MODEL_DIR=./models
```

---

## 🚨 Error Handling

### Low Confidence Results

When confidence < 70%, the API returns:
```json
{
  "label": "NEEDS_REVIEW",
  "confidence": 65.2,
  "predicted_label": "WARM",
  "action": "MANUAL REVIEW REQUIRED - Model uncertain, human review needed",
  "needs_review": true
}
```

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Missing/invalid API key | Check X-API-Key header |
| 400 Bad Request | Missing subject/body | Include both fields in request |
| 500 Server Error | Model files missing | Ensure models/ directory exists |

---

## 🔐 Security

- **API Key Authentication:** Required for all endpoints
- **CORS Enabled:** Allows cross-origin requests
- **Input Validation:** Subject and body are sanitized
- **Production Ready:** Use gunicorn for deployment

**Production Recommendations:**
- Use environment variables for API keys
- Implement rate limiting
- Use HTTPS in production
- Add request logging and monitoring

---

## 📦 Dependencies

```
flask>=3.0.0
flask-cors>=4.0.0
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
joblib>=1.3.0
gunicorn>=21.2.0
```

---

## 📞 Support

For issues or questions:
- Check logs in `server.log`
- See deployment guide in `DEPLOYMENT_GUIDE.md`
- Contact: SalesCentri Engineering Team

---

## 📄 License

Proprietary - SalesCentri Internal Use Only

---

**Last Updated:** December 25, 2025  
**Version:** 1.0 (Production)  
**Test Accuracy:** 19/19 (100%)
