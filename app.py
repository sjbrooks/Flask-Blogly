"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'zlxkcjvoiw34jpqr95ijafkdj'

# db = SQLAlchemy()
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

@app.route('/users/new')
def get_add_user():
    return render_template('add-user.html')

@app.route('/users/new', methods=["POST"])
def post_add_user():
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    img_url = request.form.get("img-url")
    print("\n \n \n IMG URL IS",img_url)
    if(img_url == ""):
        user = User(first_name=first_name, last_name=last_name)
    else:
        user = User(first_name=first_name, last_name=last_name, img_URL=img_url)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<id>')
def user_profile(id):
    id = id
    user = User.query.filter(User.id == id).first()
    return render_template('user-profile.html', user=user)

@app.route('/users/<id>/edit')
def get_edit_user(id):
    id = id
    user = User.query.filter(User.id == id).first()
    return render_template('edit-user.html', user=user)

@app.route('/users/<id>/edit', methods=["POST"])
def post_edit_user(id):
    id = id
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    img_url = request.form.get("img-url")

    user = User.query.filter(User.id == id).first()
    user.first_name = first_name
    user.last_name = last_name
    user.img_URL = img_url
    db.session.commit()
    return redirect(f"/users/{id}")

@app.route('/users/<id>/delete', methods=["POST"])
def delete_user(id):
    id = id
    user = User.query.filter(User.id == id)
    user.delete()
    db.session.commit()
    return redirect("/users")