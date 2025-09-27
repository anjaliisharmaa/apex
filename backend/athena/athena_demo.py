#!/usr/bin/env python3
"""
Athena Agent Demo - Shows RAG functionality with mock responses
This demonstrates how the RAG system works with legal documents
"""

import os
from datetime import datetime

class AthenaAgentDemo:
    """
    Athena Demo - Shows how RAG works with legal documents
    """
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'athena_data')
        self.documents = {}
        self.conversation_history = []
        
        # Load documents
        self.load_documents_demo()
    
    def load_documents_demo(self):
        """Load document information for demo"""
        print("📄 Loading legal documents...")
        
        if not os.path.exists(self.data_dir):
            print(f"❌ Data directory not found: {self.data_dir}")
            return
        
        # Process each PDF file (demo mode - just list them)
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.pdf'):
                print(f"  📖 Processing {filename}...")
                doc_name = filename.replace('.pdf', '')
                self.documents[doc_name] = {
                    'filename': filename,
                    'content': f"Legal document content from {filename} would be processed here for RAG.",
                    'path': os.path.join(self.data_dir, filename)
                }
        
        print(f"✅ Loaded {len(self.documents)} legal documents for RAG processing")
    
    def search_documents_demo(self, query: str) -> str:
        """Demo of how document search would work"""
        query_lower = query.lower()
        
        # Simulate RAG retrieval based on query keywords
        if any(word in query_lower for word in ['minimum wage', 'wage', 'salary']):
            return """
--- From MinimumWagesact ---
The Minimum Wages Act, 1948 provides for fixation of minimum wages in certain employments. 
The Act applies to scheduled employments where the number of employees is 1000 or more.
Minimum wages are fixed by the appropriate government for different categories of workers.
The rates are revised periodically taking into account factors like cost of living, etc.

--- From Labour Act ---
Various provisions related to wages, working conditions, and employee rights are covered
under different labor legislations including payment of wages, working hours, and overtime compensation.
"""
        
        elif any(word in query_lower for word in ['harassment', 'sexual harassment']):
            return """
--- From DoE_Prevention_sexual_harassment ---
The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013
defines sexual harassment and provides for prevention and redressal mechanisms.

Key provisions include:
- Constitution of Internal Complaints Committee (ICC) in organizations
- Duties of employer to provide safe working environment
- Complaint procedure and inquiry process
- Protection against victimization and false complaints
"""
        
        elif any(word in query_lower for word in ['rights', 'employee rights', 'labor law']):
            return """
--- From Labour Act ---
Indian labor law provides comprehensive protection to workers including:
- Right to fair wages and timely payment
- Right to safe working conditions
- Right to form unions and collective bargaining
- Protection against unfair dismissal
- Rights related to working hours, overtime, and leave

--- From MinimumWagesact ---
Employees are entitled to receive not less than the minimum wages fixed for their category of work.
"""
        
        else:
            return """
General legal guidance available from the following documents:
- Labour Act: Covers general employment rights and obligations
- MinimumWagesact: Specific provisions on minimum wage entitlements
- DoE_Prevention_sexual_harassment: Workplace harassment prevention and redressal
"""
    
    def get_demo_response(self, user_query: str) -> str:
        """Generate a demo response showing how RAG would work"""
        
        # Retrieve relevant context
        context = self.search_documents_demo(user_query)
        
        # Simulate AI response based on context
        responses = {
            'minimum wage': """Based on the Minimum Wages Act, 1948, employers are legally required to pay workers not less than the minimum wage rates fixed by the appropriate government. These rates vary by:

1. **Geographic location** (state/region)
2. **Type of employment** (scheduled employments)
3. **Skill category** (skilled, semi-skilled, unskilled)

Key points:
- Minimum wages are revised periodically considering cost of living
- The Act applies to establishments with specific employee thresholds
- Non-payment of minimum wages is a punishable offense

**Legal Disclaimer**: This information is for educational purposes. For current rates and specific situations, consult with qualified legal professionals or check the latest government notifications.

*Source: Based on MinimumWagesact and Labour Act provisions*""",

            'sexual harassment': """According to The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013:

**Definition**: Sexual harassment includes unwelcome acts or behavior (whether directly or by implication) such as:
- Physical contact and advances
- Demand or request for sexual favors  
- Making sexually colored remarks
- Showing pornography
- Any other unwelcome physical, verbal or non-verbal conduct of sexual nature

**Employer Obligations**:
- Constitute Internal Complaints Committee (ICC)
- Provide safe working environment
- Conduct awareness programs
- Display penal consequences

**Complaint Process**:
- File complaint within 3 months of incident
- ICC to complete inquiry within 90 days
- Protection against victimization

**Legal Disclaimer**: This is general information. For specific cases, seek professional legal counsel.

*Source: Based on DoE Prevention of Sexual Harassment provisions*""",

            'employee rights': """Under Indian Labor Law, employees have fundamental rights including:

**Wage Rights**:
- Right to minimum wages as per applicable rates
- Timely payment of wages (within specified periods)
- No unauthorized deductions from wages

**Working Conditions**:
- Safe and healthy work environment
- Prescribed working hours and overtime compensation
- Weekly rest periods and annual leave

**Protection Rights**:
- Protection against unfair dismissal
- Right to form unions and collective bargaining
- Right to raise grievances and complaints

**Legal Framework**: These rights are protected under various acts including:
- The Minimum Wages Act, 1948
- The Payment of Wages Act, 1936
- The Industrial Disputes Act, 1947
- Various state labor laws

**Legal Disclaimer**: Labor laws can be complex and vary by state. Always consult with qualified legal professionals for specific situations.

*Source: Based on comprehensive Indian Labor Law provisions*"""
        }
        
        # Determine response based on query
        query_lower = user_query.lower()
        
        if any(word in query_lower for word in ['minimum wage', 'wage', 'salary']):
            response = responses['minimum wage']
        elif any(word in query_lower for word in ['harassment', 'sexual harassment']):
            response = responses['sexual harassment']
        elif any(word in query_lower for word in ['rights', 'employee rights', 'labor law']):
            response = responses['employee rights']
        else:
            response = """I can provide legal guidance on various aspects of Indian labor law based on the available legal documents. My knowledge covers:

- **Employment Rights**: Fundamental rights of employees under Indian labor law
- **Wage Laws**: Minimum wage provisions and payment regulations  
- **Workplace Safety**: Including prevention of sexual harassment
- **Legal Procedures**: Complaint mechanisms and redressal processes

Please ask specific questions about labor law, workplace rights, or legal procedures, and I'll provide detailed information based on the relevant legal documents.

**Legal Disclaimer**: This AI provides general information for educational purposes only. For specific legal matters, always consult with qualified legal professionals.

*Available Documents: Labour Act, MinimumWagesact, DoE Prevention of Sexual Harassment*"""
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user", 
            "content": user_query,
            "timestamp": datetime.now().isoformat()
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def get_available_documents(self):
        """Get list of available legal documents"""
        if not self.documents:
            return "No legal documents available."
        
        docs = list(self.documents.keys())
        return "Available legal documents:\n" + "\n".join([f"• {doc}" for doc in docs])

