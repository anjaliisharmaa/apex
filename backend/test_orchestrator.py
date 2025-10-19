#!/usr/bin/env python3
"""
Test the APEX Orchestrator Agent
"""

import sys
import os

def test_orchestrator():
    """Test the orchestrator agent functionality"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
        from orchestrator import OrchestratorAgent
        
        print("🎯 Testing APEX Orchestrator Agent...")
        print("=" * 50)
        
        # Create orchestrator
        orchestrator = OrchestratorAgent()
        
        # Create session
        session_id = orchestrator.create_session("test_user")
        print(f"✅ Created session: {session_id}")
        
        # Test different types of messages
        test_messages = [
            {
                "message": "I'm being sexually harassed at work and don't know what to do",
                "expected_workflow": "multi_agent",
                "description": "Should trigger harassment support workflow (Legal + Emotional)"
            },
            {
                "message": "What are my maternity leave rights in India?", 
                "expected_workflow": "single_agent",
                "description": "Should route to Athena for legal guidance"
            },
            {
                "message": "I need help writing a maternity leave application",
                "expected_workflow": "multi_agent", 
                "description": "Should trigger legal documentation workflow (Legal + Scribe)"
            },
            {
                "message": "I'm feeling very stressed about my workplace situation",
                "expected_workflow": "single_agent",
                "description": "Should route to ASHA for emotional support"
            }
        ]
        
        for i, test in enumerate(test_messages, 1):
            print(f"\n🧪 Test {i}: {test['description']}")
            print(f"👤 User: {test['message']}")
            
            # Process message
            result = orchestrator.process_message(test['message'], session_id)
            
            print(f"🤖 Agent: {result['agent_used']}")
            print(f"📊 Workflow: {result['workflow_type']}")
            print(f"🎯 Intent: {result['intent_analysis']['primary_intent']}")
            print(f"📝 Response: {result['response'][:100]}...")
            
            # Check if workflow matches expectation
            if result['workflow_type'] == test['expected_workflow']:
                print("✅ Workflow routing correct")
            else:
                print(f"⚠️  Expected {test['expected_workflow']}, got {result['workflow_type']}")
        
        # Test session summary
        print(f"\n📊 Session Summary:")
        summary = orchestrator.get_session_summary(session_id)
        print(f"   Total turns: {summary['total_turns']}")
        print(f"   Agents used: {summary['agents_used']}")
        print(f"   Conversation state: {summary['conversation_state']}")
        
        print("\n🎉 Orchestrator Agent test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_orchestrator()