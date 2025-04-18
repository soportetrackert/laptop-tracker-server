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
    try:
        ip = request.form.get('ip') or 'Desconocido'
        username = request.form.get('username') or 'Desconocido'
        system_info = request.form.get('system_info') or 'Desconocido'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        image = request.files.get('image')
        
        print("[+] Reporte recibido:")
        print("  IP:", ip)
        print("  Usuario:", username)
        print("  Sistema:", system_info)

        image_filename = None
        if image:
            image_filename = f"{int(time.time())}.jpg"
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image.save(image_path)
        else:
            print("[!] No se recibió imagen")

        if not os.path.exists("reportes.json"):
            with open("reportes.json", "w") as f:
                json.dump([], f)

        with open("reportes.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("[!] Error al leer JSON. Se creará una lista vacía.")
                data = []

        data.insert(0, {
            "ip": ip,
            "username": username,
            "system_info": system_info,
            "timestamp": timestamp,
            "image": image_filename
        })

        with open("reportes.json", "w") as f:
            json.dump(data, f, indent=2)

        return "Reporte recibido correctamente", 200
    except Exception as e:
        print(f"[!] Error en /report: {e}")
        return "Error procesando el reporte", 500

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
            return
