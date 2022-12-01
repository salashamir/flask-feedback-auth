from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    # class methods
    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Cls method for registering user and doing logic to hash password"""
        hashed_pwd = bcrypt.generate_password_hash(password)
        hashed_pwd_utf8 = hashed_pwd.decode("utf8")
        user = cls(username=username,password=hashed_pwd_utf8,first_name=first_name, last_name=last_name, email=email)

        # add to db
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Cls method for authenticating whether user who has submitted credentials exists, username wexists and password is correct
        
        If user not valid returns False, otherwise user
        """
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False
    

class Feedback(db.Model):
    """Feedback"""
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)

