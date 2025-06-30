from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, DiaryEntry
from ..services.emotion_predictor import predict_emotion

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

    emotion = predict_emotion(content)

    if entry_id:
        entry = DiaryEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if entry:
            entry.emotion = emotion
            entry.model_prediction = emotion
            db.session.commit()

    return jsonify({"emotion": emotion}), 200