"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

default_img = "https://trffcc.com/img/tools/sitemap.png"



db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text,nullable=False,default=default_img)
    pst = db.relationship("Post",backref='users',cascade="all, delete-orphan")

    @property
    def fullname(self):
        """Returns a full name"""
        return f"{ self.first_name} { self.last_name }"



class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    
    
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,nullable=False,unique=True)
    posts = db.relationship("Post",secondary="post_tags",backref="tags",cascade="all,delete")
   
class PostTag(db.Model):
    __tablename__ = 'post_tags'
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'),primary_key=True)
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'),primary_key=True)

def connect_db(app):
    db.app = app
    db.init_app(app)