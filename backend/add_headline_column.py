#!/usr/bin/env python3
"""
Script to add the missing headline column to the articles table
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

def add_headline_column():
    """Add the headline column to the articles table."""
    print("🔧 Adding headline column to articles table...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if headline column already exists
            print("🔍 Checking if headline column exists...")
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'articles' AND column_name = 'headline'
            """))
            
            if result.fetchone():
                print("✅ Headline column already exists!")
                return True
            
            # Add the headline column
            print("➕ Adding headline column...")
            db.session.execute(text("""
                ALTER TABLE articles 
                ADD COLUMN headline TEXT
            """))
            
            db.session.commit()
            print("✅ Headline column added successfully!")
            
            # Verify the column was added
            print("🔍 Verifying column was added...")
            result = db.session.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'articles' 
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            print(f"📋 Articles table now has {len(columns)} columns:")
            for col in columns:
                print(f"   - {col[0]}: {col[1]}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error adding headline column: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 Add Headline Column Script")
    print("=" * 60)
    
    add_headline_column()
    
    print("=" * 60)
