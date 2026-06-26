const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// CRITICAL: Set dimensions explicitly in JS to override default 300x150
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

class Raindrop {
    constructor() {
        this.reset();
    }

    reset() {
        this.x = Math.random() * canvas.width;
        this.y = -Math.random() * canvas.height; // Start above screen
        this.speed = Math.random() * 5 + 2;
        this.length = Math.random() * 10 + 5;
    }

    update() {
        this.y += this.speed;
        if (this.y > canvas.height) {
            this.reset();
        }
    }

    draw() {
        ctx.beginPath();
        ctx.strokeStyle = "rgba(112, 146, 197, 0.5)";
        ctx.lineWidth = 3;
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.x, this.y + this.length);
        ctx.stroke();
    }
}

// Initialize drops
const drops = [];
for (let i = 0; i < 1000; i++) {
    drops.push(new Raindrop());
}

// Animation Loop
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drops.forEach(drop => {
        drop.update();
        drop.draw();
    });

    requestAnimationFrame(animate);
}

// START THE LOOP
animate();

// Optional: Handle window resize
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});   