from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import Dict, Optional

from models import Base, NewsArticle, Summary, Topic

class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def store_article_with_summary(self, article_data: Dict) -> Optional[Dict]:
        """
        Store a news article and its summary in the database.
        
        Args:
            article_data: Dictionary containing article information including:
                - title: Article headline
                - raw_content: Full article text
                - url: Article URL
                - topic_name: Topic of the article
                - summary: Summary text
                - published_date: Article publication date (optional)
        
        Returns:
            Dictionary with stored article and summary IDs if successful, None if failed
        """
        session = self.Session()
        try:
            # Get or create topic
            topic = session.query(Topic).filter_by(name=article_data['topic_name']).first()
            if not topic:
                topic = Topic(name=article_data['topic_name'])
                session.add(topic)
                session.flush()

            # Create news article
            article = NewsArticle(
                title=article_data['title'],
                raw_content=article_data['raw_content'],
                url=article_data['url'],
                topic_id=topic.id,
                published_date=article_data.get('published_date', datetime.utcnow())
            )
            session.add(article)
            session.flush()

            # Create summary with relationship to article
            summary = Summary(
                content=article_data['summary'],
                article_id=article.id
            )
            session.add(summary)

            # Commit the transaction
            session.commit()

            return {
                'article_id': article.id,
                'summary_id': summary.id,
                'topic_id': topic.id
            }

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error storing article: {str(e)}")
            return None

        finally:
            session.close()

    def get_article_with_summary(self, article_id: int) -> Optional[Dict]:
        """
        Retrieve an article and its summary from the database.
        
        Args:
            article_id: ID of the article to retrieve
            
        Returns:
            Dictionary containing article and summary information if found, None if not found
        """
        session = self.Session()
        try:
            article = session.query(NewsArticle).filter_by(id=article_id).first()
            if not article:
                return None

            return {
                'article': {
                    'id': article.id,
                    'title': article.title,
                    'raw_content': article.raw_content,
                    'url': article.url,
                    'published_date': article.published_date,
                    'topic_name': article.topic.name
                },
                'summary': {
                    'id': article.summary.id,
                    'content': article.summary.content,
                    'created_at': article.summary.created_at
                } if article.summary else None
            }

        except SQLAlchemyError as e:
            print(f"Error retrieving article: {str(e)}")
            return None

        finally:
            session.close()