#!/usr/bin/env python3
"""
APEX Backend Server - Simplified FastAPI Orchestrator
=====================================================
Central server that manages ASHA, Athena, and Scribe agents
Provides REST API endpoints for the frontend application
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json

app = FastAPI(
    title="APEX Legal Assistant API",
    description="Backend API for APEX - AI-Powered Legal Assistant Suite",
    version="1.0.0"
)

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    anonymous: Optional[bool] = True

class ChatResponse(BaseModel):
    response: str
    agent_used: str
    conversation_id: str
    timestamp: str

class DocumentRequest(BaseModel):
    document_type: str
    user_data: Dict[str, Any]

class DocumentResponse(BaseModel):
    document_content: str
    document_type: str
    generated_at: str

class CaseInfo(BaseModel):
    id: str
    title: str
    description: str
    status: str
    created_at: str
    last_updated: str

# Agent instances (lazy loaded)
agents = {
    'asha': None,
    'athena': None,
    'scribe': None
}

# Conversation storage (in production, use a database)
conversations = {}

def get_asha_agent():
    """Lazy load ASHA agent - ORIGINAL asha.py"""
    if agents['asha'] is None:
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'asha'))
            from asha import AshaAgent
            agents['asha'] = AshaAgent()
            print("✅ ASHA Agent (ORIGINAL) initialized!")
        except Exception as e:
            print(f"❌ Failed to initialize ASHA Agent: {e}")
            agents['asha'] = 'failed'
    
    return agents['asha'] if agents['asha'] != 'failed' else None

def get_athena_agent():
    """Lazy load Athena agent - ORIGINAL athena.py"""
    if agents['athena'] is None:
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'athena'))
            from athena import AthenaAgent
            agents['athena'] = AthenaAgent()
            print("✅ Athena Agent (ORIGINAL) initialized!")
        except Exception as e:
            print(f"❌ Failed to initialize Athena Agent: {e}")
            agents['athena'] = 'failed'
    
    return agents['athena'] if agents['athena'] != 'failed' else None

def get_scribe_agent():
    """Lazy load Scribe agent - ORIGINAL scribe.py"""
    if agents['scribe'] is None:
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scribe'))
            from scribe import ScribeAgent
            agents['scribe'] = ScribeAgent()
            print("✅ Scribe Agent (ORIGINAL) initialized!")
        except Exception as e:
            print(f"❌ Failed to initialize Scribe Agent: {e}")
            agents['scribe'] = 'failed'
    
    return agents['scribe'] if agents['scribe'] != 'failed' else None

class OrchestrationEngine:
    """
    Smart routing engine to determine which agent should handle each query
    """
    
    @staticmethod
    def analyze_intent(message: str) -> str:
        """
        Analyze user message to determine appropriate agent
        Returns: 'asha', 'athena', or 'scribe'
        """
        message_lower = message.lower()
        
        # Legal keywords for Athena
        legal_keywords = [
            'legal', 'law', 'rights', 'harassment', 'discrimination', 
            'wage', 'salary', 'employment', 'termination', 'contract',
            'labor', 'workplace', 'policy', 'regulation', 'act',
            'court', 'litigation', 'compliance', 'violation',
            'maternity rights', 'paternity', 'overtime', 'minimum wage'
        ]
        
        # Document generation keywords for Scribe
        document_keywords = [
            'generate', 'create', 'write', 'draft', 'compose',
            'application', 'form', 'letter', 'email', 'message',
            'whatsapp', 'sms', 'document', 'report', 'proposal',
            'contract', 'agreement', 'notice', 'memo',
            'maternity leave application', 'transfer request',
            'grievance form', 'leave application'
        ]
        
        # Emotional support keywords for ASHA
        emotional_keywords = [
            'stressed', 'anxiety', 'worried', 'scared', 'overwhelmed',
            'depressed', 'upset', 'frustrated', 'angry', 'sad',
            'support', 'help me cope', 'emotional', 'feeling',
            'mental health', 'wellbeing', 'counseling', 'guidance',
            'comfort', 'reassurance', 'encouragement'
        ]
        
        # Count keyword matches
        legal_score = sum(1 for keyword in legal_keywords if keyword in message_lower)
        document_score = sum(1 for keyword in document_keywords if keyword in message_lower)
        emotional_score = sum(1 for keyword in emotional_keywords if keyword in message_lower)
        
        # Specific phrase matching for better accuracy
        if any(phrase in message_lower for phrase in ['generate', 'create', 'write', 'draft']):
            if any(doc in message_lower for doc in ['email', 'message', 'letter', 'application', 'form']):
                return 'scribe'
        
        if any(phrase in message_lower for phrase in ['my rights', 'is this legal', 'labor law', 'can my employer']):
            return 'athena'
            
        if any(phrase in message_lower for phrase in ['i feel', 'i am worried', 'help me cope', 'emotional support']):
            return 'asha'
        
        # Score-based decision
        max_score = max(legal_score, document_score, emotional_score)
        
        if max_score == 0:
            # Default routing based on message characteristics
            if '?' in message and any(word in message_lower for word in ['how', 'what', 'when', 'where', 'why']):
                return 'athena'  # Questions likely legal
            elif any(word in message_lower for word in ['please', 'can you', 'help me']):
                return 'asha'  # Requests likely need emotional support
            else:
                return 'athena'  # Default to legal assistance
        
        if legal_score == max_score:
            return 'athena'
        elif document_score == max_score:
            return 'scribe'
        else:
            return 'asha'

# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "APEX Legal Assistant API",
        "status": "running",
        "version": "1.0.0",
        "agents": {
            "asha": "emotional support",
            "athena": "legal assistance", 
            "scribe": "document generation"
        }
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint - routes messages to appropriate agent
    """
    try:
        # Determine which agent to use
        agent_to_use = OrchestrationEngine.analyze_intent(request.message)
        
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or f"conv_{datetime.now().timestamp()}"
        
        # Route to appropriate agent
        response = None
        
        if agent_to_use == 'asha':
            agent = get_asha_agent()
            if agent:
                response = agent.get_response(request.message)
            else:
                response = "I'm sorry, the emotional support assistant is currently unavailable. Please try again later."
        
        elif agent_to_use == 'athena':
            agent = get_athena_agent()
            if agent:
                response = agent.get_response(request.message)
            else:
                response = "I'm sorry, the legal assistant is currently unavailable. Please try again later."
        
        elif agent_to_use == 'scribe':
            agent = get_scribe_agent()
            if agent:
                response = agent.process_user_input(request.message)
            else:
                response = "I'm sorry, the document generator is currently unavailable. Please try again later."
        
        if not response:
            response = "I'm sorry, I couldn't understand your request. Please try again."
        
        # Store conversation (in production, use database)
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        conversations[conversation_id].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": request.message,
            "agent_response": response,
            "agent_used": agent_to_use
        })
        
        return ChatResponse(
            response=response,
            agent_used=agent_to_use,
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")

@app.post("/api/forms/generate", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """
    Document generation endpoint - uses Scribe agent
    """
    try:
        scribe_agent = get_scribe_agent()
        if not scribe_agent:
            raise HTTPException(status_code=503, detail="Document generator not available")
        
        document_content = scribe_agent.generate_document(
            request.document_type,
            request.user_data
        )
        
        return DocumentResponse(
            document_content=document_content,
            document_type=request.document_type,
            generated_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document generation error: {str(e)}")

@app.get("/api/cases")
async def get_cases():
    """
    Get user cases - mock data for now
    """
    # Mock data - in production, fetch from database
    return [
        CaseInfo(
            id="case_001",
            title="Maternity Leave Application",
            description="Application for 6-month maternity leave",
            status="pending",
            created_at="2024-01-15",
            last_updated="2024-01-20"
        ),
        CaseInfo(
            id="case_002", 
            title="Workplace Harassment Complaint",
            description="Formal complaint regarding workplace harassment",
            status="in_progress",
            created_at="2024-01-10",
            last_updated="2024-01-25"
        )
    ]

@app.get("/api/resources")
async def get_resources():
    """
    Get legal resources and information
    """
    return {
        "legal_acts": [
            {
                "name": "Maternity Benefit Act, 2017",
                "description": "Provides for 26 weeks paid maternity leave",
                "url": "/resources/maternity-act"
            },
            {
                "name": "Sexual Harassment Act, 2013", 
                "description": "Prevention, prohibition and redressal of sexual harassment",
                "url": "/resources/posh-act"
            }
        ],
        "forms": [
            {
                "name": "Maternity Leave Application",
                "type": "maternity_leave",
                "description": "Standard maternity leave application form"
            },
            {
                "name": "Transfer Request",
                "type": "transfer_request", 
                "description": "Employee transfer request form"
            }
        ],
        "contacts": {
            "hr_helpline": "+91-80-12345678",
            "legal_aid": "+91-80-87654321",
            "employee_assistance": "support@company.com"
        }
    }

@app.get("/api/agents/status")
async def get_agents_status():
    """
    Get status of all agents
    """
    return {
        "asha": {
            "status": "available" if agents['asha'] is None or (agents['asha'] and agents['asha'] != 'failed') else "failed",
            "description": "Emotional support and wellness assistant"
        },
        "athena": {
            "status": "available" if agents['athena'] is None or (agents['athena'] and agents['athena'] != 'failed') else "failed",
            "description": "Legal guidance and consultation assistant"
        },
        "scribe": {
            "status": "available" if agents['scribe'] is None or (agents['scribe'] and agents['scribe'] != 'failed') else "failed",
            "description": "Document generation and workflow assistant"
        }
    }

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    Get conversation history
    """
    if conversation_id in conversations:
        return conversations[conversation_id]
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Handle file uploads for document processing
    """
    try:
        # Save file temporarily
        file_path = f"temp_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process with appropriate agent (example with Athena for legal docs)
        # This is where you'd add document processing logic
        
        return {
            "filename": file.filename,
            "size": len(content),
            "message": "File uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting APEX Backend Server...")
    print("🔧 Agents will be loaded on-demand for better reliability")
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000, 
        reload=False,
        log_level="info"
    )