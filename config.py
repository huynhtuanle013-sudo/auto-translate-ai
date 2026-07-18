import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///video_translator.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp', 'uploads')
    VIDEO_TEMP_FOLDER = os.path.join(os.getcwd(), 'temp', 'videos')
    AUDIO_TEMP_FOLDER = os.path.join(os.getcwd(), 'temp', 'audio')
    EXPORTS_FOLDER = os.path.join(os.getcwd(), 'exports')
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # CapCut API Settings
    CAPCUT_API_BASE_URL = 'https://api.capcut.com'
    CAPCUT_DEVICE_ID = os.getenv('CAPCUT_DEVICE_ID', '')
    CAPCUT_ACCESS_TOKEN = os.getenv('CAPCUT_ACCESS_TOKEN', '')
    
    # Video settings
    MAX_VIDEO_SIZE = 5 * 1024 * 1024 * 1024  # 5GB
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mkv', 'webm', 'mov', 'flv', 'avi'}
    SUPPORTED_PLATFORMS = ['youtube', 'tiktok', 'bilibili', 'facebook', 'twitter', 'instagram']
    
    # Audio settings
    AUDIO_BITRATES = {'high': '320k', 'medium': '256k', 'low': '128k'}
    DEFAULT_AUDIO_BITRATE = 'high'
    
    # Video resolutions
    AVAILABLE_RESOLUTIONS = ['2160p', '1440p', '1080p', '720p', '480p', '360p']
    DEFAULT_RESOLUTION = '1080p'
    
    # Celery settings
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True
    
    # SocketIO settings
    SOCKETIO_MESSAGE_QUEUE = os.getenv('SOCKETIO_MESSAGE_QUEUE', 'redis://localhost:6379/3')
    
    # Subtitle settings
    SUBTITLE_LANGUAGES = ['vi', 'en', 'es', 'fr', 'de', 'zh', 'ja', 'ko']
    DEFAULT_SUBTITLE_LANGUAGE = 'vi'
    
    # Translation styles
    TRANSLATION_STYLES = {
        'precise': 'Dịch sát nghĩa đen, nghiêm túc (Phù hợp phóng sự, tin tức, tài liệu)',
        'natural': 'Dịch thoát ý, mượt mà (Phù hợp hội thoại đời sống, vlog cá nhân)',
        'entertainment': 'Từ ngữ phóng khoáng, bắt trend, hài hước (Phù hợp video meme, TikTok)',
        'advertising': 'Ngôn từ lôi cuốn, tạo điểm nhấn (Phù hợp video sản phẩm)',
        'cinema': 'Giữ nguyên sắc thái điện ảnh, dịch trùng khớp biểu cảm'
    }
    
    # Subtitle export formats
    SUBTITLE_EXPORT_FORMATS = ['srt', 'vtt', 'ass', 'txt', 'json', 'csv', 'lrc']
    
    # File cleanup
    TEMP_FILE_RETENTION_HOURS = 24
    
    # FFmpeg path
    FFMPEG_PATH = os.getenv('FFMPEG_PATH', 'ffmpeg')
    FFPROBE_PATH = os.getenv('FFPROBE_PATH', 'ffprobe')
    
    # Tesseract OCR path (optional)
    TESSERACT_PATH = os.getenv('TESSERACT_PATH', None)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
