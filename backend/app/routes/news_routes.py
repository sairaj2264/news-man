from flask_restx import Namespace, Resource
from ..service.news_service import NewsService

# Create a namespace for news-related operations
api = Namespace('news', description='News fetching and processing operations')

# Instantiate the service
news_service = NewsService()

@api.route('/fetch/<string:topic>')
@api.param('topic', 'The news topic you want to fetch articles for (e.g., technology)')
class FetchNews(Resource):
    """
    A resource to trigger the fetching of news articles.
    """
    @api.doc('fetch_news_articles')
    def get(self, topic):
        """
        Fetches the latest news articles for a given topic.
        This endpoint is for testing Step 1.
        """
        articles = news_service.fetch_raw_articles(topic)
        if isinstance(articles, dict) and "error" in articles:
            return articles, 500
        
        return {"status": "success", "fetched_articles": len(articles), "data": articles}, 200
