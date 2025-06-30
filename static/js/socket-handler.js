/**
 * Symphonic Stories - Socket Handler
 * Manages WebSocket communication with the server
 */

class SocketHandler {
    constructor() {
        this.socket = null;
        this.connected = false;
        this.storyUpdateCallbacks = [];
    }
    
    /**
     * Connect to the server
     */
    connect() {
        // Get the server URL (default to the current host)
        const serverUrl = window.location.origin;
        
        // Create the socket connection
        this.socket = io(serverUrl);
        
        // Set up event handlers
        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.connected = true;
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.connected = false;
        });
        
        this.socket.on('story_update', (data) => {
            console.log('Received story update:', data);
            // Notify all registered callbacks
            this.storyUpdateCallbacks.forEach(callback => callback(data));
        });
        
        return this;
    }
    
    /**
     * Disconnect from the server
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
        }
        return this;
    }
    
    /**
     * Send audio data to the server
     * @param {ArrayBuffer} audioData - The audio data to send
     */
    sendAudioData(audioData) {
        if (this.connected) {
            this.socket.emit('audio_data', audioData);
        } else {
            console.warn('Cannot send audio data: not connected to server');
        }
        return this;
    }
    
    /**
     * Send text input to the server
     * @param {string} text - The text to send
     */
    sendTextInput(text) {
        if (this.connected) {
            this.socket.emit('text_input', { text });
        } else {
            console.warn('Cannot send text input: not connected to server');
        }
        return this;
    }
    
    /**
     * Register a callback for story updates
     * @param {function} callback - The callback function
     */
    onStoryUpdate(callback) {
        if (typeof callback === 'function') {
            this.storyUpdateCallbacks.push(callback);
        }
        return this;
    }
    
    /**
     * Remove a callback for story updates
     * @param {function} callback - The callback function to remove
     */
    offStoryUpdate(callback) {
        const index = this.storyUpdateCallbacks.indexOf(callback);
        if (index !== -1) {
            this.storyUpdateCallbacks.splice(index, 1);
        }
        return this;
    }
    
    /**
     * Check if connected to the server
     * @returns {boolean} - Whether connected to the server
     */
    isConnected() {
        return this.connected;
    }
} 