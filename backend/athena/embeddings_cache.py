#!/usr/bin/env python3
"""
Athena Embeddings Cache System
=============================
Pre-compute and cache document embeddings for instant loading
"""

import os
import pickle
import hashlib
import json
import numpy as np
import faiss
from typing import List, Dict, Tuple, Any
from sentence_transformers import SentenceTransformer
import PyPDF2


class EmbeddingsCache:
    """Manages pre-computed embeddings cache for fast initialization"""
    
    def __init__(self, data_dir: str, cache_dir: str = None):
        self.data_dir = data_dir
        self.cache_dir = cache_dir or os.path.join(data_dir, '.cache')
        self.embedding_model = None
        
        # Cache file paths
        self.chunks_cache_file = os.path.join(self.cache_dir, 'document_chunks.pkl')
        self.embeddings_cache_file = os.path.join(self.cache_dir, 'embeddings.npy')
        self.faiss_cache_file = os.path.join(self.cache_dir, 'faiss_index.idx')
        self.metadata_cache_file = os.path.join(self.cache_dir, 'metadata.json')
        
        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_documents_hash(self) -> str:
        """Generate hash of all PDF files to detect changes"""
        if not os.path.exists(self.data_dir):
            return ""
        
        hash_content = []
        
        for filename in sorted(os.listdir(self.data_dir)):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.data_dir, filename)
                # Get file modification time and size for quick hash
                stat = os.stat(file_path)
                hash_content.append(f"{filename}:{stat.st_mtime}:{stat.st_size}")
        
        # Create hash of all file information
        content_str = "|".join(hash_content)
        return hashlib.md5(content_str.encode()).hexdigest()
    
    def is_cache_valid(self) -> bool:
        """Check if cache is valid (exists and documents haven't changed)"""
        # Check if all cache files exist
        cache_files = [
            self.chunks_cache_file,
            self.embeddings_cache_file,
            self.faiss_cache_file,
            self.metadata_cache_file
        ]
        
        if not all(os.path.exists(f) for f in cache_files):
            print("📝 Cache files missing - will regenerate")
            return False
        
        # Check if documents have changed
        try:
            with open(self.metadata_cache_file, 'r') as f:
                metadata = json.load(f)
            
            current_hash = self.get_documents_hash()
            cached_hash = metadata.get('documents_hash', '')
            
            if current_hash != cached_hash:
                print("📝 Documents changed - will regenerate cache")
                return False
            
            print("✅ Cache is valid - loading pre-computed embeddings")
            return True
            
        except Exception as e:
            print(f"⚠️ Error checking cache validity: {e}")
            return False
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"❌ Error reading {pdf_path}: {e}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def load_embedding_model(self):
        """Load embedding model if not already loaded"""
        if self.embedding_model is None:
            print("📚 Loading sentence transformer model...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Embedding model loaded")
    
    def generate_and_cache_embeddings(self) -> Tuple[List[Tuple[str, Dict]], np.ndarray, faiss.Index]:
        """Generate embeddings and cache them"""
        print("🔧 Generating embeddings and building cache...")
        
        # Load embedding model
        self.load_embedding_model()
        
        # Process documents
        all_chunks = []
        chunk_metadata = []
        
        print("📄 Processing legal documents...")
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.pdf'):
                print(f"  📖 Processing {filename}...")
                pdf_path = os.path.join(self.data_dir, filename)
                
                # Extract text from PDF
                text = self.extract_text_from_pdf(pdf_path)
                if text:
                    # Split into chunks
                    chunks = self.chunk_text(text)
                    
                    for i, chunk in enumerate(chunks):
                        all_chunks.append(chunk)
                        chunk_metadata.append({
                            'filename': filename,
                            'chunk_id': i,
                            'source': filename.replace('.pdf', '')
                        })
        
        if not all_chunks:
            raise ValueError("No documents found or processed")
        
        print(f"✅ Processed {len(all_chunks)} text chunks from documents")
        
        # Generate embeddings
        print("🔄 Generating embeddings...")
        embeddings = self.embedding_model.encode(all_chunks, show_progress_bar=True)
        
        # Create FAISS index
        print("🗂️ Building FAISS index...")
        faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
        faiss_index.add(embeddings.astype('float32'))
        
        # Prepare document chunks with metadata
        document_chunks = list(zip(all_chunks, chunk_metadata))
        
        # Cache everything
        self.save_to_cache(document_chunks, embeddings, faiss_index)
        
        print("✅ Embeddings generated and cached successfully!")
        return document_chunks, embeddings, faiss_index
    
    def save_to_cache(self, document_chunks: List[Tuple[str, Dict]], embeddings: np.ndarray, faiss_index: faiss.Index):
        """Save all components to cache"""
        print("💾 Saving to cache...")
        
        # Save document chunks
        with open(self.chunks_cache_file, 'wb') as f:
            pickle.dump(document_chunks, f)
        
        # Save embeddings
        np.save(self.embeddings_cache_file, embeddings)
        
        # Save FAISS index
        faiss.write_index(faiss_index, self.faiss_cache_file)
        
        # Save metadata
        metadata = {
            'documents_hash': self.get_documents_hash(),
            'num_chunks': len(document_chunks),
            'embedding_dim': embeddings.shape[1],
            'created_at': str(np.datetime64('now')),
            'model_name': 'all-MiniLM-L6-v2'
        }
        
        with open(self.metadata_cache_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("✅ Cache saved successfully")
    
    def load_from_cache(self) -> Tuple[List[Tuple[str, Dict]], np.ndarray, faiss.Index]:
        """Load all components from cache"""
        print("⚡ Loading from cache...")
        
        # Load document chunks
        with open(self.chunks_cache_file, 'rb') as f:
            document_chunks = pickle.load(f)
        
        # Load embeddings
        embeddings = np.load(self.embeddings_cache_file)
        
        # Load FAISS index
        faiss_index = faiss.read_index(self.faiss_cache_file)
        
        # Load metadata for info
        with open(self.metadata_cache_file, 'r') as f:
            metadata = json.load(f)
        
        print(f"✅ Loaded {metadata['num_chunks']} cached chunks instantly!")
        return document_chunks, embeddings, faiss_index
    
    def get_or_create_embeddings(self) -> Tuple[List[Tuple[str, Dict]], np.ndarray, faiss.Index]:
        """Get embeddings from cache or create them if needed"""
        if self.is_cache_valid():
            return self.load_from_cache()
        else:
            return self.generate_and_cache_embeddings()
    
    def clear_cache(self):
        """Clear all cache files"""
        cache_files = [
            self.chunks_cache_file,
            self.embeddings_cache_file,
            self.faiss_cache_file,
            self.metadata_cache_file
        ]
        
        for cache_file in cache_files:
            if os.path.exists(cache_file):
                os.remove(cache_file)
        
        print("🧹 Cache cleared")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about current cache"""
        if not self.is_cache_valid():
            return {"status": "invalid", "message": "Cache not found or invalid"}
        
        try:
            with open(self.metadata_cache_file, 'r') as f:
                metadata = json.load(f)
            
            # Get cache file sizes
            cache_size = 0
            cache_files = [
                self.chunks_cache_file,
                self.embeddings_cache_file,
                self.faiss_cache_file,
                self.metadata_cache_file
            ]
            
            for cache_file in cache_files:
                if os.path.exists(cache_file):
                    cache_size += os.path.getsize(cache_file)
            
            return {
                "status": "valid",
                "num_chunks": metadata['num_chunks'],
                "embedding_dim": metadata['embedding_dim'],
                "created_at": metadata['created_at'],
                "model_name": metadata['model_name'],
                "cache_size_mb": round(cache_size / (1024 * 1024), 2),
                "documents_hash": metadata['documents_hash']
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    """Test the cache system"""
    data_dir = os.path.join(os.path.dirname(__file__), 'athena_data')
    cache = EmbeddingsCache(data_dir)
    
    print("🧪 Testing Embeddings Cache System")
    print("=" * 50)
    
    # Test cache info
    info = cache.get_cache_info()
    print(f"📊 Cache info: {info}")
    
    # Test loading/generating embeddings
    import time
    start_time = time.time()
    
    try:
        document_chunks, embeddings, faiss_index = cache.get_or_create_embeddings()
        load_time = time.time() - start_time
        
        print(f"⚡ Load time: {load_time:.2f} seconds")
        print(f"📚 Loaded {len(document_chunks)} chunks")
        print(f"🔢 Embedding dimension: {embeddings.shape[1]}")
        print(f"🗂️ FAISS index ready with {faiss_index.ntotal} vectors")
        
    except Exception as e:
        print(f"❌ Error: {e}")