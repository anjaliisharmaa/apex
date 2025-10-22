#!/usr/bin/env python3
"""
APEX Backend Server - Simplified FastAPI Orchestrator
=====================================================
Central server that manages ASHA, Athena, and Scribe agents
Provides REST API endpoints for the frontend application
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator
import uvicorn
import json
from passlib.context import CryptContext
from jose import JWTError, jwt
import secrets

# Load environment variables
load_dotenv()

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Import database components
from database.database import get_db, engine
from database.models import Base
from database import models
from sqlalchemy import text

app = FastAPI(
    title="APEX Legal Assistant API",
    description="Backend API for APEX - AI-Powered Legal Assistant Suite",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
        "http://localhost:3000", 
        "http://127.0.0.1:3000"
    ],
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

# Authentication Models
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None

# Authentication Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Authentication Utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_username(db: Session, username: str):
    """Get user by username from database - using email as username"""
    return db.query(models.User).filter(models.User.email == username).first()

def get_user_by_email(db: Session, email: str):
    """Get user by email from database"""
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user credentials - username can be email"""
    user = get_user_by_email(db, username)  # Try email first
    if not user:
        # If not found by email, try to find by email field directly
        user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

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
        "database": "connected",
        "agents": {
            "asha": "emotional support",
            "athena": "legal assistance", 
            "scribe": "document generation"
        }
    }

@app.get("/health")
@app.get("/api/health")  # Handle Next.js api prefix
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint that also verifies database connectivity"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "message": "All systems operational"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

@app.get("/api/test-db")
async def test_database(db: Session = Depends(get_db)):
    """Test endpoint to verify database models"""
    try:
        # Count records in main tables
        user_count = db.query(models.User).count()
        case_count = db.query(models.Case).count()
        doc_count = db.query(models.Document).count()
        
        return {
            "status": "success",
            "message": "Database models working correctly",
            "data": {
                "users": user_count,
                "cases": case_count,
                "documents": doc_count
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database query failed: {str(e)}"
        )

# Authentication Endpoints
@app.post("/api/register", response_model=UserResponse)
@app.post("/api/api/register", response_model=UserResponse)  # Handle double prefix
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        if get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = models.User(
            email=user_data.email,
            full_name=user_data.full_name or user_data.username,
            hashed_password=hashed_password,
            is_active=True,
            email_verified=False
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return UserResponse(
            id=db_user.id,
            username=db_user.email,  # Use email as username
            email=db_user.email,
            full_name=db_user.full_name,
            is_active=db_user.is_active,
            created_at=db_user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@app.post("/api/login", response_model=Token)
@app.post("/api/api/login", response_model=Token)  # Handle double prefix
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    try:
        user = authenticate_user(db, user_credentials.username, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        # Create user session record
        session = models.UserSession(
            user_id=user.id,
            session_token=access_token[:32],  # Store partial token for tracking
            ip_address="unknown",  # Can be enhanced to get real IP
            user_agent="unknown",  # Can be enhanced to get real user agent
            expires_at=datetime.utcnow() + access_token_expires,
            is_active=True
        )
        db.add(session)
        db.commit()
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@app.post("/api/logout")
async def logout_user(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logout user and invalidate session"""
    try:
        # Deactivate user sessions
        db.query(models.UserSession).filter(
            models.UserSession.user_id == current_user.id,
            models.UserSession.is_active == True
        ).update({"is_active": False})
        
        db.commit()
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )

@app.get("/api/user/profile", response_model=UserResponse)
@app.get("/api/api/user/profile", response_model=UserResponse)  # Handle double prefix
async def get_user_profile(current_user: models.User = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(
        id=current_user.id,
        username=current_user.email,  # Use email as username
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

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
    Get detailed status of orchestrator and all sub-agents
    """
    orchestrator = get_orchestrator_agent()
    
    if orchestrator and orchestrator != 'failed':
        try:
            # Get detailed status from orchestrator
            return orchestrator.get_all_agents_status()
        except Exception as e:
            print(f"Error getting detailed agent status: {e}")
            # Fallback to basic status
            pass
    
    # Fallback basic status if orchestrator not available
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