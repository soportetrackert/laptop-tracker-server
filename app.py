import os
import json
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
REPORT_FILE = os.path.join(app.root_path, 'reportes.json')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)
    else:
        reportes = []

    return render_template('index.html', reports=reportes)

@app.route('/report', methods=['POST'])
def report():
    ip = request.form.get("ip", "No recibido")
    usuario = request.form.get("usuario", "No recibido")
    sistema = request.form.get("sistema", "No recibido")
    imagen_file = request.files.get("imagen")

    filename = None
    if imagen_file:
        filename = imagen_file.filename
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        imagen_file.save(save_path)

    nuevo_reporte = {
        "ip": ip,
        "usuario": usuario,
        "sistema": sistema,
        "imagen": filename
    }

    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)
    else:
        reportes = []

    reportes.insert(0, nuevo_reporte)

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(reportes, f, ensure_ascii=False, indent=4)

    return "Reporte recibido", 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
