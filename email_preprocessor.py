"""
Email Preprocessing Utility
Cleans raw emails for classification
"""

import re
from typing import Dict

class EmailPreprocessor:
    """Extracts and cleans email body for classification"""
    
    @staticmethod
    def clean_email(raw_email: str, subject: str = "") -> str:
        """
        Clean raw email to extract only relevant content for classification
        
        Args:
            raw_email: Full email with headers, signatures, etc.
            subject: Email subject (optional, can be prepended)
            
        Returns:
            Clean email body for classification
        """
        
        # 1. REMOVE EMAIL HEADERS
        # Remove "From:", "To:", "CC:", "Date:", "Subject:", etc.
        text = re.sub(r'^From:.*?\n', '', raw_email, flags=re.MULTILINE)
        text = re.sub(r'^To:.*?\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'^CC:.*?\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'^BCC:.*?\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'^Date:.*?\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'^Subject:.*?\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'^Message-ID:.*?\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'^In-Reply-To:.*?\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'^References:.*?\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'^MIME-Version:.*?\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'^Content-Type:.*?\n', '', text, flags=re.MULTILINE)
        
        # 2. REMOVE QUOTED TEXT (previous emails in reply chains)
        # Remove lines starting with ">" or "On ... wrote:"
        lines = text.split('\n')
        filtered_lines = []
        skip_until_empty = False
        
        for line in lines:
            # Skip quoted lines (start with >)
            if line.strip().startswith('>'):
                continue
            # Skip "On [date] wrote:" pattern
            if re.match(r'On .+? wrote:', line.strip()):
                skip_until_empty = True
                continue
            # Skip divider lines
            if re.match(r'^[-_]{3,}', line.strip()):
                skip_until_empty = True
                continue
            filtered_lines.append(line)
        
        text = '\n'.join(filtered_lines)
        
        # 3. REMOVE SIGNATURES
        # Common signature patterns
        signature_patterns = [
            r'--\s*\n.*',  # Double dash signature separator
            r'___\s*\n.*',  # Underscore separator
            r'~{3,}\s*\n.*',  # Tilde separator
            r'Sent from.*',  # "Sent from my iPhone"
            r'Get Outlook.*',  # Outlook footer
            r'Envoyé de mon.*',  # French Outlook
        ]
        
        for pattern in signature_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
        
        # 4. REMOVE UNSUBSCRIBE LINKS AND FOOTERS
        # Remove "Click here to unsubscribe", privacy policies, etc.
        unsub_patterns = [
            r'unsubscribe.*',
            r'click here.*',
            r'privacy policy.*',
            r'terms of service.*',
            r'manage your preferences.*',
            r'this is a promotional message.*',
            r'©.*\d{4}',  # Copyright notices
        ]
        
        for pattern in unsub_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
        
        # 5. REMOVE HTML TAGS
        # Convert HTML entities and remove tags
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&amp;', '&')
        
        # 6. REMOVE EXCESSIVE WHITESPACE
        # Collapse multiple spaces, tabs, newlines
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
        text = text.strip()  # Remove leading/trailing whitespace
        
        # 7. PREPEND SUBJECT (OPTIONAL - improves classification)
        if subject:
            subject_clean = subject.strip()
            text = f"{subject_clean} {text}"
        
        return text
    
    @staticmethod
    def extract_body_and_subject(raw_email: str) -> Dict[str, str]:
        """
        Extract subject and body from raw email
        
        Returns:
            Dict with 'subject' and 'body' keys
        """
        lines = raw_email.split('\n')
        subject = ""
        body_start = 0
        
        # Find subject line
        for i, line in enumerate(lines):
            if line.startswith('Subject:'):
                subject = line.replace('Subject:', '').strip()
                body_start = i + 1
                break
        
        # Rest is body
        body = '\n'.join(lines[body_start:])
        
        return {
            'subject': subject,
            'body': body
        }

# Example usage in API
def preprocess_for_classification(raw_email: str, subject: str = "") -> str:
    """Convenience function for API"""
    preprocessor = EmailPreprocessor()
    return preprocessor.clean_email(raw_email, subject)


if __name__ == "__main__":
    # Test example
    messy_email = """From: john@company.com
To: sales@service.com
CC: manager@company.com
Date: Mon, 13 Jan 2025 10:30:00 +0000
Subject: Re: Enterprise License Agreement
Message-ID: <123456@company.com>

Hi Jessica,

Our procurement team has reviewed and approved the Enterprise License for 500 seats at $85K annually. Legal signed off on the MSA. Please send the Order Form and W9 so we can process payment through our Q1 budget. Need this executed by Jan 31st.

Thanks,
Robert Chen
Director of IT, Acme Corp
Phone: (555) 123-4567
Cell: (555) 987-6543

---

On Fri, Jan 10, 2025 at 2:15 PM, Jessica Smith <jessica@service.com> wrote:

> Hi Robert,
> 
> Thanks for the inquiry. Here's our pricing for Enterprise...
> 
> Best,
> Jessica

--
Sent from my iPhone
Get Outlook for iOS

© 2025 Service Company. All rights reserved.
Click here to unsubscribe: https://example.com/unsub
Privacy Policy: https://example.com/privacy"""

    preprocessor = EmailPreprocessor()
    clean = preprocessor.clean_email(messy_email, "Re: Enterprise License Agreement")
    
    print("ORIGINAL EMAIL:")
    print("=" * 80)
    print(messy_email)
    print("\n" + "=" * 80)
    print("CLEANED EMAIL:")
    print("=" * 80)
    print(clean)
