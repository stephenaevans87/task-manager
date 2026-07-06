from datetime import datetime

from flask import current_app

from itsdangerous import (
    URLSafeTimedSerializer,
    BadSignature,
    SignatureExpired
)


def format_datetime(datetime_string):

    if datetime_string is None:
        return None

    try:

        dt = datetime.strptime(
            datetime_string,
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:

        dt = datetime.fromisoformat(datetime_string)

    return dt.strftime("%b %d, %Y — %I:%M %p")


def generate_verification_token(email):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    return serializer.dumps(
        email,
        salt="email-verification"
    )


def verify_verification_token(
    token,
    max_age=86400
):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:

        email = serializer.loads(
            token,
            salt="email-verification",
            max_age=max_age
        )

        return email

    except (
        SignatureExpired,
        BadSignature
    ):

        return None