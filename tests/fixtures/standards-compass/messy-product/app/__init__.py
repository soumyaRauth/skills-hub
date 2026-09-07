import os
from flask import Flask
from .routes import visits, auth, admin, uploads

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "change-me")
    app.register_blueprint(auth.bp)
    app.register_blueprint(visits.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(uploads.bp)
    return app
