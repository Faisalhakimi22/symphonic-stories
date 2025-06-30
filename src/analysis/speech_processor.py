"""
Speech Processor Module
Handles speech-to-text conversion using various backends.
"""

import os
import logging
import numpy as np
from transformers import pipeline

logger = logging.getLogger(__name__)

class SpeechProcessor:
    """
    Handles speech-to-text conversion using various backends.
    Currently supports Hugging Face's Whisper model.
    """
    
    def __init__(self, model_name="openai/whisper-small", device=None):
        """
        Initialize the speech processor.
        
        Args:
            model_name (str): Name of the Hugging Face model to use
            device (str): Device to run the model on ('cpu', 'cuda', etc.)
        """
        logger.info(f"Initializing SpeechProcessor with model: {model_name}")
        try:
            # Initialize the speech-to-text pipeline
            self.speech_to_text = pipeline(
                "automatic-speech-recognition", 
                model=model_name,
                device=device
            )
            logger.info("Speech-to-text pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize speech-to-text pipeline: {e}")
            # Fallback to a dummy processor for testing
            self.speech_to_text = None
            logger.warning("Using dummy speech processor for testing")
    
    def transcribe(self, audio_data):
        """
        Transcribe audio data to text.
        
        Args:
            audio_data: Audio data as numpy array or path to audio file
            
        Returns:
            str: Transcribed text
        """
        if self.speech_to_text is None:
            # Dummy implementation for testing
            logger.warning("Using dummy transcription (no model loaded)")
            if isinstance(audio_data, str):
                # If it's a string, assume it's already text for testing
                return audio_data
            return "This is a dummy transcription for testing."
        
        try:
            # Process the audio data
            if isinstance(audio_data, str):
                # If it's a string, assume it's a file path
                result = self.speech_to_text(audio_data)
            else:
                # Otherwise, assume it's audio data
                result = self.speech_to_text(audio_data)
            
            # Extract the transcribed text
            transcribed_text = result.get("text", "")
            logger.debug(f"Transcribed: {transcribed_text}")
            return transcribed_text
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return ""
    
    def transcribe_file(self, file_path):
        """
        Transcribe an audio file to text.
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        if not os.path.exists(file_path):
            logger.error(f"Audio file not found: {file_path}")
            return ""
        
        return self.transcribe(file_path)


# For testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    processor = SpeechProcessor()
    
    # Test with a dummy string (for testing without a model)
    text = processor.transcribe("The sun rose with gentle warmth and promise.")
    print(f"Transcribed: {text}") 