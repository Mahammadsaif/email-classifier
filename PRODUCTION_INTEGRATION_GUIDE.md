# 📧 Email Classifier - Production Integration Guide

## 🎯 Overview

This guide explains how to integrate the **Email Classifier API** into your application. The API classifies emails into 5 categories:

- **🔴 ABUSE** - Threats, hostile content
- **🔴 SPAM** - Marketing, unsolicited
- **❄️ COLD** - Initial outreach, no interest
- **🟡 WARM** - Interested, evaluating
- **🟢 HOT** - Ready to buy, decision-maker

---

## 🚀 Production Endpoint

```
Base URL: https://email-classifier-api.onrender.com
API Key: sk-emailclassifier-2024-prod
```

---

## 📋 API Endpoints

### 1️⃣ Single Email Classification

**Endpoint:** `POST /classify`

**Authentication:**
```bash
X-API-Key: sk-emailclassifier-2024-prod
```

**Request - Option A: Raw Email (Automatic Preprocessing)**

```json
{
  "subject": "Re: Enterprise License - Approved",
  "body": "From: john@company.com\nTo: sales@service.com\nDate: Mon, 13 Jan 2025\n\n\nHi Jessica,\n\nOur procurement team has reviewed and approved the Enterprise License for 500 seats at $85K annually.\n\nLegal signed off on the MSA. Please send the Order Form.\n\nThanks,\nRobert Chen\nDirector of IT\n---\nSent from my iPhone",
  "preprocess": true
}
```

**Request - Option B: Clean Email (Skip Preprocessing)**

```json
{
  "subject": "Re: Enterprise License - Approved",
  "body": "Our procurement team has reviewed and approved the Enterprise License for 500 seats at $85K annually. Legal signed off on the MSA. Please send the Order Form.",
  "preprocess": false
}
```

**Response:**

```json
{
  "label": "HOT",
  "confidence": 96.2,
  "action": "Schedule immediate call to close deal",
  "needs_review": false,
  "preprocessing_applied": true,
  "client": "default",
  "timestamp": "2025-01-13T15:30:45.123456+00:00"
}
```

---

### 2️⃣ Batch Email Classification

**Endpoint:** `POST /classify/batch`

**Request:**

```json
{
  "emails": [
    {
      "subject": "Re: Enterprise License",
      "body": "Raw or clean email text..."
    },
    {
      "subject": "Demo Request",
      "body": "Can we schedule a demo..."
    }
  ],
  "preprocess": true
}
```

**Response:**

```json
{
  "results": [
    {
      "label": "HOT",
      "confidence": 96.2,
      "action": "Schedule immediate call",
      "needs_review": false,
      "preprocessing_applied": true,
      "timestamp": "2025-01-13T15:30:45.123456+00:00"
    },
    {
      "label": "WARM",
      "confidence": 78.5,
      "action": "Send demo meeting link",
      "needs_review": false,
      "preprocessing_applied": true,
      "timestamp": "2025-01-13T15:30:45.234567+00:00"
    }
  ],
  "total": 2,
  "summary": {
    "HOT": 1,
    "WARM": 1
  }
}
```

---

## 💻 Code Examples

### JavaScript/Node.js

```javascript
// Single email classification
async function classifyEmail(subject, body) {
  const response = await fetch('https://email-classifier-api.onrender.com/classify', {
    method: 'POST',
    headers: {
      'X-API-Key': 'sk-emailclassifier-2024-prod',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      subject: subject,
      body: body,
      preprocess: true  // API will automatically clean email
    })
  });

  const result = await response.json();
  console.log(`Classification: ${result.label} (${result.confidence}% confidence)`);
  console.log(`Action: ${result.action}`);
  
  return result;
}

// Batch email classification
async function classifyBatch(emails) {
  const response = await fetch('https://email-classifier-api.onrender.com/classify/batch', {
    method: 'POST',
    headers: {
      'X-API-Key': 'sk-emailclassifier-2024-prod',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      emails: emails,
      preprocess: true
    })
  });

  const result = await response.json();
  console.log(`Classified ${result.total} emails`);
  console.log(`Summary: ${JSON.stringify(result.summary)}`);
  
  return result;
}

// Usage
classifyEmail(
  'Re: Enterprise License - Approved',
  'Our procurement team has approved the Enterprise License for 500 seats...'
);

classifyBatch([
  { subject: 'Inquiry', body: 'Can you send more info...' },
  { subject: 'Demo Request', body: 'We would like to schedule a demo...' }
]);
```

