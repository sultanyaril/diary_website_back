from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from textblob import TextBlob
from ..models import db, DiaryEntry

evaluate_bp = Blueprint('evaluate', __name__)


@evaluate_bp.route('/evaluate', methods=['POST'])
@jwt_required()
def evaluate_entry():
    user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get('content', '')
    entry_id = data.get('entry_id')

    if not content.strip():
        return jsonify({"error": "Empty content"}), 400

    # Sentiment logic
    blob = TextBlob(content)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        sentiment = 'positive'
    elif polarity < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    # Optionally update the DB
    if entry_id:
        entry = DiaryEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if entry:
            entry.sentiment = sentiment
            db.session.commit()

    return jsonify({"sentiment": sentiment}), 200