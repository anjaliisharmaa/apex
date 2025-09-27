#!/usr/bin/env python3
"""
Demo script for Athena Agent - Tests RAG functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from athena_simple import AthenaAgentSimple

def demo_athena():
    """Demonstrate Athena's RAG capabilities"""
    print("🎬 Athena Legal Assistant Demo")
    print("=" * 40)
    
    # Initialize Athena
    print("🔄 Initializing Athena...")
    athena = AthenaAgentSimple()
    print("✅ Athena initialized successfully!")
    
    # Show available documents
    print(f"\n📚 {athena.get_available_documents()}")
    
    # Test scenarios with legal questions
    test_queries = [
        "What are the basic rights of employees under Indian labor law?",
        "What is the minimum wage in India according to the Minimum Wages Act?",
        "What constitutes sexual harassment in the workplace?",
        "What are the procedures for filing a complaint about workplace harassment?",
        "What are the working hour limits under Indian labor law?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test Query {i}:")
        print(f"Question: {query}")
        print(f"\nAthena's Response:")
        print("-" * 50)
        
        response = athena.get_response(query)
        
        # Truncate long responses for demo readability
        if len(response) > 400:
            response = response[:400] + "\n... [Response truncated for demo - full response available in interactive mode]"
        
        print(response)
        print("-" * 50)
    
    # Show conversation summary
    print(f"\n📊 Conversation Summary:")
    print(athena.get_conversation_summary())
    
    print("\n✅ Demo completed successfully!")
    print("💡 To use Athena interactively, run: python athena_simple.py")

if __name__ == "__main__":
    try:
        demo_athena()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        print("Please check your API key and internet connection.")