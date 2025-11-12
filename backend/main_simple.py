#!/usr/bin/env python3
"""
APEX Backend Server - Simplified FastAPI Orchestrator
=====================================================
Central server that manages ASHA, Athena, and Scribe agents
Provides REST API endpoints for the frontend application
"""

import os
import sys
import uuid
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone
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
from database.models import Base, User
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

class OTPRequest(BaseModel):
    email: str
    password: str

class OTPVerification(BaseModel):
    email: str
    otp_code: str

class OTPResponse(BaseModel):
    message: str
    otp_sent: bool

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
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
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

# OTP Utility Functions
def generate_otp() -> str:
    """Generate a 6-digit OTP code"""
    return str(random.randint(100000, 999999))

def send_otp_email(email: str, otp_code: str) -> bool:
    """Send OTP via email (development mode - no actual email sent)"""
    try:
        # For development, just print the OTP (replace with actual email service)
        print(f"� DEVELOPMENT MODE - OTP for {email}: {otp_code}")
        print(f"� You can enter ANY 6-digit number (e.g., 123456) to proceed!")
        
        # In production, implement real email sending here:
        # smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        # smtp_server.starttls()
        # smtp_server.login(sender_email, sender_password)
        # ...
        
        return True
    except Exception as e:
        print(f"❌ Failed to send OTP email: {e}")
        return False

def store_otp(db: Session, email: str, otp_code: str) -> bool:
    """Store OTP in database"""
    try:
        # Remove any existing unused OTP for this email
        db.query(models.OTPCode).filter(
            models.OTPCode.email == email,
            models.OTPCode.is_used == False
        ).update({"is_used": True})
        
        # Create new OTP record
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)  # 5 minute expiry
        otp_record = models.OTPCode(
            email=email,
            otp_code=otp_code,
            expires_at=expires_at
        )
        db.add(otp_record)
        db.commit()
        return True
    except Exception as e:
        print(f"❌ Failed to store OTP: {e}")
        db.rollback()
        return False

def verify_otp(db: Session, email: str, otp_code: str) -> bool:
    """Verify OTP code - accepts any 6-digit code for development"""
    try:
        # For development: Accept any 6-digit OTP code
        if len(otp_code) == 6 and otp_code.isdigit():
            print(f"✅ Development mode: Accepting any 6-digit OTP for {email}")
            return True
        
        # Original OTP verification logic (commented out for development)
        # otp_record = db.query(models.OTPCode).filter(
        #     models.OTPCode.email == email,
        #     models.OTPCode.otp_code == otp_code,
        #     models.OTPCode.is_used == False,
        #     models.OTPCode.expires_at > datetime.now(timezone.utc)
        # ).first()
        # 
        # if not otp_record:
        #     return False
        # 
        # # Increment attempts
        # otp_record.attempts += 1
        # 
        # # Check if max attempts exceeded
        # if otp_record.attempts >= otp_record.max_attempts:
        #     otp_record.is_used = True
        #     db.commit()
        #     return False
        # 
        # # Mark as used if verification successful
        # otp_record.is_used = True
        # db.commit()
        # return True
        
        return False
        
    except Exception as e:
        print(f"❌ Failed to verify OTP: {e}")
        db.rollback()
        return False

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

@app.post("/api/request-otp", response_model=OTPResponse)
@app.post("/api/api/request-otp", response_model=OTPResponse)  # Handle double prefix
async def request_otp(otp_request: OTPRequest, db: Session = Depends(get_db)):
    """Request OTP for login - validates credentials first"""
    try:
        # First authenticate the user credentials
        user = authenticate_user(db, otp_request.email, otp_request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account"
            )
        
        # Generate and send OTP
        otp_code = generate_otp()
        
        # Store OTP in database
        if not store_otp(db, otp_request.email, otp_code):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate OTP. Please try again."
            )
        
        # Send OTP via email
        if not send_otp_email(otp_request.email, otp_code):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP. Please try again."
            )
        
        return OTPResponse(
            message="OTP sent successfully to your email",
            otp_sent=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OTP request failed: {str(e)}"
        )

