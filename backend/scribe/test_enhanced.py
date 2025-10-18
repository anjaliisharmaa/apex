#!/usr/bin/env python3
"""
Test Scribe Enhanced Content Generation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scribe import ScribeAgent

def test_content_generation():
    """Test various content generation capabilities"""
    print("🧪 Testing Scribe Enhanced Content Generation")
    print("=" * 50)
    
    # Initialize Scribe
    scribe = ScribeAgent()
    
    test_requests = [
        "Generate professional email to boss about sick leave for 3 days",
        "Create WhatsApp message for team meeting reminder tomorrow at 2 PM", 
        "Write formal apology letter to client for project delay",
        "Generate SMS for appointment confirmation with doctor",
        "Create maternity leave application for employee at SSPL company",
        "Write professional email for transfer request to Mumbai office"
    ]
    
    print("\n🔍 Testing Different Content Types:")
    print("=" * 50)
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n📝 Test {i}: {request}")
        print("-" * 60)
        
        response = scribe.process_user_input(request)
        
        # Show first 200 characters of response
        if len(response) > 200:
            print(f"✅ Generated content (preview): {response[:200]}...")
            print(f"   [Full response: {len(response)} characters]")
        else:
            print(f"✅ Generated content: {response}")
        
        print()

if __name__ == "__main__":
    test_content_generation()