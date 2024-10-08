from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validate name
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty.")
        return name

    # Validate unique name during initialization
    def __init__(self, name, phone_number=None):
        # Check for existing author with the same name
        if Author.query.filter_by(name=name).first():
            raise ValueError(f"An author with the name '{name}' already exists.")
        
        self.name = name
        self.phone_number = phone_number

    # Validate phone_number
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number is not None:
            if not re.match(r'^\d{10}$', phone_number):
                raise ValueError("The phone number must be exactly 10 digits long.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validate content
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("The content must have at least 250 characters.")
        return content
    
    # Validate summary
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("The summary can only contain a maximum of 250 characters.")
        return summary
    
    # Validate category
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("The category can only be 'Fiction' or 'Non-Fiction'.")
        return category
    
    # Validate title
    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("The post title must contain at least one of the following: ['Won't Believe', 'Secret', 'Top', 'Guess'].")
        
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
