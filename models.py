from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Topic(Base):
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with NewsArticles
    articles = relationship('NewsArticle', back_populates='topic')

class NewsArticle(Base):
    __tablename__ = 'news_articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    raw_content = Column(Text, nullable=False)
    url = Column(String(500), nullable=False, unique=True)
    published_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    
    # Relationships
    topic = relationship('Topic', back_populates='articles')
    summary = relationship('Summary', back_populates='article', uselist=False)

class Summary(Base):
    __tablename__ = 'summaries'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    article_id = Column(Integer, ForeignKey('news_articles.id'), nullable=False, unique=True)
    
    # One-to-one relationship with NewsArticle
    article = relationship('NewsArticle', back_populates='summary')