from app.extensions import db, bcrypt
from enum import Enum

from app.utils.timezone import IndiaTimeStampNow

class Role(Enum):
    ADMIN = "Admin"
    STUDENT = "Student"

class Status(Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"

# Base class for common fields
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    notifications = db.Column(db.Boolean, default=True)  # Receive notifications
    phone_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String(10), nullable=True)  # Male/Female, No other
    dob = db.Column(db.Integer, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True, default="default.jpg")
    email_verified = db.Column(db.Boolean, default=False)  # Verified after email confirmation
    status = db.Column(db.Enum(Status), nullable=False, default=Status.ACTIVE)  # Active, Suspended, etc.
    role = db.Column(db.Enum(Role), nullable=False)
    date_created = db.Column(db.Integer, default=lambda:IndiaTimeStampNow())
    last_login = db.Column(db.Integer)

    oauth_account = db.relationship('OAuth', back_populates='user', uselist=False, cascade='all, delete-orphan')
    admin_data = db.relationship('Admin', back_populates='user', uselist=False, cascade='all, delete-orphan')
    student_data = db.relationship('Student', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def __init__(self, password=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if password:
            self.set_password(password)  # Hash the password during user creation
    
    # Method to set the hashed password
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Method to check if a password matches the stored hash
    def check_password(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user:
            password_hash = user.password
        return bcrypt.check_password_hash(password_hash, password)

# Admin Table
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    user = db.relationship('User', back_populates="admin_data")
    def __repr__(self):
        return f"<Admin {self.id}>"

# Student Table
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    qualification = db.Column(db.String(100), nullable=True)  # User qualification

    user = db.relationship('User', back_populates="student_data")
    scores = db.relationship('Score', back_populates='student', cascade='all, delete-orphan')
    take_quizzes = db.relationship("TakeQuiz", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student {self.id}>"


class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)


class OAuth(db.Model):
    __tablename__ = 'oauths'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    unique_id = db.Column(db.String(255), unique=False, nullable=False)
    platform = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', back_populates='oauth_account')

    def __repr__(self):
        return f"<Oauth {self.user_id}>"
