from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

# Instantiate the extensions. 
# They will be configured and linked to the app in the app factory.
db = SQLAlchemy()
api = Api(version='1.0', title='News API',
          description='A simple API to fetch news articles')