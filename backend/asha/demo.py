#!/usr/bin/env python3
"""
Quick Demo Script for ASHA Agent
"""

from asha import AshaAgent

def demo_asha():
    """Demonstrate ASHA's capabilities"""
    print("🎬 ASHA Agent Demo")
    print("=" * 30)
    
    # Initialize ASHA
    asha = AshaAgent()
    print("✅ ASHA initialized successfully!")
    
    # Test scenarios
    test_messages = [
        "Hello! I'm new here. Can you tell me about yourself?",
        "I've been feeling really anxious about an upcoming presentation at work.",
        "Thank you for the advice. Can you give me some quick breathing exercises?",
        "What resources would you recommend for ongoing stress management?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}:")
        print(f"User: {message}")
        print(f"ASHA: ", end="")
        
        response = asha.get_response(message)
        # Truncate long responses for demo
        if len(response) > 200:
            response = response[:200] + "... [truncated]"
        
        print(response)
        print("-" * 50)
    
    # Show conversation summary
    print(f"\n📊 {asha.get_conversation_summary()}")
    
    print("\n✅ Demo completed successfully!")
    print("💡 To run ASHA interactively, use: python asha.py")

if __name__ == "__main__":
    try:
        demo_asha()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Please check your API key and internet connection.")
