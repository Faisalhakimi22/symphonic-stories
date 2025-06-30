"""
Emotion Detector Module
Analyzes text to detect emotions and their intensities.
"""

import logging
import numpy as np
from transformers import pipeline

logger = logging.getLogger(__name__)

# Define the main emotion categories we'll use
EMOTION_CATEGORIES = {
    'joy': ['joy', 'happiness', 'excited', 'optimistic', 'proud', 'grateful'],
    'sadness': ['sadness', 'disappointment', 'grief', 'lonely', 'pessimistic'],
    'anger': ['anger', 'annoyance', 'disapproval', 'disgust'],
    'fear': ['fear', 'nervousness', 'anxiety', 'embarrassment'],
    'surprise': ['surprise', 'confusion', 'amazement', 'realization'],
    'neutral': ['neutral', 'calmness', 'relief']
}

# Reverse mapping to categorize detected emotions
EMOTION_MAPPING = {}
for category, emotions in EMOTION_CATEGORIES.items():
    for emotion in emotions:
        EMOTION_MAPPING[emotion] = category

class EmotionDetector:
    """
    Analyzes text to detect emotions and their intensities.
    Uses Hugging Face's emotion detection models.
    """
    
    def __init__(self, model_name="joeddav/distilbert-base-uncased-go-emotions-student", device=None):
        """
        Initialize the emotion detector.
        
        Args:
            model_name (str): Name of the Hugging Face model to use
            device (str): Device to run the model on ('cpu', 'cuda', etc.)
        """
        logger.info(f"Initializing EmotionDetector with model: {model_name}")
        try:
            # Initialize the emotion classification pipeline
            self.classifier = pipeline(
                "text-classification", 
                model=model_name, 
                top_k=5,  # Return top 5 emotions
                device=device
            )
            logger.info("Emotion classifier initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize emotion classifier: {e}")
            # Fallback to a dummy classifier for testing
            self.classifier = None
            logger.warning("Using dummy emotion classifier for testing")
    
    def analyze(self, text):
        """
        Analyze text to detect emotions and their intensities.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            tuple: (primary_emotion, intensity)
                primary_emotion (str): The primary detected emotion
                intensity (float): The intensity of the emotion (0.0 to 1.0)
        """
        if self.classifier is None:
            # Dummy implementation for testing
            logger.warning("Using dummy emotion analysis (no model loaded)")
            # Simple keyword-based emotion detection for testing
            text_lower = text.lower()
            if any(word in text_lower for word in ['happy', 'joy', 'glad', 'wonderful']):
                return 'joy', 0.8
            elif any(word in text_lower for word in ['sad', 'unhappy', 'sorrow', 'grief']):
                return 'sadness', 0.7
            elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'rage']):
                return 'anger', 0.9
            elif any(word in text_lower for word in ['afraid', 'scared', 'fear', 'terrified']):
                return 'fear', 0.6
            elif any(word in text_lower for word in ['surprise', 'amazed', 'astonished']):
                return 'surprise', 0.5
            else:
                return 'neutral', 0.3
        
        try:
            # Get emotion predictions
            results = self.classifier(text)
            
            if not results or not results[0]:
                logger.warning(f"No emotion detected for text: {text}")
                return 'neutral', 0.1
            
            # Process the results to get the primary emotion and its intensity
            emotions = {}
            for result in results[0]:
                label = result['label']
                score = result['score']
                
                # Map to our main categories
                category = EMOTION_MAPPING.get(label, 'neutral')
                
                # Aggregate scores for the same category
                if category in emotions:
                    emotions[category] = max(emotions[category], score)
                else:
                    emotions[category] = score
            
            # Find the primary emotion
            if not emotions:
                return 'neutral', 0.1
                
            primary_emotion = max(emotions, key=emotions.get)
            intensity = emotions[primary_emotion]
            
            logger.debug(f"Detected emotion: {primary_emotion} ({intensity:.2f})")
            return primary_emotion, intensity
            
        except Exception as e:
            logger.error(f"Error during emotion analysis: {e}")
            return 'neutral', 0.1
    
    def analyze_valence_arousal(self, text):
        """
        Analyze text to detect valence (positive/negative) and arousal (active/passive).
        
        Args:
            text (str): Text to analyze
            
        Returns:
            tuple: (valence, arousal)
                valence (float): -1.0 (negative) to 1.0 (positive)
                arousal (float): -1.0 (passive) to 1.0 (active)
        """
        # Map emotions to valence-arousal space
        emotion_va_map = {
            'joy': (0.8, 0.5),       # Positive valence, moderate arousal
            'sadness': (-0.8, -0.5), # Negative valence, low arousal
            'anger': (-0.5, 0.8),    # Negative valence, high arousal
            'fear': (-0.7, 0.7),     # Negative valence, high arousal
            'surprise': (0.1, 0.9),  # Neutral/slight positive valence, high arousal
            'neutral': (0.0, 0.0)    # Neutral valence, neutral arousal
        }
        
        # Get the primary emotion and intensity
        emotion, intensity = self.analyze(text)
        
        # Get the base valence and arousal for this emotion
        base_valence, base_arousal = emotion_va_map.get(emotion, (0.0, 0.0))
        
        # Scale by intensity
        valence = base_valence * intensity
        arousal = base_arousal * intensity
        
        return valence, arousal


# For testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    detector = EmotionDetector()
    
    test_texts = [
        "I'm so happy today! Everything is wonderful!",
        "I feel very sad and disappointed.",
        "This makes me so angry and frustrated!",
        "I'm really scared and worried about what might happen.",
        "Wow! I didn't expect that at all! That's amazing!",
        "It's just an ordinary day, nothing special."
    ]
    
    for text in test_texts:
        emotion, intensity = detector.analyze(text)
        valence, arousal = detector.analyze_valence_arousal(text)
        print(f"Text: {text}")
        print(f"  Emotion: {emotion} (intensity: {intensity:.2f})")
        print(f"  Valence: {valence:.2f}, Arousal: {arousal:.2f}")
        print() 