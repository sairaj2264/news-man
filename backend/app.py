import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the current directory
load_dotenv()

# Import the factory function from your 'app' package
from app import create_app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Note: debug=True is not recommended for production
    app.run(debug=True)