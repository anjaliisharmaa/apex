#!/usr/bin/env python3
"""
Test script for ASHA Agent
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from asha import AshaAgent

def test_asha():
    """Test the ASHA agent with a simple interaction"""
    print("🧪 Testing ASHA Agent...")
    print("=" * 40)
    
    try:
        # Initialize ASHA
        asha = AshaAgent()
        print("✅ ASHA initialized successfully!")
        
        # Test message
        test_message = "Hello, I'm feeling a bit stressed about work lately. Can you help?"
        print(f"\nTest Input: {test_message}")
        print("\nASHA Response:")
        print("-" * 30)
        
        response = asha.get_response(test_message)
        print(response)
        
        print("\n" + "=" * 40)
        print("✅ Test completed successfully!")
        
        # Show conversation summary
        summary = asha.get_conversation_summary()
        print(f"\nConversation Summary:\n{summary}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_asha()
