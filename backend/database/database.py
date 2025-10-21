#!/usr/bin/env python3
"""
APEX Database Configuration
==========================
Database connection, session management, and utility functions
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv
from typing import Generator
import logging

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/apex_db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=os.getenv("DATABASE_ECHO", "false").lower() == "true",  # Log SQL queries in dev
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Database dependency for FastAPI
def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session for FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logging.error(f"Database session error: {e}")
        raise
    finally:
        db.close()

# Database utility functions
def create_tables():
    """
    Create all database tables
    """
    from .models import Base
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables created successfully")

def drop_tables():
    """
    Drop all database tables (use with caution!)
    """
    from .models import Base
    Base.metadata.drop_all(bind=engine)
    logging.warning("All database tables dropped")

def init_database():
    """
    Initialize database with tables and seed data
    """
    create_tables()
    seed_initial_data()

def seed_initial_data():
    """
    Seed database with initial system data
    """
    from .models import SystemSettings, UserRole
    
    db = SessionLocal()
    try:
        # Check if system is already initialized
        existing_setting = db.query(SystemSettings).filter(
            SystemSettings.key == "system_initialized"
        ).first()
        
        if existing_setting:
            logging.info("Database already initialized")
            return
        
        # Add initial system settings
        initial_settings = [
            SystemSettings(
                key="system_initialized",
                value="true",
                data_type="boolean",
                description="System initialization flag",
                is_public=False
            ),
            SystemSettings(
                key="app_name",
                value="APEX - AI Legal Assistant",
                data_type="string",
                description="Application name",
                is_public=True
            ),
            SystemSettings(
                key="app_version",
                value="1.0.0",
                data_type="string",
                description="Application version",
                is_public=True
            ),
            SystemSettings(
                key="max_anonymous_sessions",
                value="1000",
                data_type="integer",
                description="Maximum number of concurrent anonymous sessions",
                is_public=False
            ),
            SystemSettings(
                key="conversation_retention_days",
                value="90",
                data_type="integer",
                description="Number of days to retain conversation data",
                is_public=False
            ),
            SystemSettings(
                key="anonymous_conversation_retention_hours",
                value="24",
                data_type="integer",
                description="Number of hours to retain anonymous conversations",
                is_public=False
            ),
        ]
        
        for setting in initial_settings:
            db.add(setting)
        
        db.commit()
        logging.info("Initial system data seeded successfully")
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error seeding initial data: {e}")
        raise
    finally:
        db.close()

# Database health check
def check_database_health() -> dict:
    """
    Check database connectivity and return health status
    """
    try:
        db = SessionLocal()
        # Try a simple query
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2025-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "connection_failed",
            "error": str(e),
            "timestamp": "2025-01-01T00:00:00Z"
        }

# Database migration utilities
def backup_database(backup_path: str = None):
    """
    Create database backup (placeholder for production implementation)
    """
    if not backup_path:
        from datetime import datetime
        backup_path = f"backup_apex_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    # In production, implement actual backup logic here
    logging.info(f"Database backup would be created at: {backup_path}")
    return backup_path

# Context manager for database transactions
class DatabaseTransaction:
    """
    Context manager for database transactions with automatic rollback
    """
    def __init__(self):
        self.db = None
    
    def __enter__(self):
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
            logging.error(f"Transaction rolled back due to: {exc_val}")
        else:
            self.db.commit()
        self.db.close()