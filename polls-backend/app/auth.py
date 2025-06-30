from flask import Blueprint, request, jsonify
from . import db, bcrypt
from .models import User
import jwt
from datetime import datetime, timedelta
from flask import current_app as app

auth_bp = Blueprint("auth", __name__)

def generate_token(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return token

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 400

    hashed = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password_hash=hashed)
    db.session.add(user)
    db.session.commit()

    token = generate_token(user)
    return jsonify({"token": token}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user)
    return jsonify({"token": token}), 200

@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return jsonify({
            "id": payload["user_id"],
            "username": payload["username"],
            "role": payload["role"]
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
