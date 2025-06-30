"""
Visual Generator Module
Generates visual art based on detected emotions.
"""

import os
import logging
import json
import numpy as np
import time
from collections import defaultdict

logger = logging.getLogger(__name__)

# Define emotion to visual mapping
EMOTION_VISUAL_MAPPING = {
    'joy': {
        'color_palette': ['#FFD700', '#FFA500', '#FF8C00', '#FFFF00', '#FFFACD'],  # Warm yellows and golds
        'shapes': 'circles',
        'motion': 'expanding',
        'particle_count': 200,
        'particle_size': 10,
        'background': '#FFFAF0',  # Warm off-white
        'blur': 0.2,
        'speed': 0.7
    },
    'sadness': {
        'color_palette': ['#000080', '#0000CD', '#4169E1', '#6495ED', '#B0C4DE'],  # Blues
        'shapes': 'lines',
        'motion': 'drifting',
        'particle_count': 100,
        'particle_size': 5,
        'background': '#F0F8FF',  # Light blue
        'blur': 0.5,
        'speed': 0.3
    },
    'anger': {
        'color_palette': ['#8B0000', '#B22222', '#FF0000', '#CD5C5C', '#DC143C'],  # Reds
        'shapes': 'shards',
        'motion': 'explosive',
        'particle_count': 300,
        'particle_size': 8,
        'background': '#1A0000',  # Very dark red
        'blur': 0.1,
        'speed': 0.9
    },
    'fear': {
        'color_palette': ['#2F4F4F', '#556B2F', '#483D8B', '#4B0082', '#191970'],  # Dark colors
        'shapes': 'spikes',
        'motion': 'trembling',
        'particle_count': 150,
        'particle_size': 6,
        'background': '#000000',  # Black
        'blur': 0.4,
        'speed': 0.6
    },
    'surprise': {
        'color_palette': ['#FF1493', '#FF00FF', '#BA55D3', '#9370DB', '#EE82EE'],  # Pinks and purples
        'shapes': 'stars',
        'motion': 'bursting',
        'particle_count': 250,
        'particle_size': 12,
        'background': '#FFFFFF',  # White
        'blur': 0.1,
        'speed': 0.8
    },
    'neutral': {
        'color_palette': ['#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3', '#DCDCDC'],  # Grays
        'shapes': 'squares',
        'motion': 'floating',
        'particle_count': 120,
        'particle_size': 7,
        'background': '#F5F5F5',  # Light gray
        'blur': 0.3,
        'speed': 0.5
    }
}

