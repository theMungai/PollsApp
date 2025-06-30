from flask import Flask  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_migrate import Migrate  # type: ignore
from flask_bcrypt import Bcrypt  # type: ignore
from flask_cors import CORS  # type: ignore

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from .routes import poll_bp
    from .auth import auth_bp
    from .admin_routes import admin_bp  # NEW: import admin routes

    app.register_blueprint(poll_bp, url_prefix="/polls")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")  # NEW: register admin blueprint

    return app
