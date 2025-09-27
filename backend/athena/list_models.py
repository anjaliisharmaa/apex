#!/usr/bin/env python3
"""
List available models from Google Gemini API
"""

import os
import json
import urllib.request

def list_available_models():
    """List available models from Google API"""
    
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
    
    # Try both API versions
    for version in ['v1', 'v1beta']:
        print(f"\n🔍 Checking {version} API...")
        
        try:
            # List models endpoint
            list_url = f"https://generativelanguage.googleapis.com/{version}/models?key={api_key}"
            
            req = urllib.request.Request(list_url)
            
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode())
            
            if 'models' in response_data:
                print(f"✅ Available models in {version}:")
                for model in response_data['models']:
                    model_name = model.get('name', 'Unknown')
                    # Extract just the model name part
                    if '/' in model_name:
                        short_name = model_name.split('/')[-1]
                    else:
                        short_name = model_name
                    
                    # Check if it supports generateContent
                    methods = model.get('supportedGenerationMethods', [])
                    if 'generateContent' in methods:
                        print(f"  ✅ {short_name} - supports generateContent")
                        
                        # Test this model
                        test_url = f"https://generativelanguage.googleapis.com/{version}/models/{short_name}:generateContent?key={api_key}"
                        
                        payload = {
                            "contents": [{
                                "parts": [{
                                    "text": "Test"
                                }]
                            }]
                        }
                        
                        try:
                            data = json.dumps(payload).encode('utf-8')
                            test_req = urllib.request.Request(
                                test_url,
                                data=data,
                                headers={'Content-Type': 'application/json'}
                            )
                            
                            with urllib.request.urlopen(test_req) as test_response:
                                test_data = json.loads(test_response.read().decode())
                            
                            if 'candidates' in test_data:
                                print(f"    🎉 WORKING MODEL: {version}/models/{short_name}")
                                return f"{version}/models/{short_name}"
                                
                        except Exception as e:
                            print(f"    ❌ Test failed: {str(e)[:50]}...")
                    else:
                        print(f"  ⚠️ {short_name} - no generateContent support")
            
        except Exception as e:
            print(f"❌ Failed to list {version} models: {e}")
    
    print("\n❌ No working models found!")
    return None

if __name__ == "__main__":
    working_model = list_available_models()
    if working_model:
        print(f"\n🎉 Use this model path: {working_model}")
        print(f"Full endpoint: https://generativelanguage.googleapis.com/{working_model}:generateContent?key=YOUR_API_KEY")
    else:
        print("\n💡 API may be temporarily unavailable. Use offline version: python athena_working.py")