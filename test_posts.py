from app import app
from unittest import TestCase
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class FlaskTests(TestCase):

    # this runs before each test
    def setUp(self):

        """Add sample user."""

        Post.query.delete()
        User.query.delete()
        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        """Add sample post."""

        post = Post(title="Best Pinot Noirs at Trader Joe's", content="Brand 1 is da bomb, but Trader Jose's is always good too", user_id=self.user_id)
        print(f'\n\n\n\n THE USER ID IN SET UP IS,{self.user_id}')

        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    # this runs after setUp and after each test runs
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_render_post_form(self):
        """
        Tests if post form is rendered upon visiting post/
        """
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')

            # the user id is incremented (even though we deleted the first user) because PKs are unique, meaning
            # that even after we delete an instance with that PK, that PK will not be reassigned to another instance
            # until we db.drop_all()
            print(f'\n\n\n\n THE USER ID IS NOW,{self.user_id}')

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add Post for ', html)


    def test_render_new_post(self):
        """
        Tests if the post we added in setUp is rendered on post detail page.
        """

        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Best Pinot Noirs at Trader Joe', html)

    def test_post_edit_post(self):
        """
        Tests if the edits we submit for post are committed and rendered on the post detail page.
        """

        with app.test_client() as client:
            d = {"title": "Title has changed", "content": "Content has changed", "img-url": ""}
            resp = client.post(f'/posts/{self.post_id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Title has changed', html)

    def test_post_delete_post(self):
        """
        Tests if the delete post request removes the post instance from posts table.
        Also tests if a page is found in the redirect.
        """

        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", data={}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(bool(Post.query.filter(Post.id == self.post_id).first()), False)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

