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


users_bp = Blueprint(
    "users",
    __name__
)


@users_bp.route(
    "/register",
    methods=["GET", "POST"]
)
@limiter.limit("5 per hour")
def register():

    error = None

    if request.method == "POST":

        username = request.form[
            "username"
        ].strip()

        email = request.form[
            "email"
        ].strip()

        password = request.form[
            "password"
        ]

        if username == "":
            error = "Username is required."

        elif email == "":
            error = "Email is required."

        elif password == "":
            error = "Password is required."

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
                password_hash=password_hash
            )

            db.session.add(user)

            db.session.commit()

            return redirect(
                url_for(
                    "auth.login"
                )
            )

    return render_template(
        "register.html",
        error=error
    )