/**
 * Symphonic Stories - Visual Generator
 * Generates visuals based on emotions using p5.js
 */

class VisualGenerator {
    constructor(canvasId) {
        this.canvasId = canvasId;
        this.canvas = document.getElementById(canvasId);
        this.p5Instance = null;
        this.particles = [];
        this.maxParticles = 100;
        this.backgroundColor = '#F5F5F5';
        this.colorPalette = ['#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3', '#DCDCDC'];
        this.shapeType = 'circles';
        this.motionType = 'floating';
        this.particleSize = 7;
        this.speed = 0.5;
        this.blur = 0.3;
        
        // Initialize p5.js sketch
        this.initializeSketch();
    }
    
    /**
     * Initialize the p5.js sketch
     */
    initializeSketch() {
        const self = this;
        
        // Create a new p5 instance
        this.p5Instance = new p5(function(p) {
            // Setup function
            p.setup = function() {
                // Create canvas to fill the container
                const canvas = p.createCanvas(
                    self.canvas.clientWidth,
                    self.canvas.clientHeight
                );
                canvas.parent(self.canvasId);
                
                // Initialize particles
                self.createParticles(p);
            };
            
            // Draw function
            p.draw = function() {
                // Clear background
                p.background(self.backgroundColor);
                
                // Update and draw particles
                self.updateParticles(p);
            };
            
            // Window resize function
            p.windowResized = function() {
                p.resizeCanvas(
                    self.canvas.clientWidth,
                    self.canvas.clientHeight
                );
            };
        });
    }
    
    /**
     * Create particles
     * @param {Object} p - p5.js instance
     */
    createParticles(p) {
        this.particles = [];
        
        for (let i = 0; i < this.maxParticles; i++) {
            this.particles.push({
                x: p.random(p.width),
                y: p.random(p.height),
                size: p.random(this.particleSize * 0.5, this.particleSize * 1.5),
                speedX: p.random(-this.speed, this.speed),
                speedY: p.random(-this.speed, this.speed),
                color: p.random(this.colorPalette),
                rotation: p.random(p.TWO_PI),
                rotationSpeed: p.random(-0.05, 0.05)
            });
        }
    }
    
    /**
     * Update and draw particles
     * @param {Object} p - p5.js instance
     */
    updateParticles(p) {
        for (let i = 0; i < this.particles.length; i++) {
            const particle = this.particles[i];
            
            // Update position based on motion type
            switch (this.motionType) {
                case 'floating':
                    particle.x += particle.speedX;
                    particle.y += particle.speedY;
                    break;
                    
                case 'expanding':
                    const centerX = p.width / 2;
                    const centerY = p.height / 2;
                    const dx = particle.x - centerX;
                    const dy = particle.y - centerY;
                    const dist = p.sqrt(dx * dx + dy * dy);
                    
                    if (dist > 0) {
                        particle.x += (dx / dist) * this.speed;
                        particle.y += (dy / dist) * this.speed;
                    }
                    break;
                    
                case 'drifting':
                    particle.x += particle.speedX * 0.5;
                    particle.y += particle.speedY * 0.3 + Math.sin(p.frameCount * 0.01 + i) * 0.2;
                    break;
                    
                case 'explosive':
                    particle.x += particle.speedX * 1.5;
                    particle.y += particle.speedY * 1.5;
                    break;
                    
                case 'trembling':
                    particle.x += particle.speedX + p.random(-0.5, 0.5);
                    particle.y += particle.speedY + p.random(-0.5, 0.5);
                    break;
                    
                case 'bursting':
                    if (p.frameCount % 60 < 30) {
                        particle.x += particle.speedX * 2;
                        particle.y += particle.speedY * 2;
                    } else {
                        particle.x += particle.speedX * 0.5;
                        particle.y += particle.speedY * 0.5;
                    }
                    break;
            }
            
            // Update rotation
            particle.rotation += particle.rotationSpeed;
            
            // Wrap around edges
            if (particle.x < -particle.size) particle.x = p.width + particle.size;
            if (particle.x > p.width + particle.size) particle.x = -particle.size;
            if (particle.y < -particle.size) particle.y = p.height + particle.size;
            if (particle.y > p.height + particle.size) particle.y = -particle.size;
            
            // Draw particle based on shape type
            p.push();
            p.translate(particle.x, particle.y);
            p.rotate(particle.rotation);
            
            // Apply blur effect
            if (this.blur > 0) {
                p.drawingContext.shadowBlur = this.blur * 10;
                p.drawingContext.shadowColor = particle.color;
            }
            
            p.noStroke();
            p.fill(particle.color);
            
            switch (this.shapeType) {
                case 'circles':
                    p.ellipse(0, 0, particle.size);
                    break;
                    
                case 'squares':
                    p.rectMode(p.CENTER);
                    p.rect(0, 0, particle.size, particle.size);
                    break;
                    
                case 'lines':
                    p.stroke(particle.color);
                    p.strokeWeight(particle.size / 4);
                    p.line(-particle.size, 0, particle.size, 0);
                    break;
                    
                case 'stars':
                    this.drawStar(p, 0, 0, particle.size, particle.size / 2, 5);
                    break;
                    
                case 'shards':
                    this.drawShard(p, 0, 0, particle.size);
                    break;
                    
                case 'spikes':
                    this.drawSpike(p, 0, 0, particle.size);
                    break;
            }
            
            p.pop();
        }
    }
    
