"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'zlxkcjvoiw34jpqr95ijafkdj'

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)

@app.route('/users')
def render_users():

    users = User.query.all()
    return render_template('user-listing.html', users=users)

@app.route('/users/new')
def get_add_user():
    return render_template('add-user.html')

@app.route('/users/new', methods=["POST"])
def post_add_user():
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    img_url = request.form.get("img-url") or None

    user = User(first_name=first_name, last_name=last_name, img_URL=img_url)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<id>')
def user_profile(id):
    user = User.query.get_or_404(id)
    return render_template('user-profile.html', user=user)

@app.route('/users/<id>/edit')
def get_edit_user(id):
    user = User.query.get_or_404(id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<id>/edit', methods=["POST"])
def post_edit_user(id):
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    img_url = request.form.get("img-url")

    user = User.query.get_or_404(id)
    user.first_name = first_name
    user.last_name = last_name
    user.img_URL = img_url
    db.session.commit()
    return redirect(f"/users/{id}")

@app.route('/users/<id>/delete', methods=["POST"])
def delete_user(id):
    user = User.query.filter(User.id == id)
    user.delete()
    db.session.commit()
    return redirect("/users")

@app.route('/users/<id>/posts/new')
def render_post_form(id):
    user = User.query.filter(User.id == id)
    return render_template("post-form.html", user=user)
