#!/usr/bin/env python3
"""
Test the Updated FastAPI Server with Orchestrator Agent
"""

import requests
import json

def test_orchestrator_api():
    """Test the FastAPI server with orchestrator integration"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing APEX FastAPI Server with Orchestrator Agent...")
    print("=" * 60)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/")
        print("✅ Health check:", response.json()["message"])
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test agent status
    try:
        response = requests.get(f"{base_url}/api/agents/status")
        status_data = response.json()
        print("✅ Agent status:")
        for agent, info in status_data.items():
            print(f"   {agent}: {info['status']}")
    except Exception as e:
        print(f"❌ Agent status failed: {e}")
    
    # Test different types of chat messages
    test_messages = [
        {
            "message": "I'm being harassed at work and need help",
            "expected": "Multi-agent workflow (Legal + Emotional)",
            "description": "Harassment support"
        },
        {
            "message": "What are my maternity leave rights?",
            "expected": "Single agent (Legal)",
            "description": "Legal query"
        },
        {
            "message": "Generate a maternity leave application for me",
            "expected": "Multi-agent workflow (Legal + Documentation)",
            "description": "Document generation with legal context"
        },
        {
            "message": "I'm feeling very stressed about my job",
            "expected": "Single agent (Emotional)",
            "description": "Emotional support"
        }
    ]
    
    for i, test in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: {test['description']}")
        print(f"👤 User: {test['message']}")
        
        try:
            chat_data = {
                "message": test['message'],
                "anonymous": True
            }
            response = requests.post(f"{base_url}/api/chat", json=chat_data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"🤖 Agent: {result['agent_used']}")
                print(f"📝 Response: {result['response'][:100]}...")
                print(f"🆔 Session: {result['conversation_id'][:20]}...")
                print(f"✅ Expected: {test['expected']}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Chat test failed: {e}")
    
    # Test document generation
    print(f"\n📝 Testing Document Generation...")
    try:
        doc_data = {
            "document_type": "maternity_leave_application",
            "user_data": {
                "employee_name": "Jane Doe",
                "employee_id": "EMP001",
                "expected_date": "2024-03-15"
            }
        }
        response = requests.post(f"{base_url}/api/forms/generate", json=doc_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Document generated: {result['document_type']}")
            print(f"📄 Content: {result['document_content'][:100]}...")
        else:
            print(f"❌ Document generation failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Document test failed: {e}")
    
    print("\n🎉 API Testing completed!")
    return True

if __name__ == "__main__":
    test_orchestrator_api()