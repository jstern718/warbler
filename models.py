"""SQLAlchemy models for Warbler."""
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app import engine

# Define the base class for table models
Base = declarative_base()

bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_IMAGE_URL = (
    "https://icon-library.com/images/default-user-icon/" +
    "default-user-icon-28.jpg")

DEFAULT_HEADER_IMAGE_URL = (
    "https://images.unsplash.com/photo-1519751138087-5bf79df62d5b?ixlib=" +
    "rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=for" +
    "mat&fit=crop&w=2070&q=80")


class Follow(Base):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'follows'

    user_being_followed_id = Column(
        Integer,
        ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    user_following_id = Column(
        Integer,
        ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )


class User(Base):
    """User in the system."""

    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
    )

    email = Column(
        String(50),
        nullable=False,
        unique=True,
    )

    username = Column(
        String(30),
        nullable=False,
        unique=True,
    )

    image_url = Column(
        String(255),
        nullable=False,
        default=DEFAULT_IMAGE_URL,
    )

    header_image_url = Column(
        String(255),
        nullable=False,
        default=DEFAULT_HEADER_IMAGE_URL,
    )

    bio = Column(
        String,
        nullable=False,
        default="",
    )

    location = Column(
        String(30),
        nullable=False,
        default="",
    )

    password = Column(
        String(100),
        nullable=False,
    )

    messages = relationship('Message', backref="user")

    followers = relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follow.user_being_followed_id == id),
        secondaryjoin=(Follow.user_following_id == id),
        backref="following",
    )

    likes = relationship(
        "Message",
        secondary="likes",
        backref="likers"
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, image_url=DEFAULT_IMAGE_URL):
        """Sign up user.

        Hashes password and adds user to session.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        # TODO: validate user instance before adding
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(user)
        session.commit()
        session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    def is_followed_by(self, other_user):
        """Is this user followed by `other_user`?"""

        found_user_list = [
            user for user in self.followers if user == other_user]
        return len(found_user_list) == 1

    def is_following(self, other_user):
        """Is this user following `other_user`?"""

        found_user_list = [
            user for user in self.following if user == other_user]
        return len(found_user_list) == 1


class Message(Base):
    """An individual message ("warble")."""

    __tablename__ = 'messages'

    id = Column(
        Integer,
        primary_key=True,
    )

    text = Column(
        String(140),
        nullable=False,
    )

    timestamp = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )


class Like(Base):

    __tablename__ = "likes"

    message_id = Column(
        Integer,
        ForeignKey('messages.id', ondelete="cascade"),
        primary_key=True,
    )

    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    app = app
    init_app(app)


# Create all tables in the database
Base.metadata.create_all(engine)
print("Tables created successfully")