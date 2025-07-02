import os
import json
from datetime import datetime
import streamlit as st

def create_directories():
    """Create necessary directories for the application"""
    directories = [
        "input",
        "processing", 
        "prompts",
        "outputs",
        "temp"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def save_outputs(content, transcript):
    """
    Save all generated content to files
    
    Args:
        content (dict): Generated content (summary, hashtags, titles)
        transcript (str): Original transcript
    """
    try:
        # Ensure outputs directory exists
        os.makedirs("outputs", exist_ok=True)
        
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save summary as markdown
        if content.get('summary'):
            summary_path = "outputs/video_summary.md"
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(f"# Video Summary\n\n")
                f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"{content['summary']}\n\n")
                
                # Add hashtags to summary
                if content.get('hashtags'):
                    f.write(f"## Hashtags\n\n")
                    for hashtag in content['hashtags']:
                        f.write(f"{hashtag} ")
                    f.write(f"\n\n")
                
                # Add titles to summary
                if content.get('titles'):
                    f.write(f"## Title Suggestions\n\n")
                    for i, title in enumerate(content['titles'], 1):
                        f.write(f"{i}. {title}\n")
        
        # Save hashtags
        if content.get('hashtags'):
            hashtags_path = "outputs/hashtags.txt"
            with open(hashtags_path, 'w', encoding='utf-8') as f:
                for hashtag in content['hashtags']:
                    f.write(f"{hashtag}\n")
        
        # Save titles
        if content.get('titles'):
            titles_path = "outputs/titles.txt"
            with open(titles_path, 'w', encoding='utf-8') as f:
                for i, title in enumerate(content['titles'], 1):
                    f.write(f"{i}. {title}\n")
        
        # Save transcript
        transcript_path = "outputs/transcript.txt"
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(f"Video Transcript\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n\n")
            f.write(transcript)
        
        # Save all data as JSON for programmatic access
        json_path = "outputs/content.json"
        output_data = {
            'timestamp': timestamp,
            'summary': content.get('summary', ''),
            'hashtags': content.get('hashtags', []),
            'titles': content.get('titles', []),
            'transcript': transcript
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        st.success(f"✅ All outputs saved successfully!")
        
    except Exception as e:
        st.error(f"Error saving outputs: {str(e)}")

def load_previous_results():
    """Load previous processing results if available"""
    try:
        json_path = "outputs/content.json"
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        st.error(f"Error loading previous results: {str(e)}")
        return None

def cleanup_temp_files():
    """Clean up temporary files"""
    try:
        temp_dir = "temp"
        if os.path.exists(temp_dir):
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    except Exception as e:
        st.error(f"Error cleaning up temp files: {str(e)}")

def save_video_url(url):
    """Save the processed video URL for reference"""
    try:
        os.makedirs("input", exist_ok=True)
        url_path = "input/video_url.txt"
        
        with open(url_path, 'w', encoding='utf-8') as f:
            f.write(f"Video URL: {url}\n")
            f.write(f"Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
    except Exception as e:
        st.error(f"Error saving video URL: {str(e)}")

def get_file_info(file_path):
    """Get file information (size, modification time)"""
    try:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'exists': True
            }
        return {'exists': False}
    except Exception as e:
        return {'exists': False, 'error': str(e)}
