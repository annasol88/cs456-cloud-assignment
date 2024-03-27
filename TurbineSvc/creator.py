"""
A factory function that creates a Flask web app
with the DB schema configured in models.py orm
and the relevant routes defined in routes.py
"""
def create_app(app, config):
    app.config.update(config)
    with app.app_context():
        from models import db
        db.init_app(app)
        db.create_all()
    from routes import turbines_bp, measurements_bp
    app.register_blueprint(turbines_bp)
    app.register_blueprint(measurements_bp)
    return app