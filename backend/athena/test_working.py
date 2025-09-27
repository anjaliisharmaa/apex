#!/usr/bin/env python3
"""
Quick test for the working Athena agent
"""

from athena_working import AthenaAgentWorking

def test_athena():
    """Test Athena functionality"""
    print("🧪 Testing Athena Working Version")
    print("=" * 40)
    
    try:
        # Initialize Athena
        athena = AthenaAgentWorking()
        print("✅ Athena initialized successfully!")
        
        # Test questions
        test_queries = [
            "What is the minimum wage law in India?",
            "What constitutes sexual harassment in the workplace?",
            "What are employee rights under Indian labor law?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: {query}")
            print("🤖 Athena's Response:")
            print("-" * 40)
            
            response = athena.get_response(query)
            
            # Show first 300 characters for testing
            if len(response) > 300:
                print(response[:300] + "... [Response continues]")
            else:
                print(response)
            
            print("-" * 40)
        
        print(f"\n✅ All tests completed successfully!")
        print(f"📊 {athena.get_conversation_summary()}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_athena()