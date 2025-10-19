#!/usr/bin/env python3
"""
Test Original APEX Agents
Verify that asha.py, athena.py, and scribe.py work properly
"""

import sys
import os

def test_asha():
    """Test original ASHA agent"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'asha'))
        from asha import AshaAgent
        
        agent = AshaAgent()
        response = agent.get_response("I'm feeling stressed about work")
        print("✅ ASHA Agent (Original) - Working!")
        print(f"Response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ ASHA Agent Failed: {e}")
        return False

def test_athena():
    """Test original Athena agent"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'athena'))
        from athena import AthenaAgent
        
        agent = AthenaAgent()
        response = agent.get_response("What are my maternity leave rights?")
        print("✅ Athena Agent (Original) - Working!")
        print(f"Response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Athena Agent Failed: {e}")
        return False

def test_scribe():
    """Test original Scribe agent"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scribe'))
        from scribe import ScribeAgent
        
        agent = ScribeAgent()
        response = agent.process_user_input("Generate a maternity leave application")
        print("✅ Scribe Agent (Original) - Working!")
        print(f"Response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Scribe Agent Failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Original APEX Agents...")
    print("=" * 50)
    
    asha_works = test_asha()
    print()
    
    athena_works = test_athena()
    print()
    
    scribe_works = test_scribe()
    print()
    
    print("=" * 50)
    if asha_works and athena_works and scribe_works:
        print("🎉 ALL ORIGINAL AGENTS WORKING!")
        print("✅ Ready for FastAPI Integration")
    else:
        print("⚠️  Some agents need attention")
        print("FastAPI will handle failures gracefully")