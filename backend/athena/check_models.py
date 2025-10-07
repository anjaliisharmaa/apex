#!/usr/bin/env python3
"""
Check Available Google Gemini Models
"""

import os
import json
import urllib.request
import urllib.error

def load_api_key():
    """Load API key from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('GOOGLE_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"\'')
    return None

def check_available_models():
    """Check what models are available"""
    api_key = load_api_key()
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"✅ API key loaded: {api_key[:12]}...")
    
    # Try different API versions and endpoints
    endpoints_to_try = [
        f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
    ]
    
    for endpoint in endpoints_to_try:
        print(f"\n🔍 Checking endpoint: {endpoint.split('?')[0]}")
        
        try:
            req = urllib.request.Request(endpoint)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    
                    if 'models' in data:
                        print(f"✅ Found {len(data['models'])} models:")
                        for model in data['models']:
                            name = model.get('name', 'Unknown')
                            display_name = model.get('displayName', 'Unknown')
                            supported_methods = model.get('supportedGenerationMethods', [])
                            
                            print(f"  📋 {name}")
                            print(f"     Display Name: {display_name}")
                            print(f"     Supported Methods: {', '.join(supported_methods)}")
                            print()
                    else:
                        print(f"⚠️ No models found in response")
                else:
                    print(f"❌ Status: {response.status}")
                    
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if hasattr(e, 'read') else str(e)
            print(f"❌ HTTP Error {e.code}: {error_body}")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_specific_models():
    """Test specific model endpoints"""
    api_key = load_api_key()
    
    models_to_test = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-1.5-pro-latest", 
        "gemini-1.5-pro",
        "gemini-pro",
        "gemini-pro-latest"
    ]
    
    print(f"\n🧪 Testing specific model endpoints:")
    print("=" * 50)
    
    for model in models_to_test:
        # Test both v1 and v1beta
        for version in ['v1beta', 'v1']:
            url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={api_key}"
            
            test_payload = {
                "contents": [{
                    "parts": [{"text": "Hello"}]
                }],
                "generationConfig": {
                    "maxOutputTokens": 5
                }
            }
            
            try:
                data = json.dumps(test_payload).encode('utf-8')
                req = urllib.request.Request(
                    url,
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        print(f"✅ {version}/models/{model} - WORKING")
                    else:
                        print(f"❌ {version}/models/{model} - Status {response.status}")
                        
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print(f"❌ {version}/models/{model} - NOT FOUND")
                else:
                    print(f"❌ {version}/models/{model} - HTTP {e.code}")
            except Exception as e:
                print(f"❌ {version}/models/{model} - Error: {e}")

if __name__ == "__main__":
    print("🔍 Google Gemini API Model Checker")
    print("=" * 40)
    
    check_available_models()
    test_specific_models()