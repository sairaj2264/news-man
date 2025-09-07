#!/usr/bin/env python3
"""
Test script to verify database connection and tables
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
from app.models.articles_model import Article, article_categories
from app.models.user_model import User
from app.models.category_model import Category
from app.models.user_category_join_table import user_categories
from sqlalchemy import text

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SUPABASE_DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    db.init_app(app)
    
    return app

def test_database():
    """Test database connection and tables."""
    print("🧪 Testing database connection and tables...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test basic connection
            print("📡 Testing database connection...")
            db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful!")
            
            # Test articles table
            print("📋 Testing articles table...")
            result = db.session.execute(text('SELECT COUNT(*) FROM articles'))
            count = result.scalar()
            print(f"✅ Articles table exists and has {count} records")
            
            # Test users table
            print("📋 Testing users table...")
            result = db.session.execute(text('SELECT COUNT(*) FROM users'))
            count = result.scalar()
            print(f"✅ Users table exists and has {count} records")
            
            # Test categories table
            print("📋 Testing categories table...")
            result = db.session.execute(text('SELECT COUNT(*) FROM categories'))
            count = result.scalar()
            print(f"✅ Categories table exists and has {count} records")
            
            # Test join tables
            print("📋 Testing join tables...")
            try:
                result = db.session.execute(text('SELECT COUNT(*) FROM article_categories'))
                count = result.scalar()
                print(f"✅ article_categories join table exists and has {count} records")
            except Exception as e:
                print(f"⚠️  article_categories table: {e}")
            
            try:
                result = db.session.execute(text('SELECT COUNT(*) FROM user_categories'))
                count = result.scalar()
                print(f"✅ user_categories join table exists and has {count} records")
            except Exception as e:
                print(f"⚠️  user_categories table: {e}")
            
            # Test table structures
            print("🏗️  Testing table structures...")
            inspector = db.inspect(db.engine)
            
            # Articles table
            columns = inspector.get_columns('articles')
            print(f"✅ Articles table has {len(columns)} columns:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
            
            # Users table
            columns = inspector.get_columns('users')
            print(f"✅ Users table has {len(columns)} columns:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
            
            # Categories table
            columns = inspector.get_columns('categories')
            print(f"✅ Categories table has {len(columns)} columns:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
            
            print("\n🎉 All database tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Database Test Script")
    print("=" * 60)
    
    test_database()
    
    print("=" * 60)
