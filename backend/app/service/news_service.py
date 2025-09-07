import os
import json
import uuid
import datetime
from tavily import TavilyClient
import google.generativeai as genai
from sqlalchemy import desc
from ..extensions import db
# --- CORRECTED IMPORTS ---
# This now imports from your central models/__init__.py file,
# which fixes the circular dependency error.
from ..models import Article, Category

class NewsService:
    def __init__(self):
        self.tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        summarization_config = {"response_mime_type": "application/json"}
        self.summarization_model = genai.GenerativeModel("gemini-1.5-flash", generation_config=summarization_config)
        self.validation_model = genai.GenerativeModel("gemini-1.5-flash")
        self.raw_content_map = {}

    def process_topic(self, topic_name: str):
        """
        Main public method to run the entire pipeline for a given topic.
        Includes caching check, fetch, summarize, validate, and store.
        """
        # --- CACHING LOGIC ---
        recently_fetched, message = self._is_recently_fetched(topic_name)
        if recently_fetched:
            return {"status": "skipped", "message": message}, 429 # 429 Too Many Requests

        # Step 1: Fetch
        raw_articles = self._fetch_raw_articles(topic_name)
        if not raw_articles:
            return {"status": "success", "message": "No new articles found from provider."}, 200
        
        # Step 2: Summarize
        summarized_articles = self._summarize_articles(raw_articles)

        # Step 3: Validate
        validated_articles = self._validate_articles(summarized_articles)

        # Step 4: Store
        storage_result = self._store_articles(validated_articles, topic_name)

        return {
            "status": "pipeline_complete",
            "metrics": {
                "initial_fetch_count": len(raw_articles),
                "summarized_count": len(summarized_articles),
                "validated_count": len(validated_articles),
                "newly_stored_count": storage_result.get("new_articles_stored", 0)
            }
        }, 200

    def _is_recently_fetched(self, topic_name: str):
        """
        Checks if articles for a given category have been fetched in the last 30 minutes.
        """
        thirty_minutes_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
        
        # Find the most recent article fetched for this category
        most_recent_article = Article.query \
            .join(Article.categories) \
            .filter(Category.category_name == topic_name) \
            .order_by(desc(Article.created_at)) \
            .first()

        if most_recent_article and most_recent_article.created_at > thirty_minutes_ago:
            time_since = (datetime.datetime.utcnow() - most_recent_article.created_at).seconds // 60
            return True, f"This topic was updated {time_since} minutes ago. Please try again later."
            
        return False, None

    def _fetch_raw_articles(self, topic: str, max_results: int = 5):
        try:
            query = f"latest top {max_results} news articles about {topic}"
            response = self.tavily_client.search(query=query, search_depth="advanced", max_results=max_results, include_raw_content=True)
            self.raw_content_map = {item['url']: item['raw_content'] for item in response.get('results', [])}
            return response.get('results', [])
        except Exception as e:
            print(f"Error fetching from Tavily: {e}")
            return []

    def _summarize_articles(self, articles: list):
        summarized_articles = []
        for article in articles:
            try:
                raw_content = self.raw_content_map.get(article.get('url'))
                if not raw_content: continue
                prompt = f"""
                You are a neutral news editor. Process the following article.
                Article: --- {raw_content} ---
                Based ONLY on the article, perform these actions:
                1. Create a compelling, neutral, and short headline.
                2. Create a single, concise paragraph that summarizes the key points.
                3. Extract the publication date in 'YYYY-MM-DD' format (or null).
                4. Extract the name of the news source.
                Provide the output as a valid JSON object.
                """
                response = self.summarization_model.generate_content(prompt)
                summary_data = json.loads(response.text)
                processed_article = {
                    "title": article.get('title'), "headline": summary_data.get('headline'),
                    "source_url": article.get('url'), "summary": summary_data.get('summary'),
                    "published_at": summary_data.get('published_at'), "source_name": summary_data.get('source_name')
                }
                summarized_articles.append(processed_article)
            except Exception as e:
                print(f"Error summarizing article {article.get('url')}: {e}")
        return summarized_articles

    def _validate_articles(self, summarized_articles: list):
        validated_articles = []
        for article in summarized_articles:
            try:
                if not article.get('summary') or not article.get('source_url'): continue
                original_content = self.raw_content_map.get(article['source_url'])
                if not original_content: continue
                validation_prompt = f"Based ONLY on the Original Article Text, is the Summary factually accurate? Answer only YES or NO.\nOriginal Text: ---{original_content}---\nSummary: ---{article['summary']}---"
                response = self.validation_model.generate_content(validation_prompt)
                if "YES" in response.text.upper():
                    validated_articles.append(article)
            except Exception as e:
                print(f"Error validating article {article.get('title')}: {e}")
        return validated_articles

    def _store_articles(self, validated_articles: list, topic_name: str):
        new_articles_count = 0
        try:
            # Find or create the category for this topic
            category = Category.query.filter_by(category_name=topic_name).first()
            if not category:
                category = Category(category_name=topic_name)
                db.session.add(category)
            
            for article_data in validated_articles:
                exists = Article.query.filter_by(source_url=article_data['source_url']).first()
                if not exists:
                    pub_date = None
                    date_str = article_data.get('published_at')
                    if date_str and str(date_str).lower() != 'null':
                        try:
                            pub_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                        except (ValueError, TypeError):
                            pub_date = None
                    
                    new_article = Article(
                        id=str(uuid.uuid4()), title=article_data.get('title'),
                        headline=article_data.get('headline'), summary=article_data.get('summary'),
                        source_url=article_data.get('source_url'), published_at=pub_date,
                        source_name=article_data.get('source_name')
                    )
                    # Associate the article with its category
                    new_article.categories.append(category)
                    db.session.add(new_article)
                    new_articles_count += 1
            
            db.session.commit()
            return {"status": "success", "new_articles_stored": new_articles_count}
        except Exception as e:
            db.session.rollback()
            print(f"Database error during storage: {e}")
            return {"error": "Failed to store articles in the database."}