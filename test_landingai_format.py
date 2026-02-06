#!/usr/bin/env python3
"""
Quick test for LandingAI API format based on error message
"""

import requests
import json

def test_landingai_format():
    """Test the exact format LandingAI wants"""
    
    API_KEY = "b3JjNWdsYjZobXFmaXd6ZmdsM3g0OmFHSjVUVjg0dGJRTGlFWjVVSDFhUjd2WVVVd2RjeDh0"
    ENDPOINT = "https://api.va.landing.ai/v1/ade/parse"
    
    # Simple test document
    test_doc = """
    <h1>Apple Inc. Financial Summary</h1>
    <p>Total Revenue: $383.3 billion</p>
    <p>Net Income: $97.0 billion</p>
    <p>Total Assets: $352.8 billion</p>
    """
    
    # Test formats based on error message
    test_formats = [
        # Format 1: document parameter (direct content)
        {
            "payload": {
                "document": test_doc,
                "prompt": "Extract revenue, net income and assets as JSON"
            },
            "name": "Direct document content"
        },
        
        # Format 2: document parameter (base64 encoded)
        {
            "payload": {
                "document": "PGgxPkFwcGxlIEluYy4gRmluYW5jaWFsIFN1bW1hcnk8L2gxPgo8cD5Ub3RhbCBSZXZlbnVlOiAkMzgzLjMgYmlsbGlvbjwvcD4KPHA+TmV0IEluY29tZTogJDk3LjAgYmlsbGlvbjwvcD4KPHA+VG90YWwgQXNzZXRzOiAkMzUyLjggYmlsbGlvbjwvcD4=",  # base64 of test_doc
                "prompt": "Extract revenue, net income and assets as JSON"
            },
            "name": "Base64 encoded document"
        },
        
        # Format 3: document_url parameter (though we don't have a URL)
        # Skip this one since we don't have a URL
        
        # Format 4: With model parameter
        {
            "payload": {
                "document": test_doc,
                "prompt": "Extract revenue, net income and assets as JSON",
                "model": "dpt-2-latest"
            },
            "name": "With model parameter"
        }
    ]
    
    print(f"🧪 Testing LandingAI API Format")
    print(f"Endpoint: {ENDPOINT}")
    print(f"API Key: {API_KEY[:15]}...")
    print("=" * 60)
    
    for i, test in enumerate(test_formats, 1):
        print(f"\n{i}. Testing: {test['name']}")
        
        # Try different auth methods
        auth_methods = [
            {"Authorization": f"Bearer {API_KEY}"},
            {"apikey": API_KEY},
            {"X-API-Key": API_KEY}
        ]
        
        for j, auth_header in enumerate(auth_methods, 1):
            headers = {**auth_header, "Content-Type": "application/json"}
            
            try:
                response = requests.post(
                    ENDPOINT,
                    json=test['payload'],
                    headers=headers,
                    timeout=30
                )
                
                print(f"   Auth {j}: Status {response.status_code}")
                
                if response.status_code == 200:
                    print(f"   ✅ SUCCESS! Working format found!")
                    result = response.json()
                    print(f"   Response: {json.dumps(result, indent=2)[:300]}...")
                    return test, auth_header
                else:
                    print(f"   Response: {response.text[:100]}")
                    
            except Exception as e:
                print(f"   Error: {str(e)[:50]}")
    
    print(f"\n" + "=" * 60)
    print("❌ All formats failed. Check API documentation.")
    return None, None

if __name__ == "__main__":
    test_landingai_format()
