#!/usr/bin/env python3
"""
Flask-Migrate Setup Script for News-Man Backend
This script sets up Flask-Migrate for future database migrations.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
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
    migrate = Migrate(app, db)
    
    return app, migrate

def setup_flask_migrate():
    """Set up Flask-Migrate for the application."""
    print("🚀 Setting up Flask-Migrate...")
    
    app, migrate = create_app()
    
    with app.app_context():
        try:
            # Initialize migration repository
            print("📁 Initializing migration repository...")
            init()
            print("✅ Migration repository initialized!")
            
            # Create initial migration
            print("📝 Creating initial migration...")
            migrate(message="Initial migration")
            print("✅ Initial migration created!")
            
            # Apply migration
            print("🔄 Applying migration...")
            upgrade()
            print("✅ Migration applied successfully!")
            
            print("🎉 Flask-Migrate setup completed!")
            print("\n📋 Available commands:")
            print("   - python -m flask db init          # Initialize migration repo")
            print("   - python -m flask db migrate       # Create new migration")
            print("   - python -m flask db upgrade       # Apply migrations")
            print("   - python -m flask db downgrade     # Rollback migration")
            print("   - python -m flask db current       # Show current revision")
            print("   - python -m flask db history       # Show migration history")
            
        except Exception as e:
            print(f"❌ Flask-Migrate setup failed: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 Flask-Migrate Setup Script")
    print("=" * 60)
    
    setup_flask_migrate()
    
    print("=" * 60)
