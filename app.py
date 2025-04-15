from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from datetime import datetime
import os
import json
import time

app = Flask(__name__)
app.secret_key = "supersecreta"

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    if not session.get("logged_in"):
        return redirect(url_for('login'))
    try:
        with open("reportes.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    reports = []
    for idx, r in enumerate(data, start=1):
        reports.append([
            idx,
            r.get("ip"),
            r.get("username"),
            r.get("system_info"),
            r.get("timestamp"),
            r.get("image")
        ])
    return render_template("panel.html", reports=reports)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["logged_in"] = True
            return redirect(url_for("home"))
        return "Credenciales incorrectas", 401
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/report', methods=['POST'])
def report():
    ip = request.form.get('ip')
    username = request.form.get('username')
    system_info = request.form.get('system_info')
    image = request.files.get('image')

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    image_filename = None
    if image:
        image_filename = f"{int(time.time())}.jpg"
        image.save(os.path.join(UPLOAD_FOLDER, image_filename))

    report_data = {
        "ip": ip,
        "username": username,
        "system_info": system_info,
        "timestamp": timestamp,
        "image": image_filename
    }

    if os.path.exists("reportes.json"):
        with open("reportes.json", "r") as f:
            data = json.load(f)
    else:
        data = []

    data.insert(0, report_data)

    with open("reportes.json", "w") as f:
        json.dump(data, f, indent=2)

    return "Reporte recibido", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
