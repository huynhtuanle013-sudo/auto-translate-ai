import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_socketio import SocketIO
from config import config

db = SQLAlchemy()
socketio = SocketIO()

def create_app(config_name=None):
    """Factory function to create Flask app instance"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    Session(app)
    socketio.init_app(app, message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'])
    
    # Create necessary folders
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['VIDEO_TEMP_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AUDIO_TEMP_FOLDER'], exist_ok=True)
    os.makedirs(app.config['EXPORTS_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes import video_bp, subtitle_bp, translation_bp, tts_bp
    app.register_blueprint(video_bp)
    app.register_blueprint(subtitle_bp)
    app.register_blueprint(translation_bp)
    app.register_blueprint(tts_bp)
    
    # Register SocketIO events
    from app.events import register_socketio_events
    register_socketio_events(socketio)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
