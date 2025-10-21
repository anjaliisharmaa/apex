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
    workflow_type: Optional[str] = None
    conversation_state: Optional[str] = None
    intent_analysis: Optional[Dict[str, Any]] = None
    individual_responses: Optional[List[Dict[str, Any]]] = None

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

# Orchestrator agent (manages all other agents)
orchestrator_agent = None

# Legacy conversation storage (maintained for compatibility)
conversations = {}

def get_orchestrator_agent():
    """Get or create the orchestrator agent instance"""
    global orchestrator_agent
    if orchestrator_agent is None:
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
            from orchestrator import OrchestratorAgent
            orchestrator_agent = OrchestratorAgent()
            print("✅ Orchestrator Agent initialized with all sub-agents!")
        except Exception as e:
            print(f"❌ Failed to initialize Orchestrator Agent: {e}")
            orchestrator_agent = 'failed'
    
    return orchestrator_agent if orchestrator_agent != 'failed' else None

# OrchestrationEngine replaced by OrchestratorAgent in core/orchestrator.py

# API Endpoints

@app.get("/")
@app.get("/api/")  # Handle Next.js api prefix for health check
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
@app.post("/api/api/chat", response_model=ChatResponse)  # Handle double prefix
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint - routes messages to appropriate agent
    """
    try:
        # Get orchestrator agent
        orchestrator = get_orchestrator_agent()
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator service unavailable")
        
        # Generate session/conversation ID if not provided
        session_id = request.conversation_id or f"session_{datetime.now().timestamp()}"
        
        # Process message through orchestrator (handles all routing and workflows)
        result = orchestrator.process_message(
            message=request.message,
            session_id=session_id,
            user_id=None if request.anonymous else "user"
        )
        
        response = result["response"]
        agent_used = result["agent_used"]
        conversation_id = result["session_id"]
        
        if not response:
            response = "I'm sorry, I couldn't understand your request. Please try again."
        
        # Store conversation (in production, use database)
        # Store in legacy conversation format for compatibility
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        conversations[conversation_id].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": request.message,
            "agent_response": response,
            "agent_used": agent_used
        })
        
        return ChatResponse(
            response=response,
            agent_used=agent_used,
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat(),
            workflow_type=result.get("workflow_type"),
            conversation_state=result.get("conversation_state"),
            intent_analysis=result.get("intent_analysis"),
            individual_responses=result.get("individual_responses")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")

@app.post("/api/forms/generate", response_model=DocumentResponse)
@app.post("/api/api/forms/generate", response_model=DocumentResponse)  # Handle double prefix
async def generate_document(request: DocumentRequest):
    """
    Document generation endpoint - uses Orchestrator with Scribe specialization
    """
    try:
        orchestrator = get_orchestrator_agent()
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Document generation service unavailable")
        
        # Create a document generation message
        doc_message = f"Generate a {request.document_type} document with the following information: {json.dumps(request.user_data)}"
        
        session_id = f"doc_session_{datetime.now().timestamp()}"
        result = orchestrator.process_message(doc_message, session_id)
        
        document_content = result["response"]
        
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
@app.get("/api/api/agents/status")  # Handle double prefix
async def get_agents_status():
    """
    Get status of orchestrator and all sub-agents
    """
    orchestrator = get_orchestrator_agent()
    orchestrator_status = "available" if orchestrator and orchestrator != 'failed' else "failed"
    
    return {
        "orchestrator": {
            "status": orchestrator_status,
            "description": "Central coordination agent managing all specialists"
        },
        "asha": {
            "status": orchestrator_status,  # Managed by orchestrator
            "description": "Emotional support and wellness assistant"
        },
        "athena": {
            "status": orchestrator_status,  # Managed by orchestrator
            "description": "Legal guidance and consultation assistant"
        },
        "scribe": {
            "status": orchestrator_status,  # Managed by orchestrator
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