from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import db, DiaryEntry
from ..services.emotion_predictor import get_list_of_emotions

emotion_bp = Blueprint('emotion', __name__)

ALLOWED_EMOTIONS = get_list_of_emotions()


@emotion_bp.route('/emotions', methods=['GET'])
@jwt_required()
def get_emotions():
    return jsonify(ALLOWED_EMOTIONS)


@emotion_bp.route('/entries/<int:entry_id>/emotion', methods=['PUT'])
@jwt_required()
def update_emotion(entry_id):
    user_id = get_jwt_identity()
    entry = DiaryEntry.query.filter_by(id=entry_id, user_id=user_id).first()

    if not entry:
        return jsonify({"message": "Entry not found"}), 404

    data = request.json
    new_emotion = data.get('emotion')

    if not new_emotion:
        return jsonify({"message": "Emotion cannot be empty"}), 400

    if new_emotion not in ALLOWED_EMOTIONS:
        return jsonify({"message": f"Invalid emotion. Allowed emotions are: {', '.join(ALLOWED_EMOTIONS)}"}), 400

    entry.emotion = new_emotion
    db.session.commit()

    return jsonify({"message": "Emotion updated successfully"}), 200
