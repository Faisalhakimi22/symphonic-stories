/**
 * Symphonic Stories - Main JavaScript
 * Coordinates the application's functionality
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    const socketHandler = new SocketHandler();
    const audioRecorder = new AudioRecorder();
    const musicGenerator = new MusicGenerator();
    const visualGenerator = new VisualGenerator('visualization-canvas');
    
    // DOM elements
    const inputMethods = document.querySelectorAll('.input-method');
    const textInputContainer = document.getElementById('text-input-container');
    const voiceInputContainer = document.getElementById('voice-input-container');
    const storyText = document.getElementById('story-text');
    const processTextButton = document.getElementById('process-text');
    const recordButton = document.getElementById('record-button');
    const recordingStatus = document.getElementById('recording-status');
    const recordingTime = document.getElementById('recording-time');
    const transcriptionText = document.getElementById('transcription-text');
    const emotionLabel = document.getElementById('emotion-label');
    const emotionIntensity = document.getElementById('emotion-intensity');
    const playPauseButton = document.getElementById('play-pause');
    const volumeSlider = document.getElementById('volume-slider');
    
    // State variables
    let isRecording = false;
    let recordingStartTime = 0;
    let recordingTimer = null;
    let isPlaying = false;
    
    // Initialize the application
    function init() {
        // Set up event listeners
        setupEventListeners();
        
        // Connect to the server
        socketHandler.connect();
        
        // Set up socket event handlers
        setupSocketEvents();
        
        // Initialize the audio context (needs to be after a user interaction)
        document.body.addEventListener('click', () => {
            if (!musicGenerator.isInitialized()) {
                musicGenerator.initialize();
            }
        }, { once: true });
    }
    
    // Set up event listeners
    function setupEventListeners() {
        // Input method selection
        inputMethods.forEach(method => {
            method.addEventListener('click', () => {
                // Remove active class from all methods
                inputMethods.forEach(m => m.classList.remove('active'));
                // Add active class to the clicked method
                method.classList.add('active');
                
                // Show the appropriate input container
                if (method.dataset.method === 'text') {
                    textInputContainer.classList.add('input-active');
                    voiceInputContainer.classList.remove('input-active');
                } else {
                    textInputContainer.classList.remove('input-active');
                    voiceInputContainer.classList.add('input-active');
                }
            });
        });
        
        // Process text button
        processTextButton.addEventListener('click', () => {
            const text = storyText.value.trim();
            if (text) {
                socketHandler.sendTextInput(text);
                transcriptionText.textContent = text;
            }
        });
        
        // Record button
        recordButton.addEventListener('click', toggleRecording);
        
        // Play/pause button
        playPauseButton.addEventListener('click', togglePlayback);
        
        // Volume slider
        volumeSlider.addEventListener('input', () => {
            const volume = parseFloat(volumeSlider.value);
            musicGenerator.setVolume(volume);
        });
    }
    
    // Set up socket events
    function setupSocketEvents() {
        socketHandler.onStoryUpdate((data) => {
            // Update the UI with the received data
            updateUI(data);
            
            // Generate music and visuals
            musicGenerator.generate(data.music_data);
            visualGenerator.generate(data.visual_data);
        });
    }
    
    // Toggle recording state
    function toggleRecording() {
        if (!isRecording) {
            // Start recording
            startRecording();
        } else {
            // Stop recording
            stopRecording();
        }
    }
    
    // Start recording
    function startRecording() {
        audioRecorder.start()
            .then(() => {
                isRecording = true;
                recordButton.classList.add('recording');
                recordingStatus.textContent = 'Recording...';
                
                // Start the recording timer
                recordingStartTime = Date.now();
                updateRecordingTime();
                recordingTimer = setInterval(updateRecordingTime, 1000);
                
                // Send audio data to the server
                audioRecorder.onAudioData((audioData) => {
                    socketHandler.sendAudioData(audioData);
                });
            })
            .catch(error => {
                console.error('Error starting recording:', error);
                recordingStatus.textContent = 'Error: Could not access microphone';
            });
    }
    
    // Stop recording
    function stopRecording() {
        audioRecorder.stop();
        isRecording = false;
        recordButton.classList.remove('recording');
        recordingStatus.textContent = 'Click to start recording';
        
        // Stop the recording timer
        clearInterval(recordingTimer);
        recordingTimer = null;
        recordingTime.textContent = '00:00';
    }
    
    // Update the recording time display
    function updateRecordingTime() {
        const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
        const seconds = (elapsed % 60).toString().padStart(2, '0');
        recordingTime.textContent = `${minutes}:${seconds}`;
    }
    
    // Toggle playback state
    function togglePlayback() {
        if (!isPlaying) {
            // Start playback
            musicGenerator.play();
            playPauseButton.classList.add('playing');
            isPlaying = true;
        } else {
            // Pause playback
            musicGenerator.pause();
            playPauseButton.classList.remove('playing');
            isPlaying = false;
        }
    }
    
    // Update the UI with the received data
    function updateUI(data) {
        // Update transcription
        transcriptionText.textContent = data.text;
        
        // Update emotion display
        emotionLabel.textContent = data.emotion;
        emotionLabel.className = ''; // Clear previous classes
        emotionLabel.classList.add(`emotion-${data.emotion}`);
        
        // Update emotion intensity
        const intensityPercent = data.intensity * 100;
        emotionIntensity.style.setProperty('--intensity', `${intensityPercent}%`);
        emotionIntensity.querySelector('::before').style.width = `${intensityPercent}%`;
    }
    
    // Initialize the application
    init();
}); 