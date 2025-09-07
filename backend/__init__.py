from flask import Flask
from .extensions import api
from .routes.article_routes import register_routes

def create_app():
    app = Flask(__name__)
    api.init_app(app)
    register_routes(api)
    return app