from flask_restx import Namespace, Resource
from ..service.news_service import NewsService

api = Namespace('news', description='News fetching and processing operations')
news_service = NewsService()

@api.route('/process/<string:topic>')
@api.param('topic', 'The news topic to fetch, process, and store')
class ProcessNews(Resource):
    """
    Triggers the full pipeline: Fetch -> Summarize -> Validate -> Store.
    Includes a 30-minute cache check before fetching.
    """
    @api.doc('process_news_by_topic')
    def get(self, topic):
        """
        Runs the full data processing pipeline for a given topic.
        """
        result, status_code = news_service.process_topic(topic.lower())
        return result, status_code