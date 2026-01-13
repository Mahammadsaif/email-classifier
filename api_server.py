"""
Email Classification API with API Key Authentication
=====================================================
REST API for hierarchical email classification
Includes: API key auth, rate limiting, batch classification
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import os
import secrets
from datetime import datetime, timezone

# Import the hierarchical classifier
from predict_hierarchical import classify_email, classify_batch
from email_preprocessor import EmailPreprocessor

app = Flask(__name__)
CORS(app)

# ============================================================================
# API KEY CONFIGURATION
# ============================================================================
# Generate a secure API key (you can also set via environment variable)
DEFAULT_API_KEY = os.environ.get('EMAIL_CLASSIFIER_API_KEY', 'sk-emailclassifier-2024-prod')

# Multiple API keys for different clients (add more as needed)
VALID_API_KEYS = {
    DEFAULT_API_KEY: {'name': 'default', 'rate_limit': 1000},
    'sk-test-key-12345': {'name': 'test', 'rate_limit': 100},
}

# ============================================================================
# AUTHENTICATION DECORATOR
# ============================================================================
def require_api_key(f):
    """Decorator to require API key for endpoints."""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = None
        
        # Check header first (preferred method)
        if 'X-API-Key' in request.headers:
            api_key = request.headers['X-API-Key']
        elif 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                api_key = auth_header[7:]
        # Also check query parameter (for simple testing)
        elif 'api_key' in request.args:
            api_key = request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                'error': 'API key required',
                'message': 'Please provide API key via X-API-Key header or Bearer token'
            }), 401
        
        if api_key not in VALID_API_KEYS:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is not valid'
            }), 403
        
        # Add client info to request
        request.client_info = VALID_API_KEYS[api_key]
        
        return f(*args, **kwargs)
    return decorated


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def home():
    """API information and health check."""
    return jsonify({
        'name': 'Email Classification API',
        'version': '2.0.0',
        'model': 'Hierarchical SVM (Stage 1: JUNK Filter, Stage 2: Intent)',
        'classes': ['HOT', 'WARM', 'COLD', 'SPAM', 'ABUSE'],
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            '/classify': 'POST - Classify single email (requires API key)',
            '/classify/batch': 'POST - Classify multiple emails (requires API key)',
            '/health': 'GET - Health check (no auth required)'
        },
        'authentication': 'API key required via X-API-Key header or Bearer token'
    })


@app.route('/health')
def health():
    """Health check endpoint (no auth required)."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/classify', methods=['POST'])
@require_api_key
def classify():
    """
    Classify a single email.
    
    Request body:
        {
            "subject": "Email subject (optional)",
            "body": "Email body text (required) - can be raw email with headers/signatures",
            "preprocess": true (optional, default: true)
        }
    
    Response:
        {
            "label": "HOT|WARM|COLD|SPAM|ABUSE",
            "confidence": 85.5,
            "action": "Recommended action",
            "needs_review": false,
            "preprocessing_applied": true
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body required'}), 400
        
        body = data.get('body', '')
        subject = data.get('subject', '')
        should_preprocess = data.get('preprocess', True)
        
        if not body and not subject:
            return jsonify({'error': 'Email body or subject required'}), 400
        
        # Preprocess email if requested (removes headers, signatures, etc.)
        preprocessing_applied = False
        if should_preprocess and body:
            preprocessor = EmailPreprocessor()
            body = preprocessor.clean_email(body, subject)
            preprocessing_applied = True
        
        result = classify_email(body, subject)
        result['client'] = request.client_info['name']
        result['timestamp'] = datetime.now(timezone.utc).isoformat()
        result['preprocessing_applied'] = preprocessing_applied
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': 'Classification failed',
            'message': str(e)
        }), 500


@app.route('/classify/batch', methods=['POST'])
@require_api_key
def classify_batch_endpoint():
    """
    Classify multiple emails in batch.
    
    Request body:
        {
            "emails": [
                {"subject": "...", "body": "..."},
                {"subject": "...", "body": "..."}
            ],
            "preprocess": true (optional, default: true)
        }
    
    Response:
        {
            "results": [...],
            "total": 2,
            "summary": {"HOT": 1, "COLD": 1}
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'emails' not in data:
            return jsonify({'error': 'emails array required'}), 400
        
        emails = data['emails']
        should_preprocess = data.get('preprocess', True)
        
        if not isinstance(emails, list):
            return jsonify({'error': 'emails must be an array'}), 400
        
        if len(emails) > 100:
            return jsonify({'error': 'Maximum 100 emails per batch'}), 400
        
        # Preprocess emails if requested
        preprocessor = EmailPreprocessor() if should_preprocess else None
        processed_emails = []
        for email in emails:
            processed = email.copy()
            if should_preprocess and email.get('body'):
                processed['body'] = preprocessor.clean_email(
                    email['body'], 
                    email.get('subject', '')
                )
                processed['preprocessing_applied'] = True
            processed_emails.append(processed)
        
        results = classify_batch(processed_emails)
        
        # Calculate summary
        summary = {}
        needs_review_count = 0
        for r in results:
            label = r.get('label', 'UNKNOWN')
            summary[label] = summary.get(label, 0) + 1
            if r.get('needs_review', False):
                needs_review_count += 1
        
        return jsonify({
            'results': results,
            'total': len(results),
            'summary': summary,
            'needs_review_count': needs_review_count,
            'client': request.client_info['name'],
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Batch classification failed',
            'message': str(e)
        }), 500


@app.route('/generate-key', methods=['POST'])
def generate_key():
    """
    Generate a new API key (for admin use only - should be secured in production).
    """
    # In production, this should require admin authentication
    new_key = f"sk-{secrets.token_hex(16)}"
    return jsonify({
        'api_key': new_key,
        'message': 'Add this key to VALID_API_KEYS dictionary to activate'
    })


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("📧 EMAIL CLASSIFICATION API SERVER")
    print("="*70)
    print(f"\n🔑 Default API Key: {DEFAULT_API_KEY}")
    print(f"🔑 Test API Key: sk-test-key-12345")
    print("\n📍 Endpoints:")
    print("   GET  /          - API info")
    print("   GET  /health    - Health check")
    print("   POST /classify  - Classify single email")
    print("   POST /classify/batch - Classify multiple emails")
    print("\n🔒 Authentication:")
    print("   Header: X-API-Key: <your-api-key>")
    print("   OR: Authorization: Bearer <your-api-key>")
    print("="*70)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
