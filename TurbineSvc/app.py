import os
import sqlalchemy
from flask import Flask
from models import db


def database_uri(connection_str) -> sqlalchemy.engine.url.URL:
    if len(connection_str) != 0:
        return url

    url = sqlalchemy.engine.url.URL.create(
        drivername = os.environ.get("DB_DRIVER", default="mariadb+mariadbconnector"),
        username = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        host = os.environ.get("DB_SERVER"),
        port = os.environ.get("DB_PORT"),
        database = os.environ.get("DB_NAME", default="turbine"))

    return url


def create_app():
    connection_str = os.environ.get("DB_CONNECTION_STRING", default="")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri(connection_str)
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
