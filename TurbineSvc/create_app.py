from flask import Flask
from models import db

def create_app(name, config):
    app = Flask(name)
    app.config.update(config)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    from routes import turbines_bp, measurements_bp
    app.register_blueprint(turbines_bp)
    app.register_blueprint(measurements_bp)
    return app