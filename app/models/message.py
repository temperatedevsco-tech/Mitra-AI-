from app.extensions import db


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    chat_id = db.Column(
        db.Integer,
        db.ForeignKey("chats.id"),
        nullable=False,
    )

    role = db.Column(
        db.String(20),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        server_default=db.func.now(),
    )