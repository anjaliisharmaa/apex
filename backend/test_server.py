"""
Test script for APEX Backend API
"""
import requests
import json

def test_server():
    base_url = "http://127.0.0.1:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/")
        print("✅ Health check:", response.json())
    except Exception as e:
        print("❌ Health check failed:", e)
        return False
    
    # Test agent status
    try:
        response = requests.get(f"{base_url}/api/agents/status")
        print("✅ Agent status:", response.json())
    except Exception as e:
        print("❌ Agent status failed:", e)
    
    # Test chat endpoint
    try:
        chat_data = {
            "message": "What are my maternity leave rights?",
            "anonymous": True
        }
        response = requests.post(f"{base_url}/api/chat", json=chat_data)
        print("✅ Chat test:", response.json())
    except Exception as e:
        print("❌ Chat test failed:", e)
    
    return True

if __name__ == "__main__":
    print("🧪 Testing APEX Backend API...")
    test_server()