class VisualGenerator:
    """
    Generates visual art based on detected emotions.
    """
    
    def __init__(self):
        """
        Initialize the visual generator.
        """
        logger.info("Initializing VisualGenerator")
        # Track the current visual state
        self.current_state = {
            'color_palette': ['#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3', '#DCDCDC'],
            'shapes': 'circles',
            'motion': 'floating',
            'particle_count': 120,
            'particle_size': 7,
            'background': '#F5F5F5',
            'blur': 0.3,
            'speed': 0.5,
            'last_update': time.time()
        }
        
        # For smooth transitions
        self.target_state = self.current_state.copy()
        
        # Create a history of generated visuals for continuity
        self.history = []
        
        # Load any custom mappings if available
        self._load_custom_mappings()
    
    def _load_custom_mappings(self):
        """Load custom emotion-to-visual mappings if available."""
        mapping_file = os.path.join(os.path.dirname(__file__), 'emotion_visual_mapping.json')
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r') as f:
                    custom_mappings = json.load(f)
                    # Update the default mappings with custom ones
                    for emotion, mapping in custom_mappings.items():
                        if emotion in EMOTION_VISUAL_MAPPING:
                            EMOTION_VISUAL_MAPPING[emotion].update(mapping)
                logger.info("Loaded custom emotion-to-visual mappings")
            except Exception as e:
                logger.error(f"Error loading custom mappings: {e}")
    
    def map_emotion(self, emotion, intensity):
        """
        Map an emotion to visual parameters.
        
        Args:
            emotion (str): The detected emotion
            intensity (float): The intensity of the emotion (0.0 to 1.0)
            
        Returns:
            dict: Visual parameters
        """
        # Get the base mapping for this emotion
        base_mapping = EMOTION_VISUAL_MAPPING.get(emotion, EMOTION_VISUAL_MAPPING['neutral'])
        
        # Create a copy to modify
        visual_params = base_mapping.copy()
        
        # Adjust parameters based on intensity
        visual_params['particle_count'] = int(base_mapping['particle_count'] * intensity)
        visual_params['particle_size'] = base_mapping['particle_size'] * intensity
        visual_params['speed'] = base_mapping['speed'] * intensity
        
        # Add the emotion and intensity to the parameters
        visual_params['emotion'] = emotion
        visual_params['intensity'] = intensity
        
        # Update the target state
        self.target_state = visual_params.copy()
        self.target_state['last_update'] = time.time()
        
        logger.debug(f"Mapped {emotion} ({intensity:.2f}) to visual parameters: {visual_params}")
        return visual_params
    
    def generate(self, visual_params):
        """
        Generate visuals based on the provided parameters.
        
        Args:
            visual_params (dict): Visual parameters
            
        Returns:
            dict: Generated visual data (in a format suitable for the client)
        """
        # In a real implementation, this would generate actual visuals
        # For now, we'll just return the parameters for the client to use
        
        # Smooth transition from current state to target state
        self._update_current_state()
        
        # Add to history
        self.history.append(visual_params)
        if len(self.history) > 10:
            self.history.pop(0)
        
        # For demonstration, return the parameters that would be used to generate visuals
        result = {
            'color_palette': visual_params['color_palette'],
            'shapes': visual_params['shapes'],
            'motion': visual_params['motion'],
            'particle_count': visual_params['particle_count'],
            'particle_size': visual_params['particle_size'],
            'background': visual_params['background'],
            'blur': visual_params['blur'],
            'speed': visual_params['speed'],
            'emotion': visual_params.get('emotion', 'neutral'),
            'timestamp': time.time()
        }
        
        logger.debug(f"Generated visuals with parameters: {result}")
        return result
    
    def _update_current_state(self):
        """Update the current state with a smooth transition to the target state."""
        # Calculate how much time has passed since the last update
        now = time.time()
        elapsed = now - self.current_state['last_update']
        
        # Simple linear interpolation for continuous parameters
        # In a real implementation, this would be more sophisticated
        alpha = min(1.0, elapsed / 2.0)  # 2-second transition
        
        self.current_state['particle_count'] = int(
            self.current_state['particle_count'] * (1 - alpha) + 
            self.target_state['particle_count'] * alpha
        )
        
        self.current_state['particle_size'] = (
            self.current_state['particle_size'] * (1 - alpha) + 
            self.target_state['particle_size'] * alpha
        )
        
        self.current_state['speed'] = (
            self.current_state['speed'] * (1 - alpha) + 
            self.target_state['speed'] * alpha
        )
        
        self.current_state['blur'] = (
            self.current_state['blur'] * (1 - alpha) + 
            self.target_state['blur'] * alpha
        )
        
        # For discrete parameters, change if we're more than halfway through the transition
        if alpha > 0.5:
            self.current_state['color_palette'] = self.target_state['color_palette']
            self.current_state['shapes'] = self.target_state['shapes']
            self.current_state['motion'] = self.target_state['motion']
            self.current_state['background'] = self.target_state['background']
        
        self.current_state['last_update'] = now
    
    def get_color_for_valence_arousal(self, valence, arousal):
        """
        Get a color based on valence and arousal values.
        
        Args:
            valence (float): Valence value (-1.0 to 1.0)
            arousal (float): Arousal value (-1.0 to 1.0)
            
        Returns:
            str: Hex color code
        """
        # Map valence to hue (0-360)
        # Negative valence: blues and purples (180-300)
        # Positive valence: reds, oranges, yellows (0-60)
        if valence < 0:
            hue = 240 + valence * 60  # 240 (blue) to 180 (cyan)
        else:
            hue = 60 - valence * 60  # 60 (yellow) to 0 (red)
        
        # Map arousal to saturation and brightness
        # High arousal: high saturation, high brightness
        # Low arousal: low saturation, medium brightness
        saturation = 0.5 + arousal * 0.5  # 0.0 to 1.0
        brightness = 0.5 + arousal * 0.3  # 0.5 to 0.8
        
        # Convert HSB to RGB (simplified conversion)
        # In a real implementation, use a proper HSB to RGB conversion
        h = hue / 60
        i = int(h)
        f = h - i
        p = brightness * (1 - saturation)
        q = brightness * (1 - saturation * f)
        t = brightness * (1 - saturation * (1 - f))
        
        if i == 0:
            r, g, b = brightness, t, p
        elif i == 1:
            r, g, b = q, brightness, p
        elif i == 2:
            r, g, b = p, brightness, t
        elif i == 3:
            r, g, b = p, q, brightness
        elif i == 4:
            r, g, b = t, p, brightness
        else:
            r, g, b = brightness, p, q
        
        # Convert to hex
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        
        return f'#{r:02x}{g:02x}{b:02x}'


# For testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generator = VisualGenerator()
    
    # Test with different emotions
    emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'neutral']
    for emotion in emotions:
        params = generator.map_emotion(emotion, 0.8)
        result = generator.generate(params)
        print(f"Emotion: {emotion}")
        print(f"  Visuals: {result}")
        print() 