    /**
     * Draw a star shape
     * @param {Object} p - p5.js instance
     * @param {number} x - X position
     * @param {number} y - Y position
     * @param {number} radius1 - Outer radius
     * @param {number} radius2 - Inner radius
     * @param {number} npoints - Number of points
     */
    drawStar(p, x, y, radius1, radius2, npoints) {
        let angle = p.TWO_PI / npoints;
        let halfAngle = angle / 2.0;
        
        p.beginShape();
        for (let a = 0; a < p.TWO_PI; a += angle) {
            let sx = x + p.cos(a) * radius1;
            let sy = y + p.sin(a) * radius1;
            p.vertex(sx, sy);
            sx = x + p.cos(a + halfAngle) * radius2;
            sy = y + p.sin(a + halfAngle) * radius2;
            p.vertex(sx, sy);
        }
        p.endShape(p.CLOSE);
    }
    
    /**
     * Draw a shard shape
     * @param {Object} p - p5.js instance
     * @param {number} x - X position
     * @param {number} y - Y position
     * @param {number} size - Size
     */
    drawShard(p, x, y, size) {
        p.beginShape();
        p.vertex(x, y - size);
        p.vertex(x + size / 2, y + size / 4);
        p.vertex(x - size / 3, y + size / 2);
        p.endShape(p.CLOSE);
    }
    
    /**
     * Draw a spike shape
     * @param {Object} p - p5.js instance
     * @param {number} x - X position
     * @param {number} y - Y position
     * @param {number} size - Size
     */
    drawSpike(p, x, y, size) {
        p.beginShape();
        p.vertex(x, y - size);
        p.vertex(x + size / 4, y);
        p.vertex(x, y + size);
        p.vertex(x - size / 4, y);
        p.endShape(p.CLOSE);
    }
    
    /**
     * Generate visuals based on the provided parameters
     * @param {Object} params - Visual parameters
     */
    generate(params) {
        // Extract parameters
        this.colorPalette = params.color_palette || this.colorPalette;
        this.shapeType = params.shapes || this.shapeType;
        this.motionType = params.motion || this.motionType;
        this.maxParticles = params.particle_count || this.maxParticles;
        this.particleSize = params.particle_size || this.particleSize;
        this.backgroundColor = params.background || this.backgroundColor;
        this.blur = params.blur || this.blur;
        this.speed = params.speed || this.speed;
        
        // Recreate particles with new parameters
        if (this.p5Instance) {
            this.createParticles(this.p5Instance);
        }
        
        return this;
    }
} 