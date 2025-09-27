#!/usr/bin/env python3
"""
Test script for Athena Agent (RAG-enabled Legal AI)
"""

import sys
import os

# Add the athena directory to path
sys.path.append(os.path.dirname(__file__))

def test_athena_simple():
    """Simple test without full RAG to check basic functionality"""
    print("🧪 Testing Athena Agent (Basic Mode)...")
    print("=" * 40)
    
    try:
        from athena import AthenaAgent
        
        # Test initialization
        print("🔄 Initializing Athena...")
        athena = AthenaAgent()
        print("✅ Athena initialized successfully!")
        
        # Test basic functionality
        test_query = "What are the basic rights of employees under Indian labor law?"
        print(f"\nTest Query: {test_query}")
        print("\nAthena Response:")
        print("-" * 30)
        
        response = athena.get_response(test_query)
        # Truncate long responses for testing
        if len(response) > 300:
            response = response[:300] + "... [truncated for test]"
        
        print(response)
        
        print("\n" + "=" * 40)
        print("✅ Basic test completed successfully!")
        
        # Show conversation summary
        summary = athena.get_conversation_summary()
        print(f"\nConversation Summary:\n{summary}")
        
        # Show available documents
        docs = athena.get_available_documents()
        print(f"\n{docs}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please install required packages: pip install sentence-transformers faiss-cpu pypdf2")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def test_simple_without_rag():
    """Test basic functionality without RAG dependencies"""
    print("🧪 Testing Basic Athena Functionality...")
    print("=" * 40)
    
    # Test API key loading
    import os
    
    # Load API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        # Try .env file
        env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file_path):
            with open(env_file_path, 'r') as f:
                for line in f:
                    if line.startswith('GOOGLE_API_KEY='):
                        api_key = line.split('=', 1)[1].strip().strip('"\'')
                        break
    
    if api_key:
        print(f"✅ API key loaded: {api_key[:10]}...")
    else:
        print("❌ No API key found!")
        return False
    
    # Check data directory
    data_dir = os.path.join(os.path.dirname(__file__), 'athena_data')
    if os.path.exists(data_dir):
        docs = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
        print(f"✅ Data directory found with {len(docs)} PDF files:")
        for doc in docs:
            print(f"  📄 {doc}")
    else:
        print("❌ Data directory not found!")
        return False
    
    print("\n✅ Basic setup test completed successfully!")
    print("💡 Ready to test full Athena agent with RAG capabilities!")
    return True

if __name__ == "__main__":
    print("🎯 Athena Agent Testing")
    print("=" * 50)
    
    # First test basic setup
    if test_simple_without_rag():
        print("\n" + "=" * 50)
        # Then test full functionality
        test_athena_simple()
    else:
        print("❌ Basic setup failed. Please check your configuration.")