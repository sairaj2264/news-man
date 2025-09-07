import os
import sys
from flask import Flask
from flask_restx import Api

from sqlalchemy import text
from flask_migrate import Migrate

# Add the current directory to Python path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# We import the namespace from your new routes file
from app.routes.article_routes import api as articles_ns
# We import the db instance from extensions
from extensions import db
# Import models to ensure they are registered
from app.models.articles_model import Article

migrate = Migrate()
# Initialize Flask app
app = Flask(__name__)
@app.cli.command("test-db")
def test_db_connection():
    """Tests the database connection."""
    try:
        db.session.execute(text('SELECT 1'))
        print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:")
        print(e)
# --- Database Configuration ---
# Get the database URI from your .env file
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SUPABASE_DB_URI")
# Optional: Disable modification tracking to save resources
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Initialize Extensions ---
# Connect the SQLAlchemy instance to your Flask app
db.init_app(app)

# --- API Setup ---
api = Api(app,
          version='1.0',
          title='News API',
          description='A simple API to fetch news articles')

# Add the articles namespace from your routes file to the API
api.add_namespace(articles_ns)
migrate.init_app(app, db) 


# A simple route to confirm the server is running
@app.route("/")
def home():
    return "Flask backend is running! Navigate to / to see the Swagger UI."


if __name__ == "__main__":
    app.run(debug=True)