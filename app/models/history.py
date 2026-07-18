from app import db
from datetime import datetime

class TranslationHistory(db.Model):
    """Model for storing translation history and metadata"""
    __tablename__ = 'translation_history'
    
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # download, asr, translate, tts, export
    status = db.Column(db.String(50), nullable=False)  # pending, processing, completed, failed
    input_data = db.Column(db.JSON, nullable=True)
    output_data = db.Column(db.JSON, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Float, nullable=True)  # execution time in seconds
    processing_details = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<TranslationHistory {self.id}: {self.action} - {self.status}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'video_id': self.video_id,
            'action': self.action,
            'status': self.status,
            'input_data': self.input_data,
            'output_data': self.output_data,
            'error_message': self.error_message,
            'duration': self.duration,
            'processing_details': self.processing_details,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
