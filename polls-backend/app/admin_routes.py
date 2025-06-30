from flask import Blueprint, request, jsonify
from .models import db, User, Poll, PollOption, Vote
from flask import current_app as app
import jwt

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

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

def is_admin(user_data):
    return user_data and user_data.get("role") == "admin"

@admin_bp.route("/polls", methods=["POST"])
def create_poll_admin():
    user_data = decode_token(request)
    if not is_admin(user_data):
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    poll = Poll(question=data["question"], creator_id=user_data["user_id"])
    db.session.add(poll)
    db.session.flush()

    for text in data.get("options", []):
        option = PollOption(text=text, poll_id=poll.id)
        db.session.add(option)

    db.session.commit()
    return jsonify({"message": "Admin poll created", "poll_id": poll.id}), 201

@admin_bp.route("/polls", methods=["GET"])
def get_all_polls():
    user_data = decode_token(request)
    if not is_admin(user_data):
        return jsonify({"error": "Admin access required"}), 403

    polls = Poll.query.all()
    return jsonify([
        {
            "id": poll.id,
            "question": poll.question,
            "creator": poll.creator.username,
            "is_active": poll.is_active
        }
        for poll in polls
    ]), 200

@admin_bp.route("/polls/<int:poll_id>/activate", methods=["PATCH"])
def toggle_poll_activation(poll_id):
    user_data = decode_token(request)
    if not is_admin(user_data):
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    poll = Poll.query.get(poll_id)
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    poll.is_active = data.get("active", False)
    db.session.commit()
    return jsonify({"message": "Poll status updated"}), 200

@admin_bp.route("/polls/<int:poll_id>", methods=["DELETE"])
def delete_poll(poll_id):
    user_data = decode_token(request)
    if not is_admin(user_data):
        return jsonify({"error": "Admin access required"}), 403

    poll = Poll.query.get(poll_id)
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    db.session.delete(poll)
    db.session.commit()
    return jsonify({"message": "Poll deleted"}), 200

@admin_bp.route("/users", methods=["GET"])
def get_users():
    user_data = decode_token(request)
    if not is_admin(user_data):
        return jsonify({"error": "Admin access required"}), 403

    users = User.query.all()
    return jsonify([
        {"id": user.id, "username": user.username, "role": user.role}
        for user in users
    ]), 200

@admin_bp.route("/promote/<int:user_id>", methods=["PATCH"])
def promote_user(user_id):
    user_data = decode_token(request)
    if not is_admin(user_data):
        return jsonify({"error": "Admin access required"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.role = "admin"
    db.session.commit()
    return jsonify({"message": f"{user.username} promoted to admin"}), 200

@admin_bp.route("/votes", methods=["GET"])
def get_all_votes():
    user_data = decode_token(request)
    if not is_admin(user_data):
        return jsonify({"error": "Admin access required"}), 403

    votes = Vote.query.all()
    return jsonify([
        {
            "voter": vote.voter.username,
            "poll_option": vote.option.text,
            "justification": vote.justification
        }
        for vote in votes
    ]), 200
