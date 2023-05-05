"""Message View tests."""

# run these tests like:
#
#    FLASK_DEBUG=False python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app, CURR_USER_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# This is a bit of hack, but don't use Flask DebugToolbar

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

"""
Make sure that requests to all the endpoints supported in the views files return valid responses.
Start by testing that the response code is what you expect,
then do some light HTML testing to make sure the response is what you expect
"""


class UserBaseViewTestCase(TestCase):
    """Set up mock data for User tests"""

    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)
        db.session.add_all()
        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()


class UserAddViewTestCase(UserBaseViewTestCase):
    def test_add_user(self):
        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            # Now, that session setting is saved, so we can have
            # the rest of ours test
            resp = c.post("/users/new", data={"text": "Hello"})

            self.assertEqual(resp.status_code, 302)

            User.query.filter_by(text="Hello").one()

    def test_show_followers(self):
        """
        When you’re logged in, can you see the follower pages for any user?
        """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get(f"/users/{self.u2_id}/followers")
            self.assertEqual(resp.status_code, 200)

    def test_show_following(self):
        """
        When you’re logged in, can you see the following pages for any user?
        """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get(f"/users/{self.u2_id}/following")
            self.assertEqual(resp.status_code, 200)

    def test_show_followers(self):
        """
        When you’re logged out, are you disallowed from visiting a user’s
        follower pages?
        """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id


            resp = c.get(f"/users/{self.u2_id}/followers")
            self.assertEqual(resp.status_code, 302)

    def test_show_following(self):
        """
        When you’re logged out, are you disallowed from visiting a user’s
        following pages?
        """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get(f"/users/{self.u2_id}/following")
            self.assertEqual(resp.status_code, 302)

    def test_add_message(self):
             """
             When you’re logged in, can you add a message as yourself?
            """

            with self.client as c:
                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = self.u1_id

                resp = c.get(f"/users/{self.u2_id}/following")


    """
    When you’re logged in, can you delete a message as yourself?
    """
    """
    When you’re logged out, are you prohibited from adding messages?
    """
    """
    When you’re logged out, are you prohibited from deleting messages?
    """
    """
    When you’re logged in, are you prohibited from deleting another user’s message?
    """