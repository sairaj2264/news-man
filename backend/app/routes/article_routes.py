from flask_restx import Namespace, Resource, fields
from ..service.article_service import ArticleService
from ..models.articles_model import Article # Import the model

# Define the DTO here to avoid circular imports
article_dto = {
    'id': fields.String(readonly=True, description='The article unique identifier'),
    'created_at': fields.DateTime(readonly=True, description='The timestamp of creation'),
    'title': fields.String(required=True, description='The article title'),
    'summary': fields.String(required=True, description='The article summary'),
    'source_url': fields.String(required=True, description='The original URL of the article'),
    'image_url': fields.String(description='URL for the article image'),
    'published_at': fields.DateTime(description='The original publication date'),
    'source_name': fields.String(description='The name of the news source'),
}

# Create a namespace for article-related operations
api = Namespace('articles', description='Article related operations')

@api.route('/')
class ArticleList(Resource):
    """Resource for handling the list of articles."""
    @api.doc('list_articles')
    @api.marshal_list_with(api.model('ArticleDTO', article_dto)) # Use the DTO for marshalling
    def get(self):
        """Fetch all articles"""
        return ArticleService.get_all_articles()