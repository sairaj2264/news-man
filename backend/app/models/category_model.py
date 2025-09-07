# import sys
# import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from extensions import db
# --- NEW ---
# Import the join table from its separate file
from .user_category_join_table import user_categories

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), unique=True, nullable=False)

    # This relationship allows you to see all articles associated with a category
    articles = db.relationship(
        'Article', 
        secondary='article_categories', 
        back_populates='categories'
    )

    # --- NEW ---
    # This relationship links categories to the users who are interested in them.
    users = db.relationship(
        'User',
        secondary=user_categories,
        back_populates='categories'
    )

    def __repr__(self):
        return f'<Category {self.category_name}>'

