from faster_whisper import WhisperModel
import os
import streamlit as st
import tempfile

@st.cache_resource
def load_whisper_model():
    """Load and cache the Whisper model"""
    try:
        model = WhisperModel("base", device="cpu", compute_type="int8")
        return model
    except Exception as e:
        st.error(f"Error loading Whisper model: {str(e)}")
        return None

def transcribe_audio(audio_path):
    """
    Transcribe audio file to text using faster-whisper
    
    Args:
        audio_path (str): Path to audio file
        
    Returns:
        str: Transcribed text or None if failed
    """
    try:
        # Load model
        model = load_whisper_model()
        if not model:
            return None
        
        # Transcribe audio
        segments, info = model.transcribe(audio_path, beam_size=5)
        
        # Extract text from segments
        transcript = ""
        for segment in segments:
            transcript += segment.text + " "
        
        # Clean up transcript
        cleaned_transcript = clean_transcript(transcript.strip())
        
        return cleaned_transcript
        
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return None

def clean_transcript(transcript):
    """
    Clean and format the transcript
    
    Args:
        transcript (str): Raw transcript text
        
    Returns:
        str: Cleaned transcript
    """
    try:
        # Remove extra whitespace
        cleaned = " ".join(transcript.split())
        
        # Remove common filler words and artifacts
        filler_words = [
            " um ", " uh ", " ah ", " er ", " like ",
            " you know ", " I mean ", " basically ",
            " actually ", " literally "
        ]
        
        for filler in filler_words:
            cleaned = cleaned.replace(filler, " ")
        
        # Remove multiple spaces
        while "  " in cleaned:
            cleaned = cleaned.replace("  ", " ")
        
        # Capitalize first letter
        cleaned = cleaned.strip().capitalize()
        
        return cleaned
        
    except Exception as e:
        st.error(f"Error cleaning transcript: {str(e)}")
        return transcript

def save_transcript(transcript, filename="transcript.txt"):
    """
    Save transcript to file
    
    Args:
        transcript (str): Transcript text
        filename (str): Output filename
    """
    try:
        # Ensure input directory exists
        os.makedirs("input", exist_ok=True)
        
        filepath = os.path.join("input", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(transcript)
            
        return filepath
        
    except Exception as e:
        st.error(f"Error saving transcript: {str(e)}")
        return None

def transcribe_with_timestamps(audio_path):
    """
    Transcribe audio with timestamp information
    
    Args:
        audio_path (str): Path to audio file
        
    Returns:
        dict: Transcription result with timestamps
    """
    try:
        model = load_whisper_model()
        if not model:
            return None
        
        # Transcribe with word-level timestamps
        segments, info = model.transcribe(audio_path, word_timestamps=True)
        
        # Convert to dict format similar to original whisper
        result = {
            "segments": [
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text,
                    "words": [
                        {
                            "start": word.start,
                            "end": word.end,
                            "word": word.word,
                            "probability": word.probability
                        } for word in segment.words
                    ] if hasattr(segment, 'words') and segment.words else []
                } for segment in segments
            ],
            "language": info.language,
            "language_probability": info.language_probability
        }
        
        return result
        
    except Exception as e:
        st.error(f"Error transcribing with timestamps: {str(e)}")
        return None
