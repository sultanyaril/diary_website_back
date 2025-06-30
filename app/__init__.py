from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db, bcrypt
from .config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    # Register Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.entry_routes import entry_bp
    from .routes.evaluate_routes import evaluate_bp
    from .routes.emotion_routes import emotion_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(entry_bp)
    app.register_blueprint(evaluate_bp)
    app.register_blueprint(emotion_bp)

    return app
