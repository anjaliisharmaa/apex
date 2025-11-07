#!/usr/bin/env python3
"""
Test Cache Performance
=====================
Compare initialization times with and without cache
"""

import os
import sys
import time
import tempfile
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'athena'))

def test_cache_performance():
    """Test the performance difference with and without cache"""
    print("🧪 Testing Cache Performance")
    print("=" * 40)
    
    try:
        from athena.embeddings_cache import EmbeddingsCache
        
        data_dir = os.path.join(current_dir, 'athena', 'athena_data')
        
        if not os.path.exists(data_dir):
            print(f"❌ Data directory not found: {data_dir}")
            return
        
        # Test 1: With cache (if available)
        print("\n1️⃣ Testing WITH cache:")
        cache = EmbeddingsCache(data_dir)
        
        if cache.is_cache_valid():
            start_time = time.time()
            document_chunks, embeddings, faiss_index = cache.load_from_cache()
            cache_time = time.time() - start_time
            
            print(f"   ⚡ Cache load time: {cache_time:.2f} seconds")
            print(f"   📄 Loaded {len(document_chunks)} chunks")
            print(f"   🔢 Embedding dimension: {embeddings.shape[1]}")
        else:
            print("   ⚠️ No valid cache found")
            cache_time = None
        
        # Test 2: Without cache (simulate fresh generation)
        print("\n2️⃣ Testing WITHOUT cache (simulation):")
        
        # Temporarily move cache to simulate no cache
        cache_backup_dir = None
        if os.path.exists(cache.cache_dir):
            cache_backup_dir = tempfile.mkdtemp()
            for item in os.listdir(cache.cache_dir):
                shutil.move(
                    os.path.join(cache.cache_dir, item),
                    os.path.join(cache_backup_dir, item)
                )
        
        try:
            # Time fresh generation
            start_time = time.time()
            fresh_chunks, fresh_embeddings, fresh_index = cache.get_or_create_embeddings()
            fresh_time = time.time() - start_time
            
            print(f"   🔧 Fresh generation time: {fresh_time:.2f} seconds")
            print(f"   📄 Generated {len(fresh_chunks)} chunks")
            print(f"   🔢 Embedding dimension: {fresh_embeddings.shape[1]}")
            
        finally:
            # Restore cache backup
            if cache_backup_dir:
                for item in os.listdir(cache_backup_dir):
                    shutil.move(
                        os.path.join(cache_backup_dir, item),
                        os.path.join(cache.cache_dir, item)
                    )
                os.rmdir(cache_backup_dir)
        
        # Show comparison
        if cache_time and fresh_time:
            print(f"\n📊 Performance Comparison:")
            print(f"   ⚡ With cache: {cache_time:.2f} seconds")
            print(f"   🔧 Without cache: {fresh_time:.2f} seconds")
            print(f"   🚀 Speed improvement: {fresh_time/cache_time:.1f}x faster")
            
            if fresh_time > 60:
                print(f"   💡 Cache saves {fresh_time - cache_time:.1f} seconds per startup!")
        
        # Test Athena initialization
        print(f"\n3️⃣ Testing Athena Agent Initialization:")
        try:
            from athena.athena import AthenaAgent
            
            # Clear singleton to force re-initialization
            AthenaAgent._instance = None
            AthenaAgent._initialized = False
            
            start_time = time.time()
            athena = AthenaAgent()
            athena_time = time.time() - start_time
            
            print(f"   🤖 Athena initialization: {athena_time:.2f} seconds")
            
            # Test readiness
            if athena.is_ready():
                print(f"   ✅ Athena is ready with {len(athena.document_chunks)} chunks")
                
                # Get status
                status = athena.get_status()
                print(f"   📊 Status: {status['status']}")
                if 'cache' in status:
                    cache_status = status['cache']['status']
                    print(f"   💾 Cache: {cache_status}")
            else:
                print(f"   ❌ Athena not ready")
            
        except Exception as e:
            print(f"   ❌ Athena test failed: {e}")
        
        print(f"\n✅ Performance testing complete!")
        
    except Exception as e:
        print(f"❌ Error testing performance: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cache_performance()