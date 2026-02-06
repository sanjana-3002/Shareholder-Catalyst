#!/usr/bin/env python3
"""
Test LandingAI Agentic Document Analysis API
Using the correct endpoint provided by organizers
"""

import requests
import json

def test_landingai_correct_endpoint():
    """Test the correct LandingAI endpoint"""
    
    API_KEY = "b3JjNWdsYjZobXFmaXd6ZmdsM3g0OmFHSjVUVjg0dGJRTGlFWjVVSDFhUjd2WVVVd2RjeDh0"
    ENDPOINT = "https://api.va.landing.ai/v1/tools/agentic-document-analysis"
    
    print("🎯 Testing Correct LandingAI Endpoint")
    print(f"Endpoint: {ENDPOINT}")
    print(f"API Key: {API_KEY[:10]}...")
    print("\n" + "="*60)
    
    # Test different auth methods with correct endpoint
    auth_methods = [
        {"headers": {"apikey": API_KEY}},
        {"headers": {"Authorization": f"Bearer {API_KEY}"}},
        {"headers": {"Authorization": f"API-Key {API_KEY}"}},
        {"headers": {"X-API-Key": API_KEY}},
        {"headers": {"api-key": API_KEY}},  # lowercase
        {"headers": {"Api-Key": API_KEY}},   # mixed case
    ]
    
    # Create test document
    test_content = b"""
    <html>
    <body>
    <h1>Apple Inc. 10-K Filing (Test)</h1>
    <table>
    <tr><td>Total Revenue</td><td>$383.3 billion</td></tr>
    <tr><td>Net Income</td><td>$97.0 billion</td></tr>
    <tr><td>Total Assets</td><td>$352.8 billion</td></tr>
    </table>
    </body>
    </html>
    """
    
    for i, auth in enumerate(auth_methods, 1):
        print(f"\n{i}. Testing auth method: {list(auth['headers'].keys())[0]}")
        
        try:
            # Test with file upload
            files = {'file': ('test_10k.html', test_content, 'text/html')}
            data = {
                'prompt': 'Extract total revenue, net income, and total assets from this document and return as JSON',
                'response_format': 'json'
            }
            
            response = requests.post(
                ENDPOINT,
                files=files,
                data=data,
                headers=auth['headers'],
                timeout=30
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS! LandingAI is working!")
                print(f"   Response preview: {response.text[:200]}...")
                try:
                    json_response = response.json()
                    print(f"   Parsed JSON: {json_response}")
                except:
                    print(f"   Raw response: {response.text}")
                return True
            elif response.status_code == 401:
                print(f"   🔑 401 - Still unauthorized with this method")
            elif response.status_code == 422:
                print(f"   📝 422 - Validation error (check request format)")
                print(f"   Response: {response.text}")
            else:
                print(f"   ⚠️  {response.status_code} - {response.reason}")
                print(f"   Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n" + "="*60)
    print("❌ Still getting authorization errors")
    print("\nPossible issues:")
    print("1. API key format is still wrong")
    print("2. Need additional parameters (project ID, etc.)")
    print("3. Different request body format required")
    print("4. Key needs to be decoded/transformed")
    
    return False

def test_key_decoding():
    """Test if the API key needs to be decoded"""
    
    print(f"\n🔍 Testing API Key Formats")
    print("="*60)
    
    original_key = "b3JjNWdsYjZobXFmaXd6ZmdsM3g0OmFHSjVUVjg0dGJRTGlFWjVVSDFhUjd2WVVVd2RjeDh0"
    
    # Test 1: Original key
    print(f"1. Original key: {original_key[:20]}...")
    
    # Test 2: Try base64 decode
    try:
        import base64
        decoded = base64.b64decode(original_key).decode('utf-8')
        print(f"2. Base64 decoded: {decoded[:20]}...")
        
        # Check if it's username:password format
        if ':' in decoded:
            parts = decoded.split(':')
            print(f"   Looks like username:password format")
            print(f"   Part 1: {parts[0]}")
            print(f"   Part 2: {parts[1][:10]}...")
        
    except Exception as e:
        print(f"2. Base64 decode failed: {e}")
    
    # Test 3: Try URL decode
    try:
        import urllib.parse
        url_decoded = urllib.parse.unquote(original_key)
        print(f"3. URL decoded: {url_decoded[:20]}...")
    except Exception as e:
        print(f"3. URL decode failed: {e}")

if __name__ == "__main__":
    # Test the key formats first
    test_key_decoding()
    
    # Test the correct endpoint
    test_landingai_correct_endpoint()
    
    print(f"\n💡 Next steps if still failing:")
    print("1. Ask organizers for exact Python example code")
    print("2. Check if you need project ID or model ID parameters")
    print("3. Ask about request body format (JSON vs multipart)")
    print("4. Verify your account has proper permissions")
