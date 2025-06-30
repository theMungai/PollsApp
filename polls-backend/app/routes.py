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
    user_data = decode_token(request)
    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    question = data.get("question")
    options = data.get("options", [])

    if not question or not options:
        return jsonify({"error": "Question and options are required"}), 400

    poll = Poll(question=question, creator_id=user_data["user_id"])
    db.session.add(poll)
    db.session.flush()  # Get poll.id before commit

    for option_text in options:
        option = PollOption(text=option_text, poll_id=poll.id)
        db.session.add(option)

    db.session.commit()
    return jsonify({"message": "Poll created", "poll_id": poll.id}), 201

@poll_bp.route("/<int:poll_id>/options", methods=["POST"])
def add_option(poll_id):
    user_data = decode_token(request)
    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    option = PollOption(text=data["text"], poll_id=poll_id)
    db.session.add(option)
    db.session.commit()
    return jsonify({"message": "Option added"}), 201

@poll_bp.route("/<int:poll_id>/vote", methods=["POST"])
def vote(poll_id):
    user_data = decode_token(request)
    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    vote = Vote(
        user_id=user_data["user_id"],
        poll_option_id=data["option_id"],
        justification=data.get("justification", "")
    )
    db.session.add(vote)
    db.session.commit()
    return jsonify({"message": "Vote cast"}), 201

@poll_bp.route("/<int:poll_id>/results", methods=["GET"])
def poll_results(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    results = []
    for option in poll.options:
        results.append({
            "option": option.text,
            "votes": len(option.votes)
        })
    return jsonify({
        "question": poll.question,
        "results": results
    }), 200
