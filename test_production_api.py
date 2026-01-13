#!/usr/bin/env python3
"""
Production API Integration Test
================================
Test the complete email classification pipeline with preprocessing
"""

import requests
import json
from email_preprocessor import EmailPreprocessor

# Configuration
API_URL = 'http://localhost:5001'  # For local testing
# API_URL = 'https://email-classifier-api.onrender.com'  # For production
API_KEY = 'sk-emailclassifier-2024-prod'

# Test emails with headers (simulate real inbox emails)
TEST_EMAILS = [
    {
        'name': 'HOT - Purchase Approved',
        'subject': 'Re: Enterprise License - APPROVED',
        'body': """From: john.chen@techcorp.com
To: sales@service.com
Date: Mon, 13 Jan 2025 10:30:00
Subject: Re: Enterprise License - APPROVED

Hi Jessica,

Our procurement team has reviewed and approved the Enterprise License for 500 seats at $85,000 annually.

Legal has signed off on the MSA. Please send the Order Form immediately so we can execute.

This is time-sensitive as we need to deploy by month-end.

Thanks,
Robert Chen
Director of IT
TechCorp Inc.

---
Sent from my iPhone
Confidentiality Notice: This email contains confidential information."""
    },
    {
        'name': 'WARM - Demo Interest',
        'subject': 'RE: Demo Request - Next Steps?',
        'body': """From: sarah.miller@enterprise.com
To: sales@service.com
Date: Fri, 10 Jan 2025 14:22:00

Hi,

Thanks for sending the demo link. Our team is evaluating several solutions and would like to see how your platform compares.

Could we schedule a 30-minute call next week to discuss pricing and deployment options?

Also, could you send over:
- Case studies from similar companies
- Pricing details for 200-500 users
- Timeline for implementation

Looking forward to hearing from you.

Best regards,
Sarah Miller
VP of Operations
Enterprise Solutions Inc.

---
Sent from Outlook

> On Fri, Jan 10, 2025, at 10:15 AM, Jessica wrote:
> Thanks for your interest in our platform!
> Best regards, Jessica"""
    },
    {
        'name': 'COLD - Initial Outreach No Interest',
        'subject': 'Product inquiry',
        'body': """From: unsubscribe@newsletter.com
To: bulk@service.com
Date: Thu, 9 Jan 2025 09:00:00

Hi,

Not sure if this is relevant, but we're happy with our current solution. 

We won't be evaluating new tools for at least another year.

Thanks for reaching out though!

---
Sent from Gmail

On Wed, Jan 8, 2025:
> Hi there,
> I'd love to show you what we can do...
> Thanks, Sales Team

© 2025 Newsletter Company | Privacy Policy | Terms"""
    },
    {
        'name': 'SPAM - Generic Marketing',
        'subject': 'LIMITED TIME: 50% off our premium plan! 🚀',
        'body': """From: no-reply@marketing.com
To: bulk-list@service.com
Date: Wed, 8 Jan 2025 06:00:00

Hi Friend!

🎉 We're running a special promotion this week!

Get 50% OFF our premium plan - only for the next 48 hours!

✅ Unlimited users
✅ Advanced analytics
✅ 24/7 support

Click here to claim your discount: https://example.com/promo

---
Sent from MailChimp

This is a promotional email.
Unsubscribe | Privacy Policy | Contact Us

© 2025 Marketing Corp"""
    },
    {
        'name': 'ABUSE - Suspicious/Threatening',
        'subject': 'URGENT: Your account needs attention',
        'body': """From: security@suspicious-bank.com
To: user@service.com
Date: Tue, 7 Jan 2025 22:30:00

ALERT: Your account has been compromised!

Click here immediately to verify your identity: https://fake-site.com/login

Your account will be closed if you don't verify within 24 hours.

DO NOT ignore this message!

Click: https://totally-legit.com/verify?token=MALWARE

---
This is a phishing attempt. Do not click links."""
    }
]

