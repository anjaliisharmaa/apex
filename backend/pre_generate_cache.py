#!/usr/bin/env python3
"""
Pre-generate Embeddings Cache
=============================
Run this script to pre-generate embeddings cache for instant Athena initialization
"""

import os
import sys
import time

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'athena'))

def pre_generate_cache():
    """Pre-generate embeddings cache for fast startup"""
    print("🚀 Pre-generating Embeddings Cache for APEX")
    print("=" * 50)
    
    try:
        # Fix import path
        sys.path.append('athena')
        from embeddings_cache import EmbeddingsCache
        
        # Initialize cache system
        data_dir = os.path.join(current_dir, 'athena', 'athena_data')
        cache = EmbeddingsCache(data_dir)
        
        print(f"📁 Data directory: {data_dir}")
        print(f"💾 Cache directory: {cache.cache_dir}")
        
        # Check if documents exist
        if not os.path.exists(data_dir):
            print(f"❌ Data directory not found: {data_dir}")
            return False
        
        pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
        if not pdf_files:
            print(f"❌ No PDF files found in {data_dir}")
            return False
        
        print(f"📚 Found {len(pdf_files)} PDF documents:")
        for pdf in pdf_files:
            print(f"  • {pdf}")
        
        # Generate cache
        print("\n🔧 Generating embeddings cache...")
        start_time = time.time()
        
        # This will either load from cache or generate new cache
        document_chunks, embeddings, faiss_index = cache.get_or_create_embeddings()
        
        generation_time = time.time() - start_time
        
        # Get cache info
        cache_info = cache.get_cache_info()
        
        print(f"\n✅ Cache Generation Complete!")
        print(f"⏱️ Time taken: {generation_time:.2f} seconds")
        print(f"📄 Document chunks: {len(document_chunks)}")
        print(f"🔢 Embedding dimension: {embeddings.shape[1]}")
        print(f"💾 Cache size: {cache_info.get('cache_size_mb', 0):.2f} MB")
        
        # Test loading speed
        print(f"\n🧪 Testing cache loading speed...")
        
        # Clear cache and reload to test speed
        cache_test = EmbeddingsCache(data_dir)
        if cache_test.is_cache_valid():
            load_start = time.time()
            test_chunks, test_embeddings, test_index = cache_test.load_from_cache()
            load_time = time.time() - load_start
            
            print(f"⚡ Cache loading time: {load_time:.2f} seconds")
            print(f"📊 Speed improvement: {generation_time/load_time:.1f}x faster")
        
        print(f"\n🎉 Cache pre-generation successful!")
        print(f"💡 Next startup of Athena will be instant!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required packages are installed:")
        print("   pip install sentence-transformers faiss-cpu PyPDF2 numpy")
        return False
        
    except Exception as e:
        print(f"❌ Error generating cache: {e}")
        return False

def clean_cache():
    """Clean existing cache"""
    print("🧹 Cleaning Embeddings Cache")
    print("=" * 30)
    
    try:
        sys.path.append('athena')
        from embeddings_cache import EmbeddingsCache
        
        data_dir = os.path.join(current_dir, 'athena', 'athena_data')
        cache = EmbeddingsCache(data_dir)
        
        cache.clear_cache()
        print("✅ Cache cleaned successfully")
        
    except Exception as e:
        print(f"❌ Error cleaning cache: {e}")

def show_cache_info():
    """Show current cache information"""
    print("📊 Cache Information")
    print("=" * 20)
    
    try:
        sys.path.append('athena')
        from embeddings_cache import EmbeddingsCache
        
        data_dir = os.path.join(current_dir, 'athena', 'athena_data')
        cache = EmbeddingsCache(data_dir)
        
        info = cache.get_cache_info()
        
        if info['status'] == 'valid':
            print(f"✅ Cache Status: Valid")
            print(f"📄 Document chunks: {info['num_chunks']}")
            print(f"🔢 Embedding dimension: {info['embedding_dim']}")
            print(f"💾 Cache size: {info['cache_size_mb']} MB")
            print(f"📅 Created: {info['created_at']}")
            print(f"🧠 Model: {info['model_name']}")
        else:
            print(f"❌ Cache Status: {info['status']}")
            if 'message' in info:
                print(f"📝 Message: {info['message']}")
        
    except Exception as e:
        print(f"❌ Error getting cache info: {e}")

def main():
    """Main function"""
    print("🎯 APEX Embeddings Cache Manager")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pre_generate_cache.py generate   # Generate cache")
        print("  python pre_generate_cache.py clean      # Clean cache")
        print("  python pre_generate_cache.py info       # Show cache info")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'generate':
        success = pre_generate_cache()
        if success:
            print("\n🎉 Ready! Next Athena startup will be much faster!")
        else:
            print("\n❌ Cache generation failed")
            
    elif command == 'clean':
        clean_cache()
        
    elif command == 'info':
        show_cache_info()
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: generate, clean, info")

if __name__ == "__main__":
    main()