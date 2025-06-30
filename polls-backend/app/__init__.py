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

    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)  # ✅
    db.init_app(app)  # ✅
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from .routes import poll_bp
    from .auth import auth_bp
    from .admin_routes import admin_bp

    app.register_blueprint(poll_bp, url_prefix="/polls")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
