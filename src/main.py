#!/usr/bin/env python3
"""
Symphonic Stories - Main Application
Translates voice into musical and visual art based on emotional content.
"""

import os
import sys
import time
import threading
import queue
import logging
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from src.analysis.speech_processor import SpeechProcessor
from src.analysis.emotion_detector import EmotionDetector
from src.music.music_generator import MusicGenerator
from src.visual.visual_generator import VisualGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__, 
            static_folder='../static',
            template_folder='../static/templates')
app.config['SECRET_KEY'] = 'symphonic-stories-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Create message queue for communication between components
message_queue = queue.Queue()

# Initialize components
speech_processor = SpeechProcessor()
emotion_detector = EmotionDetector()
music_generator = MusicGenerator()
visual_generator = VisualGenerator()

def process_audio_stream():
    """Background thread for processing audio and generating content."""
    logger.info("Starting audio processing thread")
    while True:
        try:
            # Get audio data from the queue
            audio_data = message_queue.get(timeout=1.0)
            if audio_data is None:
                # None is our signal to exit
                break
                
            # Process speech to text
            text = speech_processor.transcribe(audio_data)
            if not text:
                continue
                
            # Analyze emotion
            emotion, intensity = emotion_detector.analyze(text)
            
            # Generate music based on emotion
            music_params = music_generator.map_emotion(emotion, intensity)
            music_data = music_generator.generate(music_params)
            
            # Generate visuals based on emotion
            visual_params = visual_generator.map_emotion(emotion, intensity)
            visual_data = visual_generator.generate(visual_params)
            
            # Send results to clients
            result = {
                'text': text,
                'emotion': emotion,
                'intensity': intensity,
                'music_data': music_data,
                'visual_data': visual_data
            }
            socketio.emit('story_update', result)
            logger.info(f"Processed: '{text}' -> {emotion} ({intensity:.2f})")
            
        except queue.Empty:
            continue
        except Exception as e:
            logger.error(f"Error in processing thread: {e}")

@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('audio_data')
def handle_audio_data(data):
    """Handle incoming audio data from clients."""
    message_queue.put(data)

@socketio.on('text_input')
def handle_text_input(data):
    """Handle text input for testing without audio."""
    text = data.get('text', '')
    if text:
        # Analyze emotion directly from text
        emotion, intensity = emotion_detector.analyze(text)
        
        # Generate music based on emotion
        music_params = music_generator.map_emotion(emotion, intensity)
        music_data = music_generator.generate(music_params)
        
        # Generate visuals based on emotion
        visual_params = visual_generator.map_emotion(emotion, intensity)
        visual_data = visual_generator.generate(visual_params)
        
        # Send results to clients
        result = {
            'text': text,
            'emotion': emotion,
            'intensity': intensity,
            'music_data': music_data,
            'visual_data': visual_data
        }
        socketio.emit('story_update', result)
        logger.info(f"Processed text: '{text}' -> {emotion} ({intensity:.2f})")

def main():
    """Main application entry point."""
    logger.info("Starting Symphonic Stories application")
    
    # Start the audio processing thread
    processing_thread = threading.Thread(target=process_audio_stream)
    processing_thread.daemon = True
    processing_thread.start()
    
    # Start the Flask-SocketIO server
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Server starting on {host}:{port}")
    socketio.run(app, host=host, port=port, debug=debug)
    
    # Clean up
    message_queue.put(None)  # Signal the processing thread to exit
    processing_thread.join()
    logger.info("Application shutdown complete")

if __name__ == '__main__':
    main() 