from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(40),
        unique=True,
        nullable=False,
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
    )

    password_hash = db.Column(
        db.Text,
        nullable=True,
    )

    google_id = db.Column(
        db.String(255),
        nullable=True,
        unique=True,
    )

    profile_picture = db.Column(
        db.Text,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
    )

    chats = db.relationship(
        "Chat",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )