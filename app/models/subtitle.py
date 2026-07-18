from app import db
from datetime import datetime

class Subtitle(db.Model):
    """Model for storing subtitle/caption information"""
    __tablename__ = 'subtitles'
    
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    index = db.Column(db.Integer, nullable=False)  # Line number
    start_time = db.Column(db.Float, nullable=False)  # in milliseconds
    end_time = db.Column(db.Float, nullable=False)  # in milliseconds
    original_text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text, nullable=True)
    source_language = db.Column(db.String(10), default='en')
    target_language = db.Column(db.String(10), default='vi')
    duration = db.Column(db.Float, nullable=True)  # end_time - start_time
    cps = db.Column(db.Float, nullable=True)  # characters per second
    voice_speed = db.Column(db.Float, default=1.0)  # 0.5x - 3.0x
    voice_type = db.Column(db.String(100), nullable=True)
    audio_file = db.Column(db.String(255), nullable=True)  # path to generated audio
    font_name = db.Column(db.String(100), default='Arial')
    font_size = db.Column(db.Integer, default=20)
    font_color = db.Column(db.String(7), default='#FFFFFF')  # hex color
    background_color = db.Column(db.String(7), default='#000000')
    is_edited = db.Column(db.Boolean, default=False)  # whether user edited this line
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Subtitle {self.id}: [{self.index}] {self.original_text[:50]}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'video_id': self.video_id,
            'index': self.index,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'original_text': self.original_text,
            'translated_text': self.translated_text,
            'source_language': self.source_language,
            'target_language': self.target_language,
            'duration': self.duration,
            'cps': self.cps,
            'voice_speed': self.voice_speed,
            'voice_type': self.voice_type,
            'font_name': self.font_name,
            'font_size': self.font_size,
            'font_color': self.font_color,
            'background_color': self.background_color,
            'is_edited': self.is_edited,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
