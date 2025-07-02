import os
from google import genai
from google.genai import types
import streamlit as st

# Initialize Gemini client
def get_gemini_client():
    """Initialize and return Gemini client"""
    api_key = os.environ.get("GEMINI_API_KEY", "default_key")
    return genai.Client(api_key=api_key)

def load_prompt(prompt_file):
    """Load prompt template from file"""
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        st.error(f"Error loading prompt from {prompt_file}: {str(e)}")
        return None

def generate_summary(transcript):
    """
    Generate video summary using Gemini Flash
    
    Args:
        transcript (str): Video transcript
        
    Returns:
        str: Generated summary
    """
    try:
        client = get_gemini_client()
        
        # Load summary prompt
        prompt_template = load_prompt("prompts/summary_prompt.txt")
        if not prompt_template:
            prompt_template = """Given the following transcript of a YouTube video, write a concise summary in 3–4 sentences.

Transcript:
"""

        prompt = f"{prompt_template}\n\"\"\"\n{transcript}\n\"\"\""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        return response.text or "Failed to generate summary"
        
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return "Error generating summary"

def generate_hashtags(transcript):
    """
    Generate SEO hashtags using Gemini Flash
    
    Args:
        transcript (str): Video transcript
        
    Returns:
        list: List of hashtags
    """
    try:
        client = get_gemini_client()
        
        # Load hashtags prompt
        prompt_template = load_prompt("prompts/hashtags_prompt.txt")
        if not prompt_template:
            prompt_template = """Extract the top 10 SEO-optimized hashtags from this YouTube video transcript. Focus on relevancy, search trends, and audience discoverability. Return only the hashtags, one per line, with # prefix.

Transcript:
"""

        prompt = f"{prompt_template}\n\"\"\"\n{transcript}\n\"\"\""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if response.text:
            # Parse hashtags from response
            hashtags = []
            for line in response.text.split('\n'):
                line = line.strip()
                if line and (line.startswith('#') or line.startswith('-')):
                    # Clean up hashtag
                    hashtag = line.replace('-', '').strip()
                    if not hashtag.startswith('#'):
                        hashtag = '#' + hashtag
                    hashtags.append(hashtag)
            
            return hashtags[:10]  # Return max 10 hashtags
        
        return []
        
    except Exception as e:
        st.error(f"Error generating hashtags: {str(e)}")
        return []

def generate_titles(transcript):
    """
    Generate title suggestions using Gemini Flash
    
    Args:
        transcript (str): Video transcript
        
    Returns:
        list: List of title suggestions
    """
    try:
        client = get_gemini_client()
        
        # Load titles prompt
        prompt_template = load_prompt("prompts/titles_prompt.txt")
        if not prompt_template:
            prompt_template = """Generate 5 catchy, YouTube-optimized video titles based on this transcript. Include curiosity, clarity, and trending language. Make them engaging and click-worthy.

Transcript:
"""

        prompt = f"{prompt_template}\n\"\"\"\n{transcript}\n\"\"\""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if response.text:
            # Parse titles from response
            titles = []
            for line in response.text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    # Clean up title
                    title = line
                    # Remove numbering
                    if line[0].isdigit():
                        title = '. '.join(line.split('. ')[1:])
                    elif line.startswith('-'):
                        title = line[1:].strip()
                    
                    if title:
                        titles.append(title)
                elif line and not any(x in line.lower() for x in ['title', 'suggestion', 'here are']):
                    # Handle plain titles without numbering
                    titles.append(line)
            
            return titles[:5]  # Return max 5 titles
        
        return []
        
    except Exception as e:
        st.error(f"Error generating titles: {str(e)}")
        return []

def generate_content(transcript):
    """
    Generate all content types (summary, hashtags, titles)
    
    Args:
        transcript (str): Video transcript
        
    Returns:
        dict: Dictionary containing all generated content
    """
    try:
        content = {}
        
        # Generate summary
        content['summary'] = generate_summary(transcript)
        
        # Generate hashtags
        content['hashtags'] = generate_hashtags(transcript)
        
        # Generate titles
        content['titles'] = generate_titles(transcript)
        
        return content
        
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return {}

def generate_chapters(transcript):
    """
    Generate suggested video chapters/timestamps
    
    Args:
        transcript (str): Video transcript with timestamps
        
    Returns:
        list: List of chapter suggestions
    """
    try:
        client = get_gemini_client()
        
        prompt = f"""Based on this video transcript, suggest 5-8 chapter divisions with descriptive titles. Format as:
        
0:00 - Introduction
2:30 - Main Topic
5:15 - Key Points
etc.

Transcript:
\"\"\"{transcript}\"\"\""""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if response.text:
            chapters = []
            for line in response.text.split('\n'):
                line = line.strip()
                if ':' in line and any(char.isdigit() for char in line):
                    chapters.append(line)
            
            return chapters
        
        return []
        
    except Exception as e:
        st.error(f"Error generating chapters: {str(e)}")
        return []