### Python

```python
import requests
import json

# Configuration
API_URL = 'https://email-classifier-api.onrender.com'
API_KEY = 'sk-emailclassifier-2024-prod'

def classify_email(subject, body):
    """Classify a single email."""
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'subject': subject,
        'body': body,
        'preprocess': True  # Automatically clean email
    }
    
    response = requests.post(
        f'{API_URL}/classify',
        headers=headers,
        json=payload
    )
    
    result = response.json()
    print(f"Classification: {result['label']} ({result['confidence']}% confidence)")
    print(f"Action: {result['action']}")
    
    return result

def classify_batch(emails):
    """Classify multiple emails."""
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'emails': emails,
        'preprocess': True
    }
    
    response = requests.post(
        f'{API_URL}/classify/batch',
        headers=headers,
        json=payload
    )
    
    result = response.json()
    print(f"Classified {result['total']} emails")
    print(f"Summary: {result['summary']}")
    
    return result

# Usage
classify_email(
    'Re: Enterprise License - Approved',
    'Our procurement team has approved the Enterprise License for 500 seats...'
)

classify_batch([
    {'subject': 'Inquiry', 'body': 'Can you send more info...'},
    {'subject': 'Demo Request', 'body': 'We would like to schedule a demo...'}
])
```

### Python - Using Local Preprocessor

```python
from email_preprocessor import EmailPreprocessor
import requests

# Initialize preprocessor
preprocessor = EmailPreprocessor()

# Get raw email from inbox
raw_email = """
From: john@company.com
To: sales@service.com
Date: Mon, 13 Jan 2025 10:30:00

Hi Jessica,

Our procurement team has reviewed the license.

Thanks,
Robert Chen
---
Sent from iPhone
"""

# Clean email locally (optional, API can do this automatically)
clean_body = preprocessor.clean_email(raw_email)

# Send to API
headers = {'X-API-Key': 'sk-emailclassifier-2024-prod'}
response = requests.post(
    'https://email-classifier-api.onrender.com/classify',
    headers=headers,
    json={
        'body': clean_body,
        'preprocess': False  # Already cleaned locally
    }
)

result = response.json()
print(f"Label: {result['label']}")
print(f"Confidence: {result['confidence']}%")
```

---

## 🧹 Email Preprocessing

The API **automatically preprocesses** emails when `"preprocess": true`:

### What Gets Removed

```
✂️ Email headers (From, To, CC, Date, Subject, Message-ID, etc.)
✂️ Quoted text (> Previous messages)
✂️ Signatures (---, ___, ~~~, "Sent from", etc.)
✂️ HTML tags and entities (&nbsp; &lt; &amp; etc.)
✂️ Unsubscribe links and footers
✂️ Extra whitespace and blank lines
```

### Example Transformation

**BEFORE (Raw Email):**
```
From: john@company.com
To: sales@service.com
Date: Mon, 13 Jan 2025 10:30:00
Subject: Re: Enterprise License

Hi Jessica,

Our procurement team has reviewed and approved the Enterprise License for 500 seats at $85K annually.

Legal signed off on the MSA. Please send the Order Form.

Thanks,
Robert Chen
Director of IT

---
Sent from my iPhone

On Fri, Jan 10, 2025, Jessica wrote:
> Thanks for the inquiry...
> Best regards, Jessica

© 2025 Service Company
Unsubscribe: https://example.com/unsub
```

**AFTER (Cleaned for Classification):**
```
Our procurement team has reviewed and approved the Enterprise License for 500 seats at $85K annually. Legal signed off on the MSA. Please send the Order Form.
```

---

## 🎨 Response Actions & UI Display

Based on the `label` and `confidence`, use these recommended actions:

