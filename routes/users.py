
import re

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from werkzeug.security import (
    generate_password_hash
)

from extensions import limiter
from models import db
from models import User

from utils import (
    generate_verification_token,
    verify_verification_token
)


users_bp = Blueprint(
    "users",
    __name__
)


def is_valid_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(
        pattern,
        email
    ) is not None


def is_valid_username(username):

    pattern = r"^[A-Za-z0-9_-]+$"

    return re.match(
        pattern,
        username
    ) is not None


@users_bp.route(
    "/register",
    methods=["GET", "POST"]
)
@limiter.limit("5 per hour")
def register():

    error = None

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if username == "":
            error = "Username is required."

        elif len(username) < 3 or len(username) > 50:
            error = "Username must be between 3 and 50 characters."

        elif not is_valid_username(username):
            error = "Username may only contain letters, numbers, hyphens, and underscores."

        elif email == "":
            error = "Email is required."

        elif len(email) > 255:
            error = "Email is too long."

        elif not is_valid_email(email):
            error = "Please enter a valid email address."

        elif password == "":
            error = "Password is required."

        elif len(password) < 8:
            error = "Password must be at least 8 characters."

        elif User.query.filter_by(
            username=username
        ).first():

            error = "Username already exists."

        elif User.query.filter_by(
            email=email
        ).first():

            error = "Email already exists."

        else:

            password_hash = (
                generate_password_hash(
                    password
                )
            )

            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                is_verified=False
            )

            db.session.add(user)

            db.session.commit()

            token = generate_verification_token(
                user.email
            )

            verification_link = (
                request.host_url.rstrip("/")
                + url_for(
                    "users.verify_email",
                    token=token
                )
            )

            print("\n" + "=" * 60)
            print("EMAIL VERIFICATION LINK")
            print(verification_link)
            print("=" * 60 + "\n")

            return redirect(
                url_for(
                    "auth.login"
                )
            )

    return render_template(
        "register.html",
        error=error
    )


@users_bp.route("/verify-email/<token>")
def verify_email(token):

    email = verify_verification_token(
        token
    )

    if email is None:

        return render_template(
            "login.html",
            error="Invalid or expired verification link."
        )

    user = User.query.filter_by(
        email=email
    ).first()

    if user is None:

        return render_template(
            "login.html",
            error="User not found."
        )

    if not user.is_verified:

        user.is_verified = True

        db.session.commit()

    return render_template(
        "login.html",
        error="Email verified successfully! You may now log in."
    )
