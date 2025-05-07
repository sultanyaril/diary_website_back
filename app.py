from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, bcrypt, User, DiaryEntry
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)


with app.app_context():
    db.create_all()


# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 409

    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401


# Add a diary entry
@app.route('/entries', methods=['POST'])
@jwt_required()
def add_entry():
    user_id = get_jwt_identity()
    data = request.json
    entry = DiaryEntry(user_id=user_id, content=data['content'])
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Entry added"}), 201

# Get all diary entries
@app.route('/entries', methods=['GET'])
@jwt_required()
def get_entries():
    user_id = get_jwt_identity()
    entries = DiaryEntry.query.filter_by(user_id=user_id).order_by(DiaryEntry.timestamp.desc()).all()
    result = [
        {
            "id": entry.id,
            "content": entry.content,
            "timestamp": entry.timestamp.isoformat()
        }
        for entry in entries
    ]
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
