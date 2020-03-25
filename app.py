"""Blogly application."""

from flask import Flask, render_template, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.conf['SECRET_KEY'] = 'zlxkcjvoiw34jpqr95ijafkdj'

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)

@app.route('/users')
def render_users():

    users = User.query.all()
    # # names = []

    # # for user in users:
    # #     names.append(User.combine_name())

    # for user in users:

    return render_template('user-listing.html', users=users)