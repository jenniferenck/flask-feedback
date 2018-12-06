from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20), primary_key=True, nullable=False, unique=True)
    # UnicodeText allows for symbols
    password = db.Column(db.UnicodeText, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship(
        'Feedback', backref='user', cascade='all, delete-orphan')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user, hashing their password"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')

        return cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Checking for correct credentials at login"""

        # query for user instance
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False


class Feedback(db.Model):
    """Feedback... """

    __tablename__ = "feedback"

    id = id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String, db.ForeignKey('users.username'), nullable=False)
