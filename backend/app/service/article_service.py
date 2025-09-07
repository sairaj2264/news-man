from ..models.articles_model import Article

class ArticleService:
    @staticmethod
    def get_all_articles():
        """
        Fetches all articles using the SQLAlchemy Article model.
        """
        try:
            # This is the new ORM query
            articles = Article.query.order_by(Article.created_at.desc()).all()
            return articles, 200
        except Exception as e:
            # In a real app, you'd want to log this error
            return {"error": "An error occurred while fetching articles."}, 500