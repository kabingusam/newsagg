from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from newsagg import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    interests = db.relationship('Interest', backref='user', lazy=True)
    google_id = db.Column(db.String(50), unique=True, nullable=True)

class Interest(db.Model):
    __tablename__ = 'interests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id'), nullable=False)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(255), nullable=False)
    url_to_image = db.Column(db.String(255), nullable=True)
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    source = db.Column(db.String(255), nullable=False)
    interests = db.relationship('Interest', secondary='article_interests', backref='articles', lazy=True)

class ArticleInterest(db.Model):
    __tablename__ = 'article_interests'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interests.id'), nullable=False)
