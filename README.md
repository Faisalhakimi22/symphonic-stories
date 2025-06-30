# Symphonic Stories

An interactive system that translates voice into musical and visual art, capturing emotions through stories and mapping them into visual and auditory forms of storytelling.

## Overview

Symphonic Stories listens to spoken narratives and instantly transforms them into synchronized musical scores and generative visual artwork that represents the emotional arc of the story.

### Components

1. **Audio Input**: Live microphone or prerecorded voice files
2. **Analysis Layer**: Speech-to-text conversion and emotion detection
3. **Mapping Engine**: Translates emotions to music and visual parameters
4. **Generators**: Creates music and visuals based on the mapped parameters
5. **Synchronization**: Ensures music and visuals are in sync
6. **Output**: Delivers the final audiovisual experience

## Features

- **Voice Input**: Record your voice to tell a story
- **Text Input**: Type your story if you prefer not to use voice
- **Emotion Detection**: Automatically detects emotions in your story
- **Dynamic Music Generation**: Creates music that matches the emotional tone
- **Real-time Visualization**: Generates visual art synchronized with the music
- **Interactive Interface**: User-friendly controls for playback and adjustment

## Installation

### Prerequisites

- Python 3.8 or higher
- Web browser with WebAudio and WebGL support

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/symphonic-stories.git
cd symphonic-stories

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy the example environment file and edit as needed
cp .env.example .env
# Edit .env with your preferred settings
```

## Usage

```bash
# Run the application
python run.py
```

Then open your web browser and navigate to `http://localhost:5000` (or the host/port specified in your .env file).

### Using the Application

1. Choose between text or voice input
2. Enter your story or record your voice
3. Watch and listen as your story is transformed into music and visuals
4. Use the playback controls to pause/play or adjust volume

## Project Structure

```
symphonic-stories/
├── src/
│   ├── analysis/        # Speech-to-text and emotion detection
│   ├── music/           # Music generation components
│   ├── visual/          # Visual generation components
│   └── main.py          # Main application entry point
├── static/
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── templates/       # HTML templates
├── requirements.txt     # Project dependencies
├── run.py               # Startup script
└── .env.example         # Example environment variables
```

## Extending the Project

### Adding New Emotions

Edit the emotion mappings in:
- `src/music/music_generator.py` for music parameters
- `src/visual/visual_generator.py` for visual parameters

### Custom Instruments

Modify the `createInstruments()` method in `static/js/music-generator.js` to add or change instruments.

### Visual Effects

Add new visual effects by extending the shape and motion options in `static/js/visual-generator.js`.

## License

MIT License

## Acknowledgments

- [Tone.js](https://tonejs.github.io/) for web audio synthesis
- [p5.js](https://p5js.org/) for visual generation
- [Hugging Face](https://huggingface.co/) for emotion detection models
- [Flask](https://flask.palletsprojects.com/) and [Socket.IO](https://socket.io/) for the web framework 