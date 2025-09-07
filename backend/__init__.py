from flask import Flask
from .extensions import db


def create_app():
    app = Flask(__name__)
    
    # Database configuration
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SUPABASE_DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    db.init_app(app)
    
    return app