#!/usr/bin/env python3
"""
Database Migration Script for News-Man Backend
This script creates the necessary database tables for the application.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from flask import Flask
from extensions import db
from app.models.articles_model import Article

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SUPABASE_DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    db.init_app(app)
    
    return app

def run_migration():
    """Run the database migration."""
    print("🚀 Starting database migration...")
    
    # Create the Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Test database connection
            print("📡 Testing database connection...")
            db.session.execute(db.text('SELECT 1'))
            print("✅ Database connection successful!")
            
            # Create all tables
            print("🏗️  Creating database tables...")
            db.create_all()
            print("✅ All tables created successfully!")
            
            # List created tables
            print("\n📋 Created tables:")
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            for table in tables:
                print(f"   - {table}")
            
            print(f"\n🎉 Migration completed successfully! {len(tables)} table(s) created.")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
    
    return True

def check_tables():
    """Check existing tables in the database."""
    print("🔍 Checking existing database tables...")
    
    app = create_app()
    
    with app.app_context():
        try:
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"📋 Found {len(tables)} existing table(s):")
                for table in tables:
                    print(f"   - {table}")
            else:
                print("📋 No tables found in the database.")
                
            return tables
            
        except Exception as e:
            print(f"❌ Error checking tables: {e}")
            return []

def drop_tables():
    """Drop all tables (use with caution!)."""
    print("⚠️  WARNING: This will drop ALL tables in the database!")
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("❌ Operation cancelled.")
        return False
    
    app = create_app()
    
    with app.app_context():
        try:
            print("🗑️  Dropping all tables...")
            db.drop_all()
            print("✅ All tables dropped successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error dropping tables: {e}")
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("🗄️  News-Man Database Migration Script")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "check":
            check_tables()
        elif command == "drop":
            drop_tables()
        elif command == "migrate":
            run_migration()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: check, drop, migrate")
    else:
        # Default action: run migration
        run_migration()
    
    print("=" * 60)
