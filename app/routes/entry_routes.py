from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, DiaryEntry

entry_bp = Blueprint('entries', __name__)


@entry_bp.route('/entries', methods=['POST'])
@jwt_required()
def add_entry():
    user_id = get_jwt_identity()
    data = request.json

    content = data.get('content', '').strip()
    if not content:
        return jsonify({"message": "Content cannot be empty"}), 400

    entry = DiaryEntry(
        user_id=user_id,
        title=data.get('title'),
        content=content
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Entry added", "id": entry.id}), 201


@entry_bp.route('/entries', methods=['GET'])
@jwt_required()
def get_entries():
    user_id = get_jwt_identity()
    entries = DiaryEntry.query.filter_by(user_id=user_id).order_by(DiaryEntry.timestamp.desc()).all()
    return jsonify([
        {
            "id": entry.id,
            "title": entry.title,
            "content": entry.content,
            "timestamp": entry.timestamp,
            "emotion": entry.emotion
        } for entry in entries
    ])


@entry_bp.route('/entries/<int:entry_id>', methods=['GET'])
@jwt_required()
def get_entry(entry_id):
    user_id = get_jwt_identity()
    entry = DiaryEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({"message": "Entry not found"}), 404
    return jsonify({
        "id": entry.id,
        "title": entry.title,
        "content": entry.content,
        "timestamp": entry.timestamp,
        "emotion": entry.emotion
    })


@entry_bp.route('/entries/<int:entry_id>', methods=['PUT'])
@jwt_required()
def update_entry(entry_id):
    user_id = get_jwt_identity()
    entry = DiaryEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({"message": "Entry not found"}), 404

    data = request.json
    new_content = data.get('content', '').strip()
    if not new_content:
        return jsonify({"message": "Content cannot be empty"}), 400

    entry.title = data.get('title', entry.title)
    entry.content = new_content
    db.session.commit()
    return jsonify({"message": "Entry updated"}), 200


@entry_bp.route('/entries/<int:entry_id>', methods=['DELETE'])
@jwt_required()
def delete_entry(entry_id):
    user_id = get_jwt_identity()
    entry = DiaryEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({"message": "Entry not found"}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Entry deleted"}), 200
