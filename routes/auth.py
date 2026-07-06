from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

from werkzeug.security import (
    check_password_hash
)

from models import User
from extensions import limiter


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
@limiter.limit("5 per minute")
def login():

    error = None

    if request.method == "POST":

        username = request.form[
            "username"
        ].strip()

        password = request.form[
            "password"
        ]

        user = User.query.filter_by(
            username=username
        ).first()

        if user is None:

            error = (
                "Invalid username or password."
            )

        elif not check_password_hash(
            user.password_hash,
            password
        ):

            error = (
                "Invalid username or password."
            )

        elif not user.is_verified:

            error = (
                "Please verify your email before logging in."
            )

        else:

            session["user_id"] = (
                user.id
            )

            session["username"] = (
                user.username
            )

            return redirect(
                url_for(
                    "tasks.home"
                )
            )

    return render_template(
        "login.html",
        error=error
    )


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for(
            "auth.login"
        )
    )