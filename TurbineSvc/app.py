from flask import Flask
from creator import create_app
import dbutils as db

"""
Contains callable flask app for the gunicorn server
"""


"""
The app config to be used for establishing
"""
def app_config():
    return {
        'SQLALCHEMY_DATABASE_URI': db.uri(),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {'connect_args': db.connection_args()},
    }


""" 
Creates flask app calling the creator factory function 
"""
def create():
    app = Flask(__name__)
    return create_app(app, app_config())
