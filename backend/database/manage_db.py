#!/usr/bin/env python3
"""
Database Management CLI Tool
===========================
Command-line interface for managing the APEX database.
Provides utilities for database initialization, maintenance, and operations.
"""

import argparse
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database.database import engine, SessionLocal, init_database, create_tables, drop_tables
from database.models import Base, User, Case, Document, Conversation, Message, UserSession
from sqlalchemy import text, inspect
import json
from datetime import datetime

def check_database_health():
    """Check if database is accessible and responsive"""
    try:
        with SessionLocal() as db:
            # Test basic connectivity
            result = db.execute(text("SELECT 1")).scalar()
            if result == 1:
                print("✅ Database connectivity: OK")
                
                # Check if tables exist
                inspector = inspect(db.get_bind())
                tables = inspector.get_table_names()
                
                if tables:
                    print(f"✅ Found {len(tables)} tables: {', '.join(tables)}")
                    
                    # Count records in main tables
                    user_count = db.query(User).count()
                    case_count = db.query(Case).count()
                    doc_count = db.query(Document).count()
                    
                    print(f"📊 Records - Users: {user_count}, Cases: {case_count}, Documents: {doc_count}")
                else:
                    print("⚠️ No tables found in database")
                
                return True
            else:
                print("❌ Database query test failed")
                return False
                
    except Exception as e:
        print(f"❌ Database health check failed: {str(e)}")
        return False

def initialize_database():
    """Initialize database with tables and basic data"""
    print("🔄 Initializing APEX Database...")
    print("=" * 50)
    
    try:
        # Check connection first
        print("1. Checking database connection...")
        if not check_database_health():
            print("❌ Cannot connect to database. Please check your configuration.")
            return False
        
        # Create tables
        print("\n2. Creating database tables...")
        result = create_tables()
        if result:
            print("✅ Tables created successfully")
        else:
            print("⚠️ Tables may already exist")
        
        # Verify table creation
        print("\n3. Verifying table creation...")
        with SessionLocal() as db:
            inspector = inspect(db.get_bind())
            tables = inspector.get_table_names()
            expected_tables = ['users', 'cases', 'documents', 'conversations', 'messages', 'user_sessions', 'system_settings', 'case_updates', 'audit_logs']
            
            missing_tables = [table for table in expected_tables if table not in tables]
            if missing_tables:
                print(f"⚠️ Missing tables: {', '.join(missing_tables)}")
            else:
                print("✅ All required tables created")
        
        print("\n🎉 Database initialization completed successfully!")
        print("📝 Next steps:")
        print("   - Run 'python main.py' to start the API server")
        print("   - Visit http://localhost:8000/health to test the connection")
        print("   - Visit http://localhost:8000/docs for API documentation")
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

def create_database_tables():
    """Create all database tables"""
    try:
        print("🔄 Creating database tables...")
        result = create_tables()
        if result:
            print("✅ All tables created successfully")
        else:
            print("⚠️ Tables creation completed (some may have already existed)")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {str(e)}")
        return False

def drop_database_tables():
    """Drop all database tables"""
    print("⚠️ WARNING: This will delete all data in the database!")
    confirm = input("Are you sure you want to continue? (type 'yes' to confirm): ")
    
    if confirm.lower() == 'yes':
        try:
            print("🔄 Dropping all tables...")
            result = drop_tables()
            if result:
                print("✅ All tables dropped successfully")
            else:
                print("⚠️ Tables drop completed")
            return True
        except Exception as e:
            print(f"❌ Failed to drop tables: {str(e)}")
            return False
    else:
        print("❌ Operation cancelled")
        return False

def seed_database():
    """Add sample data to the database"""
    try:
        print("🔄 Seeding database with sample data...")
        
        with SessionLocal() as db:
            # Check if data already exists
            if db.query(User).count() > 0:
                print("⚠️ Database already contains data. Skipping seed operation.")
                return True
            
            # Create sample user
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            sample_user = User(
                username="demo_user",
                email="demo@example.com",
                full_name="Demo User",
                hashed_password=pwd_context.hash("demo123"),
                is_active=True,
                is_verified=True
            )
            
            db.add(sample_user)
            db.commit()
            db.refresh(sample_user)
            
            print("✅ Sample data added successfully")
            print("📝 Demo user created: username='demo_user', password='demo123'")
            
        return True
        
    except Exception as e:
        print(f"❌ Failed to seed database: {str(e)}")
        return False

def backup_database():
    """Create a backup of the database"""
    try:
        print("🔄 Creating database backup...")
        
        # This is a simplified backup - in production you'd use pg_dump
        backup_data = {}
        
        with SessionLocal() as db:
            # Backup users (without passwords for security)
            users = db.query(User).all()
            backup_data['users'] = [
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                }
                for user in users
            ]
            
            # Backup cases
            cases = db.query(Case).all()
            backup_data['cases'] = [
                {
                    'id': case.id,
                    'case_number': case.case_number,
                    'title': case.title,
                    'description': case.description,
                    'case_type': case.case_type.value if case.case_type else None,
                    'status': case.status.value if case.status else None,
                    'created_at': case.created_at.isoformat() if case.created_at else None
                }
                for case in cases
            ]
        
        # Save backup to file
        backup_filename = f"apex_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_filename, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)
        
        print(f"✅ Database backup created: {backup_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create backup: {str(e)}")
        return False

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="APEX Database Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_db.py init          # Initialize database
  python manage_db.py health        # Check database health
  python manage_db.py create-tables # Create all tables
  python manage_db.py seed          # Add sample data
        """
    )
    
    parser.add_argument(
        'command',
        choices=['init', 'create-tables', 'drop-tables', 'seed', 'health', 'backup'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    print("🚀 APEX Database Management Tool")
    print("=" * 40)
    
    success = False
    
    if args.command == 'init':
        success = initialize_database()
    elif args.command == 'create-tables':
        success = create_database_tables()
    elif args.command == 'drop-tables':
        success = drop_database_tables()
    elif args.command == 'seed':
        success = seed_database()
    elif args.command == 'health':
        success = check_database_health()
    elif args.command == 'backup':
        success = backup_database()
    
    if success:
        print("\n✅ Operation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Operation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()