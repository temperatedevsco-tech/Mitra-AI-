from app.extensions import db

from app.models.chat import Chat
from app.models.message import Message


def create_chat(user):

    chat = Chat(
        user_id=user.id,
        title="New Chat",
    )

    db.session.add(chat)
    db.session.commit()

    return chat


def save_message(chat, role, content):

    message = Message(
        chat_id=chat.id,
        role=role,
        content=content,
    )

    db.session.add(message)

    db.session.commit()

    return message


def get_messages(chat):

    return Message.query.filter_by(

        chat_id=chat.id

    ).order_by(

        Message.timestamp.asc()

    ).all()


def get_user_chats(user):

    return Chat.query.filter_by(

        user_id=user.id

    ).order_by(

        Chat.updated_at.desc()

    ).all()
    
    from app.models.chat import Chat


def get_user_chats(user):

    return Chat.query.filter_by(
        user_id=user.id
    ).order_by(
        Chat.updated_at.desc()
    ).all()


def get_chat(user, chat_id):

    return Chat.query.filter_by(
        id=chat_id,
        user_id=user.id,
    ).first()
    
def rename_chat(chat, title):

    chat.title = title

    db.session.commit()
    
def delete_chat(chat):

    db.session.delete(chat)

    db.session.commit()