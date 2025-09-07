from flask_restx import fields
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from extensions import db

# --- Many-to-Many Join Table ---
# This is not a class, but a helper table for the relationship.
# SQLAlchemy will manage this table for you.
article_categories = db.Table('article_categories',
    db.Column('article_id', db.String, db.ForeignKey('articles.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

# --- SQLAlchemy Database Model ---
class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    title = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    source_name = db.Column(db.Text, nullable=True)

    # This relationship allows you to see all categories for an article
    categories = db.relationship(
        'Category', 
        secondary=article_categories, 
        back_populates='articles'
    )

    def __repr__(self):
        return f'<Article {self.title}>'
