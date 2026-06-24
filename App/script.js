const canvas = document.getElementById("canvas")
const ctx = canvas.getContext('2d')

const boxes = []
const boxCount = 0

for (let i = 0; i < boxCount; i++) {
    boxes.push(new Box()) 
}

function animate() {
    // REPLACE ctx.clearRect(...) with this:
    // Draw a semi-transparent black rectangle (alpha 0.1 creates a long trail, 0.3 a short one)
    ctx.fillStyle = "rgba(255, 255, 255, 0.1)"; 
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    boxes.forEach(box => {
        box.update();
        box.draw();
    });
    requestAnimationFrame(animate);
}


animate()