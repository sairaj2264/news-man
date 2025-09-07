from sqlalchemy import desc
from ..extensions import db
from ..models import Article, Category

class ArticleService:
    """
    A service layer to handle database operations for articles.
    """
    @staticmethod
    def get_all_articles():
        """Retrieves all articles from the database, newest first."""
        try:
            return Article.query.order_by(desc(Article.created_at)).all()
        except Exception as e:
            print(f"Error getting all articles: {e}")
            return []

    @staticmethod
    def get_articles_by_category(category_name: str):
        """Retrieves all articles for a specific category, newest first."""
        try:
            return Article.query.join(Article.categories).filter(
                Category.category_name == category_name.lower()
            ).order_by(desc(Article.created_at)).all()
        except Exception as e:
            print(f"Error getting articles for category '{category_name}': {e}")
            return []

    @staticmethod
    def get_all_categories():
        """Retrieves all unique categories from the database."""
        try:
            return Category.query.order_by(Category.category_name).all()
        except Exception as e:
            print(f"Error getting all categories: {e}")
            return []
