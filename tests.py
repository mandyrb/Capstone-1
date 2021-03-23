"""View tests."""

import os
from unittest import TestCase
from models import db, connect_db, User, Paragraph, Image
import datetime

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///paragraph_test_db"

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for users"""

    def setUp(self):
        """Create test client, add sample data."""
        
        Paragraph.query.delete()
        Image.query.delete()
        User.query.delete()

        self.client = app.test_client()

        self.firstuser = User.register(username="firstuser",
                                    email="first@test.com",
                                    password="firstuser")
        self.firstuser.id = 1234

        self.seconduser = User.register(username="seconduser",
                                    password="seconduser")
        self.seconduser.id = 5678

        db.session.add_all([self.firstuser, self.seconduser])
        db.session.commit()

        self.image = Image(
            image_url = "https://images.unsplash.com/photo-1613993729048-84d5639ac8c1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyMTIzOTh8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MTUyOTA4NTA&ixlib=rb-1.2.1&q=80&w=200",
            date_added = datetime.date(2021, 3, 7),
            photographer = "Anne Sack",
            credit_url = "https://unsplash.com/@anne_sack"
        )
        self.image.id = 111

        db.session.add(self.image)
        db.session.commit()

        self.paragraph = Paragraph(
            title = "My first paragraph",
            content = "Paragraph content",
            public = True,
            user_id = 1234,
            image_id = 111
        )
        self.paragraph.id = 222

        db.session.add(self.paragraph)
        db.session.commit()


    def test_homepage(self):
        """Make sure if no one is logged in, we can view the homepage"""

        with self.client as c:
        
            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to Paragraph A Day!", html)

    def test_about_page(self):
        """Make sure if no one is logged in, we can view the "about" page"""

        with self.client as c:
        
            resp = c.get('/about')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("About Paragraph A Day", html)
    
    def test_register_user(self):
        """Ensure that registration works with email provided"""

        with self.client as c:

            data={"username": "thirdtestuser", "password": "thirdtestuser", "email": "third@test.com"}
            resp = c.post("/register", data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(User.query.all()), 3)

    def test_register_user_no_email(self):
        """Ensure that registration works with no email provided"""

        with self.client as c:

            data={"username": "fourthtestuser", "password": "fourthtestuser"}
            resp = c.post("/register", data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(User.query.all()), 3)

    def test_login_user(self):
        """Ensure that login works for valid user"""

        with self.client as c:

            data={"username": "firstuser", "password": "firstuser"}
            resp = c.post("/login", data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome firstuser", str(resp.data))

    def test_login_invalid_user(self):
        """Ensure that login doesn't work for invalid user"""

        with self.client as c:

            data={"username": "username_invalid", "password": "username_invalid"}
            resp = c.post("/login", data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Invalid username", str(resp.data))

    def test_my_paragraph_view(self):
        """Make sure a logged in user can view their paragraphs"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.firstuser.id
            
            resp = c.get('/users/1234/paragraphs')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("My first paragraph", html)

    def test_my_paragraph_view_no_user(self):
        """Make sure if no one is logged in, we can't see a user's paragraphs"""

        with self.client as c:
            
            resp = c.get('/users/1234/paragraphs', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You must login to view your paragraphs", html)
            self.assertNotIn("My first paragraph", html)
    
    def test_my_paragraph_view_wrong_user(self):
        """Make sure a logged in user can't view another user's private paragraphs"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.seconduser.id
            
            resp = c.get('/users/1234/paragraphs', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You may not view", html)
            self.assertNotIn("My first paragraph", html)

    def test_create_paragraph(self):
        """Make sure a logged in user can create and submit a new paragraph"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.firstuser.id

            data={"title": "Test Title", "content": "Test Content", "public": True}
            resp = c.post("/users/1234", data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Title", str(resp.data))

    def test_create_paragraph_wrong_user(self):
        """Make sure a logged in user can't create a paragraph for another user"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.seconduser.id

            data={"title": "Test Title", "content": "Test Content", "public": True}
            resp = c.post("/users/1234", data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You may not create a paragraph for another user", str(resp.data))

    def test_create_paragraph_no_user(self):
        """Make sure someone can't create a paragraph if they're not logged in"""

        with self.client as c:

            data={"title": "Test Title", "content": "Test Content", "public": True}
            resp = c.post("/users/1234", data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You must login to create a paragraph", str(resp.data))

    def test_public_paragraph_view(self):
        """Make sure a logged in user can view public paragraphs from another user"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.seconduser.id
            
            resp = c.get('/public_paragraphs')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("My first paragraph", html)

    def test_public_paragraph_view_no_user(self):
        """Make sure a user can't view public paragraphs unless they're logged in"""

        with self.client as c:
            
            resp = c.get('/public_paragraphs', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You must login to view public paragraphs", html)

    def test_public_paragraph_search(self):
        """Make sure a logged in user can search for public paragraphs by date"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.seconduser.id
            
            data={"date_added" : "datetime.date(2021, 3, 7)"}
            resp = c.post("/public_paragraphs", data=data)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("My first paragraph", str(resp.data))
    
    def test_edit_paragraph_view(self):
        """Make sure a logged in user can get to the edit paragraph view"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.firstuser.id
            
            resp = c.get('/edit_paragraph/222')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit Your Paragraph", html)

    def test_edit_paragraph(self):
        """Make sure a logged in user can edit their paragraph"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.firstuser.id
            
            data={"title" : "New Title", "content" : "New Content", "public" : False}
            resp = c.post('/edit_paragraph/222', data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("New Title", str(resp.data))
            self.assertNotIn("My first paragraph", str(resp.data))

    def test_edit_paragraph_wrong_user(self):
        """Make sure a logged in user can't edit someone else's paragraph and instead
        redirects to their own home view"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.seconduser.id
            
            data={"title" : "New Title", "content" : "New Content", "public" : False}
            resp = c.post('/edit_paragraph/222', data=data, follow_redirects=True)
            

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You may not edit", str(resp.data))
            self.assertNotIn("New Title", str(resp.data))

    def test_edit_paragraph_no_user(self):
        """Make sure someone can't edit a paragraph if they're not logged in"""

        with self.client as c:
            
            data={"title" : "New Title", "content" : "New Content", "public" : False}
            resp = c.post('/edit_paragraph/222', data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You must login to edit paragraphs", str(resp.data))
            self.assertNotIn("New Title", str(resp.data))

    def test_delete_paragraph(self):
        """Make sure a logged in user can delete their paragraph"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.firstuser.id
            
            resp = c.post('/delete_paragraph/222', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(Paragraph.query.all()), 0)

    def test_delete_paragraph_wrong_user(self):
        """Make sure a logged in user can't delete someone else's paragraph'"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.seconduser.id
            
            resp = c.post('/delete_paragraph/222', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You may not delete", str(resp.data))
            self.assertEqual(len(Paragraph.query.all()), 1)

    def test_delete_paragraph_no_user(self):
        """Make sure if no one is logged in, they can't delete someone's paragraph'"""

        with self.client as c:
            
            resp = c.post('/delete_paragraph/222', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You may not delete", str(resp.data))
            self.assertEqual(len(Paragraph.query.all()), 1)