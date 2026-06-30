from flask import Flask
from flask import render_template

from flask_migrate import Migrate

from config import Config
from models import db

from routes.auth import auth_bp
from routes.users import users_bp
from routes.tasks import tasks_bp
from routes.api import api_bp

from utils import format_datetime


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(
    app,
    db
)

app.jinja_env.globals.update(
    format_datetime=format_datetime
)

app.register_blueprint(tasks_bp)

app.register_blueprint(users_bp)

app.register_blueprint(auth_bp)

app.register_blueprint(api_bp)


@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template(
        "500.html"
    ), 500


if __name__ == "__main__":
    app.run(debug=True)