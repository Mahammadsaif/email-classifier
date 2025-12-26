"""
3-Stage Hierarchical Email Classifier
======================================
Stage 1: ABUSE Detection (99.4% accuracy)
Stage 2: SPAM Detection (99.4% accuracy)  
Stage 3: HOT/WARM/COLD Classification (92.9% accuracy)

Flow: Email → Is ABUSE? → Is SPAM? → HOT/WARM/COLD
"""

import joblib
import os
import numpy as np

# Configuration
CONFIDENCE_THRESHOLD = 0.70  # 70% threshold
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

# Load models lazily
_models = {}

def _load_models():
    """Load all 3-stage models."""
    if not _models:
        # Stage 1: ABUSE detector
        _models['abuse_model'] = joblib.load(os.path.join(MODEL_DIR, 'abuse_detector.joblib'))
        _models['abuse_tfidf'] = joblib.load(os.path.join(MODEL_DIR, 'abuse_tfidf.joblib'))
        
        # Stage 2: SPAM detector
        _models['spam_model'] = joblib.load(os.path.join(MODEL_DIR, 'spam_detector.joblib'))
        _models['spam_tfidf'] = joblib.load(os.path.join(MODEL_DIR, 'spam_tfidf.joblib'))
        
        # Stage 3: Intent classifier
        _models['intent_model'] = joblib.load(os.path.join(MODEL_DIR, 'intent_classifier.joblib'))
        _models['intent_tfidf'] = joblib.load(os.path.join(MODEL_DIR, 'intent_tfidf.joblib'))
        _models['intent_le'] = joblib.load(os.path.join(MODEL_DIR, 'intent_label_encoder.joblib'))
    return _models


def get_action(label):
    """Get recommended action for each label."""
    actions = {
        'HOT': 'IMMEDIATE FOLLOW-UP REQUIRED - High interest lead, contact within 24 hours',
        'WARM': 'SCHEDULE FOLLOW-UP - Moderate interest, add to nurture sequence',
        'COLD': 'ADD TO NURTURE LIST - Low interest, continue general outreach',
        'SPAM': 'AUTO-DELETE - Move to spam folder, no action needed',
        'ABUSE': 'BLOCK & REPORT - Abusive content, block sender and document',
        'NEEDS_REVIEW': 'MANUAL REVIEW REQUIRED - Model uncertain, human review needed'
    }
    return actions.get(label, 'Unknown action')


def classify_email(body, subject=''):
    """
    Classify email using 3-stage hierarchical model.
    
    Flow:
    1. Check if ABUSE → return ABUSE
    2. Check if SPAM → return SPAM
    3. Classify as HOT/WARM/COLD
    
    Args:
        body: Email body text
        subject: Email subject (optional)
    
    Returns:
        dict with classification result
    """
    models = _load_models()
    
    # Combine subject and body
    text = f"{subject} {body}".strip()
    
    if not text:
        return {
            'label': 'NEEDS_REVIEW',
            'confidence': 0.0,
            'action': 'Empty email - manual review required',
            'stage': 'none',
            'needs_review': True
        }
    
    # ========================================
    # STAGE 1: ABUSE Detection (binary: 0=NOT_ABUSE, 1=ABUSE)
    # ========================================
    X1 = models['abuse_tfidf'].transform([text])
    abuse_proba = models['abuse_model'].predict_proba(X1)[0]
    abuse_pred = models['abuse_model'].predict(X1)[0]
    
    # Get ABUSE probability (class 1 = ABUSE)
    abuse_classes = list(models['abuse_model'].classes_)
    abuse_idx = 1 if 1 in abuse_classes else abuse_classes.index(max(abuse_classes))
    abuse_conf = float(abuse_proba[abuse_idx])
    
    # abuse_pred is 1 for ABUSE, 0 for NOT_ABUSE
    if abuse_pred == 1 and abuse_conf >= CONFIDENCE_THRESHOLD:
        return {
            'label': 'ABUSE',
            'confidence': round(abuse_conf * 100, 1),
            'action': get_action('ABUSE'),
            'stage': 'abuse_detection',
            'needs_review': False
        }
    
    # ========================================
    # STAGE 2: SPAM Detection
    # ========================================
    X2 = models['spam_tfidf'].transform([text])
    spam_proba = models['spam_model'].predict_proba(X2)[0]
    spam_pred = models['spam_model'].predict(X2)[0]
    
    # Get SPAM probability (class 1 = SPAM)
    spam_classes = list(models['spam_model'].classes_)
    spam_idx = 1 if 1 in spam_classes else spam_classes.index(max(spam_classes))
    spam_conf = float(spam_proba[spam_idx])
    
    # spam_pred is 1 for SPAM, 0 for NOT_SPAM
    if spam_pred == 1 and spam_conf >= CONFIDENCE_THRESHOLD:
        return {
            'label': 'SPAM',
            'confidence': round(spam_conf * 100, 1),
            'action': get_action('SPAM'),
            'stage': 'spam_detection',
            'needs_review': False
        }
    
    # ========================================
    # STAGE 3: HOT/WARM/COLD Classification
    # ========================================
    X3 = models['intent_tfidf'].transform([text])
    intent_proba = models['intent_model'].predict_proba(X3)[0]
    intent_pred_idx = models['intent_model'].predict(X3)[0]
    intent_label = models['intent_le'].inverse_transform([intent_pred_idx])[0]
    intent_conf = float(max(intent_proba))
    
    # Apply confidence threshold
    needs_review = intent_conf < CONFIDENCE_THRESHOLD
    final_label = intent_label if not needs_review else 'NEEDS_REVIEW'
    
    return {
        'label': final_label,
        'predicted_label': intent_label,
        'confidence': round(intent_conf * 100, 1),
        'action': get_action(final_label),
        'stage': 'intent_classification',
        'needs_review': needs_review
    }


