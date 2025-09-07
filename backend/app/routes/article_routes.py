from flask_restx import Namespace, Resource, fields
from ..service.article_service import ArticleService

api = Namespace('articles', description='Article retrieval operations')

# DTO for displaying a single article
article_display_dto = api.model('ArticleDisplay', {
    'id': fields.String(readonly=True),
    'published_at': fields.Date,
    'headline': fields.String(required=True),
    'summary': fields.String(required=True),
    'source_url': fields.String(required=True),
    'image_url': fields.String,
    'source_name': fields.String
})

# DTO for displaying a category
category_display_dto = api.model('CategoryDisplay', {
    'id': fields.Integer(readonly=True),
    'category_name': fields.String(required=True)
})

@api.route('/')
class ArticleList(Resource):
    """Resource for getting all articles for the main news feed."""
    @api.marshal_list_with(article_display_dto)
    def get(self):
        """Get all articles for the main feed, sorted by most recent"""
        return ArticleService.get_all_articles()

@api.route('/by-category/<string:category_name>')
class ArticlesByCategory(Resource):
    """Resource for getting articles filtered by a specific category."""
    @api.marshal_list_with(article_display_dto)
    def get(self, category_name):
        """Get articles for a specific category, sorted by most recent"""
        return ArticleService.get_articles_by_category(category_name)

@api.route('/categories')
class CategoryList(Resource):
    """Resource for getting all unique categories."""
    @api.marshal_list_with(category_display_dto)
    def get(self):
        """Get all unique categories"""
        return ArticleService.get_all_categories()
