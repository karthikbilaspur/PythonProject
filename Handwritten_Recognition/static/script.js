const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const clearButton = document.getElementById('clear-button');
const recognizeButton = document.getElementById('recognize-button');
const predictionDiv = document.getElementById('prediction');

let drawing = false;

canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
});

canvas.addEventListener('mousemove', (e) => {
    if (drawing) {
        ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
        ctx.stroke();
    }
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
});

clearButton.addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    predictionDiv.innerText = '';
});

recognizeButton.addEventListener('click', () => {
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    const data = [];
    for (let i = 0; i < imageData.length; i += 4) {
        data.push(imageData[i]);
    }
    const resizedData = resizeImage(data, canvas.width, canvas.height);
    fetch('/recognize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: resizedData })
    })
    .then(response => response.json())
    .then(data => {
        predictionDiv.innerText = `Prediction: ${data.prediction}`;
    });
});

function resizeImage(data, width, height) {
    const resizedData = [];
    const resizedWidth = 28;
    const resizedHeight = 28;
    for (let y = 0; y < resizedHeight; y++) {
        for (let x = 0; x < resizedWidth; x++) {
            const originalX = Math.floor(x * width / resizedWidth);
            const originalY = Math.floor(y * height / resizedHeight);
            const index = (originalY * width * 4) + (originalX * 4);
            resizedData.push(255 - data[index]);
        }
    }
    return resizedData;
}