def classify_batch(emails):
    """Classify multiple emails."""
    results = []
    for email in emails:
        body = email.get('body', '')
        subject = email.get('subject', '')
        result = classify_email(body, subject)
        result['input'] = {'subject': subject[:50], 'body': body[:100]}
        results.append(result)
    return results


if __name__ == '__main__':
    # Test on the 7 failed examples
    test_cases = [
        {'subject': 'Purchase Order #12345 - Final Approval', 'body': "Hi, we've completed internal review and our CFO has signed off. Please send the final paperwork so we can process payment this week.", 'expected': 'HOT'},
        {'subject': 'Re: Your solution for our team', 'body': "Thanks for reaching out. We're currently evaluating several options. Can we schedule a call next month to discuss further?", 'expected': 'WARM'},
        {'subject': 'URGENT: Your account will be closed', 'body': 'Dear user, your account has suspicious activity. Verify your identity immediately by clicking here and entering your password.', 'expected': 'SPAM'},
        {'subject': 'Re: Re: Re: Fw: Fw: Check this out', 'body': 'lol this is hilarious [LINK] you have to see this everyone is sharing it', 'expected': 'SPAM'},
        {'subject': 'TERRIBLE SERVICE - YOU WILL PAY', 'body': "This is the worst company I've ever dealt with. You're all incompetent idiots. I will make sure everyone knows what a scam you're running. Expect a lawsuit.", 'expected': 'ABUSE'},
        {'subject': 'I know where you work', 'body': "You think you can ignore me? I have your personal information. I know where your office is. This isn't over.", 'expected': 'ABUSE'},
        {'subject': 'Final warning', 'body': "I have been trying to reach you for weeks. If you don't respond within 24 hours, I will personally come to your office and we can settle this face to face.", 'expected': 'ABUSE'},
    ]
    
    print("="*70)
    print("TESTING 7 EXAMPLES WITH 3-STAGE MODEL")
    print("="*70)
    
    correct = 0
    for i, tc in enumerate(test_cases, 1):
        result = classify_email(tc['body'], tc['subject'])
        predicted = result['label']
        expected = tc['expected']
        match = '✅' if predicted == expected else '❌'
        if predicted == expected:
            correct += 1
        print(f"\n{i}. {tc['subject'][:45]}...")
        print(f"   Expected: {expected} | Predicted: {predicted} {match}")
        print(f"   Confidence: {result['confidence']}% | Stage: {result['stage']}")
    
    print(f"\n{'='*70}")
    print(f"RESULT: {correct}/7 correct ({correct/7*100:.0f}%)")
    print("="*70)