def main():
    """Demo of Athena Legal Assistant with RAG"""
    print("⚖️  Athena Legal Assistant - RAG Demo ⚖️")
    print("=" * 50)
    print("This demo shows how RAG (Retrieval-Augmented Generation) works")
    print("with legal documents to provide contextual legal guidance.")
    print("=" * 50)
    
    # Initialize Athena Demo
    athena = AthenaAgentDemo()
    
    print(f"\n{athena.get_available_documents()}")
    
    # Demo queries
    demo_queries = [
        "What is the minimum wage law in India?",
        "What constitutes sexual harassment in the workplace?", 
        "What are the basic rights of employees under Indian labor law?",
        "How do I file a complaint about workplace harassment?"
    ]
    
    print(f"\n🎬 RAG Demo - Testing {len(demo_queries)} queries:")
    print("=" * 50)
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("\n🔍 RAG Context Retrieved:")
        context = athena.search_documents_demo(query)
        print(context[:300] + "..." if len(context) > 300 else context)
        
        print(f"\n🤖 Athena's Response:")
        print("-" * 30)
        response = athena.get_demo_response(query)
        print(response)
        print("-" * 50)
    
    print(f"\n✅ Demo completed! This shows how Athena would work with:")
    print("• Document processing and chunking")
    print("• Semantic search and retrieval") 
    print("• Context-aware AI responses")
    print("• Legal document integration")
    
    print(f"\n💡 For interactive mode, the full Athena agent would:")
    print("• Process PDF documents with PyPDF2")
    print("• Use sentence transformers for embeddings")
    print("• Implement FAISS for vector search")
    print("• Generate responses via Google Gemini API")

if __name__ == "__main__":
    main()