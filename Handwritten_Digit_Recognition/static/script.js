const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const clearButton = document.getElementById('clear-button');
const predictionDiv = document.getElementById('prediction');

let drawing = false;

canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
});

canvas.addEventListener('mousemove', (e) => {
    if (drawing) {
        ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
        ctx.stroke();
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
        const data = [];
        for (let i = 0; i < imageData.length; i += 4) {
            data.push(imageData[i]);
        }
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: data })
        })
        .then(response => response.json())
        .then(data => {
            predictionDiv.innerText = `Prediction: ${data.prediction}`;
        });
    }
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
});

clearButton.addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    predictionDiv.innerText = '';
});