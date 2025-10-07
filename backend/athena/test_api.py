#!/usr/bin/env python3
"""
Quick API Test for Athena
"""

import os
import json
import urllib.request

def load_api_key():
    """Load API key from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('GOOGLE_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"\'')
    return None

def test_gemini_api():
    """Test the Gemini 2.5 Flash API"""
    api_key = load_api_key()
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"✅ API key loaded: {api_key[:12]}...")
    
    # Test the new model
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello! Please respond with 'Gemini 2.5 Flash is working correctly' to confirm the API is functional."
            }]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 50
        }
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print("🔄 Testing Gemini 2.5 Flash API...")
        
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                result = json.loads(response.read().decode())
                
                if 'candidates' in result and result['candidates']:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    print(f"✅ API Response: {content}")
                    print("🎉 Gemini 2.5 Flash API is working perfectly!")
                    return True
                else:
                    print("❌ Unexpected response format")
                    print(json.dumps(result, indent=2))
            else:
                print(f"❌ HTTP Status: {response.status}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Gemini 2.5 Flash API")
    print("=" * 35)
    test_gemini_api()