"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, bcrypt, User, DEFAULT_IMAGE_URL, DEFAULT_HEADER_IMAGE_URL
from sqlalchemy.exc import IntegrityError


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Verify that models have the attributes you expect"""
        u1 = User.query.get(self.u1_id)

        # test attributes
        self.assertEqual(u1.id, self.u1_id)
        self.assertEqual(u1.email, "u1@email.com")
        self.assertEqual(u1.username, "u1")
        self.assertEqual(u1.image_url, DEFAULT_IMAGE_URL)
        self.assertEqual(u1.header_image_url, DEFAULT_HEADER_IMAGE_URL)
        self.assertEqual(u1.bio, "")
        self.assertEqual(u1.location, "")

        # test hashed password
        is_auth = bcrypt.check_password_hash(u1.password, "password")
        self.assertEqual(is_auth, True)

        # User should have no messages, followers, following, or likes
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)
        self.assertEqual(len(u1.following), 0)
        self.assertEqual(len(u1.likes), 0)

    """Tests for model methods."""

    def test_user_is_following(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        """Does is_following successfully detect when user1 is following user2?"""
        u2.followers.append(u1)
        self.assertEqual(u1.is_following(u2), True)

        """Does is_following successfully detect when user1 is not following user2?"""
        u2.followers.clear()
        self.assertEqual(u1.is_following(u2), False)


    def test_user_is_followed_by(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        """Does is_followed_by successfully detect when user1 is followed by user2?"""
        u1.followers.append(u2)
        self.assertEqual(u1.is_followed_by(u2), True)

        """Does is_followed_by successfully detect when user1 is not followed by user2?"""
        u1.followers.clear()
        self.assertEqual(u1.is_followed_by(u2), False)


    def test_user_signup(self):
        """Does User.signup successfully return and create a new user given valid credentials?"""
        u3 = User.signup("u3", "u3@email.com", "password", None)
        db.session.commit()

        stored_u3 = User.query.get(u3.id)

        # is this a valid way to test?
        self.assertEqual(stored_u3, u3)

        # test attributes
        self.assertEqual(u3.email, "u3@email.com")
        self.assertEqual(u3.username, "u3")
        self.assertEqual(u3.image_url, DEFAULT_IMAGE_URL)
        self.assertEqual(u3.header_image_url, DEFAULT_HEADER_IMAGE_URL)
        self.assertEqual(u3.bio, "")
        self.assertEqual(u3.location, "")

        # test hashed password
        is_auth = bcrypt.check_password_hash(u3.password, "password")
        self.assertEqual(is_auth, True)

        # User should have no messages, followers, following, or likes
        self.assertEqual(len(u3.messages), 0)
        self.assertEqual(len(u3.followers), 0)
        self.assertEqual(len(u3.following), 0)
        self.assertEqual(len(u3.likes), 0)

        """Does User.signup fail to create a new user if any of the validations (eg uniqueness, non-nullable fields) fail?"""
        # u4 = User.signup(None, "u4@email.com", "password", None)
        # self.assertRaises(IntegrityError, db.session.commit)

        # u5 = User.signup("u5", None, "password", None)
        # self.assertRaises(IntegrityError, db.session.commit)

        # TODO: find bcrypt error for this one
        # u6 = User.signup("u5", "u5@email.com", None, None)


    def test_user_authenticate(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""
        u1 = User.query.get(self.u1_id)
        u_auth = User.authenticate("u1", "password")

        self.assertEqual(u_auth, u1)

        """Does User.authenticate fail to return a user when the username is invalid?"""
        u_auth = User.authenticate("invalid username", "password")
        self.assertEqual(u_auth, False)


        """Does User.authenticate fail to return a user when the password is invalid?"""
        u_auth = User.authenticate("u1", "invalid password")
        self.assertEqual(u_auth, False)
