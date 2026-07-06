from app.extensions import db
from app.models.user import User

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)


def create_user(username, email, password):

    existing = User.query.filter_by(email=email).first()

    if existing:
        return None, "Email already exists."

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )

    db.session.add(user)
    db.session.commit()

    return user, None


def authenticate_user(email, password):

    user = User.query.filter_by(email=email).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user