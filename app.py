from flask import Flask, request, render_template, jsonify
import os
import json

app = Flask(__name__)

# Rutas
REPORT_FILE = os.path.join(app.root_path, 'reportes.json')

@app.route('/')
def index():
    reportes = []
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)
    return render_template('index.html', reports=reportes)

@app.route('/report', methods=['POST'])
def report():
    print('🔔 Reporte recibido')
    print('📥 FORM:', request.form)

    ip = request.form.get('ip', 'No recibido')
    usuario = request.form.get('usuario', 'No recibido')
    sistema = request.form.get('sistema', 'No recibido')
    hora = request.form.get('hora', 'No recibido')

    nuevo = { 'ip': ip, 'usuario': usuario, 'sistema': sistema, 'hora': hora }

    reportes = []
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)

    reportes.insert(0, nuevo)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(reportes, f, ensure_ascii=False, indent=4)

    return jsonify(status='ok')

@app.route('/debug_reportes')
def debug_reportes():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            data = f.read()
    else:
        data = '[]'
    return app.response_class(data, mimetype='application/json')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
