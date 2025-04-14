import os
import time
import json
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory

app = Flask(__name__)
app.secret_key = "clave-secreta"
UPLOAD_FOLDER = 'static/uploads'

# Crear carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    with open("reportes.json", "r") as f:
        data = json.load(f)
    reports = []
    for idx, d in enumerate(data, 1):
        reports.append([
            idx,
            d.get("ip"),
            d.get("username"),
            json.loads(d.get("system_info", "{}")).get("sistema"),
            d.get("timestamp"),
            d.get("image")
        ])
    return render_template("index.html", reports=reports)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["usuario"] == "admin" and request.form["clave"] == "1234":
            session["logged_in"] = True
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))

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

    if not os.path.exists("reportes.json"):
        with open("reportes.json", "w") as f:
            json.dump([], f)

    with open("reportes.json", "r") as f:
        data = json.load(f)

    data.insert(0, report_data)

    with open("reportes.json", "w") as f:
        json.dump(data, f, indent=2)

    return "Reporte recibido", 200

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 👇 Esta parte es crucial para que Render detecte que tu app está activa 👇
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
