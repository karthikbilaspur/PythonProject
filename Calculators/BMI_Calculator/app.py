from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_bmi():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        bmi = weight / (height ** 2)
        return render_template('index.html', bmi=bmi)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)