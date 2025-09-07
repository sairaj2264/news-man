import os
from flask import Flask
from flask_migrate import Migrate

from flask_cors import CORS 

# Import the extensions that will be linked to the app
from .extensions import db, api

# Import all your models so that Flask-Migrate can see them
from .models import Article, User, Category

# Import all your API namespaces
from .routes.article_routes import api as articles_ns
from .routes.news_routes import api as news_ns

migrate = Migrate()

def create_app():
    """
    Application Factory: Creates and configures the Flask app.
    This is the industry-standard pattern to avoid circular imports and context errors.
    """
    app = Flask(__name__)
 # Allow both your local development server and your deployed frontend
    origins = [
    "http://localhost:5173",
    "https://news-mann.netlify.app" # Your Netlify URL
    ]
    CORS(app, resources={r"/*": {"origins": origins}})

    # --- Configuration ---
    # Load configuration from environment variables
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SUPABASE_DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["RESTX_MASK_SWAGGER"] = False

    # --- Initialize Extensions with the App ---
    # This is the crucial step that links your db and api objects to the
    # Flask app instance, fixing the "app is not registered" error.
    db.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)

    # --- Add API Namespaces (Routes) ---
    # Define URL prefixes here for better organization
    api.add_namespace(articles_ns, path='/articles')
    api.add_namespace(news_ns, path='/news')

    return app