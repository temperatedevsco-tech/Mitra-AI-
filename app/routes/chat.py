from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)

from app.services.chat_service import (
    delete_chat,
)

from app.services.ai_service import (
    generate_reply,
    generate_title,
)

from app.services.chat_service import (
    create_chat,
    save_message,
    get_messages,
    get_chat,
    get_user_chats,
    rename_chat,
)

from flask_login import current_user, login_required

from app.services.chat_service import (
    get_user_chats,
    get_chat,
    get_messages,
)

from app.services.ai_service import generate_reply

chat_bp = Blueprint(
    "chat",
    __name__,
)


@chat_bp.route("/")
def home():

    return render_template("index.html")


from flask_login import login_required, current_user

from app.services.chat_service import (
    create_chat,
    save_message,
)

from app.services.ai_service import generate_reply


@chat_bp.route("/api/chat", methods=["POST"])
@login_required
def chat():

    data = request.get_json()

    message = data.get("message", "")

    chat_id = data.get("chat_id")

    if chat_id:

        from app.models.chat import Chat

        chat = Chat.query.filter_by(
            id=chat_id,
            user_id=current_user.id,
        ).first()

        if chat is None:

            return jsonify({
                "error": "Chat not found."
            }), 404

    else:

        chat = create_chat(current_user)

    save_message(
        chat,
        "user",
        message,
    )
    
    if chat.title == "New Chat":

        title=generate_title(message)

        rename_chat(
            chat,
            title,
        )

    reply = generate_reply(message)

    save_message(
        chat,
        "assistant",
        reply,
    )

    return jsonify({

        "reply": reply,

        "chat_id": chat.id,

    })
    
@chat_bp.route("/api/chats")
@login_required
def chats():

    chats = get_user_chats(current_user)

    return jsonify([

        {
            "id": chat.id,
            "title": chat.title
        }

        for chat in chats

    ])
    
@chat_bp.route("/api/chat/<int:chat_id>")
@login_required
def load_chat(chat_id):

    chat = get_chat(current_user, chat_id)

    if chat is None:

        return jsonify({
            "error": "Chat not found"
        }),404

    messages = get_messages(chat)

    return jsonify([

        {

            "role": m.role,

            "content": m.content

        }

        for m in messages

    ])
    
@chat_bp.route("/api/chat/new", methods=["POST"])
@login_required
def new_chat():

    chat = create_chat(current_user)

    return jsonify({

        "id": chat.id,

        "title": chat.title

    })
    
@chat_bp.route("/api/chat/<int:chat_id>", methods=["DELETE"])
@login_required
def remove_chat(chat_id):

    chat = get_chat(current_user, chat_id)

    if chat is None:

        return jsonify({
            "error": "Chat not found"
        }),404

    delete_chat(chat)

    return jsonify({
        "success": True
    })