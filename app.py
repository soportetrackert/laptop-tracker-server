# app.py (Servidor Flask definitivo)
import os
import json
from flask import Flask, request, render_template, send_from_directory, jsonify

app = Flask(__name__)
# Configuración de rutas\UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
REPORT_FILE = os.path.join(app.root_path, 'reportes.json')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/debug_reportes')
def debug_reportes():
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

    # Leer campos del form-data
    ip = request.form.get('ip', 'No recibido')
    usuario = request.form.get('usuario', 'No recibido')
    sistema = request.form.get('sistema', 'No recibido')
    hora = request.form.get('hora', 'No recibido')

    # Acepta imagen en campo 'imagen'
    imagen = request.files.get('imagen')
    filename = None
    if imagen and imagen.filename:
        safe_name = f"{hora.replace(':','-')}_{imagen.filename.replace(' ','_')}"
        path = os.path.join(UPLOAD_FOLDER, safe_name)
        imagen.save(path)
        filename = safe_name
        print('✅ Imagen guardada en', path)
    else:
        print('⚠️ No se recibió archivo de imagen')

    nuevo = { 'ip': ip, 'usuario': usuario, 'sistema': sistema, 'hora': hora, 'imagen': filename }
    print('💾 Reporte a guardar:', nuevo)

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


# advanced_tracker.py (Cliente simplificado)
import requests
import platform
import socket
import getpass
from datetime import datetime
import cv2
import json

SERVER_URL = 'https://laptop-tracker-server.onrender.com/report'

def capturar_webcam(path='webcam.jpg'):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(path, frame)
    cam.release()

 def recolectar_info():
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

    # Enviar datos como form-data y archivo
    files = {'imagen': open('webcam.jpg', 'rb')}
    response = requests.post(SERVER_URL, data=info, files=files)
    print('✅ STATUS:', response.status_code, response.text)

 if __name__ == '__main__':
    enviar_reporte()
