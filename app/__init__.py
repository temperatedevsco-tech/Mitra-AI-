from flask import Flask

from app.config import Config

from app.extensions import (
    db,
    migrate,
    login_manager,
    oauth,
)

# Import models so Flask-Migrate can discover them
from app.models.user import User
from app.models.chat import Chat
from app.models.message import Message


def create_app():

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    oauth.init_app(app)
    
    oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    },
)

    # Register the Flask-Login user_loader callback
    from importlib import import_module

    import_module("app.login_manager")

    # Register blueprints
    from app.routes.chat import chat_bp
    from app.routes.history import history_bp
    from app.routes.auth import auth_bp
    from app.routes.image import image_bp

    app.register_blueprint(chat_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(image_bp)

    return app