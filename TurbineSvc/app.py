import os
import sqlalchemy
from flask import Flask
from models import db


# def database_uri() -> sqlalchemy.engine.url.URL:
    
#     url = sqlalchemy.engine.url.URL.create(
#         drivername = os.environ.get("DB_DRIVER", default="mariadb+mariadbconnector"),
#         username = os.environ.get("DB_USER", default="none"),
#         password = os.environ.get("DB_PASSWORD", default="none"),
#         host = os.environ.get("DB_SERVER", default="127.0.0.1"),
#         port = os.environ.get("DB_PORT", default="3306"),
#         database = os.environ.get("DB_NAME", default="mydb"))

#     return url


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        db.create_all()
    from routes import turbines_bp, measurements_bp
    app.register_blueprint(turbines_bp)
    app.register_blueprint(measurements_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    svc_host = os.environ.get("SVC_HOST", default=None)
    app.run(host=svc_host)
