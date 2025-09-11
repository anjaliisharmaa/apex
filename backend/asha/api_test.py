#!/usr/bin/env python3
"""
API Test for ASHA Agent
"""

import os
import json
import urllib.request
import urllib.parse

def test_api():
    """Test the Google Gemini API"""
    print("🧪 Testing Google Gemini API...")
    print("=" * 40)
    
    # Load API key
    api_key = None
    
    # Try environment variable first
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        # Try .env file
        env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file_path):
            with open(env_file_path, 'r') as f:
                for line in f:
                    if line.startswith('GOOGLE_API_KEY='):
                        api_key = line.split('=', 1)[1].strip().strip('"\'')
                        break
    
    if not api_key:
        print("❌ No API key found!")
        return False
    
    print(f"✅ API key loaded: {api_key[:10]}...")
    
    # Test API endpoint (updated)
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    
    print(f"🔗 API URL: {api_url[:80]}...")
    
    # Simple test payload
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello! Please respond with a simple greeting."
            }]
        }]
    }
    
    try:
        # Convert to JSON
        data = json.dumps(payload).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(
            api_url,
            data=data,
            headers={
                'Content-Type': 'application/json',
            }
        )
        
        print("📤 Sending test request...")
        
        # Make the request
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode())
            print("📥 Response received!")
            print(f"Response data keys: {list(response_data.keys())}")
            
            if 'candidates' in response_data:
                candidate = response_data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    text = candidate['content']['parts'][0]['text']
                    print(f"\n🤖 API Response: {text}")
                    print("\n✅ API test successful!")
                    return True
            
            print("⚠️ Unexpected response structure")
            print(f"Full response: {response_data}")
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        print(f"Response: {e.read().decode() if hasattr(e, 'read') else 'No response body'}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return False

if __name__ == "__main__":
    test_api()
