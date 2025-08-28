from flask import Flask, render_template, request, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import os
from scrapper import simple_image_download
import threading

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'
bootstrap = Bootstrap(app)
response = simple_image_download()

class ImageForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    number_of_images = IntegerField('number_of_images', validators=[DataRequired()])
    submit = SubmitField('Submit')

def download_images(name, number_of_images):
    try:
        response.download(name, int(number_of_images))
        flash('All of your images have been downloaded')
    except Exception as e:
        flash('Error downloading images: ' + str(e))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ImageForm()
    if form.validate_on_submit():
        name = request.form['name']
        number_of_images = request.form['number_of_images']
        flash('Your images are being downloaded. Please wait.')
        threading.Thread(target=download_images, args=(name, number_of_images)).start()
        return redirect('/')
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)