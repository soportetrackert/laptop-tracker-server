# app.py (Servidor Flask definitivo)
import os
import json
from flask import Flask, request, render_template, send_from_directory, jsonify

app = Flask(__name__)
# Configuración de rutas
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
REPORT_FILE = os.path.join(app.root_path, 'reportes.json')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/debug_reportes')
def debug_reportes():
    # Devuelve el JSON crudo de reportes.json
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            data = f.read()
    else:
        data = '[]'
    return app.response_class(data, mimetype='application/json')

@app.route('/')
def index():
    reportes = []
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)
    return render_template('index.html', reports=reportes)

@app.route('/report', methods=['POST'])
def report():
    print('🔔 Se recibió un reporte')
    print('📥 FORM DATA:', request.form)
    print('📥 FILES   :', request.files)

    # Primero intentamos leer JSON en campo 'info'
    info = request.form.get('info')
    if info:
        js = json.loads(info)
        # IP puede venir en 'ip' o en 'ip_publica'
        ip = js.get('ip') or js.get('ip_publica') or 'No recibido'
        usuario = js.get('usuario', 'No recibido')
        sistema = js.get('sistema', 'No recibido')
        hora = js.get('hora', 'No recibido')
    else:
        # Si no viene JSON, leemos campos sueltos
        ip = request.form.get('ip', 'No recibido')
        usuario = request.form.get('usuario', 'No recibido')
        sistema = request.form.get('sistema', 'No recibido')
        hora = request.form.get('hora', 'No recibido')

    # Acepta imagen del campo 'imagen' o 'imagen_webcam'
    imagen = request.files.get('imagen') or request.files.get('imagen_webcam')
    filename = None
    if imagen and imagen.filename:
        safe_name = f"{hora.replace(':','-')}_{imagen.filename.replace(' ','_')}"
        full_path = os.path.join(UPLOAD_FOLDER, safe_name)
        imagen.save(full_path)
        filename = safe_name
        print('✅ Imagen guardada en', full_path)
    else:
        print('⚠️ No se recibió archivo de imagen')

    nuevo = { 'ip': ip, 'usuario': usuario, 'sistema': sistema, 'hora': hora, 'imagen': filename }
    print('💾 Reporte a guardar:', nuevo)

    # Escribir en reportes.json
    reportes = []
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)
    reportes.insert(0, nuevo)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(reportes, f, ensure_ascii=False, indent=4)
    print('✅ reportes.json actualizado')

    return jsonify(status='ok')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f'🚀 Servidor arrancando en 0.0.0.0:{port}')
    app.run(debug=True, host='0.0.0.0', port=port)


# advanced_tracker.py (Cliente definitivo)
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
    # Obtiene IP pública real
    try:
        ip_publica = requests.get('https://api.ipify.org').text
    except:
        ip_publica = 'No obtenido'
    return {
        'ip': ip_publica,
        'usuario': getpass.getuser(),
        'sistema': f"{platform.system()} {platform.release()}",
        'hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def enviar_reporte():
    capturar_webcam('webcam.jpg')
    info = recolectar_info()
    print('📤 INFO:', info)

    # Envia multipart con campos de texto y archivo
    files = {
        'info':    (None, json.dumps(info), 'application/json'),
        'imagen':  ('webcam.jpg', open('webcam.jpg','rb'), 'image/jpeg')
    }
    print('📎 PARTES:', list(files.keys()))

    r = requests.post(SERVER_URL, files=files)
    print('✅ STATUS:', r.status_code, r.text)

if __name__ == '__main__':
    enviar_reporte()
