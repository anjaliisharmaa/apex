#!/usr/bin/env python3
"""
Performance Testing Script for APEX Orchestrator
================================================
Test response times and optimization improvements
"""

import os
import sys
import time
import json
import requests
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_api_performance():
    """Test API response times"""
    base_url = "http://localhost:8000/api"
    
    test_messages = [
        "I'm being harassed at work and need help",
        "What are my maternity leave rights?",
        "Can you help me draft a complaint letter?",
        "I'm feeling overwhelmed with my legal situation",
        "What documents do I need for transfer request?",
        "How do I apply for child care leave?"
    ]
    
    print("🧪 Testing API Performance...")
    print("=" * 50)
    
    total_times = []
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Testing: '{message[:50]}...'")
        
        start_time = time.time()
        
        try:
            response = requests.post(f"{base_url}/chat", json={
                "message": message,
                "anonymous": True
            })
            
            end_time = time.time()
            response_time = end_time - start_time
            total_times.append(response_time)
            
            if response.status_code == 200:
                data = response.json()
                agent_used = data.get("agent_used", "unknown")
                workflow_type = data.get("workflow_type", "unknown")
                cached = data.get("cached", False)
                fast_mode = data.get("fast_mode", False)
                
                cache_indicator = " [CACHED]" if cached else ""
                fast_indicator = " [FAST]" if fast_mode else ""
                
                print(f"   ✅ Response time: {response_time:.2f}s{cache_indicator}{fast_indicator}")
                print(f"   🤖 Agent: {agent_used} | Workflow: {workflow_type}")
                print(f"   📝 Response length: {len(data.get('response', ''))}")
                
                # Color code based on performance
                if response_time < 5:
                    print(f"   🟢 EXCELLENT performance")
                elif response_time < 15:
                    print(f"   🟡 GOOD performance")
                else:
                    print(f"   🔴 SLOW performance - needs optimization")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
            
        # Small delay between requests
        time.sleep(1)
    
    print(f"\n{'='*50}")
    print(f"📊 Performance Summary:")
    print(f"   Total requests: {len(total_times)}")
    print(f"   Average response time: {sum(total_times)/len(total_times):.2f}s")
    print(f"   Fastest response: {min(total_times):.2f}s")
    print(f"   Slowest response: {max(total_times):.2f}s")
    
    # Performance targets
    fast_responses = sum(1 for t in total_times if t < 10)
    print(f"   Responses under 10s: {fast_responses}/{len(total_times)} ({fast_responses/len(total_times)*100:.1f}%)")
    
    excellent_responses = sum(1 for t in total_times if t < 5)
    print(f"   Excellent responses (<5s): {excellent_responses}/{len(total_times)} ({excellent_responses/len(total_times)*100:.1f}%)")

def test_orchestrator_direct():
    """Test orchestrator agent directly (bypass API)"""
    try:
        from core.orchestrator import OrchestratorAgent
        
        print("\n🎯 Testing Orchestrator Direct Access...")
        print("=" * 50)
        
        orchestrator = OrchestratorAgent()
        
        # Enable fast mode
        orchestrator.set_performance_mode(fast_mode=True, single_agent_preference=True)
        
        test_messages = [
            "What are my rights regarding workplace harassment?",
            "I need emotional support dealing with workplace stress",
            "Can you generate a leave application for me?"
        ]
        
        session_id = orchestrator.create_session("test_user")
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n{i}. Testing: '{message}'")
            
            start_time = time.time()
            result = orchestrator.process_message(message, session_id)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            print(f"   ⚡ Direct response time: {response_time:.2f}s")
            print(f"   🤖 Agent: {result['agent_used']}")
            print(f"   🔄 Workflow: {result['workflow_type']}")
            print(f"   💾 Cached: {result.get('cached', False)}")
            print(f"   📝 Response length: {len(result['response'])}")
            
            if response_time < 3:
                print(f"   🟢 EXCELLENT direct performance")
            elif response_time < 10:
                print(f"   🟡 GOOD direct performance")
            else:
                print(f"   🔴 SLOW direct performance")
        
        # Get performance stats
        stats = orchestrator.get_performance_stats()
        print(f"\n📊 Orchestrator Stats:")
        print(f"   Cache size: {stats['cache_size']}")
        print(f"   Cache hits: {stats['cache_hits']}")
        print(f"   Fast mode: {stats['fast_mode']}")
        print(f"   Single agent preference: {stats['single_agent_preference']}")
        
    except Exception as e:
        print(f"❌ Direct orchestrator test failed: {e}")

def test_performance_endpoints():
    """Test performance control endpoints"""
    base_url = "http://localhost:8000/api"
    
    print("\n⚙️ Testing Performance Control Endpoints...")
    print("=" * 50)
    
    try:
        # Get current performance stats
        response = requests.get(f"{base_url}/agents/performance")
        if response.status_code == 200:
            stats = response.json()
            print("📊 Current Performance Stats:")
            print(json.dumps(stats, indent=2))
        
        # Enable fast mode
        print("\n⚡ Enabling Fast Mode...")
        response = requests.post(f"{base_url}/agents/performance", json={
            "fast_mode": True,
            "single_agent_preference": True
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Fast mode enabled successfully")
            print(f"   Settings: {result['settings']}")
        
        # Get agent status
        response = requests.get(f"{base_url}/agents/status")
        if response.status_code == 200:
            status = response.json()
            print("\n🤖 Agent Status:")
            for agent, info in status.items():
                print(f"   {agent}: {info.get('status', 'unknown')}")
                
    except Exception as e:
        print(f"❌ Performance endpoint test failed: {e}")

if __name__ == "__main__":
    print("🚀 APEX Performance Testing Suite")
    print("=" * 50)
    
    try:
        # Test 1: API Performance
        test_api_performance()
        
        # Test 2: Direct Orchestrator Access
        test_orchestrator_direct()
        
        # Test 3: Performance Control Endpoints
        test_performance_endpoints()
        
        print(f"\n🎉 Performance testing completed!")
        print(f"💡 Tips for faster responses:")
        print(f"   • Enable fast mode via API: POST /api/agents/performance")
        print(f"   • Clear cache periodically: POST /api/agents/cache/clear")
        print(f"   • Use single agent preference for simple queries")
        print(f"   • Monitor cache hit rates for optimization")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")