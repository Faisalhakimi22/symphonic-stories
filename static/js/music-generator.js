/**
 * Symphonic Stories - Music Generator
 * Generates music based on emotions using Tone.js
 */

class MusicGenerator {
    constructor() {
        this.initialized = false;
        this.playing = false;
        this.instruments = {};
        this.effects = {};
        this.currentChords = [];
        this.currentScale = [];
        this.currentKey = 'C';
        this.currentTempo = 90;
        this.volume = 0.7;
        this.part = null;
        this.loop = null;
    }
    
    /**
     * Initialize the music generator
     */
    initialize() {
        if (this.initialized) return this;
        
        try {
            // Start audio context
            Tone.start();
            
            // Set volume
            Tone.Master.volume.value = Tone.gainToDb(this.volume);
            
            // Create a simple synth
            this.instruments.synth = new Tone.PolySynth().toDestination();
            
            this.initialized = true;
            console.log('Music generator initialized');
        } catch (error) {
            console.error('Error initializing music generator:', error);
        }
        
        return this;
    }
    
    /**
     * Generate music based on the provided parameters
     * @param {Object} params - Music parameters
     */
    generate(params) {
        if (!this.initialized) this.initialize();
        
        // Extract parameters
        const key = params.key || 'C';
        const scale = params.scale || 'major';
        const tempo = params.tempo || 90;
        const emotion = params.emotion || 'neutral';
        
        // Set the BPM
        Tone.Transport.bpm.value = tempo;
        
        console.log(`Generating music for ${emotion} in ${key} ${scale} at ${tempo} BPM`);
        
        return this;
    }
    
    /**
     * Play the generated music
     */
    play() {
        if (!this.initialized) this.initialize();
        
        // Play a simple chord
        this.instruments.synth.triggerAttackRelease(['C4', 'E4', 'G4'], '2n');
        
        this.playing = true;
        return this;
    }
    
    /**
     * Pause the music
     */
    pause() {
        Tone.Transport.pause();
        this.playing = false;
        return this;
    }
    
    /**
     * Stop the music
     */
    stop() {
        Tone.Transport.stop();
        this.playing = false;
        return this;
    }
    
    /**
     * Set the volume
     * @param {number} volume - Volume level (0 to 1)
     */
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        if (this.initialized) {
            Tone.Master.volume.value = Tone.gainToDb(this.volume);
        }
        return this;
    }
    
    /**
     * Check if the music generator is initialized
     * @returns {boolean} - Whether the music generator is initialized
     */
    isInitialized() {
        return this.initialized;
    }
    
    /**
     * Check if the music is playing
     * @returns {boolean} - Whether the music is playing
     */
    isPlaying() {
        return this.playing;
    }
} 