from werkzeug.security import generate_password_hash

from .models import User
from . import db


def create_user(email: str, name: str, password: str) -> User:
    """A helper function to create a user entry into the database"""
    new_user = User(email=email, name=name, password=generate_password_hash(password, method="pbkdf2:sha256"))
    db.session.add(new_user)
    db.session.commit()

    return new_user