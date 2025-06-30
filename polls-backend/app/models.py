from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="user")

    polls = db.relationship("Poll", backref="creator", lazy=True)
    votes = db.relationship("Vote", backref="voter", lazy=True)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Changed lazy from True to "joined" to ensure options load with polls
    options = db.relationship("PollOption", backref="poll", cascade="all, delete", lazy="joined")

class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"), nullable=False)

    votes = db.relationship("Vote", backref="option", lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    poll_option_id = db.Column(db.Integer, db.ForeignKey("poll_option.id"))
    justification = db.Column(db.String(300))
