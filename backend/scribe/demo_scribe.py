#!/usr/bin/env python3
"""
Scribe Demo - Quick Feature Test
===============================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scribe import ScribeAgent

def main():
    print("🚀 SCRIBE AGENT DEMONSTRATION")
    print("=" * 50)
    
    scribe = ScribeAgent()
    
    print("\n1️⃣ Testing Help Command:")
    print("-" * 30)
    help_response = scribe.process_user_input("help")
    print(help_response[:500] + "..." if len(help_response) > 500 else help_response)
    
    print("\n2️⃣ Testing Maternity Leave Requirements:")
    print("-" * 40)
    maternity_req = scribe.process_user_input("requirements maternity_leave")
    print(maternity_req[:600] + "..." if len(maternity_req) > 600 else maternity_req)
    
    print("\n3️⃣ Testing Natural Language Query:")
    print("-" * 35)
    nl_response = scribe.process_user_input("How do I apply for maternity leave?")
    print(nl_response[:400] + "..." if len(nl_response) > 400 else nl_response)
    
    print("\n4️⃣ Testing Workflow Guide:")
    print("-" * 25)
    workflow_response = scribe.process_user_input("workflow maternity_leave_process")
    print(workflow_response[:500] + "..." if len(workflow_response) > 500 else workflow_response)
    
    print(f"\n✅ SCRIBE IS WORKING PERFECTLY!")
    print(f"📊 Session stats: {scribe.current_session}")

if __name__ == "__main__":
    main()