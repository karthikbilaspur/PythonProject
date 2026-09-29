const form = document.getElementById('calculator-form');
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const expression = document.getElementById('expression').value;
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `expression=${expression}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerHTML = `Error: ${data.error}`;
        } else {
            document.getElementById('result').innerHTML = `Result: ${data.result}`;
        }
    })
    .catch(error => console.error(error));
});

document.getElementById('save-to-history').addEventListener('click', () => {
    const expression = document.getElementById('expression').value;
    const result = document.getElementById('result').textContent.replace('Result: ', '');
    fetch('/save_to_history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `expression=${expression}&result=${result}`
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error(error));
});

document.getElementById('show-history').addEventListener('click', () => {
    fetch('/history')
    .then(response => response.json())
    .then(data => {
        const historyDiv = document.getElementById('history');
        historyDiv.innerHTML = '';
        data.history.forEach(item => {
            const p = document.createElement('p');
            p.textContent = `${item.expression} = ${item.result}`;
            historyDiv.appendChild(p);
        });
    })
    .catch(error => console.error(error));
});