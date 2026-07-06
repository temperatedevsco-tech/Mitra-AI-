from app.extensions import db


class Chat(db.Model):

    __tablename__ = "chats"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(255),
        default="New Chat",
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    messages = db.relationship(
        "Message",
        backref="chat",
        lazy=True,
        cascade="all, delete-orphan",
    )
    
