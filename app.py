import os
import json
import time
from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

# Asegura la carpeta de subida
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

    # Asegura que el archivo JSON exista
    if not os.path.exists("reportes.json"):
        with open("reportes.json", "w") as f:
            json.dump([], f)

    with open("reportes.json", "r") as f:
        data = json.load(f)

    data.insert(0, report_data)

    with open("reportes.json", "w") as f:
        json.dump(data, f, indent=2)

    return "Reporte recibido", 200


