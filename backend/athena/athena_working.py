#!/usr/bin/env python3
"""
Athena Agent - Working Version with Offline Mode
This version works even if the API is temporarily unavailable
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any

class AthenaAgentWorking:
    """
    Athena - AI Legal Assistant with working RAG capabilities
    """
    
    def __init__(self):
        # Load API key from environment or file
        self.api_key = self.load_api_key()
        
        # Try different API endpoints that might work
        self.api_endpoints = [
            f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={self.api_key}",
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}",
            f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={self.api_key}",
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.api_key}"
        ]
        
        # Find working API endpoint
        self.working_api_url = self.find_working_endpoint()
        
        # Data directory path
        self.data_dir = os.path.join(os.path.dirname(__file__), 'athena_data')
        
        # Document storage
        self.documents = {}
        
        # Load documents
        self.load_documents()
        
        # System prompt for Athena
        self.system_prompt = """You are Athena, an AI Legal Assistant specializing in Indian labor law and workplace rights. Provide professional, accurate legal guidance based on the context provided.

IMPORTANT GUIDELINES:
- Always include legal disclaimers
- Cite relevant acts and sections when possible  
- Distinguish between general information and specific legal advice
- Recommend professional legal counsel for complex matters
- Be professional, clear, and helpful

Context from legal documents: {context}

User question: {query}

