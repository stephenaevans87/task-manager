
import os
from dotenv import load_dotenv


load_dotenv()


class Config:

    ENV = os.getenv(
        "FLASK_ENV",
        "development"
    )

    DEBUG = ENV == "development"

    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )

    if not SECRET_KEY:

        if ENV == "development":

            SECRET_KEY = "fallback-dev-secret-key"

        else:

            raise RuntimeError(
                "SECRET_KEY must be set in production."
            )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///tasks.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = ENV != "development"
