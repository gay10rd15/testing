class Box {
    constructor() {
        this.width = 48;
        this.height = 32;   
        this.y = Math.random() * (canvas.height - this.height);
        this.x = Math.random() * (canvas.width - this.width);
        this.vx = 10
        this.vy = 10
        let r = Math.floor(Math.random() * 255)
        let g = Math.floor(Math.random() * 255)
        let b = Math.floor(Math.random() * 255)
        this.color = "rgb(" + r + ", " + g + ", " + b + ")"
    }
    draw() {
        ctx.fillStyle = this.color
        ctx.fillRect(this.x, this.y, this.width, this.height)
    }
    update() {
        this.x += this.vx
        this.y += this.vy

        if (this.x + this.width > canvas.width || this.x < 0) {
            this.vx *= -1
        }
        if (this.y + this.height > canvas.height || this.y < 0) {
            this.vy *= -1
        }
    }
}