import os
from dotenv import load_dotenv

# This MUST be at the top to load your .env file before the app starts
load_dotenv()

# Import the factory function from your 'app' package
from app import create_app

# Create the application instance by calling the factory
app = create_app()

if __name__ == '__main__':
    # This block only runs when you execute `python app.py`
    app.run(debug=True)