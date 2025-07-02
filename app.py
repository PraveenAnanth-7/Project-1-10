import streamlit as st
import os
import tempfile
import shutil
from datetime import datetime
from processing.extract_audio import extract_audio_from_url
from processing.transcribe import transcribe_audio
from processing.summarize_and_generate import generate_content
from utils.file_manager import save_outputs, create_directories

def main():
    st.title("🎥 YouTube Content Optimizer")
    st.markdown("**AI-powered tool to generate summaries, hashtags, and titles from YouTube videos**")
    
    # Create necessary directories
    create_directories()
    
    # Input section
    st.header("📝 Input")
    youtube_url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")
    
    # Processing button
    if st.button("🚀 Process Video", type="primary"):
        if not youtube_url:
            st.error("Please enter a YouTube URL")
            return
            
        # Validate URL format
        if not ("youtube.com/watch" in youtube_url or "youtu.be/" in youtube_url):
            st.error("Please enter a valid YouTube URL")
            return
            
        process_video(youtube_url)

def process_video(url):
    """Process the YouTube video through the complete pipeline"""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Extract audio
        status_text.text("🎵 Extracting audio from YouTube video...")
        progress_bar.progress(20)
        
        audio_path = extract_audio_from_url(url)
        if not audio_path:
            st.error("Failed to extract audio from the video. Please check the URL.")
            return
            
        st.success("✅ Audio extracted successfully")
        
        # Step 2: Transcribe audio
        status_text.text("🎤 Transcribing audio to text...")
        progress_bar.progress(40)
        
        transcript = transcribe_audio(audio_path)
        if not transcript:
            st.error("Failed to transcribe audio")
            return
            
        st.success("✅ Audio transcribed successfully")
        
        # Step 3: Generate content using AI
        status_text.text("🤖 Generating summaries, hashtags, and titles...")
        progress_bar.progress(70)
        
        content = generate_content(transcript)
        if not content:
            st.error("Failed to generate content")
            return
            
        st.success("✅ Content generated successfully")
        
        # Step 4: Save outputs
        status_text.text("💾 Saving outputs...")
        progress_bar.progress(90)
        
        save_outputs(content, transcript)
        
        progress_bar.progress(100)
        status_text.text("🎉 Processing completed!")
        
        # Display results
        display_results(content, transcript)
        
        # Cleanup temporary audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def display_results(content, transcript):
    """Display the generated content results"""
    
    st.header("📊 Results")
    
    # Create tabs for different outputs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "🏷️ Hashtags", "📰 Titles", "📜 Transcript"])
    
    with tab1:
        st.subheader("Video Summary")
        st.markdown(content.get('summary', 'No summary generated'))
        
    with tab2:
        st.subheader("SEO Hashtags")
        hashtags = content.get('hashtags', [])
        if hashtags:
            # Display hashtags as tags
            hashtag_text = " ".join([f"#{tag.strip('#')}" for tag in hashtags])
            st.markdown(f"**{hashtag_text}**")
            
            # Copy button
            st.code(hashtag_text, language="text")
        else:
            st.write("No hashtags generated")
            
    with tab3:
        st.subheader("Title Suggestions")
        titles = content.get('titles', [])
        if titles:
            for i, title in enumerate(titles, 1):
                st.markdown(f"**{i}.** {title}")
        else:
            st.write("No titles generated")
            
    with tab4:
        st.subheader("Full Transcript")
        st.text_area("Transcript", transcript, height=300, disabled=True)
    
    # Download section
    st.header("💾 Download Files")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if os.path.exists("outputs/video_summary.md"):
            with open("outputs/video_summary.md", "r") as f:
                st.download_button(
                    "📝 Download Summary",
                    f.read(),
                    "video_summary.md",
                    "text/markdown"
                )
    
    with col2:
        if os.path.exists("outputs/hashtags.txt"):
            with open("outputs/hashtags.txt", "r") as f:
                st.download_button(
                    "🏷️ Download Hashtags",
                    f.read(),
                    "hashtags.txt",
                    "text/plain"
                )
    
    with col3:
        if os.path.exists("outputs/titles.txt"):
            with open("outputs/titles.txt", "r") as f:
                st.download_button(
                    "📰 Download Titles",
                    f.read(),
                    "titles.txt",
                    "text/plain"
                )

if __name__ == "__main__":
    main()
