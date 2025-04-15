from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from datetime import datetime
import json
import os
import time

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if not os.path.exists("reportes.json"):
        with open("reportes.json", "w") as f:
            json.dump([], f)

    with open("reportes.json", "r") as f:
        data = json.load(f)

    reports = []
    for idx, r in enumerate(data):
        reports.append([
            idx + 1,
            r.get("ip", "Sin dato"),
            r.get("username", "Sin dato"),
            r.get("system_info", "Sin dato"),
            r.get("timestamp", "Sin dato"),
            r.get("image", None)
        ])

    return render_template("index.html", reports=reports)

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
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image.save(image_path)

    if not os.path.exists("reportes.json"):
        with open("reportes.json", "w") as f:
            json.dump([], f)

    with open("reportes.json", "r") as f:
        data = json.load(f)

    data.insert(0, {
        "ip": ip,
        "username": username,
        "system_info": system_info,
        "timestamp": timestamp,
        "image": image_filename
    })

    with open("reportes.json", "w") as f:
        json.dump(data, f, indent=2)

    return "Reporte recibido", 200

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")
        if user == "admin" and pw == "admin123":
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return "Credenciales incorrectas", 403
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
