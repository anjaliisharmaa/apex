#!/usr/bin/env python3
"""
Scribe Agent Test Suite
======================
Demonstrates the capabilities of the Scribe Documentation Assistant
"""

import sys
import os

# Add the scribe module to path
sys.path.insert(0, os.path.dirname(__file__))

from scribe import ScribeAgent

def test_scribe_responses():
    """Test various Scribe agent responses."""
    print("🧪 Testing Scribe Agent Capabilities")
    print("=" * 50)
    
    # Initialize agent
    scribe = ScribeAgent()
    print("\n" + "=" * 50)
    
    # Test queries
    test_queries = [
        "help",
        "How do I apply for maternity leave?",
        "requirements maternity_leave", 
        "workflow transfer_process",
        "documents",
        "What documents do I need for a grievance?",
        "Can you guide me through the transfer process?",
        "requirements grievance_form"
    ]
    
    print("\n🔍 Testing Different Types of Queries:")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 40)
        
        response = scribe.process_user_input(query)
        
        # Show first 300 characters of response
        if len(response) > 300:
            print(f"🤖 Scribe: {response[:300]}...")
            print(f"   [Response continues for {len(response)} total characters]")
        else:
            print(f"🤖 Scribe: {response}")
        
        print("\n" + "=" * 50)
    
    # Test session summary
    print("\n📊 Final Session Summary:")
    print("-" * 30)
    summary = scribe.get_session_summary()
    print(summary)

if __name__ == "__main__":
    test_scribe_responses()