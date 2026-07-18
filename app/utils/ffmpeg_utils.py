import os
import subprocess
import json
from pathlib import Path

class FFmpegUtils:
    """Utility functions for FFmpeg operations"""
    
    def __init__(self, ffmpeg_path='ffmpeg', ffprobe_path='ffprobe'):
        self.ffmpeg_path = ffmpeg_path
        self.ffprobe_path = ffprobe_path
    
    def get_video_info(self, video_path):
        """Get detailed video information using ffprobe"""
        try:
            cmd = [
                self.ffprobe_path,
                '-v', 'error',
                '-show_format',
                '-show_streams',
                '-print_format', 'json',
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return None
    
    def get_duration(self, video_path):
        """Get video duration in seconds"""
        info = self.get_video_info(video_path)
        if info and 'format' in info and 'duration' in info['format']:
            return float(info['format']['duration'])
        return 0
    
    def get_dimensions(self, video_path):
        """Get video dimensions (width, height)"""
        info = self.get_video_info(video_path)
        if info and 'streams' in info:
            for stream in info['streams']:
                if stream.get('codec_type') == 'video':
                    return (stream.get('width'), stream.get('height'))
        return (0, 0)
    
    def get_fps(self, video_path):
        """Get video FPS (frames per second)"""
        info = self.get_video_info(video_path)
        if info and 'streams' in info:
            for stream in info['streams']:
                if stream.get('codec_type') == 'video' and 'r_frame_rate' in stream:
                    fps_str = stream['r_frame_rate']
                    if '/' in fps_str:
                        num, den = map(int, fps_str.split('/'))
                        return num / den
        return 30
    
    def extract_audio(self, video_path, audio_path, bitrate='192k'):
        """Extract audio from video"""
        try:
            cmd = [
                self.ffmpeg_path,
                '-i', video_path,
                '-q:a', '0',
                '-map', 'a',
                '-b:a', bitrate,
                '-y',
                audio_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=300)
            return os.path.exists(audio_path)
        except Exception as e:
            print(f"Error extracting audio: {str(e)}")
            return False
    
    def mux_video_audio_subtitle(self, video_path, audio_path, subtitle_path, output_path):
        """Mux video, audio, and subtitle into single file"""
        try:
            cmd = [
                self.ffmpeg_path,
                '-i', video_path,
                '-i', audio_path,
                '-i', subtitle_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-c:s', 'mov_text',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-map', '2:s:0',
                '-y',
                output_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=600)
            return os.path.exists(output_path)
        except Exception as e:
            print(f"Error muxing files: {str(e)}")
            return False
    
    def apply_blur_to_region(self, video_path, output_path, x, y, w, h, blur_type='gaussian'):
        """Apply blur effect to specific region in video"""
        try:
            if blur_type == 'gaussian':
                blur_filter = f"boxblur=lr=20:lh=20"
            elif blur_type == 'pixelate':
                blur_filter = f"pixelize=w=10:h=10"
            else:
                blur_filter = f"boxblur=lr=10:lh=10"
            
            crop_filter = f"crop=w={w}:h={h}:x={x}:y={y}"
            cmd = [
                self.ffmpeg_path,
                '-i', video_path,
                '-vf', f"[0:v]split[main][blur];[blur]{crop_filter},{blur_filter}[blurred];[main][blurred]overlay=x={x}:y={y}",
                '-c:a', 'copy',
                '-y',
                output_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=600)
            return os.path.exists(output_path)
        except Exception as e:
            print(f"Error applying blur: {str(e)}")
            return False
    
    def add_watermark(self, video_path, watermark_path, output_path, x=10, y=10, scale='w=100:h=-1'):
        """Add watermark/logo to video"""
        try:
            cmd = [
                self.ffmpeg_path,
                '-i', video_path,
                '-i', watermark_path,
                '-filter_complex', f"[1:v]scale={scale}[watermark];[0:v][watermark]overlay=x={x}:y={y}:enable='between(t\,0\,100)'",
                '-c:a', 'copy',
                '-y',
                output_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=600)
            return os.path.exists(output_path)
        except Exception as e:
            print(f"Error adding watermark: {str(e)}")
            return False
    
    def hardcode_subtitles(self, video_path, subtitle_path, output_path, font_path=None):
        """Burn subtitles into video"""
        try:
            subtitle_filter = f"subtitles={subtitle_path}"
            if font_path:
                subtitle_filter += f":fontfile={font_path}"
            
            cmd = [
                self.ffmpeg_path,
                '-i', video_path,
                '-vf', subtitle_filter,
                '-c:a', 'copy',
                '-y',
                output_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=600)
            return os.path.exists(output_path)
        except Exception as e:
            print(f"Error hardcoding subtitles: {str(e)}")
            return False
    
    def convert_video_format(self, input_path, output_path, codec='libx264', preset='medium'):
        """Convert video to different format/codec"""
        try:
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-c:v', codec,
                '-preset', preset,
                '-c:a', 'aac',
                '-y',
                output_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=600)
            return os.path.exists(output_path)
        except Exception as e:
            print(f"Error converting video: {str(e)}")
            return False
    
    def resize_video(self, input_path, output_path, width=-1, height=720):
        """Resize video to specified dimensions"""
        try:
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-vf', f"scale={width}:{height}",
                '-c:a', 'copy',
                '-y',
                output_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=600)
            return os.path.exists(output_path)
        except Exception as e:
            print(f"Error resizing video: {str(e)}")
            return False
