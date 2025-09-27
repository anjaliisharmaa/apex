#!/usr/bin/env python3
"""
Test the corrected API endpoint
"""

import os
import json
import urllib.request

def test_corrected_api():
    """Test the corrected API endpoint"""
    
    # Load API key
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
    
    # Test the corrected endpoint
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello! I am Athena, an AI legal assistant. Please respond with 'API connection successful' to confirm the connection is working."
            }]
        }]
    }
    
    try:
        print("🔄 Testing corrected API endpoint...")
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            api_url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode())
        
        if 'candidates' in response_data:
            text = response_data['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ SUCCESS! API Response: {text}")
            return True
        else:
            print(f"⚠️ Unexpected response: {response_data}")
            return False
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        if hasattr(e, 'read'):
            error_body = e.read().decode()
            print(f"Error details: {error_body}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_corrected_api()
    if success:
        print("\n🎉 API is working! You can now use:")
        print("   python athena_simple.py")
    else:
        print("\n💡 API still not working. Use offline version:")
        print("   python athena_working.py")