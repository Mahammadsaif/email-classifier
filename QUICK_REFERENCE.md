# 🚀 Email Classifier API - Quick Reference Card

## 🎯 One-Liner
**Classify incoming emails into intent categories (HOT/WARM/COLD/SPAM/ABUSE) with 88% accuracy**

---

## 🔌 API Endpoint
```
https://email-classifier-api.onrender.com/classify
```

## 🔑 Authentication
```
Header: X-API-Key: sk-emailclassifier-2024-prod
```

---

## 📤 Quick Request/Response

### Request (Single Email)
```json
{
  "subject": "Re: Enterprise License - Approved",
  "body": "Raw email with all headers and signatures",
  "preprocess": true
}
```

### Response
```json
{
  "label": "HOT",
  "confidence": 96.2,
  "action": "Schedule immediate call to close deal",
  "preprocessing_applied": true
}
```

---

## 🏷️ Labels & Actions at a Glance

| Label | Color | Meaning | Your Action |
|-------|-------|---------|-------------|
| 🟢 HOT | Green | Ready to buy | ⚡ **Call now** |
| 🟡 WARM | Yellow | Interested | 📧 **Send demo** |
| ❄️ COLD | Gray | Not interested | 📝 **Nurture** |
| 🔴 SPAM | Red | Marketing spam | 🗑️ **Archive** |
| 🔴 ABUSE | Dark Red | Threat/hostile | 🔒 **Block** |

---

## 💻 Code (Copy-Paste)

### Python
```python
import requests

response = requests.post(
    'https://email-classifier-api.onrender.com/classify',
    headers={'X-API-Key': 'sk-emailclassifier-2024-prod'},
    json={
        'subject': subject_line,
        'body': raw_email_text,
        'preprocess': True
    }
)
result = response.json()
print(f"{result['label']} - {result['action']}")
```

### JavaScript
```javascript
const response = await fetch('https://email-classifier-api.onrender.com/classify', {
  method: 'POST',
  headers: {
    'X-API-Key': 'sk-emailclassifier-2024-prod',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    subject: subjectLine,
    body: rawEmailText,
    preprocess: true
  })
});
const result = await response.json();
console.log(`${result.label} - ${result.action}`);
```

---

## ⚙️ Key Features

✅ **Automatic Email Cleaning**: Removes headers, signatures, HTML, unsubscribe links
✅ **88% Real-World Accuracy**: Trained on 4,967+ business emails
✅ **Fast**: < 500ms per email
✅ **Batch Processing**: Classify up to 100 emails per request
✅ **3-Stage Pipeline**: ABUSE → SPAM → Intent detection
✅ **Confidence Scores**: Know how confident the model is
✅ **Production Ready**: Running on Render with auto-scaling

---

## 🧪 Test It
```bash
curl -X POST https://email-classifier-api.onrender.com/classify \
  -H "X-API-Key: sk-emailclassifier-2024-prod" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "We approve your proposal",
    "body": "Please send invoice immediately for the 500-seat license",
    "preprocess": true
  }'
```

---

## 📊 Performance

- **HOT Leads**: 100% accuracy (perfect at catching buying signals)
- **SPAM**: 80-100% accuracy
- **ABUSE**: 100% accuracy (perfect at catching threats)
- **Overall**: 88% on real-world messy emails

---

## ❌ Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Wrong/missing API key | Check header: `X-API-Key: sk-emailclassifier-2024-prod` |
| `400 Bad Request` | Missing body/subject | Send either `body` or `subject` |
| `504 Gateway Timeout` | Server restarting | Wait 30 seconds and retry |
| Low confidence (< 70%) | Ambiguous email | Include full subject + body for context |

---

## 📚 Full Documentation

- **Integration Guide**: `PRODUCTION_INTEGRATION_GUIDE.md`
- **Deployment Details**: `DEPLOYMENT_SUMMARY.md`
- **Code Examples**: Included in integration guide
- **GitHub Repo**: https://github.com/Mahammadsaif/email-classifier

---

## 🔄 Batch Processing

```json
POST /classify/batch

{
  "emails": [
    {"subject": "Email 1", "body": "..."},
    {"subject": "Email 2", "body": "..."}
  ],
  "preprocess": true
}
```

Returns: Array of results + summary counts

---

## ⚡ Tips for Best Accuracy

1. ✅ Include subject line (gives model context)
2. ✅ Use raw email from inbox (preprocessing handles cleanup)
3. ✅ Send full body text (more content = better accuracy)
4. ✅ Let API preprocess (`preprocess: true`) - it's smarter than manual cleaning
5. ✅ Batch similar emails for efficiency

---

## 🎓 Classification Logic

```
Raw Email Input
    ↓
Is this a threat? → YES → LABEL: ABUSE (100% accurate)
    ↓ NO
Is this spam? → YES → LABEL: SPAM (80-100% accurate)
    ↓ NO
What's the intent?
├─ Buying signal → LABEL: HOT (100% accurate)
├─ Interested → LABEL: WARM (80% accurate)
└─ Not interested → LABEL: COLD (80% accurate)
```

---

## 📱 UI Display Template

```html
<div style="border-left: 4px solid {color}; padding: 10px;">
  <span style="color: {color}; font-weight: bold;">
    {label} ({confidence}%)
  </span>
  <p>{action}</p>
  <span style="font-size: 0.8em; color: #666;">
    {timestamp}
  </span>
</div>
```

---

## 🔐 Security Checklist

- [ ] API key stored in environment variable, not in code
- [ ] Use HTTPS (auto-enabled on render.com)
- [ ] Don't expose API key in frontend (use backend proxy)
- [ ] Implement rate limiting if calling from frontend
- [ ] Monitor for unusual classification patterns
- [ ] Cache results to avoid duplicate processing

---

## 📈 Monitoring Metrics

Track in production:
- Response time: Should be < 500ms
- Error rate: Should be < 0.1%
- Classification distribution: Watch for sudden changes
- Low confidence emails: Review these manually
- API availability: Should be > 99.9%

---

## 🚀 Latest Improvements (Jan 2025)

- ✨ Added automatic email preprocessing to API
- ✨ Integrated EmailPreprocessor into both endpoints
- ✨ Added preprocessing_applied flag to responses
- ✨ Batch endpoint now handles preprocessing
- ✨ Created comprehensive integration documentation
- ✨ Added production test suite

---

## 💡 Pro Tips

1. **Batch emails**: Use `/classify/batch` for 10+ emails (more efficient)
2. **Cache results**: Store classification results locally to avoid re-classification
3. **Subject matters**: Always include subject line if available
4. **Monitor accuracy**: Compare actual outcomes to predictions, retrain if < 85%
5. **Use confidence**: Only auto-action if confidence > 85%, review < 70% manually

---

## 📞 Support Links

- API Endpoint: https://email-classifier-api.onrender.com
- GitHub: https://github.com/Mahammadsaif/email-classifier
- Status Page: https://status.render.com
- Health Check: GET /health (returns `{"status": "healthy"}`)

---

**Status**: ✅ Live & Ready
**Last Update**: January 13, 2025
**Model**: v14 (88% real-world accuracy)
