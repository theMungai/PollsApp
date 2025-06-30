from flask import Blueprint, request, jsonify
from .models import db, Poll, PollOption, Vote, User
from flask import current_app as app
import jwt

poll_bp = Blueprint("polls", __name__)

def decode_token(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except:
        return None

@poll_bp.route("/", methods=["GET"])
def get_polls():
    polls = Poll.query.all()
    return jsonify([
        {
            "id": p.id,
            "question": p.question,
            "creator": p.creator.username,
            "is_active": p.is_active,
            "options": [{"id": o.id, "text": o.text} for o in p.options]
        }
        for p in polls
    ]), 200

@poll_bp.route("/", methods=["POST"])
def create_poll():
    user