| Label | Color | Confidence | Action | Urgency |
|-------|-------|-----------|--------|---------|
| **🟢 HOT** | Green | > 80% | ⚡ **Call immediately** | CRITICAL |
| **🟡 WARM** | Yellow | > 70% | 📧 Send meeting link | HIGH |
| **❄️ COLD** | Gray | > 60% | 📝 Add to nurture | MEDIUM |
| **🔴 SPAM** | Red | > 75% | 🗑️ Archive/Delete | LOW |
| **🔴 ABUSE** | Dark Red | > 80% | 🔒 Block/Report | CRITICAL |

---

## 📊 Example Frontend Integration (React)

```jsx
import React, { useState } from 'react';

const EmailClassifier = () => {
  const [email, setEmail] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const classifyEmail = async () => {
    setLoading(true);
    try {
      const response = await fetch('https://email-classifier-api.onrender.com/classify', {
        method: 'POST',
        headers: {
          'X-API-Key': 'sk-emailclassifier-2024-prod',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          subject: email.subject,
          body: email.body,
          preprocess: true
        })
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Classification failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const getLabelColor = (label) => {
    const colors = {
      HOT: '#10b981',
      WARM: '#f59e0b',
      COLD: '#6b7280',
      SPAM: '#ef4444',
      ABUSE: '#7f1d1d'
    };
    return colors[label] || '#9ca3af';
  };

  return (
    <div>
      <textarea
        value={email.body}
        onChange={(e) => setEmail({ ...email, body: e.target.value })}
        placeholder="Paste email here..."
      />
      <button onClick={classifyEmail} disabled={loading}>
        {loading ? 'Classifying...' : 'Classify Email'}
      </button>

      {result && (
        <div style={{ borderLeft: `4px solid ${getLabelColor(result.label)}`, padding: '10px' }}>
          <strong style={{ color: getLabelColor(result.label) }}>
            {result.label}
          </strong>
          <p>{result.confidence}% confidence</p>
          <p><strong>Action:</strong> {result.action}</p>
        </div>
      )}
    </div>
  );
};

export default EmailClassifier;
```

---

## ⚠️ Important Notes

### 1. **API Key Security**
- Never expose API key in frontend code (use backend proxy)
- Store securely in environment variables
- Contact support to rotate key if compromised

### 2. **Preprocessing**
- The API **automatically handles messy emails** when `preprocess: true`
- You can **skip preprocessing** if emails are already clean
- Preprocessing is **included in the request**, no additional cost

### 3. **Rate Limits**
- Default: 1000 requests/day per API key
- Batch endpoint: Max 100 emails per request
- Contact for higher limits

### 4. **Best Practices**
✅ Use `preprocess: true` for emails from email clients (Gmail, Outlook, etc.)
✅ Use `preprocess: false` if you've already cleaned emails
✅ Include subject line for better context
✅ Use batch endpoint for multiple emails (more efficient)
✅ Cache results to avoid duplicate classifications

---

## 🔍 Example API Response Fields

```json
{
  "label": "HOT",           // Classification label
  "confidence": 96.2,       // 0-100 confidence percentage
  "action": "...",          // Recommended action
  "needs_review": false,    // Manual review flag
  "preprocessing_applied": true,  // Whether email was cleaned
  "client": "default",      // API key identifier
  "timestamp": "..."        // ISO timestamp of classification
}
```

---

## 🐛 Troubleshooting

### Empty Response
- Ensure `body` or `subject` is provided
- Check API key in headers

### Low Confidence Scores
- Email may be ambiguous or missing context
- Include subject line for better results
- Check preprocessing output

### 401 Unauthorized
- Verify API key is correct
- Use `X-API-Key` header (not query parameter)
- Check for typos in key

### 504 Gateway Timeout
- Server might be restarting
- Retry after 30 seconds
- Contact support for persistent issues

---

## 📞 Support

- Email: support@example.com
- Status: https://status.example.com
- Docs: https://docs.example.com

---

## 🎓 What Gets Classified

The classifier analyzes the **email intent** after cleaning:

- **✅ HOT**: "We've approved", "Ready to buy", "Signing MSA", "Need immediate help"
- **✅ WARM**: "Would like to discuss", "Evaluating options", "Send demo"
- **✅ COLD**: "Not interested", "Budget doesn't allow", "Maybe next year"
- **✅ SPAM**: Generic newsletters, mass marketing, unrelated offers
- **✅ ABUSE**: Threats, hostile language, spam attacks

The preprocessing ensures **only relevant business content** is classified! 🎯
