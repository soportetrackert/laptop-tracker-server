from flask import Flask, request, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

reportes = []

@app.route('/')
def index():
    return render_template('index.html', reportes=reportes[::-1])

@app.route('/report', methods=['POST'])
def recibir_reporte():
    ip = request.form.get('ip', 'No recibido')
    usuario = request.form.get('usuario', 'No recibido')
    sistema = request.form.get('sistema', 'No recibido')
    hora = request.form.get('hora', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    reporte = {
        'ip': ip,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora
    }

    reportes.append(reporte)
    return 'Reporte recibido', 200

@app.route('/api/reportes')
def api_reportes():
    return jsonify(reportes[::-1])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
