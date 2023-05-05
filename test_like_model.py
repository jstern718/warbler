"""Like model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, Like

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
# TODO: in the future, only create the tables necessary for this test suite


class LikeModelTestCase(TestCase):
    def setUp(self):
        Like.query.delete()

        l1 = Like.signup("l1", "l1@email.com", "password", None)
        l2 = Like.signup("l2", "l2@email.com", "password", None)

        db.session.commit()
        self.l1_id = l1.id
        self.l2_id = l2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_like_model(self):
        """Verify that models have the attributes you expect"""
        """write tests for any model methods"""