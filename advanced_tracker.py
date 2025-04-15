from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from datetime import datetime
import os
import json
import time

app = Flask(__name__)
app.secret_key = 'clave-super-secreta'
UPLOAD_FOLDER = 'static/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists("reportes.json"):
    with open("reportes.json", "w") as f:
        json.dump([], f)

@app.route('/report', methods=['POST'])
def report():
    ip = request.form.get('ip')
    username = request.form.get('username')
    system_info = request.form.get('system_info')
    image = request.files.get('image')

    print("\n📥 NUEVO REPORTE RECIBIDO")
    print("IP:", ip)
    print("Usuario:", username)
    print("Sistema:", system_info)
    print("Imagen recibida:", "Sí" if image else "No")

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    image_filename = None
    if image:
        image_filename = f"{int(time.time())}.jpg"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image.save(image_path)

    report_data = {
        "ip": ip,
        "username": username,
        "system_info": system_info,
        "timestamp": timestamp,
        "image": image_filename
    }

    with open("reportes.json", "r") as f:
        data = json.load(f)

    data.insert(0, report_data)

    with open("reportes.json", "w") as f:
        json.dump(data, f, indent=2)

    return "Reporte recibido", 200

@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    with open("reportes.json", "r") as f:
        data = json.load(f)
    reports = []
    for i, r in enumerate(data, 1):
        reports.append([
            i,
            r.get("ip", "None"),
            r.get("username", "None"),
            r.get("system_info", "None"),
            r.get("timestamp", "None"),
            r.get("image", None)
        ])
    return render_template("panel.html", reports=reports)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["logged_in"] = True
            return redirect(url_for("home"))
        return "Credenciales incorrectas", 403
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
