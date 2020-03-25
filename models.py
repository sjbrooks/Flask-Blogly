"""Models for Blogly."""

from flask_alchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User class.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    first_name = db.Column(db.String(),
                 nullable=False)
    last_name = db.Column(db.String(),
                 nullable=False)
    img_URL = db.Column(db.String(),
              nullable=True, default='https://picsum.photos/100
')

