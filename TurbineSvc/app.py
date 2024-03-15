import os
import sqlalchemy
from flask import Flask
from models import db

def database_uri() -> sqlalchemy.engine.url.URL:

    url = os.environ.get("DB_CONNECTION_STRING", default="")
    if len(url) != 0:
        return url

    url = sqlalchemy.engine.url.URL.create(
        drivername = os.environ.get("DB_DRIVER", default="mariadb+mariadbconnector"),
        username = os.environ.get("DB_USER", default='webapp'),
        password = os.environ.get("DB_PASSWORD", default=123),
        host = os.environ.get("DB_SERVER", default="172.17.0.3"),
        port = os.environ.get("DB_PORT", default="3306"),
        database = os.environ.get("DB_NAME", default="turbine"))

    return url


def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        db.create_all()
    from routes import turbines_bp, measurements_bp
    app.register_blueprint(turbines_bp)
    app.register_blueprint(measurements_bp)
    return app

app = Flask(__name__)
app = create_app()
