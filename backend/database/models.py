#!/usr/bin/env python3
"""
APEX Database Models
===================
SQLAlchemy models for all database tables in the APEX system
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

Base = declarative_base()

class UserRole(enum.Enum):
    EMPLOYEE = "employee"
    HR = "hr"
    ADMIN = "admin"

class CaseStatus(enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INVESTIGATION = "investigation"
    RESOLVED = "resolved"
    CLOSED = "closed"

class CaseType(enum.Enum):
    HARASSMENT = "harassment"
    DISCRIMINATION = "discrimination"
    GRIEVANCE = "grievance"
    POLICY_VIOLATION = "policy_violation"
    GENERAL = "general"

class DocumentType(enum.Enum):
    MATERNITY_LEAVE = "maternity_leave"
    TRANSFER_REQUEST = "transfer_request"
    GRIEVANCE_FORM = "grievance_form"
    LEAVE_APPLICATION = "leave_application"
    COMPLAINT_LETTER = "complaint_letter"
    OTHER = "other"

class ConversationMode(enum.Enum):
    AUTHENTICATED = "authenticated"
    ANONYMOUS = "anonymous"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    employee_id = Column(String(100), unique=True, index=True)
    department = Column(String(255))
    designation = Column(String(255))
    organization = Column(String(255))
    phone_number = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    cases = relationship("Case", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    user_sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    case_type = Column(Enum(CaseType), nullable=False)
    status = Column(Enum(CaseStatus), default=CaseStatus.DRAFT)
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    is_anonymous = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous cases
    assigned_to = Column(String(255))  # HR personnel assigned
    resolution_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True))
    due_date = Column(DateTime(timezone=True))
    
    # Additional metadata
    extra_data = Column(JSON)  # For flexible additional data
    
    # Relationships
    user = relationship("User", back_populates="cases")
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    case_updates = relationship("CaseUpdate", back_populates="case", cascade="all, delete-orphan")

class CaseUpdate(Base):
    __tablename__ = "case_updates"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    update_type = Column(String(50))  # status_change, comment, document_added, etc.
    message = Column(Text)
    old_status = Column(String(50))
    new_status = Column(String(50))
    updated_by = Column(String(255))  # User who made the update
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    case = relationship("Case", back_populates="case_updates")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255))
    document_type = Column(Enum(DocumentType), nullable=False)
    file_path = Column(String(500))  # Path to stored file
    file_size = Column(Integer)  # File size in bytes
    mime_type = Column(String(100))
    content = Column(Text)  # For generated documents
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=True)
    is_generated = Column(Boolean, default=False)  # True for AI-generated docs
    generation_prompt = Column(Text)  # Prompt used to generate document
    agent_used = Column(String(50))  # Which agent generated this
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Metadata for document generation
    form_data = Column(JSON)  # Data used to fill the form
    
    # Relationships
    user = relationship("User", back_populates="documents")
    case = relationship("Case", back_populates="documents")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous
    mode = Column(Enum(ConversationMode), default=ConversationMode.AUTHENTICATED)
    title = Column(String(255))  # Auto-generated conversation title
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))
    message_count = Column(Integer, default=0)
    agents_used = Column(JSON)  # List of agents that participated
    conversation_summary = Column(Text)  # AI-generated summary
    
    # Privacy settings
    is_anonymous = Column(Boolean, default=False)
    auto_delete_at = Column(DateTime(timezone=True))  # For anonymous conversations
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    message_type = Column(String(20))  # user, assistant, system
    content = Column(Text, nullable=False)
    agent_used = Column(String(50))  # Which agent responded (for assistant messages)
    workflow_type = Column(String(100))  # Type of workflow detected
    intent_analysis = Column(JSON)  # Intent analysis data from orchestrator
    individual_responses = Column(JSON)  # Multi-agent responses
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Message metadata
    extra_data = Column(JSON)  # For additional message data
    
    # Relationship
    conversation = relationship("Conversation", back_populates="messages")

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String(255), unique=True, index=True, nullable=False)
    refresh_token = Column(String(255), unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Relationship
    user = relationship("User", back_populates="user_sessions")

class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    value = Column(Text)
    data_type = Column(String(50))  # string, integer, boolean, json
    description = Column(Text)
    is_public = Column(Boolean, default=False)  # Can be accessed by frontend
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)  # login, document_generated, case_created, etc.
    resource_type = Column(String(50))  # user, case, document, conversation
    resource_id = Column(String(50))  # ID of the affected resource
    details = Column(JSON)  # Additional details about the action
    ip_address = Column(String(45))
    user_agent = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # For compliance and security
    severity = Column(String(20), default="info")  # info, warning, error, critical
    category = Column(String(50))  # security, data_access, system, user_action

class OTPCode(Base):
    __tablename__ = "otp_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    otp_code = Column(String(6), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)