import os
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path

class FileUtils:
    """Utility functions for file operations"""
    
    @staticmethod
    def create_directory(path):
        """Create directory if it doesn't exist"""
        os.makedirs(path, exist_ok=True)
        return path
    
    @staticmethod
    def get_file_size(file_path):
        """Get file size in bytes"""
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        return 0
    
    @staticmethod
    def get_file_extension(file_path):
        """Get file extension"""
        return os.path.splitext(file_path)[1].lower().lstrip('.')
    
    @staticmethod
    def safe_filename(filename):
        """Generate a safe filename"""
        import unicodedata
        filename = unicodedata.normalize('NFKD', filename)
        filename = filename.encode('ascii', 'ignore').decode('ascii')
        filename = ''.join(c if c.isalnum() or c in ('-', '_', '.') else '_' for c in filename)
        return filename
    
    @staticmethod
    def delete_file(file_path):
        """Delete a file safely"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")
        return False
    
    @staticmethod
    def delete_directory(directory_path):
        """Delete entire directory"""
        try:
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
                return True
        except Exception as e:
            print(f"Error deleting directory {directory_path}: {str(e)}")
        return False
    
    @staticmethod
    def cleanup_old_files(directory_path, hours=24):
        """Delete files older than specified hours"""
        if not os.path.exists(directory_path):
            return 0
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        deleted_count = 0
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                file_mtime = datetime.utcfromtimestamp(os.path.getmtime(file_path))
                if file_mtime < cutoff_time:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"Error cleaning up {file_path}: {str(e)}")
        
        return deleted_count
    
    @staticmethod
    def load_json(file_path):
        """Load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON from {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def save_json(file_path, data, indent=2):
        """Save data to JSON file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON to {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def file_exists(file_path):
        """Check if file exists"""
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    @staticmethod
    def list_files(directory_path, extension=None):
        """List files in directory"""
        files = []
        if not os.path.exists(directory_path):
            return files
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                if extension is None or filename.lower().endswith(extension.lower()):
                    files.append(file_path)
        
        return files
    
    @staticmethod
    def get_file_info(file_path):
        """Get file information"""
        if not os.path.exists(file_path):
            return None
        
        stat = os.stat(file_path)
        return {
            'path': file_path,
            'name': os.path.basename(file_path),
            'size': stat.st_size,
            'extension': FileUtils.get_file_extension(file_path),
            'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat()
        }
