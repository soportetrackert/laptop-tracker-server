from flask import Flask, request, render_template, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Crear reportes.json si no existe
if not os.path.exists("reportes.json"):
    with open("reportes.json", "w") as f:
        json.dump([], f)

@app.route("/")
def index():
    with open("reportes.json", "r") as f:
        reportes = json.load(f)
    return render_template("index.html", reportes=reportes)

@app.route("/report", methods=["POST"])
def report():
    ip = request.form.get("ip", "No recibido")
    username = request.form.get("username", "No recibido")
    system_info = request.form.get("system_info", "No recibido")
    hostname = request.form.get("hostname", "N/A")
    ciudad = request.form.get("ciudad", "N/A")
    region = request.form.get("region", "N/A")
    pais = request.form.get("pais", "N/A")
    loc = request.form.get("loc", "N/A")
    hora = request.form.get("hora", str(datetime.now()))

    filename = None
    image = request.files.get("image")
    if image:
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        image.save(os.path.join(UPLOAD_FOLDER, filename))

    reporte = {
        "ip": ip,
        "username": username,
        "system_info": system_info,
        "hostname": hostname,
        "ciudad": ciudad,
        "region": region,
        "pais": pais,
        "loc": loc,
        "hora": hora,
        "imagen": filename
    }

    with open("reportes.json", "r") as f:
        datos = json.load(f)
    datos.insert(0, reporte)
    with open("reportes.json", "w") as f:
        json.dump(datos, f, indent=2)

    return "Reporte recibido"

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Compatible con Render.com
    app.run(host="0.0.0.0", port=port)
