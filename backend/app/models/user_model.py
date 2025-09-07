# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ..extensions import db
from flask_restx import fields
import datetime
# --- NEW ---
# Import the join table from its separate file
from .user_category_join_table import user_categories

# --- SQLAlchemy Database Model for Users ---
# This class defines the 'users' table in your database.
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # This will store the hashed password
    name = db.Column(db.String(100), nullable=True)
    joined_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_of_birth = db.Column(db.Date, nullable=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)

    # --- NEW ---
    # This relationship links users to the categories they are interested in.
    categories = db.relationship(
        'Category',
        secondary=user_categories,
        back_populates='users'
    )

    def __repr__(self):
        return f'<User {self.email_id}>'


# --- Flask-RESTX API Data Transfer Object (DTO) for Users ---
# This model defines the shape of the user data for the API output.
# We'll define this in the routes file to avoid circular imports
user_dto = {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'email_id': fields.String(required=True, description='User email address'),
    'name': fields.String(description='User full name'),
    'joined_at': fields.DateTime(readonly=True, description='Timestamp of when the user joined'),
    'date_of_birth': fields.Date(description='User date of birth'),
    'phone_number': fields.String(description='User phone number'),
}

