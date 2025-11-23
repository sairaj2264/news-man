News-Man: AI-Powered News Fetching and Summarization
//Hashira Hackathon Problem statement  "-1,-2" 
Live Demo: Yet to Be Hosted.

An intelligent news aggregation platform that uses a sophisticated AI pipeline to fetch the latest articles, generate concise summaries, and deliver a clean, clutter-free reading experience.....
Yes It is True !!
Project Overview
News-Man is a full-stack web application designed to combat information overload. Instead of browsing multiple news sites, users can add topics of interest, and the application's AI-powered backend takes over. It uses the Tavily API for real-time, comprehensive web searches to find the latest news, then leverages the power of Google's Gemini model to create high-quality, fact-checked summaries. The results are stored and served via a robust Flask API to a dynamic React frontend, providing an always-up-to-date, personalized news feed.

Key Features
AI-Powered Summarization: Utilizes Google's Gemini 1.5 Flash model to generate concise, neutral summaries and compelling headlines.

Real-Time News Fetching: Integrates with the Tavily Search API to find and scrape the latest articles from across the web.

Category Management: Users can dynamically add new topics, triggering the AI pipeline to fetch and process news for that category..

Intelligent Caching: A 30-minute caching mechanism prevents redundant API calls for the same topic, saving resources and costs.

AI-Powered Validation: An extra validation step ensures the factual accuracy of summaries before they are stored.

Clean, Modern UI: A responsive and intuitive React frontend with category filtering and pagination for a seamless user experience.

Tech Stack & Architecture
This project is built with a modern, decoupled architecture, separating the backend processing from the frontend presentation layer.

Frontend:

React (Vite): A fast and modern library for building the user interface.

Tailwind CSS: For utility-first styling and a responsive design.

Axios: For making HTTP requests to the backend API.

Backend:

Flask: A lightweight Python web framework for building the API.

Flask-RESTX: For creating structured RESTful APIs with automatic Swagger documentation.

Flask-SQLAlchemy & Flask-Migrate: For ORM and handling database schema migrations.

Database:

Supabase (PostgreSQL): A scalable and robust open-source SQL database.

AI & External Services:

Google Gemini 1.5 Flash: For all generative AI tasks (summarization, headline generation, validation).

Tavily Search API: For real-time, AI-optimized web searching and content scraping.

Architecture Diagram
Getting Started
To get a local copy up and running, follow these simple steps.

Prerequisites
Node.js (v18 or later)

Python (v3.10 or later) & Pip

Git

Local Setup
Clone the repository:

git clone [https://github.com/your-username/news-man.git](https://github.com/your-username/news-man.git)
cd news-man

Backend Setup:

# Navigate to the backend directory
cd backend

# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file and add your API keys (see .env.example)
cp .env.example .env

# Initialize the database and run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run the Flask server
python app.py

Frontend Setup (in a new terminal):

# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Create a .env.local file and add your backend API URL
# VITE_API_BASE_URL=[http://127.0.0.1:5000](http://127.0.0.1:5000)

# Run the React development server
npm run dev

You can now access the application at http://localhost:5173.

Environment Variables
You will need to create .env files for both the frontend and backend.

backend/.env
SUPABASE_DB_URI="your_postgresql_connection_string"
TAVILY_API_KEY="your_tavily_api_key"
GOOGLE_API_KEY="your_google_ai_studio_api_key"

frontend/.env.local
VITE_API_BASE_URL=[http://127.0.0.1:5000](http://127.0.0.1:5000)
