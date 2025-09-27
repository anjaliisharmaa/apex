#!/usr/bin/env python3
"""
Athena Agent - Legal AI Assistant (Simplified version with basic RAG)
This agent provides legal guidance using documents from athena_data/
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any
import re

class AthenaAgentSimple:
    """
    Athena - AI Legal Assistant with basic document retrieval
    Provides legal guidance based on uploaded documents
    """
    
    def __init__(self):
        # Load API key from environment or file
        self.api_key = self.load_api_key()
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in .env file or environment variables")
        
        # Gemini API endpoint (using correct model name)
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.api_key}"
        
        # Data directory path
        self.data_dir = os.path.join(os.path.dirname(__file__), 'athena_data')
        
        # Document storage
        self.documents = {}
        
        # Load documents
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
        
        **Available Legal Documents:**
        {document_list}
        
        **Relevant Context:**
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
    
    def extract_text_from_pdf_simple(self, pdf_path: str) -> str:
        """Extract text from PDF using basic method (fallback if PyPDF2 not available)"""
        try:
            # Try to use PyPDF2 if available
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            # Fallback: return filename and basic info
            filename = os.path.basename(pdf_path)
            return f"Document: {filename}\nContent: Legal document available for reference. Specific extraction requires PyPDF2 package."
        except Exception as e:
            print(f"❌ Error extracting text from {pdf_path}: {e}")
            return f"Document: {os.path.basename(pdf_path)} (Error reading content)"
    
    def load_documents(self):
        """Load and process all PDF documents in athena_data directory"""
        print("📄 Loading legal documents...")
        
        if not os.path.exists(self.data_dir):
            print(f"❌ Data directory not found: {self.data_dir}")
            return
        
        # Process each PDF file
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.pdf'):
                print(f"  📖 Processing {filename}...")
                pdf_path = os.path.join(self.data_dir, filename)
                
                # Extract text from PDF
                text = self.extract_text_from_pdf_simple(pdf_path)
                doc_name = filename.replace('.pdf', '')
                self.documents[doc_name] = {
                    'filename': filename,
                    'content': text,
                    'path': pdf_path
                }
        
        print(f"✅ Loaded {len(self.documents)} legal documents")
    
    def search_documents_simple(self, query: str) -> str:
        """Simple keyword-based search through documents"""
        query_lower = query.lower()
        relevant_content = []
        
        # Keywords that might indicate different types of legal queries
        labor_keywords = ['salary', 'wage', 'minimum wage', 'overtime', 'working hours', 'leave', 'termination', 'dismissal']
        harassment_keywords = ['harassment', 'sexual harassment', 'workplace harassment', 'complaint', 'grievance']
        general_keywords = ['rights', 'employee', 'employer', 'law', 'act', 'section']
        
        # Determine document relevance based on keywords
        for doc_name, doc_data in self.documents.items():
            content = doc_data['content'].lower()
            
            # Check if query keywords match document content
            matches = 0
            for word in query_lower.split():
                if word in content:
                    matches += 1
            
            # Include document if it has keyword matches or is generally relevant
            if matches > 0 or any(keyword in query_lower for keyword in general_keywords):
                # Get a relevant excerpt (first 1000 chars)
                excerpt = doc_data['content'][:1000]
                if len(doc_data['content']) > 1000:
                    excerpt += "... [document continues]"
                
                relevant_content.append(f"\n--- From {doc_name} ---\n{excerpt}")
        
        if relevant_content:
            return "\n".join(relevant_content)
        else:
            return "No specific document content found for this query, but I can provide general legal guidance based on Indian labor law principles."
    
    def get_response(self, user_query: str) -> str:
        """
        Generate a response using simple RAG - search documents and generate answer
        
        Args:
            user_query (str): The user's legal question
            
        Returns:
            str: Athena's response with legal guidance
        """
        try:
            # Search for relevant context in documents
            context = self.search_documents_simple(user_query)
            
            # Create document list
            doc_list = "\n".join([f"• {doc}" for doc in self.documents.keys()])
            
            # Prepare the prompt with context
            prompt = self.system_prompt.format(
                document_list=doc_list,
                context=context,
                query=user_query
            )
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
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
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode())
            
            # Extract the response text
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                content = response_data['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    athena_response = content['parts'][0]['text']
                    
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
                    
                    return athena_response
            
            return "I apologize, but I'm having trouble generating a response right now. Please try again."
            
        except Exception as e:
            error_response = f"I apologize, but I'm experiencing some technical difficulties right now. Error: {str(e)}"
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
        if not self.documents:
            return "No legal documents available."
        
        docs = list(self.documents.keys())
        return "Available legal documents:\n" + "\n".join([f"• {doc}" for doc in docs])

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
        print("🔄 Initializing Athena Legal Assistant...")
        athena = AthenaAgentSimple()
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
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()