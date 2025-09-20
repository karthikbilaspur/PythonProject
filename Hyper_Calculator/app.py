from flask import Flask, render_template, request, jsonify, session
import gettext

app = Flask(__name__)
app.secret_key = 'secret_key'

# Initialize gettext
gettext.bindtextdomain('calculator', './locale')
gettext.textdomain('calculator')
_ = gettext.gettext

@app.route('/')
def index():
    lang = request.args.get('lang', 'en')
    gettext.bindtextdomain('calculator', './locale')
    gettext.textdomain('calculator')
    lang_trans = gettext.translation('calculator', localedir='./locale', languages=[lang])
    lang_trans.install()
    session['lang'] = lang
    return render_template('index.html', lang=lang)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        expression = request.form['expression']
        result = eval(expression)
        return jsonify({'result': str(result)})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/history', methods=['GET'])
def history():
    if 'history' not in session:
        session['history'] = []
    return jsonify({'history': session['history']})

@app.route('/save_to_history', methods=['POST'])
def save_to_history():
    expression = request.form['expression']
    result = request.form['result']
    if 'history' not in session:
        session['history'] = []
    session['history'].append({'expression': expression, 'result': result})
    return jsonify({'message': _('Expression saved to history')})

if __name__ == '__main__':
    app.run(debug=True)