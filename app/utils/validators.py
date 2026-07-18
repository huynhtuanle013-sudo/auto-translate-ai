from flask import request
from functools import wraps
import os

class Validators:
    """Validation utility functions"""
    
    @staticmethod
    def validate_file_extension(filename, allowed_extensions):
        """Validate if file has allowed extension"""
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in allowed_extensions
    
    @staticmethod
    def validate_file_size(file_path, max_size):
        """Validate if file size is within limit"""
        if not os.path.exists(file_path):
            return False
        file_size = os.path.getsize(file_path)
        return file_size <= max_size
    
    @staticmethod
    def validate_video_url(url):
        """Validate if URL is valid video URL"""
        valid_domains = [
            'youtube.com', 'youtu.be',
            'tiktok.com', 'vm.tiktok.com',
            'bilibili.com',
            'facebook.com', 'fb.watch',
            'twitter.com', 'x.com',
            'instagram.com'
        ]
        return any(domain in url.lower() for domain in valid_domains)
    
    @staticmethod
    def validate_language_code(code):
        """Validate language code"""
        valid_codes = ['vi', 'en', 'es', 'fr', 'de', 'zh', 'ja', 'ko', 'th', 'id']
        return code.lower() in valid_codes
    
    @staticmethod
    def validate_translation_style(style):
        """Validate translation style"""
        valid_styles = ['precise', 'natural', 'entertainment', 'advertising', 'cinema']
        return style.lower() in valid_styles
    
    @staticmethod
    def validate_subtitle_format(format_type):
        """Validate subtitle export format"""
        valid_formats = ['srt', 'vtt', 'ass', 'txt', 'json', 'csv', 'lrc']
        return format_type.lower() in valid_formats
    
    @staticmethod
    def validate_resolution(resolution):
        """Validate video resolution"""
        valid_resolutions = ['2160p', '1440p', '1080p', '720p', '480p', '360p']
        return resolution in valid_resolutions
    
    @staticmethod
    def validate_audio_bitrate(bitrate):
        """Validate audio bitrate"""
        valid_bitrates = ['320k', '256k', '192k', '128k', '96k', '64k']
        return bitrate in valid_bitrates
    
    @staticmethod
    def validate_crop_coordinates(x, y, w, h, video_width, video_height):
        """Validate crop region coordinates"""
        if x < 0 or y < 0 or w <= 0 or h <= 0:
            return False
        if x + w > video_width or y + h > video_height:
            return False
        return True
    
    @staticmethod
    def validate_voice_speed(speed):
        """Validate voice speed multiplier"""
        return 0.5 <= float(speed) <= 3.0

def require_json(f):
    """Decorator to require JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return {'error': 'Content-Type must be application/json'}, 400
        return f(*args, **kwargs)
    return decorated_function

def validate_request_json(required_fields):
    """Decorator to validate required JSON fields"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json(force=True)
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return {'error': f'Missing required fields: {missing_fields}'}, 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator
