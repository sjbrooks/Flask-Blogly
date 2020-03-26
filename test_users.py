from app import app
from unittest import TestCase
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class FlaskTests(TestCase):
    def setUp(self):
        """Add sample user."""

        User.query.delete()
        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users(self):
        """
        Tests if getting /users works
        """
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<ul>', html)
            self.assertIn('Test User', html)

    def test_profile(self):
        """
        Tests if getting user profile by users/{id} works
        """
        with app.test_client() as client:
            # print("\n \n \n self user id is", self.user_id)
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)
            self.assertIn('</span>', html)

    def test_user_edit(self):
        """
        Tests if editing user works,
        checks for profile being updated with new names,
        checks if redirects properly to /users/{id}
        """
        with app.test_client() as client:
            d = {"first-name": "Sarah", "last-name": "Brooks", "img-url": ""}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sarah Brooks", html)

    def test_delete_user(self):
        """
        Tests if deleting a user works,
        checks if user deleted from database,
        checks if redirects properly to /users
        """
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", data={}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            # Checks if no longer in database after delete
            self.assertEqual(bool(User.query.filter(User.id == self.user_id).first()), False)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<ul>', html)

