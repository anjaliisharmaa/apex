#!/usr/bin/env python3
"""
Minimal ASHA Agent Test
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_minimal_asha():
    print("🧪 Testing Minimal ASHA Agent...")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv("../.env")
    
    # Get API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ No API key found!")
        return False
    
    print("✅ API key loaded successfully!")
    
    # Configure Google AI
    genai.configure(api_key=api_key)
    print("✅ Google AI configured!")
    
    # Initialize model
    model = genai.GenerativeModel('gemini-pro')
    print("✅ Model initialized!")
    
    # Test a simple prompt
    test_prompt = "Hello! I'm ASHA, an AI assistant. Please respond with a brief, friendly greeting that shows empathy and willingness to help."
    
    print(f"\nSending test prompt...")
    response = model.generate_content(test_prompt)
    
    print(f"\n🤖 ASHA Response:")
    print("-" * 30)
    print(response.text)
    print("-" * 30)
    
    print("\n✅ Minimal test completed successfully!")
    return True

if __name__ == "__main__":
    try:
        test_minimal_asha()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
