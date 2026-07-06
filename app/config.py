import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "mitra-secret"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENROUTER_API_KEY = os.getenv(
        "OPENROUTER_API_KEY"
    )

    APP_URL = os.getenv(
        "APP_URL",
        "http://127.0.0.1:5000"
    )

    IMAGE_MODEL = os.getenv(
        "IMAGE_MODEL",
        "openai/gpt-image-1"
    )
    
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
WTF_CSRF_ENABLED = True

print("OPENROUTER:", Config.OPENROUTER_API_KEY)