/**
 * Symphonic Stories - Audio Recorder
 * Handles recording audio from the microphone
 */

class AudioRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.audioStream = null;
        this.isRecording = false;
        this.audioDataCallback = null;
        
        // Audio context for processing
        this.audioContext = null;
        this.analyser = null;
        this.microphone = null;
    }
    
    /**
     * Start recording audio
     * @returns {Promise} - Resolves when recording starts
     */
    start() {
        return new Promise((resolve, reject) => {
            // Check if already recording
            if (this.isRecording) {
                resolve();
                return;
            }
            
            // Check if browser supports getUserMedia
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                reject(new Error('Browser does not support audio recording'));
                return;
            }
            
            // Request access to the microphone
            navigator.mediaDevices.getUserMedia({ audio: true, video: false })
                .then(stream => {
                    this.audioStream = stream;
                    
                    // Create the media recorder
                    this.mediaRecorder = new MediaRecorder(stream);
                    
                    // Set up event handlers
                    this.mediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            this.audioChunks.push(event.data);
                            
                            // Convert to ArrayBuffer and send to callback
                            if (this.audioDataCallback) {
                                const reader = new FileReader();
                                reader.onloadend = () => {
                                    this.audioDataCallback(reader.result);
                                };
                                reader.readAsArrayBuffer(event.data);
                            }
                        }
                    };
                    
                    // Start recording
                    this.audioChunks = [];
                    this.mediaRecorder.start(1000); // Collect data every second
                    this.isRecording = true;
                    
                    // Set up audio processing if Web Audio API is available
                    if (window.AudioContext || window.webkitAudioContext) {
                        this.setupAudioProcessing(stream);
                    }
                    
                    resolve();
                })
                .catch(error => {
                    console.error('Error accessing microphone:', error);
                    reject(error);
                });
        });
    }
    
    /**
     * Stop recording audio
     * @returns {Promise} - Resolves with the recorded audio blob
     */
    stop() {
        return new Promise((resolve, reject) => {
            // Check if not recording
            if (!this.isRecording || !this.mediaRecorder) {
                resolve(null);
                return;
            }
            
            // Stop the media recorder
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            // Stop all tracks in the stream
            if (this.audioStream) {
                this.audioStream.getTracks().forEach(track => track.stop());
                this.audioStream = null;
            }
            
            // Clean up audio processing
            if (this.audioContext) {
                if (this.microphone) {
                    this.microphone.disconnect();
                    this.microphone = null;
                }
                if (this.analyser) {
                    this.analyser.disconnect();
                    this.analyser = null;
                }
            }
            
            // Create a blob from the recorded chunks
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
            resolve(audioBlob);
        });
    }
    
    /**
     * Set up audio processing with Web Audio API
     * @param {MediaStream} stream - The audio stream
     */
    setupAudioProcessing(stream) {
        // Create audio context
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.audioContext = new AudioContext();
        
        // Create analyser node
        this.analyser = this.audioContext.createAnalyser();
        this.analyser.fftSize = 2048;
        
        // Connect microphone to analyser
        this.microphone = this.audioContext.createMediaStreamSource(stream);
        this.microphone.connect(this.analyser);
        
        // Note: We don't connect the analyser to the destination (speakers)
        // to avoid feedback loops
    }
    
    /**
     * Get audio level (volume)
     * @returns {number} - Audio level from 0 to 1
     */
    getAudioLevel() {
        if (!this.analyser) {
            return 0;
        }
        
        // Get frequency data
        const bufferLength = this.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        this.analyser.getByteFrequencyData(dataArray);
        
        // Calculate average level
        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
            sum += dataArray[i];
        }
        
        // Return normalized value (0 to 1)
        return sum / (bufferLength * 255);
    }
    
    /**
     * Register a callback for audio data
     * @param {function} callback - The callback function
     */
    onAudioData(callback) {
        if (typeof callback === 'function') {
            this.audioDataCallback = callback;
        }
        return this;
    }
    
    /**
     * Check if currently recording
     * @returns {boolean} - Whether currently recording
     */
    isActive() {
        return this.isRecording;
    }
} 