"""Follow model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, Follow

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


class FollowModelTestCase(TestCase):
    def setUp(self):
        Follow.query.delete()

        f1 = Follow.signup("f1", "f1@email.com", "password", None)
        f2 = Follow.signup("f2", "f2@email.com", "password", None)

        db.session.commit()
        self.f1_id = f1.id
        self.f2_id = f2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_follow_model(self):
        """Verify that models have the attributes you expect"""
        """write tests for any model methods"""