from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  # <-- NEW IMPORT
from werkzeug.security import generate_password_hash, check_password_hash # For password hashing

db = SQLAlchemy()

# User model for authentication
class User(UserMixin, db.Model): # Inherits from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.String(50), nullable=True)

    # Optional: Link tasks to a user
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"<Task {self.title}>"
