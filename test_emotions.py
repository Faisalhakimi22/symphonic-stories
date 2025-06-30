#!/usr/bin/env python3
"""
Test script for emotion detection
"""

import sys
import os
import logging

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the emotion detector
from src.analysis.emotion_detector import EmotionDetector

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_emotion_detection():
    """Test the emotion detector with various inputs."""
    detector = EmotionDetector()
    
    test_texts = [
        "I'm so happy today! Everything is wonderful!",
        "I feel very sad and disappointed.",
        "This makes me so angry and frustrated!",
        "I'm really scared and worried about what might happen.",
        "Wow! I didn't expect that at all! That's amazing!",
        "It's just an ordinary day, nothing special."
    ]
    
    print("\n===== EMOTION DETECTION TEST =====\n")
    
    for text in test_texts:
        emotion, intensity = detector.analyze(text)
        valence, arousal = detector.analyze_valence_arousal(text)
        
        print(f"Text: {text}")
        print(f"  Emotion: {emotion} (intensity: {intensity:.2f})")
        print(f"  Valence: {valence:.2f}, Arousal: {arousal:.2f}")
        print()

if __name__ == "__main__":
    test_emotion_detection() 