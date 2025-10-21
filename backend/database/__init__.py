#!/usr/bin/env python3
"""
APEX Database Package
====================
Database models, connections, and utilities for the APEX system
"""

from .database import (
    engine,
    SessionLocal, 
    get_db,
    create_tables,
    drop_tables,
    init_database,
    check_database_health,
    DatabaseTransaction
)

from .models import (
    Base,
    User,
    Case,
    CaseUpdate,
    Document,
    Conversation,
    Message,
    UserSession,
    SystemSettings,
    AuditLog,
    UserRole,
    CaseStatus,
    CaseType,
    DocumentType,
    ConversationMode
)

__all__ = [
    # Database connections
    "engine",
    "SessionLocal",
    "get_db",
    "DatabaseTransaction",
    
    # Database functions
    "create_tables",
    "drop_tables", 
    "init_database",
    "check_database_health",
    
    # Models
    "Base",
    "User",
    "Case", 
    "CaseUpdate",
    "Document",
    "Conversation",
    "Message",
    "UserSession",
    "SystemSettings",
    "AuditLog",
    
    # Enums
    "UserRole",
    "CaseStatus",
    "CaseType", 
    "DocumentType",
    "ConversationMode"
]