import os
from dotenv import load_dotenv


load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "fallback-dev-secret-key"
    )

    ENV = os.getenv(
        "FLASK_ENV",
        "development"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///tasks.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False