from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=True, unique = True)

    paragraphs = db.relationship("Paragraph", backref = "user", cascade="all,delete")

    @classmethod
    def register(cls, username, password, email=None):
        """Register user w/hashed password & return user."""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email)
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.
        Return user if valid; else return False."""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Paragraph(db.Model):

    __tablename__ = 'paragraphs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)

class Image(db.Model):

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=datetime.date.today())
    photographer = db.Column(db.Text, nullable=False)
    credit_url = db.Column(db.Text, nullable=False)

    paragraphs = db.relationship("Paragraph", backref = "image")