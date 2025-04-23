# app.py (Servidor Flask corregido)
import os
import json
from flask import Flask, request, render_template, send_from_directory, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
REPORT_FILE = os.path.join(app.root_path, 'reportes.json')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    reportes = []
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)
    return render_template('index.html', reports=reportes)

@app.route('/report', methods=['POST'])
def report():
    # Leer campos de form-data
    ip = request.form.get('ip', 'No recibido')
    usuario = request.form.get('usuario', 'No recibido')
    sistema = request.form.get('sistema', 'No recibido')
    hora = request.form.get('hora', 'No recibido')
    imagen = request.files.get('imagen')

    # Guardar imagen si existe
    filename = None
    if imagen and imagen.filename:
        filename = f"{hora.replace(':','-')}_{imagen.filename.replace(' ','_')}"
        imagen.save(os.path.join(UPLOAD_FOLDER, filename))

    nuevo = { 'ip': ip, 'usuario': usuario, 'sistema': sistema, 'hora': hora, 'imagen': filename }
    # Actualizar JSON
    reportes = []
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)
    reportes.insert(0, nuevo)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(reportes, f, ensure_ascii=False, indent=4)

    return jsonify(status='ok')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


# advanced_tracker.py (Cliente corregido)
import requests
import platform
import socket
import getpass
from datetime import datetime
import cv2

SERVER_URL = 'https://laptop-tracker-server.onrender.com/report'

def capturar_webcam(path='webcam.jpg'):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(path, frame)
    cam.release()


def recolectar_info():
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = 'No obtenido'
    return {
        'ip': ip,
        'usuario': getpass.getuser(),
        'sistema': f"{platform.system()} {platform.release()}",
        'hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def enviar_reporte():
    capturar_webcam('webcam.jpg')
    info = recolectar_info()
    print('📤 INFO:', info)
    files = {
        'ip': (None, info['ip']),
        'usuario': (None, info['usuario']),
        'sistema': (None, info['sistema']),
        'hora': (None, info['hora']),
        'imagen': ('webcam.jpg', open('webcam.jpg','rb'), 'image/jpeg')
    }
    print('📎 PARTES multipart:', files.keys())
    r = requests.post(SERVER_URL, files=files)
    print('✅ STATUS:', r.status_code, r.text)

if __name__ == '__main__':
    enviar_reporte()
