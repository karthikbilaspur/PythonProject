const form = document.getElementById('prediction-form');
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('prediction-result').innerHTML = `Error: ${data.error}`;
        } else {
            document.getElementById('prediction-result').innerHTML = `Prediction: ${data.prediction}`;
        }
    })
    .catch(error => console.error(error));
});