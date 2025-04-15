from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from datetime import datetime
import json
import os
import time

app = Flask(__name__)
app.secret_key = 'clave_secreta'

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Credenciales
USUARIO = "admin"
CONTRASENA = "1234"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USUARIO and password == CONTRASENA:
            session["autenticado"] = True
            return redirect(url_for("index"))
        else:
            return "Credenciales inválidas", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("autenticado", None)
    return redirect(url_for("login"))

@app.route("/")
def index():
    if not session.get("autenticado"):
        return redirect(url_for("login"))

    if not os.path.exists("reportes.json"):
        with open("reportes.json", "w") as f:
            json.dump([], f)

    with open("reportes.json", "r") as f:
        data = json.load(f)

    reports = []
    for i, reporte in enumerate(data):
        reports.append([
            i + 1,
            reporte.get("ip"),
            reporte.get("username"),
            reporte.get("system_info"),
            reporte.get("timestamp"),
            reporte.get("image")
        ])

    return render_template("index.html", reports=reports)

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

    if not os.path.exists("reportes.json"):
        with open("reportes.json", "w") as f:
            json.dump([], f)

    with open("reportes.json", "r") as f:
        data = json.load(f)

    data.insert(0, report_data)

    with open("reportes.json", "w") as f:
        json.dump(data, f, indent=2)

    return "Reporte recibido", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
