from flask import Blueprint, request, jsonify
from flask import current_app as app
from .models import db, Poll, PollOption, Vote, User
import jwt

poll_bp = Blueprint("polls", __name__)

# Helper: Decode JWT token from Authorization header
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

# Get all polls
@poll_bp.route("/", methods=["GET"])
def get_polls():
    polls = Poll.query.all()
    return jsonify([
        {
            "id": p.id,
            "question": p.question,
            "creator": p.creator.username,
            "active": p.is_active,
            "options": [
                {
                    "id": o.id,
                    "text": o.text,
                    "votes": len(o.votes)
                } for o in p.options
            ]
        }
        for p in polls
    ]), 200

# Create new poll
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

# Add an option to a poll
@poll_bp.route("/<int:poll_id>/options", methods=["POST"])
def add_option(poll_id):
    user_data = decode_token(request)
    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    option_text = data.get("text")
    if not option_text:
        return jsonify({"error": "Option text required"}), 400

    option = PollOption(text=option_text, poll_id=poll_id)
    db.session.add(option)
    db.session.commit()
    return jsonify({"message": "Option added"}), 201

# Submit a vote
@poll_bp.route("/<int:poll_id>/vote", methods=["POST"])
def vote(poll_id):
    user_data = decode_token(request)
    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    poll = Poll.query.get(poll_id)
    if not poll or not poll.is_active:
        return jsonify({"error": "Poll not found or inactive"}), 400

    data = request.get_json()
    option_id = data.get("option_id")

    if not option_id:
        return jsonify({"error": "Option ID required"}), 400

    option = PollOption.query.get(option_id)
    if not option or option.poll_id != poll_id:
        return jsonify({"error": "Invalid option"}), 400

    justification = data.get("justification", "")
    vote = Vote(
        user_id=user_data["user_id"],
        poll_option_id=option_id,
        justification=justification
    )
    db.session.add(vote)
    db.session.commit()
    return jsonify({"message": "Vote submitted"}), 201

# Get poll results
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