Provide a comprehensive legal response:"""
        
        self.conversation_history = []
        
        # Legal knowledge base for offline mode
        self.legal_knowledge = {
            'minimum_wage': {
                'title': 'Minimum Wages Act, 1948',
                'content': '''The Minimum Wages Act, 1948 is a key legislation that ensures workers receive fair compensation for their labor.

Key provisions:
• Applies to scheduled employments with specified employee thresholds
• Minimum wage rates fixed by appropriate government (Central/State)
• Rates vary by geographical area, type of work, and skill level
• Periodic revision based on cost of living and other factors
• Penalties for non-compliance

Current Structure:
- Skilled workers: Higher rate
- Semi-skilled workers: Medium rate  
- Unskilled workers: Basic rate

Legal Remedy:
Non-payment of minimum wages can result in penalties and compensation to workers.'''
            },
            'sexual_harassment': {
                'title': 'Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013',
                'content': '''This Act provides comprehensive framework for prevention and redressal of sexual harassment at workplace.

Definition of Sexual Harassment:
• Physical contact and advances
• Demand or request for sexual favors
• Making sexually colored remarks
• Showing pornography
• Any unwelcome physical, verbal, or non-verbal conduct of sexual nature

Employer Obligations:
• Constitute Internal Complaints Committee (ICC)
• Provide safe working environment free from harassment
• Conduct awareness programs
• Display penal consequences prominently

Complaint Mechanism:
• File complaint within 3 months of incident
• ICC to complete inquiry within 90 days
• Interim relief during inquiry
• Protection against victimization'''
            },
            'employee_rights': {
                'title': 'Fundamental Employee Rights under Indian Labor Law',
                'content': '''Indian labor legislation provides comprehensive protection to workers across various aspects.

Wage Rights:
• Right to minimum wages as per applicable rates
• Timely payment of wages (within 7-10 days)
• No unauthorized deductions except as permitted by law
• Overtime compensation for extra hours

Working Conditions:
• Maximum 48 hours per week for adult workers
• Weekly rest of at least 24 consecutive hours
• Annual leave with wages
• Safe and healthy work environment

Protection Rights:
• Protection against unfair dismissal
• Right to form unions and collective bargaining
• Grievance redressal mechanisms
• Social security benefits

Legal Framework:
- Minimum Wages Act, 1948
- Payment of Wages Act, 1936
- Factories Act, 1948
- Industrial Disputes Act, 1947
- Various state-specific labor laws'''
            }
        }
    
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
    
    def find_working_endpoint(self):
        """Try to find a working API endpoint"""
        if not self.api_key:
            return None
            
        test_payload = {
            "contents": [{
                "parts": [{
                    "text": "Test"
                }]
            }]
        }
        
        for endpoint in self.api_endpoints:
            try:
                data = json.dumps(test_payload).encode('utf-8')
                req = urllib.request.Request(
                    endpoint,
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req) as response:
                    response_data = json.loads(response.read().decode())
                
                if 'candidates' in response_data:
                    print(f"✅ Found working API endpoint!")
                    return endpoint
                    
            except Exception:
                continue
        
        print("⚠️  API temporarily unavailable - running in offline mode")
        return None
    
    def extract_text_from_pdf_simple(self, pdf_path: str) -> str:
        """Extract text from PDF using basic method"""
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            filename = os.path.basename(pdf_path)
            return f"Document: {filename}\n[PDF content extraction requires PyPDF2 package]\nLegal document available for reference."
        except Exception as e:
            return f"Document: {os.path.basename(pdf_path)}\n[Error reading PDF: {e}]"
    
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
    
    def search_documents_and_knowledge(self, query: str) -> str:
        """Search both documents and built-in legal knowledge"""
        query_lower = query.lower()
        context_parts = []
        
        # Search built-in knowledge base first
        if any(word in query_lower for word in ['minimum wage', 'wage', 'salary', 'payment']):
            knowledge = self.legal_knowledge['minimum_wage']
            context_parts.append(f"\n=== {knowledge['title']} ===\n{knowledge['content']}")
        
        if any(word in query_lower for word in ['harassment', 'sexual harassment', 'complaint']):
            knowledge = self.legal_knowledge['sexual_harassment']
            context_parts.append(f"\n=== {knowledge['title']} ===\n{knowledge['content']}")
        
        if any(word in query_lower for word in ['rights', 'employee rights', 'labor law', 'worker rights']):
            knowledge = self.legal_knowledge['employee_rights']
            context_parts.append(f"\n=== {knowledge['title']} ===\n{knowledge['content']}")
        
        # Search loaded documents
        for doc_name, doc_data in self.documents.items():
            content = doc_data['content'].lower()
            matches = sum(1 for word in query_lower.split() if word in content)
            
            if matches > 0:
                # Get relevant excerpt
                excerpt = doc_data['content'][:500]
                if len(doc_data['content']) > 500:
                    excerpt += "... [document continues]"
                context_parts.append(f"\n=== From {doc_name} ===\n{excerpt}")
        
        return "\n".join(context_parts) if context_parts else "General legal principles and Indian labor law provisions apply."
    
    def generate_offline_response(self, query: str, context: str) -> str:
        """Generate response using built-in legal knowledge when API unavailable"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['minimum wage', 'wage', 'salary']):
            return f"""**Minimum Wage Law in India**

Based on the Minimum Wages Act, 1948:

{self.legal_knowledge['minimum_wage']['content']}

**Important Notes:**
- Current rates vary by state and are updated periodically
- Check with local labor department for current applicable rates
- Both central and state governments can fix minimum wages

**Legal Disclaimer:** This information is for educational purposes only. For specific wage-related disputes or current rates, consult with qualified labor law professionals or contact the relevant labor department.

*Source: Minimum Wages Act, 1948 and related provisions*"""

        elif any(word in query_lower for word in ['harassment', 'sexual harassment']):
            return f"""**Sexual Harassment at Workplace - Legal Framework**

Under the Sexual Harassment of Women at Workplace Act, 2013:

{self.legal_knowledge['sexual_harassment']['content']}

**Steps to File a Complaint:**
1. Submit written complaint to ICC within 3 months
2. ICC conducts inquiry within 90 days
3. Interim relief may be provided during inquiry
4. Final report with recommendations

**Legal Disclaimer:** This is general information about the legal framework. For specific harassment cases, immediately consult with qualified legal professionals and consider filing a formal complaint with appropriate authorities.

*Source: Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013*"""

        elif any(word in query_lower for word in ['rights', 'employee rights']):
            return f"""**Employee Rights Under Indian Labor Law**

{self.legal_knowledge['employee_rights']['content']}

**Key Legislation:**
- Constitution of India (Fundamental Rights)
- Industrial Relations Code, 2020
- Occupational Safety Code, 2020
- Social Security Code, 2020

**Enforcement Mechanisms:**
- Labor courts and tribunals
- Grievance redressal committees
- Trade union representation
- Government labor inspectors

**Legal Disclaimer:** Labor laws are complex and frequently updated. This information provides general guidance only. For specific employment issues, consult with qualified labor law attorneys or contact relevant labor authorities.

*Source: Various Indian Labor Laws and Codes*"""

        else:
            return f"""**Legal Assistance Available**

I can provide guidance on various aspects of Indian labor law based on available legal documents:

**Areas of Expertise:**
• Employment Rights and Obligations
• Wage and Hour Laws (Minimum Wages Act)
• Workplace Harassment Prevention
• Industrial Relations and Disputes
• Safety and Working Conditions

**Available Legal Documents:**
{chr(10).join([f'• {doc}' for doc in self.documents.keys()])}

**How to Get Specific Help:**
Please ask specific questions about:
- Minimum wage rates and calculations
- Sexual harassment prevention and complaints
- Employee rights and employer obligations
- Working hours, overtime, and leave policies
- Termination and dismissal procedures

**Legal Disclaimer:** This AI assistant provides general legal information for educational purposes only. For specific legal matters, always consult with qualified legal professionals.

*Based on Indian Labor Law and available legal documents*"""
    
    def get_response(self, user_query: str) -> str:
        """Generate response using API or offline mode"""
        try:
            # Search for relevant context
            context = self.search_documents_and_knowledge(user_query)
            
            # Try API first if available
            if self.working_api_url:
                prompt = self.system_prompt.format(context=context, query=user_query)
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }]
                }
                
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(
                    self.working_api_url,
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req) as response:
                    response_data = json.loads(response.read().decode())
                
                if 'candidates' in response_data and len(response_data['candidates']) > 0:
                    content = response_data['candidates'][0]['content']
                    if 'parts' in content and len(content['parts']) > 0:
                        athena_response = content['parts'][0]['text']
                        
                        # Add to conversation history
                        self.add_to_history(user_query, athena_response)
                        return athena_response
            
            # Fallback to offline mode
            print("💡 Using offline knowledge base...")
            response = self.generate_offline_response(user_query, context)
            self.add_to_history(user_query, response)
            return response
            
        except Exception as e:
            print(f"⚠️  Switching to offline mode due to: {str(e)}")
            context = self.search_documents_and_knowledge(user_query)
            response = self.generate_offline_response(user_query, context)
            self.add_to_history(user_query, response)
            return response
    
    def add_to_history(self, query: str, response: str):
        """Add exchange to conversation history"""
        self.conversation_history.append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now().isoformat()
        })
        self.conversation_history.append({
            "role": "assistant", 
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
    
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
    """Main function to run Athena in interactive mode"""
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
        athena = AthenaAgentWorking()
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
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main()