from flask_restx import Namespace, Resource, fields
from ..service.article_service import ArticleService

# Create a namespace for article-related operations
api = Namespace('articles', description='Article retrieval operations')

# --- API Model (DTO) for Frontend Display ---
# This defines the structure of the JSON data sent to the frontend.
article_display_dto = api.model('ArticleDisplay', {
    'id': fields.String(readonly=True, description='The unique identifier for the article'),
    'published_at': fields.Date(description='The date the article was published'),
    'headline': fields.String(required=True, description='The AI-generated headline for the article'),
    'summary': fields.String(required=True, description='The AI-generated summary of the article'),
    'source_url': fields.String(required=True, description='The URL to the original article'),
    'image_url': fields.String(description='A URL for a relevant image'),
    'source_name': fields.String(description='The name of the news publication')
})

@api.route('/')
class ArticleList(Resource):
    """
    Resource for getting all articles for the main news feed.
    """
    @api.doc('get_all_articles')
    @api.marshal_list_with(article_display_dto)
    def get(self):
        """Get all articles for the main feed, sorted by most recent"""
        # Call the service layer to get the data
        return ArticleService.get_all_articles()

@api.route('/by-category/<string:category_name>')
@api.param('category_name', 'The name of the category to filter by (e.g., chess, technology)')
class ArticlesByCategory(Resource):
    """
    Resource for getting articles filtered by a specific category.
    """
    @api.doc('get_articles_by_category')
    @api.marshal_list_with(article_display_dto)
    def get(self, category_name):
        """Get articles for a specific category, sorted by most recent"""
        # Call the service layer with the category name
        return ArticleService.get_articles_by_category(category_name)