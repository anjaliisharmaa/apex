#!/usr/bin/env python3
"""
Quick test for Athena functionality
"""

import os
import json
import urllib.request

def quick_test():
    """Quick test to verify API and basic setup"""
    print("🧪 Quick Athena Test")
    print("=" * 30)
    
    # Test API key
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
    
    # Test documents directory
    data_dir = os.path.join(os.path.dirname(__file__), 'athena_data')
    if os.path.exists(data_dir):
        docs = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
        print(f"✅ Found {len(docs)} legal documents:")
        for doc in docs:
            print(f"  📄 {doc}")
    else:
        print("❌ No athena_data directory found!")
        return
    
    # Test API call (using v1 API)
    api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello! I am Athena, an AI legal assistant. Please respond with a brief legal disclaimer about AI legal advice."
            }]
        }]
    }
    
    try:
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
            print(f"\n🤖 API Test Response:\n{text[:200]}...")
        
        print("\n✅ All tests passed! Athena is ready to use.")
        
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    quick_test()