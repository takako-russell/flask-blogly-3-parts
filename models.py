"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

default_img = "https://trffcc.com/img/tools/sitemap.png"



db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text,nullable=False,default=default_img)
    pst = db.relationship("Post",backref='users')



class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
   

def connect_db(app):
    db.app = app
    db.init_app(app)