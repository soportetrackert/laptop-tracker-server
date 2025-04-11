from flask import Flask, request, render_template, redirect, url_for, send_from_directory, session
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- AUTH DECORATOR ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- INIT DATABASE ---
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                username TEXT,
                system_info TEXT,
                timestamp TEXT,
                image_path TEXT
            )
        ''')
        conn.commit()

# --- PANEL WEB ---
@app.route('/')
@login_required
def index():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports ORDER BY id DESC")
        reports = cursor.fetchall()
    return render_template("index.html", reports=reports)

# --- LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# --- RECIBIR DATOS ---
@app.route('/report', methods=['POST'])
def report():
    ip = request.form.get('ip')
    username = request.form.get('username')
    system_info = request.form.get('system_info')
    image = request.files.get('image')

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    image_path = ''
    if image and '.' in image.filename:
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}")
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = filename

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reports (ip, username, system_info, timestamp, image_path) VALUES (?, ?, ?, ?, ?)",
                       (ip, username, system_info, timestamp, image_path))
        conn.commit()

    return "Reporte recibido", 200

# --- SERVIR IMAGENES ---
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- INIT ---
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    init_db()
    app.run(host='0.0.0.0', port=5000)