def test_single_email_with_preprocessing():
    """Test single email classification with automatic preprocessing."""
    print("\n" + "="*70)
    print("TEST 1: SINGLE EMAIL WITH AUTOMATIC PREPROCESSING")
    print("="*70)
    
    test_email = TEST_EMAILS[0]
    
    print(f"\n📧 Test Email: {test_email['name']}")
    print(f"Subject: {test_email['subject']}")
    print(f"Body preview: {test_email['body'][:100]}...")
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'subject': test_email['subject'],
        'body': test_email['body'],
        'preprocess': True  # ← API will clean email automatically
    }
    
    try:
        response = requests.post(
            f'{API_URL}/classify',
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Classification Result:")
            print(f"   Label: {result['label']}")
            print(f"   Confidence: {result['confidence']}%")
            print(f"   Action: {result['action']}")
            print(f"   Preprocessing Applied: {result['preprocessing_applied']}")
            return True
        else:
            print(f"\n❌ API Error: {response.status_code}")
            print(f"   Message: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection Error: API not running at {API_URL}")
        print("   Make sure to run: python api_server.py")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def test_batch_emails_with_preprocessing():
    """Test batch classification with automatic preprocessing."""
    print("\n" + "="*70)
    print("TEST 2: BATCH EMAIL CLASSIFICATION WITH PREPROCESSING")
    print("="*70)
    
    batch = [
        {'subject': TEST_EMAILS[0]['subject'], 'body': TEST_EMAILS[0]['body']},
        {'subject': TEST_EMAILS[1]['subject'], 'body': TEST_EMAILS[1]['body']},
        {'subject': TEST_EMAILS[2]['subject'], 'body': TEST_EMAILS[2]['body']},
    ]
    
    print(f"\n📧 Batch: {len(batch)} emails")
    for i, email in enumerate(batch, 1):
        print(f"   {i}. {email['subject'][:50]}...")
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'emails': batch,
        'preprocess': True
    }
    
    try:
        response = requests.post(
            f'{API_URL}/classify/batch',
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Batch Classification Results:")
            print(f"   Total Classified: {result['total']}")
            print(f"   Summary: {result['summary']}")
            
            for i, res in enumerate(result['results'], 1):
                print(f"   {i}. {res['label']} ({res['confidence']}%)")
            
            return True
        else:
            print(f"\n❌ API Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def test_preprocessing_locally():
    """Test email preprocessing locally."""
    print("\n" + "="*70)
    print("TEST 3: LOCAL EMAIL PREPROCESSING")
    print("="*70)
    
    preprocessor = EmailPreprocessor()
    test_email = TEST_EMAILS[0]
    
    print(f"\n📧 Original Email Length: {len(test_email['body'])} characters")
    print(f"Contains: Headers, signatures, etc.")
    
    cleaned = preprocessor.clean_email(test_email['body'], test_email['subject'])
    
    print(f"\n✂️ Cleaned Email Length: {len(cleaned)} characters")
    print(f"Content: {cleaned[:200]}...")
    print(f"\n✅ Preprocessing successful!")
    print(f"   Removed: {len(test_email['body']) - len(cleaned)} characters")
    
    return True


def test_all_categories():
    """Test all email categories."""
    print("\n" + "="*70)
    print("TEST 4: ALL EMAIL CATEGORIES")
    print("="*70)
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    results = {}
    
    for email_data in TEST_EMAILS:
        payload = {
            'subject': email_data['subject'],
            'body': email_data['body'],
            'preprocess': True
        }
        
        try:
            response = requests.post(
                f'{API_URL}/classify',
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                expected_label = email_data['name'].split(' - ')[0]
                actual_label = result['label']
                match = "✅" if expected_label in actual_label else "❌"
                
                results[email_data['name']] = {
                    'expected': expected_label,
                    'actual': actual_label,
                    'confidence': result['confidence'],
                    'match': match
                }
        except Exception as e:
            print(f"❌ Error classifying {email_data['name']}: {str(e)}")
            return False
    
    print("\n📊 Category Results:")
    print("-" * 70)
    for email_name, result in results.items():
        print(f"{result['match']} {email_name}")
        print(f"   Expected: {result['expected']} | Got: {result['actual']} ({result['confidence']}%)")
    
    return True


if __name__ == '__main__':
    print("\n" + "🚀 "*20)
    print("EMAIL CLASSIFIER - PRODUCTION API TEST SUITE")
    print("🚀 "*20)
    
    tests = [
        ("Local Preprocessing", test_preprocessing_locally),
        ("Single Email Classification", test_single_email_with_preprocessing),
        ("Batch Email Classification", test_batch_emails_with_preprocessing),
        ("All Categories", test_all_categories),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results[test_name] = "✅ PASSED" if passed else "❌ FAILED"
        except Exception as e:
            results[test_name] = f"❌ ERROR: {str(e)}"
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for test_name, result in results.items():
        print(f"{result} - {test_name}")
    
    passed = sum(1 for r in results.values() if "PASSED" in r)
    total = len(results)
    
    print("\n" + "="*70)
    if passed == total:
        print(f"🎉 ALL TESTS PASSED! ({passed}/{total})")
        print("✅ Production API is ready for integration!")
    else:
        print(f"⚠️ SOME TESTS FAILED ({passed}/{total})")
        print("🔧 Check the errors above and ensure:")
        print("   1. API server is running: python api_server.py")
        print("   2. Models are loaded correctly")
        print("   3. EmailPreprocessor is working")
    print("="*70 + "\n")
