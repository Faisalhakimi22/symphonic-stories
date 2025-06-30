"""
Music Generator Module
Generates music based on detected emotions.
"""

import os
import logging
import json
import numpy as np
import time
from collections import defaultdict

logger = logging.getLogger(__name__)

# Define emotion to music mapping
EMOTION_MUSIC_MAPPING = {
    'joy': {
        'key': 'C',
        'scale': 'lydian',
        'tempo': 120,
        'instruments': ['piano', 'strings', 'glockenspiel'],
        'dynamics': 'mf',
        'articulation': 'legato',
        'density': 0.7
    },
    'sadness': {
        'key': 'D',
        'scale': 'aeolian',
        'tempo': 70,
        'instruments': ['cello', 'piano', 'pad'],
        'dynamics': 'p',
        'articulation': 'legato',
        'density': 0.4
    },
    'anger': {
        'key': 'E',
        'scale': 'locrian',
        'tempo': 160,
        'instruments': ['brass', 'drums', 'distorted_guitar'],
        'dynamics': 'ff',
        'articulation': 'staccato',
        'density': 0.8
    },
    'fear': {
        'key': 'F#',
        'scale': 'phrygian',
        'tempo': 90,
        'instruments': ['tremolo_strings', 'vibes', 'bass'],
        'dynamics': 'mp',
        'articulation': 'tremolo',
        'density': 0.5
    },
    'surprise': {
        'key': 'G',
        'scale': 'whole_tone',
        'tempo': 110,
        'instruments': ['piccolo', 'bells', 'harp'],
        'dynamics': 'mf',
        'articulation': 'staccato',
        'density': 0.6
    },
    'neutral': {
        'key': 'A',
        'scale': 'ionian',
        'tempo': 90,
        'instruments': ['piano', 'strings', 'guitar'],
        'dynamics': 'mp',
        'articulation': 'normal',
        'density': 0.5
    }
}