@app.post("/api/verify-otp", response_model=Token)
@app.post("/api/api/verify-otp", response_model=Token)  # Handle double prefix
async def verify_otp_and_login(otp_verification: OTPVerification, db: Session = Depends(get_db)):
    """Verify OTP and return JWT token"""
    try:
        # Verify OTP code
        if not verify_otp(db, otp_verification.email, otp_verification.otp_code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired OTP code",
            )
        
        # Get user by email
        user = get_user_by_email(db, otp_verification.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
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
        
        # Clean up old sessions for this user
        db.query(models.UserSession).filter(
            models.UserSession.user_id == user.id,
            models.UserSession.is_active == True
        ).update({"is_active": False})
        db.commit()
        
        # Create user session record with unique session token
        unique_session_token = f"{access_token[:24]}_{str(uuid.uuid4())[:8]}"
        session = models.UserSession(
            user_id=user.id,
            session_token=unique_session_token,
            ip_address="unknown",
            user_agent="unknown",
            expires_at=datetime.now(timezone.utc) + access_token_expires,
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
            detail=f"OTP verification failed: {str(e)}"
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
        
        # Clean up old sessions for this user
        db.query(models.UserSession).filter(
            models.UserSession.user_id == user.id,
            models.UserSession.is_active == True
        ).update({"is_active": False})
        db.commit()
        
        # Create user session record with unique session token
        unique_session_token = f"{access_token[:24]}_{str(uuid.uuid4())[:8]}"
        session = models.UserSession(
            user_id=user.id,
            session_token=unique_session_token,  # Use unique token
            ip_address="unknown",  # Can be enhanced to get real IP
            user_agent="unknown",  # Can be enhanced to get real user agent
            expires_at=datetime.now(timezone.utc) + access_token_expires,
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
            status="approved",
            created_at="2024-01-15",
            last_updated="2024-01-20"
        ),
        CaseInfo(
            id="case_002", 
            title="Spouse Ground Transfer Request",
            description="Request for transfer to Delhi office due to spouse's job relocation",
            status="under-review",
            created_at="2024-01-02",
            last_updated="2024-02-10"
        ),
        CaseInfo(
            id="case_003",
            title="Workplace Harassment Complaint", 
            description="Formal complaint regarding inappropriate behavior and harassment",
            status="additional-info-required",
            created_at="2024-02-15",
            last_updated="2024-02-25"
        ),
        CaseInfo(
            id="case_004",
            title="Child Care Leave Application",
            description="Application for child care leave to take care of newborn child",
            status="submitted",
            created_at="2024-03-01",
            last_updated="2024-03-01"
        ),
        CaseInfo(
            id="case_005",
            title="Medical Ground Transfer",
            description="Draft application for medical ground transfer due to health condition",
            status="draft",
            created_at="2024-03-05",
            last_updated="2024-03-05"
        )
    ]

@app.get("/api/cases/{case_id}")
async def get_case_by_id(case_id: str):
    """
    Get detailed information for a specific case by ID
    """
    # Mock case data - each case has unique details
    case_data = {
        "case_001": {
            "id": "case_001",
            "referenceNumber": "ML-2024-001",
            "title": "Maternity Leave Application",
            "type": "Leave Application",
            "status": "approved",
            "createdDate": "2024-01-15",
            "lastUpdate": "2024-01-20",
            "description": "Application for maternity leave for 26 weeks starting from February 1, 2024, as per the Maternity Benefits Act.",
            "submittedBy": "Dr. Priya Sharma",
            "assignedTo": "HR Department - Mrs. Anjali Gupta",
            "department": "Human Resources",
            "priority": "high",
            "comments": "Medical certificate attached. Expected delivery date: February 15, 2024.",
            "timeline": [
                {
                    "id": "1",
                    "title": "Application Submitted",
                    "description": "Maternity leave application submitted with all required documents",
                    "timestamp": "2024-01-15T09:00:00",
                    "type": "submitted",
                    "user": "Dr. Priya Sharma"
                },
                {
                    "id": "2",
                    "title": "Under Review",
                    "description": "Application forwarded to HR department for review",
                    "timestamp": "2024-01-16T10:30:00",
                    "type": "update",
                    "user": "System"
                },
                {
                    "id": "3",
                    "title": "Medical Certificate Verified",
                    "description": "Medical certificate verified by medical officer",
                    "timestamp": "2024-01-18T14:15:00",
                    "type": "update",
                    "user": "Dr. Rajesh Kumar (Medical Officer)"
                },
                {
                    "id": "4",
                    "title": "Application Approved",
                    "description": "Maternity leave approved for 26 weeks starting February 1, 2024",
                    "timestamp": "2024-01-20T11:45:00",
                    "type": "approved",
                    "user": "Mrs. Anjali Gupta (HR)"
                }
            ],
            "documents": [
                {
                    "id": "1",
                    "name": "Maternity_Leave_Application.pdf",
                    "type": "PDF",
                    "size": "245 KB",
                    "uploadDate": "2024-01-15"
                },
                {
                    "id": "2",
                    "name": "Medical_Certificate.pdf",
                    "type": "PDF",
                    "size": "180 KB",
                    "uploadDate": "2024-01-15"
                },
                {
                    "id": "3",
                    "name": "Approval_Letter.pdf",
                    "type": "PDF",
                    "size": "156 KB",
                    "uploadDate": "2024-01-20"
                }
            ]
        },
        "case_002": {
            "id": "case_002",
            "referenceNumber": "TR-2024-001",
            "title": "Spouse Ground Transfer Request",
            "type": "Transfer Request",
            "status": "under-review",
            "createdDate": "2024-01-02",
            "lastUpdate": "2024-02-10",
            "description": "Request for transfer to Delhi office due to spouse's job relocation. Current position: Senior Software Engineer, Mumbai office.",
            "submittedBy": "Mr. Rahul Verma",
            "assignedTo": "HR Transfer Committee - Mr. Suresh Kumar",
            "department": "Human Resources",
            "priority": "medium",
            "comments": "Spouse employment letter and marriage certificate provided. Transfer subject to position availability in Delhi office.",
            "timeline": [
                {
                    "id": "1",
                    "title": "Transfer Request Submitted",
                    "description": "Employee submitted transfer request with supporting documents",
                    "timestamp": "2024-01-02T14:30:00",
                    "type": "submitted",
                    "user": "Mr. Rahul Verma"
                },
                {
                    "id": "2",
                    "title": "Initial Review",
                    "description": "HR department initiated preliminary review of transfer request",
                    "timestamp": "2024-01-05T10:15:00",
                    "type": "update",
                    "user": "HR Department"
                },
                {
                    "id": "3",
                    "title": "Documentation Verified",
                    "description": "All supporting documents verified and found to be in order",
                    "timestamp": "2024-01-12T16:20:00",
                    "type": "update",
                    "user": "Ms. Priti Singh (HR Executive)"
                },
                {
                    "id": "4",
                    "title": "Position Availability Check",
                    "description": "Checking for suitable positions in Delhi office",
                    "timestamp": "2024-02-01T09:45:00",
                    "type": "update",
                    "user": "Mr. Suresh Kumar (Transfer Committee)"
                },
                {
                    "id": "5",
                    "title": "Interview Scheduled",
                    "description": "Interview scheduled with Delhi office team lead for February 15, 2024",
                    "timestamp": "2024-02-10T11:30:00",
                    "type": "update",
                    "user": "Delhi Office HR"
                }
            ],
            "documents": [
                {
                    "id": "1",
                    "name": "Transfer_Request_Form.pdf",
                    "type": "PDF",
                    "size": "198 KB",
                    "uploadDate": "2024-01-02"
                },
                {
                    "id": "2",
                    "name": "Spouse_Employment_Letter.pdf",
                    "type": "PDF",
                    "size": "156 KB",
                    "uploadDate": "2024-01-02"
                },
                {
                    "id": "3",
                    "name": "Marriage_Certificate.pdf",
                    "type": "PDF",
                    "size": "234 KB",
                    "uploadDate": "2024-01-02"
                },
                {
                    "id": "4",
                    "name": "Performance_Review_2023.pdf",
                    "type": "PDF",
                    "size": "289 KB",
                    "uploadDate": "2024-01-05"
                }
            ]
        },
        "case_003": {
            "id": "case_003",
            "referenceNumber": "GR-2024-001",
            "title": "Workplace Harassment Complaint",
            "type": "Grievance",
            "status": "additional-info-required",
            "createdDate": "2024-02-15",
            "lastUpdate": "2024-02-25",
            "description": "Formal complaint regarding inappropriate behavior and harassment by a senior colleague. Seeking immediate investigation and resolution.",
            "submittedBy": "Ms. Kavya Patel",
            "assignedTo": "Internal Complaints Committee - Ms. Neha Shah",
            "department": "Legal & Compliance",
            "priority": "high",
            "comments": "Confidential complaint filed. Additional witness statements required to proceed with investigation.",
            "timeline": [
                {
                    "id": "1",
                    "title": "Complaint Filed",
                    "description": "Formal harassment complaint submitted to Internal Complaints Committee",
                    "timestamp": "2024-02-15T11:15:00",
                    "type": "submitted",
                    "user": "Ms. Kavya Patel"
                },
                {
                    "id": "2",
                    "title": "Complaint Acknowledged",
                    "description": "ICC acknowledged receipt and assigned case reference number",
                    "timestamp": "2024-02-16T09:30:00",
                    "type": "update",
                    "user": "Ms. Neha Shah (ICC Chairperson)"
                },
                {
                    "id": "3",
                    "title": "Initial Assessment",
                    "description": "Initial assessment completed, case marked for detailed investigation",
                    "timestamp": "2024-02-20T14:45:00",
                    "type": "update",
                    "user": "Internal Complaints Committee"
                },
                {
                    "id": "4",
                    "title": "Additional Information Requested",
                    "description": "Committee requested additional witness statements and evidence",
                    "timestamp": "2024-02-25T10:20:00",
                    "type": "info-required",
                    "user": "Ms. Neha Shah (ICC)"
                }
            ],
            "documents": [
                {
                    "id": "1",
                    "name": "Harassment_Complaint_Form.pdf",
                    "type": "PDF",
                    "size": "267 KB",
                    "uploadDate": "2024-02-15"
                },
                {
                    "id": "2",
                    "name": "Incident_Documentation.pdf",
                    "type": "PDF",
                    "size": "423 KB",
                    "uploadDate": "2024-02-15"
                },
                {
                    "id": "3",
                    "name": "Email_Evidence.pdf",
                    "type": "PDF",
                    "size": "187 KB",
                    "uploadDate": "2024-02-18"
                }
            ]
        },
        "case_004": {
            "id": "case_004",
            "referenceNumber": "CCL-2024-001",
            "title": "Child Care Leave Application",
            "type": "Leave Application",
            "status": "submitted",
            "createdDate": "2024-03-01",
            "lastUpdate": "2024-03-01",
            "description": "Application for child care leave to take care of newborn child as per company policy. Requesting 6 months leave starting from March 15, 2024.",
            "submittedBy": "Mr. Amit Sharma",
            "assignedTo": "HR Department - Mrs. Anjali Gupta",
            "department": "Human Resources",
            "priority": "medium",
            "comments": "Child birth certificate and medical documents submitted. Leave application under review.",
            "timeline": [
                {
                    "id": "1",
                    "title": "Application Submitted",
                    "description": "Child care leave application submitted with required documents",
                    "timestamp": "2024-03-01T10:45:00",
                    "type": "submitted",
                    "user": "Mr. Amit Sharma"
                }
            ],
            "documents": [
                {
                    "id": "1",
                    "name": "Childcare_Leave_Application.pdf",
                    "type": "PDF",
                    "size": "213 KB",
                    "uploadDate": "2024-03-01"
                },
                {
                    "id": "2",
                    "name": "Birth_Certificate.pdf",
                    "type": "PDF",
                    "size": "165 KB",
                    "uploadDate": "2024-03-01"
                },
                {
                    "id": "3",
                    "name": "Medical_Records.pdf",
                    "type": "PDF",
                    "size": "298 KB",
                    "uploadDate": "2024-03-01"
                }
            ]
        },
        "case_005": {
            "id": "case_005",
            "referenceNumber": "DRAFT-001",
            "title": "Medical Ground Transfer",
            "type": "Transfer Request",
            "status": "draft",
            "createdDate": "2024-03-05",
            "lastUpdate": "2024-03-05",
            "description": "Draft application for medical ground transfer due to health condition requiring specific climate and medical facilities available in Bangalore office.",
            "submittedBy": "Dr. Sarah Khan",
            "assignedTo": "Not Assigned",
            "department": "Pending Submission",
            "priority": "low",
            "comments": "Draft application saved. Medical reports and specialist recommendations pending attachment.",
            "timeline": [
                {
                    "id": "1",
                    "title": "Draft Created",
                    "description": "Transfer request draft created and saved",
                    "timestamp": "2024-03-05T16:30:00",
                    "type": "submitted",
                    "user": "Dr. Sarah Khan"
                }
            ],
            "documents": [
                {
                    "id": "1",
                    "name": "Draft_Transfer_Application.pdf",
                    "type": "PDF",
                    "size": "142 KB",
                    "uploadDate": "2024-03-05"
                }
            ]
        }
    }
    
    if case_id not in case_data:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return case_data[case_id]

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

# Performance Control Models
class PerformanceSettings(BaseModel):
    fast_mode: Optional[bool] = True
    single_agent_preference: Optional[bool] = True

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

@app.post("/api/agents/performance")
@app.post("/api/api/agents/performance")  # Handle double prefix
async def set_performance_mode(settings: PerformanceSettings):
    """
    Configure agent performance settings for faster responses
    """
    orchestrator = get_orchestrator_agent()
    
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator service unavailable")
    
    try:
        orchestrator.set_performance_mode(
            fast_mode=settings.fast_mode,
            single_agent_preference=settings.single_agent_preference
        )
        
        # Get updated stats
        stats = orchestrator.get_performance_stats()
        
        return {
            "message": "Performance settings updated successfully",
            "settings": {
                "fast_mode": stats["fast_mode"],
                "single_agent_preference": stats["single_agent_preference"]
            },
            "stats": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update performance settings: {str(e)}")

@app.get("/api/agents/performance")
@app.get("/api/api/agents/performance")  # Handle double prefix
async def get_performance_stats():
    """
    Get current performance statistics and settings
    """
    orchestrator = get_orchestrator_agent()
    
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator service unavailable")
    
    try:
        stats = orchestrator.get_performance_stats()
        return {
            "status": "success",
            "performance_stats": stats,
            "recommendations": {
                "fast_mode": "Enable for responses under 10 seconds",
                "single_agent_preference": "Enable to avoid multi-agent delays", 
                "cache_usage": f"Cache hit rate: {stats['cache_hits']} hits"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance stats: {str(e)}")

@app.post("/api/agents/cache/clear")
@app.post("/api/api/agents/cache/clear")  # Handle double prefix
async def clear_agent_cache():
    """
    Clear response cache to free memory
    """
    orchestrator = get_orchestrator_agent()
    
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator service unavailable")
    
    try:
        orchestrator.clear_cache()
        return {"message": "Agent cache cleared successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")

@app.post("/api/agents/cache/regenerate")
@app.post("/api/api/agents/cache/regenerate")  # Handle double prefix
async def regenerate_agent_cache():
    """
    Regenerate embeddings cache for faster startup
    """
    orchestrator = get_orchestrator_agent()
    
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator service unavailable")
    
    try:
        # Get Athena agent and regenerate cache
        athena = orchestrator._get_athena_agent()
        if athena and hasattr(athena, 'regenerate_cache'):
            result = athena.regenerate_cache()
            return {
                "message": "Agent cache regenerated successfully",
                "result": result
            }
        else:
            return {"message": "Cache regeneration not available"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to regenerate cache: {str(e)}")

@app.get("/api/agents/cache/info")
@app.get("/api/api/agents/cache/info")  # Handle double prefix
async def get_cache_info():
    """
    Get detailed cache information
    """
    orchestrator = get_orchestrator_agent()
    
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator service unavailable")
    
    try:
        # Get cache info from all agents
        cache_info = {}
        
        # Athena cache info
        athena = orchestrator._get_athena_agent()
        if athena and hasattr(athena, 'get_status'):
            athena_status = athena.get_status()
            cache_info["athena"] = athena_status.get("cache", {})
        
        # Orchestrator cache info
        orchestrator_stats = orchestrator.get_performance_stats()
        cache_info["orchestrator"] = {
            "response_cache_size": orchestrator_stats.get("cache_size", 0),
            "cache_hits": orchestrator_stats.get("cache_hits", 0)
        }
        
        return {
            "status": "success",
            "cache_info": cache_info,
            "recommendations": [
                "Regenerate cache when documents are updated",
                "Clear response cache periodically to free memory",
                "Monitor cache hit rates for optimization"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cache info: {str(e)}")

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    Get conversation history
    """
    if conversation_id in conversations:
        return conversations[conversation_id]
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")

@app.get("/api/upload")
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

# Admin Dashboard APIs

@app.get("/api/admin/stats")
@app.get("/api/api/admin/stats")  # Handle double prefix
async def get_admin_stats(current_user: User = Depends(get_current_user)):
    """
    Get admin dashboard statistics
    """
    try:
        # For now, return mock stats. In production, query actual database
        stats = {
            "total_cases": 147,
            "total_pending": 23,
            "total_approved": 89,
            "total_rejected": 35,
            "new_today": 8,
            "active_users": 342,
            "avg_response_time": 8.3,
            "success_rate": 87.2
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.get("/api/admin/cases")
@app.get("/api/api/admin/cases")  # Handle double prefix
async def get_all_cases(
    status: str = None,
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(get_current_user)
):
    """
    Get all cases for admin dashboard
    """
    try:
        # Mock case data - in production, query from database
        mock_cases = [
            {
                "id": "CASE-2024-001",
                "user_name": "Sarah Johnson",
                "user_email": "sarah.j@company.com",
                "case_type": "Maternity Leave",
                "title": "Maternity Leave Application",
                "submitted_date": "2024-11-12",
                "status": "pending",
                "priority": "high",
                "description": "Requesting 12 weeks maternity leave starting December 15, 2024.",
                "department": "Engineering",
                "created_at": "2024-11-12T09:15:00Z",
                "updated_at": "2024-11-12T09:15:00Z"
            },
            {
                "id": "CASE-2024-002",
                "user_name": "Michael Chen",
                "user_email": "michael.c@company.com",
                "case_type": "Transfer Request",
                "title": "Department Transfer Request",
                "submitted_date": "2024-11-11",
                "status": "approved",
                "priority": "medium",
                "description": "Request to transfer from Marketing to Product Management.",
                "department": "Marketing",
                "created_at": "2024-11-11T14:30:00Z",
                "updated_at": "2024-11-12T10:45:00Z"
            },
            {
                "id": "CASE-2024-003",
                "user_name": "Emily Davis",
                "user_email": "emily.d@company.com",
                "case_type": "Harassment Report",
                "title": "Workplace Harassment Complaint",
                "submitted_date": "2024-11-10",
                "status": "under_review",
                "priority": "high",
                "description": "Formal complaint regarding inappropriate behavior from supervisor.",
                "department": "Sales",
                "created_at": "2024-11-10T16:20:00Z",
                "updated_at": "2024-11-11T11:30:00Z"
            },
            {
                "id": "CASE-2024-004",
                "user_name": "David Wilson",
                "user_email": "david.w@company.com",
                "case_type": "Policy Query",
                "title": "Remote Work Policy Clarification",
                "submitted_date": "2024-11-09",
                "status": "approved",
                "priority": "low",
                "description": "Request for clarification on hybrid work schedule policy.",
                "department": "Finance",
                "created_at": "2024-11-09T13:45:00Z",
                "updated_at": "2024-11-10T09:15:00Z"
            },
            {
                "id": "CASE-2024-005",
                "user_name": "Lisa Rodriguez",
                "user_email": "lisa.r@company.com",
                "case_type": "Leave Request",
                "title": "Extended Medical Leave",
                "submitted_date": "2024-11-08",
                "status": "rejected",
                "priority": "medium",
                "description": "Request for 6 months medical leave due to surgery.",
                "department": "HR",
                "created_at": "2024-11-08T10:20:00Z",
                "updated_at": "2024-11-09T15:30:00Z"
            },
            {
                "id": "CASE-2024-006",
                "user_name": "James Brown",
                "user_email": "james.b@company.com",
                "case_type": "Salary Review",
                "title": "Annual Salary Review Request",
                "submitted_date": "2024-11-12",
                "status": "pending",
                "priority": "medium",
                "description": "Request for performance-based salary increase review.",
                "department": "Operations",
                "created_at": "2024-11-12T11:00:00Z",
                "updated_at": "2024-11-12T11:00:00Z"
            }
        ]
        
        # Filter by status if provided
        if status and status != "all":
            filtered_cases = [case for case in mock_cases if case["status"] == status]
        else:
            filtered_cases = mock_cases
        
        # Apply pagination
        paginated_cases = filtered_cases[offset:offset + limit]
        
        return {
            "cases": paginated_cases,
            "total": len(filtered_cases),
            "has_more": len(filtered_cases) > offset + limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cases: {str(e)}")

@app.put("/api/admin/cases/{case_id}/status")
@app.put("/api/api/admin/cases/{case_id}/status")  # Handle double prefix
async def update_case_status(
    case_id: str,
    status_data: dict,
    current_user: User = Depends(get_current_user)
):
    """
    Update case status
    """
    try:
        new_status = status_data.get("status")
        notes = status_data.get("notes", "")
        
        if new_status not in ["pending", "approved", "rejected", "under_review"]:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        # In production, update the database
        # For now, return success response
        return {
            "message": f"Case {case_id} status updated to {new_status}",
            "case_id": case_id,
            "new_status": new_status,
            "updated_by": current_user.username,
            "updated_at": "2024-11-12T12:00:00Z",
            "notes": notes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update case: {str(e)}")

@app.get("/api/admin/cases/{case_id}")
@app.get("/api/api/admin/cases/{case_id}")  # Handle double prefix
async def get_case_details(
    case_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed information for a specific case
    """
    try:
        # Mock detailed case data - in production, query from database
        case_details = {
            "id": case_id,
            "user_name": "Sarah Johnson",
            "user_email": "sarah.j@company.com",
            "case_type": "Maternity Leave",
            "title": "Maternity Leave Application",
            "submitted_date": "2024-11-12",
            "status": "pending",
            "priority": "high",
            "description": "Requesting 12 weeks maternity leave starting December 15, 2024. This is a standard maternity leave request following company policy guidelines.",
            "department": "Engineering",
            "created_at": "2024-11-12T09:15:00Z",
            "updated_at": "2024-11-12T09:15:00Z",
            "attachments": [
                {
                    "filename": "maternity_leave_form.pdf",
                    "size": 245632,
                    "uploaded_at": "2024-11-12T09:15:00Z"
                },
                {
                    "filename": "doctor_certificate.pdf",
                    "size": 156482,
                    "uploaded_at": "2024-11-12T09:16:00Z"
                }
            ],
            "history": [
                {
                    "action": "Case submitted",
                    "timestamp": "2024-11-12T09:15:00Z",
                    "user": "sarah.j@company.com",
                    "notes": "Initial submission"
                },
                {
                    "action": "Documents uploaded",
                    "timestamp": "2024-11-12T09:16:00Z",
                    "user": "sarah.j@company.com",
                    "notes": "Medical certificate and form attached"
                }
            ]
        }
        
        return case_details
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get case details: {str(e)}")

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