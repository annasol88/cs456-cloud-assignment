import os
from creator import create_app
import dbutils as db


def app_config():
    connection_str = os.environ.get("DB_CONNECTION_STRING", default="")
    return {
        'SQLALCHEMY_DATABASE_URI': db.get_uri(connection_str),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {'connect_args': db.connection_args()},
    }


app = create_app(__name__, app_config())
