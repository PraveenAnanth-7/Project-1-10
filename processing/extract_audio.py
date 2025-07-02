import os
import tempfile
from pytube import YouTube
import yt_dlp
import streamlit as st

def extract_audio_from_url(url):
    """
    Extract audio from YouTube URL using yt-dlp only
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Path to extracted audio file or None if failed
    """
    return extract_audio_with_ytdlp(url)

def extract_audio_with_ytdlp(url):
    """
    Extract audio from YouTube URL using yt-dlp as fallback
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Path to extracted audio file or None if failed
    """
    try:
        # Create temporary directory
        temp_dir = tempfile.gettempdir()
        
        # Generate unique filename
        filename = f"audio_ytdlp_{abs(hash(url)) % 10000}"
        output_path = os.path.join(temp_dir, f"{filename}.%(ext)s")
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'extractaudio': True,
            'audioformat': 'mp3',
            'embed_subs': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'no_warnings': True,
            'quiet': True
        }
        
        # Download audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find the downloaded file
        for file in os.listdir(temp_dir):
            if file.startswith(f"audio_ytdlp_{abs(hash(url)) % 10000}"):
                return os.path.join(temp_dir, file)
        
        return None
        
    except Exception as e:
        st.error(f"Error extracting audio with yt-dlp: {str(e)}")
        return None

def extract_audio_from_file(file_path):
    """
    Extract audio from local video file using FFmpeg
    
    Args:
        file_path (str): Path to video file
        
    Returns:
        str: Path to extracted audio file or None if failed
    """
    try:
        import subprocess
        
        # Save audio to temporary file
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "extracted_audio.wav")
        
        # Use FFmpeg to extract audio (if available)
        try:
            subprocess.run([
                'ffmpeg', '-i', file_path, 
                '-vn', '-acodec', 'pcm_s16le', 
                '-ar', '44100', '-ac', '2', 
                audio_path, '-y'
            ], check=True, capture_output=True)
            return audio_path
        except (subprocess.CalledProcessError, FileNotFoundError):
            st.error("FFmpeg not available. Cannot extract audio from local video files.")
            st.info("For local video files, please use the YouTube URL option instead.")
            return None
        
    except Exception as e:
        st.error(f"Error extracting audio from file: {str(e)}")
        return None

def get_video_info(url):
    """
    Get video information from YouTube URL
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        dict: Video information or None if failed
    """
    try:
        yt = YouTube(url)
        
        info = {
            'title': yt.title,
            'author': yt.author,
            'length': yt.length,
            'views': yt.views,
            'description': yt.description[:500] + "..." if len(yt.description) > 500 else yt.description
        }
        
        return info
        
    except Exception as e:
        st.error(f"Error getting video info: {str(e)}")
        return None
