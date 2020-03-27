"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag
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


# Start of Part II
@app.route('/users/<id>/posts/new')
def render_post_form(id):
    user = User.query.get_or_404(id)
    return render_template("post-form.html", user=user)

@app.route('/users/<id>/posts/new', methods=['POST'])
def post_new_post(id):
    user = User.query.get_or_404(id)

    title = request.form.get("title")
    content = request.form.get("content")

    # other way to do it is appending this to the users table
    post = Post(title=title, content=content, user_id=id)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{id}")

@app.route('/posts/<id>')
def render_new_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post-detail.html', post=post)

@app.route('/posts/<id>/edit')
def get_edit_post(id):
    post = Post.query.get_or_404(id)
    return render_template('edit-post.html', post=post)

@app.route('/posts/<id>/edit', methods=['POST'])
def post_edit_post(id):
    post = Post.query.get_or_404(id)
    title = request.form.get("title")
    content = request.form.get("content")

    post.title = title
    post.content = content
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<id>/delete', methods=['POST'])
def post_delete_post(id):
    post = Post.query.filter(Post.id == id)
    user_id = f'{post.first().user.id}'
    post.delete()
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/tags')
def render_tags():
    tags = Tag.query.all()
    return render_template('tag-listing.html', tags=tags)

@app.route('/tags/<id>')
def render_tag(id):
    tag = Tag.query.get_or_404(id)
    return render_template('tag-detail.html', tag=tag)