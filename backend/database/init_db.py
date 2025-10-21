#!/usr/bin/env python3
"""
Database initialization script for APEX
Run this script to set up the database schema and initial data
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from database.database import init_database, check_database_health, engine
from database.models import Base
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """
    Main function to initialize the database
    """
    print("🚀 APEX Database Initialization")
    print("================================")
    
    # Check database connection
    print("🔍 Checking database connection...")
    health = check_database_health()
    
    if health["status"] != "healthy":
        print(f"❌ Database connection failed: {health.get('error', 'Unknown error')}")
        print("Please check your DATABASE_URL in the .env file")
        return 1
    
    print("✅ Database connection successful!")
    
    # Create tables
    print("📊 Creating database tables...")
    try:
        init_database()
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return 1
    
    # Verify tables were created
    print("🔍 Verifying table creation...")
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = [
            'users', 'cases', 'case_updates', 'documents', 
            'conversations', 'messages', 'user_sessions', 
            'system_settings', 'audit_logs'
        ]
        
        created_tables = [table for table in expected_tables if table in tables]
        
        print(f"✅ Created {len(created_tables)}/{len(expected_tables)} tables:")
        for table in created_tables:
            print(f"   📋 {table}")
        
        if len(created_tables) != len(expected_tables):
            missing = set(expected_tables) - set(created_tables)
            print(f"⚠️  Missing tables: {missing}")
            
    except Exception as e:
        print(f"⚠️  Error verifying tables: {e}")
    
    print("\n🎉 Database initialization complete!")
    print("You can now start the APEX backend server.")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)