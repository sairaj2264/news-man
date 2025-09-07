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
    A resource to trigger the fetching of news articles (Step 1).
    """
    @api.doc('fetch_raw_news_articles')
    def get(self, topic):
        """
        Fetches the latest raw news articles for a given topic.
        """
        articles = news_service.fetch_raw_articles(topic)
        if isinstance(articles, dict) and "error" in articles:
            return articles, 500
        
        return {"status": "success", "fetched_articles": len(articles), "data": articles}, 200

@api.route('/process/<string:topic>')
@api.param('topic', 'The news topic to fetch and summarize (e.g., technology)')
class ProcessNews(Resource):
    """
    A resource to trigger the full fetch and summarize pipeline (Step 1 + Step 2).
    """
    @api.doc('process_news_articles')
    def get(self, topic):
        """
        Fetches AND summarizes the latest news articles for a given topic.
        """
        # Step 1: Fetch
        raw_articles = news_service.fetch_raw_articles(topic)
        if isinstance(raw_articles, dict) and "error" in raw_articles:
            return raw_articles, 500
        
        if not raw_articles:
            return {"status": "success", "message": "No articles found to process."}, 200

        # Step 2: Summarize
        summarized_articles = news_service.summarize_articles(raw_articles)

        return {
            "status": "success", 
            "processed_articles": len(summarized_articles), 
            "data": summarized_articles
        }, 200