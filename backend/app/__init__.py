import os
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import text

# Import extensions and namespaces
from .extensions import db, api
from .routes.article_routes import api as articles_ns
from .routes.news_routes import api as news_ns

# Initialize Migrate outside the factory
migrate = Migrate()

def create_app():
    """
    Application Factory: Creates and configures the Flask app.
    This is the industry-standard pattern.
    """
    app = Flask(__name__)

    # --- Configuration ---
    # Load configuration from environment variables
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SUPABASE_DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["RESTX_MASK_SWAGGER"] = False

    # --- Initialize Extensions with the App ---
    # This crucial step connects your extensions to the Flask app instance
    db.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)

    # --- Add API Namespaces (Routes) ---
    # Define URL prefixes here for better organization
    api.add_namespace(articles_ns, path='/articles')
    api.add_namespace(news_ns, path='/news')
    
    # --- Register Custom CLI Commands ---
    # This integrates your 'test-db' command into the factory pattern
    @app.cli.command("test-db")
    def test_db_connection():
        """Tests the database connection."""
        try:
            # Use the app's context to ensure the connection is active
            with app.app_context():
                db.session.execute(text('SELECT 1'))
            print("Database connection successful!")
        except Exception as e:
            print("Database connection failed:")
            print(e)

    return app