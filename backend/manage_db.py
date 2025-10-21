#!/usr/bin/env python3
"""
Database management script for APEX
Provides utilities for database operations
"""

import argparse
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from database.database import (
    init_database, 
    create_tables, 
    drop_tables, 
    check_database_health,
    backup_database,
    seed_initial_data
)
import logging

logging.basicConfig(level=logging.INFO)

def cmd_init(args):
    """Initialize database with tables and seed data"""
    print("🚀 Initializing database...")
    init_database()
    print("✅ Database initialized successfully!")

def cmd_create_tables(args):
    """Create all database tables"""
    print("📊 Creating database tables...")
    create_tables()
    print("✅ Tables created successfully!")

def cmd_drop_tables(args):
    """Drop all database tables"""
    if not args.force:
        confirm = input("⚠️  This will DELETE ALL DATA. Are you sure? (type 'yes'): ")
        if confirm.lower() != 'yes':
            print("❌ Operation cancelled")
            return
    
    print("🗑️  Dropping all tables...")
    drop_tables()
    print("✅ Tables dropped successfully!")

def cmd_seed(args):
    """Seed database with initial data"""
    print("🌱 Seeding initial data...")
    seed_initial_data()
    print("✅ Initial data seeded successfully!")

def cmd_health(args):
    """Check database health"""
    print("🔍 Checking database health...")
    health = check_database_health()
    
    if health["status"] == "healthy":
        print("✅ Database is healthy!")
        print(f"   Status: {health['status']}")
        print(f"   Connection: {health['database']}")
    else:
        print("❌ Database is unhealthy!")
        print(f"   Status: {health['status']}")
        print(f"   Error: {health.get('error', 'Unknown error')}")

def cmd_backup(args):
    """Create database backup"""
    print("💾 Creating database backup...")
    backup_path = backup_database(args.path)
    print(f"✅ Backup created: {backup_path}")

def main():
    parser = argparse.ArgumentParser(description="APEX Database Management")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize database')
    init_parser.set_defaults(func=cmd_init)
    
    # Create tables command
    create_parser = subparsers.add_parser('create-tables', help='Create all tables')
    create_parser.set_defaults(func=cmd_create_tables)
    
    # Drop tables command
    drop_parser = subparsers.add_parser('drop-tables', help='Drop all tables')
    drop_parser.add_argument('--force', action='store_true', help='Skip confirmation')
    drop_parser.set_defaults(func=cmd_drop_tables)
    
    # Seed command
    seed_parser = subparsers.add_parser('seed', help='Seed initial data')
    seed_parser.set_defaults(func=cmd_seed)
    
    # Health check command
    health_parser = subparsers.add_parser('health', help='Check database health')
    health_parser.set_defaults(func=cmd_health)
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create database backup')
    backup_parser.add_argument('--path', help='Backup file path')
    backup_parser.set_defaults(func=cmd_backup)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        args.func(args)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())