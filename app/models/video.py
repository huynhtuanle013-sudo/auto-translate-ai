from app import db
from datetime import datetime

class Video(db.Model):
    """Model for storing video information"""
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_url = db.Column(db.String(500), nullable=True)
    platform = db.Column(db.String(50), nullable=True)  # youtube, tiktok, etc.
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False)
    duration = db.Column(db.Float, nullable=True)  # in seconds
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    fps = db.Column(db.Float, nullable=True)
    source_language = db.Column(db.String(10), default='en')
    target_language = db.Column(db.String(10), default='vi')
    translation_style = db.Column(db.String(50), default='natural')  # precise, natural, entertainment, advertising, cinema
    voice_type = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='uploaded')  # uploaded, processing, completed, failed
    progress = db.Column(db.Integer, default=0)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    subtitles = db.relationship('Subtitle', backref='video', lazy=True, cascade='all, delete-orphan')
    history = db.relationship('TranslationHistory', backref='video', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Video {self.id}: {self.filename}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_url': self.original_url,
            'platform': self.platform,
            'file_size': self.file_size,
            'duration': self.duration,
            'width': self.width,
            'height': self.height,
            'fps': self.fps,
            'source_language': self.source_language,
            'target_language': self.target_language,
            'translation_style': self.translation_style,
            'voice_type': self.voice_type,
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
