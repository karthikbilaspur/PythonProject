from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, User, PhotoJob
from utils.photo_processor import process_folder
import os
from typing import cast
from werkzeug.utils import secure_filename
from sqlalchemy import select

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    os.makedirs(cast(str, app.config['UPLOAD_FOLDER']), exist_ok=True)
    os.makedirs(cast(str, app.config['BEST_FOLDER']), exist_ok=True)

ALLOWED_EXT = {'png','jpg','jpeg'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        if db.session.scalars(select(User).where(User.username == username)).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        if db.session.scalars(select(User).where(User.email == email)).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(name=name, username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully, please login')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = db.session.scalars(select(User).where(User.username == username)).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['name'] = user.name
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    jobs = db.session.scalars(
        select(PhotoJob)
        .where(PhotoJob.user_id == user_id)
        .order_by(PhotoJob.processed_at.desc())
        .limit(50)
    ).all()
    
    if request.method == 'POST':
        # handle folder upload (multiple files)
        files = request.files.getlist('files')
        user_upload = os.path.join(cast(str, app.config['UPLOAD_FOLDER']), str(user_id))
        user_best = os.path.join(cast(str, app.config['BEST_FOLDER']), str(user_id))
        os.makedirs(user_upload, exist_ok=True)
        os.makedirs(user_best, exist_ok=True)
        
        for f in files:
            original_filename = f.filename if f else None
            if original_filename and allowed_file(original_filename):
                filename = secure_filename(original_filename)
                f.save(os.path.join(user_upload, filename))
        
        results = process_folder(user_upload, user_best, user_id, db, PhotoJob)
        flash(f'Processed {len(results)} images. {len([r for r in results if r["is_best"]])} best shots found.')
        return redirect(url_for('dashboard'))
    
    return render_template('dashboard.html', name=session.get('name'), jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
