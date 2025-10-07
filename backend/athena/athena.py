#!/usr/bin/env python3
"""
Athena Agent - Legal AI Assistant with RAG (Retrieval-Augmented Generation)
This agent provides legal guidance using documents from athena_data/
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any
import PyPDF2
import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class AthenaAgent:
    """
    Athena - AI Legal Assistant with RAG capabilities
    Provides legal guidance based on uploaded documents
    """
    
    def __init__(self):
        # Load API key from environment or file
        print("🔑 Loading API key...")
        self.api_key = self.load_api_key()
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in .env file or environment variables")
        
        print(f"✅ API key loaded: {self.api_key[:12]}...")
        
        # Gemini API endpoint - Using the latest available model (Gemini 2.5 Flash)
        self.api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={self.api_key}"
        
        # Initialize sentence transformer for embeddings
        print("📚 Loading sentence transformer model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Data directory path
        self.data_dir = os.path.join(os.path.dirname(__file__), 'athena_data')
        
        # RAG components
        self.document_chunks = []
        self.chunk_embeddings = None
        self.faiss_index = None
        
        # Test API connection
        print("🔄 Testing API connection...")
        self.test_api_connection()
        
        # Load and process documents
        self.load_documents()
        
        # System prompt for Athena
        self.system_prompt = """
        You are Athena, an AI Legal Assistant with expertise in Indian labor law and workplace rights. You have access to relevant legal documents and can provide accurate legal guidance based on the provided context.
        
        **Your Capabilities:**
        1. **Legal Guidance**: Provide accurate information about labor laws, workplace rights, and legal procedures
        2. **Document Analysis**: Analyze and interpret legal documents and regulations
        3. **Compliance Advice**: Help understand legal compliance requirements
        4. **Case Assessment**: Provide preliminary assessment of legal situations
        5. **Resource Direction**: Guide users to appropriate legal resources and next steps
        
        **Your Personality:**
        - Professional and authoritative
        - Clear and precise in explanations
        - Objective and factual
        - Helpful and educational
        - Ethical and responsible
        
        **Important Guidelines:**
        - Always base your responses on the provided legal context when available
        - Clearly distinguish between general information and specific legal advice
        - Recommend consulting with qualified legal professionals for complex matters
        - Stay within the bounds of the legal documents provided
        - Be transparent about limitations of AI legal assistance
        - Cite relevant sections or acts when providing information
        
        **Disclaimer:**
        Always remind users that this is AI-generated information for educational purposes and should not replace professional legal counsel for specific legal matters.
        
        **Context from Legal Documents:**
        {context}
        
        **User Query:**
        {query}
        
        Please provide a comprehensive response based on the context above:
        """
        
        self.conversation_history = []
    
    def load_api_key(self):
        """Load API key from environment or .env file"""
        # First try environment variable
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            return api_key
        
        # Try to load from .env file
        env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file_path):
            with open(env_file_path, 'r') as f:
                for line in f:
                    if line.startswith('GOOGLE_API_KEY='):
                        return line.split('=', 1)[1].strip().strip('"\'')
        
        return None
    
    def test_api_connection(self):
        """Test if the Gemini API is working with our API key"""
        try:
            test_payload = {
                "contents": [{
                    "parts": [{"text": "Hello, respond with 'API working'"}]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 10
                }
            }
            
            data = json.dumps(test_payload).encode('utf-8')
            req = urllib.request.Request(
                self.api_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    response_data = json.loads(response.read().decode())
                    if 'candidates' in response_data and response_data['candidates']:
                        print("✅ API connection successful!")
                        return True
                    else:
                        print("⚠️ API responded but with unexpected format")
                        return False
                else:
                    print(f"⚠️ API returned status {response.status}")
                    return False
                    
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if hasattr(e, 'read') else str(e)
            print(f"❌ API HTTP Error {e.code}: {error_body}")
            return False
        except Exception as e:
            print(f"❌ API connection failed: {e}")
            return False
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"❌ Error extracting text from {pdf_path}: {e}")
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
    
    def load_documents(self):
        """Load and process all PDF documents in athena_data directory"""
        print("📄 Loading legal documents...")
        
        if not os.path.exists(self.data_dir):
            print(f"❌ Data directory not found: {self.data_dir}")
            return
        
        all_chunks = []
        chunk_metadata = []
        
        # Process each PDF file
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
        
        if all_chunks:
            print(f"✅ Processed {len(all_chunks)} text chunks from {len(os.listdir(self.data_dir))} documents")
            
            # Generate embeddings
            print("🔄 Generating embeddings...")
            embeddings = self.embedding_model.encode(all_chunks)
            
            # Create FAISS index
            self.faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
            self.faiss_index.add(embeddings.astype('float32'))
            
            # Store chunks and metadata
            self.document_chunks = list(zip(all_chunks, chunk_metadata))
            
            print("✅ RAG system initialized successfully!")
        else:
            print("❌ No documents found or processed")
    
    def retrieve_relevant_context(self, query: str, top_k: int = 5) -> str:
        """Retrieve relevant document chunks based on query"""
        if not self.faiss_index or not self.document_chunks:
            return "No legal documents available for reference."
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            
            # Search for similar chunks
            scores, indices = self.faiss_index.search(query_embedding.astype('float32'), top_k)
            
            # Collect relevant chunks
            context_parts = []
            seen_sources = set()
            
            for i, idx in enumerate(indices[0]):
                if idx < len(self.document_chunks):
                    chunk_text, metadata = self.document_chunks[idx]
                    source = metadata['source']
                    
                    # Add source header if new
                    if source not in seen_sources:
                        context_parts.append(f"\n--- From {source} ---")
                        seen_sources.add(source)
                    
                    context_parts.append(chunk_text.strip())
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            print(f"❌ Error retrieving context: {e}")
            return "Error retrieving relevant legal context."
    
    def get_response(self, user_query: str) -> str:
        """
        Generate a response using RAG - retrieve relevant context and generate answer
        
        Args:
            user_query (str): The user's legal question
            
        Returns:
            str: Athena's response with legal guidance
        """
        try:
            # Retrieve relevant context from documents
            context = self.retrieve_relevant_context(user_query, top_k=5)
            
            # Prepare the prompt with context
            prompt = self.system_prompt.format(
                context=context,
                query=user_query
            )
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "topP": 0.8,
                    "topK": 40,
                    "maxOutputTokens": 2048
                }
            }
            
            # Convert to JSON
            data = json.dumps(payload).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(
                self.api_url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                }
            )
            
            # Make the request
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    if response.status == 200:
                        response_data = json.loads(response.read().decode())
                        
                        # Debug: Print response structure for troubleshooting
                        print(f"🔍 API Response Status: {response.status}")
                        
                        # Extract the response text
                        if 'candidates' in response_data and len(response_data['candidates']) > 0:
                            candidate = response_data['candidates'][0]
                            
                            if 'content' in candidate and 'parts' in candidate['content']:
                                athena_response = candidate['content']['parts'][0]['text']
                                
                                # Add to conversation history
                                self.conversation_history.append({
                                    "role": "user",
                                    "content": user_query,
                                    "timestamp": datetime.now().isoformat()
                                })
                                self.conversation_history.append({
                                    "role": "assistant",
                                    "content": athena_response,
                                    "timestamp": datetime.now().isoformat()
                                })
                                
                                return f"⚖️ {athena_response}"
                            else:
                                return "❌ Unexpected response format from API. The response structure has changed."
                        else:
                            return "❌ No valid response candidates returned from API."
                    else:
                        return f"❌ API returned status code: {response.status}"
                        
            except urllib.error.HTTPError as e:
                error_body = e.read().decode() if hasattr(e, 'read') else str(e)
                return f"❌ HTTP Error {e.code}: {error_body}"
            except urllib.error.URLError as e:
                return f"❌ Connection Error: {e.reason}"
            except json.JSONDecodeError as e:
                return f"❌ Invalid JSON response from API: {e}"
            
        except Exception as e:
            print(f"🔍 Debug - Unexpected error: {type(e).__name__}: {str(e)}")
            error_response = f"❌ I'm experiencing technical difficulties. Please check your internet connection and API key. Error: {str(e)}"
            return error_response
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        return "Conversation history has been reset. How can I assist you with legal matters today?"
    
    def get_conversation_summary(self):
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history available."
        
        summary = f"Conversation started: {self.conversation_history[0]['timestamp']}\n"
        summary += f"Total messages: {len(self.conversation_history)}\n"
        summary += f"Last message: {self.conversation_history[-1]['timestamp']}"
        
        return summary
    
    def get_available_documents(self):
        """Get list of available legal documents"""
        if not os.path.exists(self.data_dir):
            return "No document directory found."
        
        docs = [f for f in os.listdir(self.data_dir) if f.endswith('.pdf')]
        if docs:
            return "Available legal documents:\n" + "\n".join([f"• {doc}" for doc in docs])
        else:
            return "No legal documents available."

def main():
    """
    Main function to run Athena in interactive mode
    """
    print("⚖️  Welcome to Athena - AI Legal Assistant ⚖️")
    print("=" * 50)
    print("I provide legal guidance based on Indian labor law documents.")
    print("Type 'quit' or 'exit' to end our conversation.")
    print("Type 'reset' to start a new conversation.")
    print("Type 'summary' to see conversation statistics.")
    print("Type 'documents' to see available legal documents.")
    print("=" * 50)
    
    try:
        # Initialize Athena
        print("🔄 Initializing Athena RAG system...")
        athena = AthenaAgent()
        print("✅ Athena is ready to provide legal assistance!")
        
        # Show available documents
        print(f"\n{athena.get_available_documents()}")
        
        while True:
            print("\n" + "-" * 30)
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("\nAthena: Thank you for consulting with me. Remember to seek professional legal counsel for specific matters. ⚖️")
                break
            
            elif user_input.lower() == 'reset':
                response = athena.reset_conversation()
                print(f"\nAthena: {response}")
                continue
            
            elif user_input.lower() == 'summary':
                summary = athena.get_conversation_summary()
                print(f"\nConversation Summary:\n{summary}")
                continue
            
            elif user_input.lower() == 'documents':
                docs = athena.get_available_documents()
                print(f"\n{docs}")
                continue
            
            elif not user_input:
                print("\nAthena: I'm here to help with your legal questions. Please ask me anything about labor law or workplace rights.")
                continue
            
            # Get response from Athena
            print("\nAthena: ", end="", flush=True)
            response = athena.get_response(user_input)
            print(response)
            
    except KeyboardInterrupt:
        print("\n\nAthena: Session ended. Remember to consult with qualified legal professionals for specific legal matters. ⚖️")
    except Exception as e:
        print(f"\n❌ Error initializing Athena: {e}")
        print("Please check your API key, internet connection, and ensure the required packages are installed.")

if __name__ == "__main__":
    main()