class MusicGenerator:
    """
    Generates music based on detected emotions.
    """
    
    def __init__(self):
        """
        Initialize the music generator.
        """
        logger.info("Initializing MusicGenerator")
        # Track the current musical state
        self.current_state = {
            'key': 'C',
            'scale': 'ionian',
            'tempo': 90,
            'instruments': ['piano', 'strings'],
            'dynamics': 'mp',
            'articulation': 'normal',
            'density': 0.5,
            'last_update': time.time()
        }
        
        # For smooth transitions
        self.target_state = self.current_state.copy()
        
        # Create a history of generated music for continuity
        self.history = []
        
        # Load any custom mappings if available
        self._load_custom_mappings()
    
    def _load_custom_mappings(self):
        """Load custom emotion-to-music mappings if available."""
        mapping_file = os.path.join(os.path.dirname(__file__), 'emotion_music_mapping.json')
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r') as f:
                    custom_mappings = json.load(f)
                    # Update the default mappings with custom ones
                    for emotion, mapping in custom_mappings.items():
                        if emotion in EMOTION_MUSIC_MAPPING:
                            EMOTION_MUSIC_MAPPING[emotion].update(mapping)
                logger.info("Loaded custom emotion-to-music mappings")
            except Exception as e:
                logger.error(f"Error loading custom mappings: {e}")
    
    def map_emotion(self, emotion, intensity):
        """
        Map an emotion to music parameters.
        
        Args:
            emotion (str): The detected emotion
            intensity (float): The intensity of the emotion (0.0 to 1.0)
            
        Returns:
            dict: Music parameters
        """
        # Get the base mapping for this emotion
        base_mapping = EMOTION_MUSIC_MAPPING.get(emotion, EMOTION_MUSIC_MAPPING['neutral'])
        
        # Create a copy to modify
        music_params = base_mapping.copy()
        
        # Adjust parameters based on intensity
        music_params['tempo'] = int(base_mapping['tempo'] * (0.8 + 0.4 * intensity))
        music_params['density'] = base_mapping['density'] * intensity
        
        # Add the emotion and intensity to the parameters
        music_params['emotion'] = emotion
        music_params['intensity'] = intensity
        
        # Update the target state
        self.target_state = music_params.copy()
        self.target_state['last_update'] = time.time()
        
        logger.debug(f"Mapped {emotion} ({intensity:.2f}) to music parameters: {music_params}")
        return music_params
    
    def generate(self, music_params):
        """
        Generate music based on the provided parameters.
        
        Args:
            music_params (dict): Music parameters
            
        Returns:
            dict: Generated music data (in a format suitable for the client)
        """
        # In a real implementation, this would generate actual music
        # For now, we'll just return the parameters for the client to use
        
        # Smooth transition from current state to target state
        self._update_current_state()
        
        # Add to history
        self.history.append(music_params)
        if len(self.history) > 10:
            self.history.pop(0)
        
        # For demonstration, return the parameters that would be used to generate music
        result = {
            'key': music_params['key'],
            'scale': music_params['scale'],
            'tempo': music_params['tempo'],
            'instruments': music_params['instruments'],
            'dynamics': music_params['dynamics'],
            'emotion': music_params.get('emotion', 'neutral'),
            'timestamp': time.time()
        }
        
        logger.debug(f"Generated music with parameters: {result}")
        return result
    
    def _update_current_state(self):
        """Update the current state with a smooth transition to the target state."""
        # Calculate how much time has passed since the last update
        now = time.time()
        elapsed = now - self.current_state['last_update']
        
        # Simple linear interpolation for continuous parameters
        # In a real implementation, this would be more sophisticated
        alpha = min(1.0, elapsed / 2.0)  # 2-second transition
        
        self.current_state['tempo'] = int(
            self.current_state['tempo'] * (1 - alpha) + 
            self.target_state['tempo'] * alpha
        )
        
        self.current_state['density'] = (
            self.current_state['density'] * (1 - alpha) + 
            self.target_state['density'] * alpha
        )
        
        # For discrete parameters, change if we're more than halfway through the transition
        if alpha > 0.5:
            self.current_state['key'] = self.target_state['key']
            self.current_state['scale'] = self.target_state['scale']
            self.current_state['instruments'] = self.target_state['instruments']
            self.current_state['dynamics'] = self.target_state['dynamics']
            self.current_state['articulation'] = self.target_state['articulation']
        
        self.current_state['last_update'] = now
    
    def get_chord_progression(self, key, scale):
        """
        Generate a chord progression based on the key and scale.
        
        Args:
            key (str): The musical key
            scale (str): The musical scale
            
        Returns:
            list: A list of chords
        """
        # Define common chord progressions for different scales
        progressions = {
            'ionian': ['I', 'IV', 'V', 'I'],
            'aeolian': ['i', 'VI', 'VII', 'i'],
            'dorian': ['i', 'IV', 'i', 'VII'],
            'phrygian': ['i', 'II', 'VII', 'i'],
            'lydian': ['I', 'II', 'VII', 'I'],
            'mixolydian': ['I', 'VII', 'IV', 'I'],
            'locrian': ['i', 'VII', 'VI', 'i'],
            'whole_tone': ['I+', 'III+', 'V+', 'VII+']
        }
        
        # Get the progression for this scale
        progression = progressions.get(scale, progressions['ionian'])
        
        # In a real implementation, we would translate these to actual chords
        # based on the key, but for now we'll just return the progression
        return progression


# For testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generator = MusicGenerator()
    
    # Test with different emotions
    emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'neutral']
    for emotion in emotions:
        params = generator.map_emotion(emotion, 0.8)
        result = generator.generate(params)
        print(f"Emotion: {emotion}")
        print(f"  Music: {result}")
        print(f"  Chord Progression: {generator.get_chord_progression(result['key'], result['scale'])}")
        print() 