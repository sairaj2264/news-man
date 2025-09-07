# Import all of your models and join tables into this one file.
# This ensures SQLAlchemy is aware of every table and relationship.

from .articles_model import Article, article_categories
from .user_model import User
from .category_model import Category
from .user_category_join_table import user_categories