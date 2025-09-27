#!/usr/bin/env python3
"""
Test different Gemini API endpoints to find working model
"""

import os
import json
import urllib.request

def test_models():
    """Test different model names to find working endpoint"""
    
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
        return
    
    print(f"✅ API key loaded: {api_key[:10]}...")
    
    # Test different model names
    models_to_test = [
        "gemini-pro",
        "gemini-1.5-pro", 
        "gemini-1.5-flash",
        "gemini-flash",
        "text-bison-001"
    ]
    
    api_versions = ["v1", "v1beta"]
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello! Please respond with just 'API working' to confirm connection."
            }]
        }]
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    for version in api_versions:
        print(f"\n🔍 Testing API version: {version}")
        for model in models_to_test:
            api_url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={api_key}"
            
            try:
                req = urllib.request.Request(
                    api_url,
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req) as response:
                    response_data = json.loads(response.read().decode())
                
                if 'candidates' in response_data:
                    text = response_data['candidates'][0]['content']['parts'][0]['text']
                    print(f"✅ SUCCESS: {version}/models/{model}")
                    print(f"   Response: {text.strip()}")
                    return f"{version}/models/{model}"
                    
            except urllib.error.HTTPError as e:
                print(f"❌ FAILED: {version}/models/{model} - {e.code} {e.reason}")
            except Exception as e:
                print(f"❌ ERROR: {version}/models/{model} - {str(e)}")
    
    print("\n❌ No working model found!")
    return None

if __name__ == "__main__":
    working_model = test_models()
    if working_model:
        print(f"\n🎉 Use this endpoint: https://generativelanguage.googleapis.com/{working_model}:generateContent?key=YOUR_API_KEY")
    else:
        print("\n💡 Try checking Google AI Studio for current model names: https://ai.google.dev/")