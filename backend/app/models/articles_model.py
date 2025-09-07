from flask_restx import fields
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from extensions import db

# --- SQLAlchemy Database Model ---
# This class defines the 'articles' table in your database.
class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.String, primary_key=True) # Assuming UUID is stored as a string
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    title = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    source_name = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Article {self.title}>'


# --- Flask-RESTX API Data Transfer Object (DTO) ---
# This model defines the shape of the data for the API output.
# We'll define this in the routes file to avoid circular imports