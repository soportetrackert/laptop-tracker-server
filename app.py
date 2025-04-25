from flask import Flask, request, render_template
from datetime import datetime
import os

app = Flask(__name__)

# Lista global para almacenar los reportes
reportes = []

@app.route('/')
def index():
    return render_template('index.html', reportes=reportes)

@app.route('/report', methods=['POST'])
def recibir_datos():
    ip = request.form.get('ip', 'No recibido')
    usuario = request.form.get('usuario', 'No recibido')
    sistema = request.form.get('sistema', 'No recibido')
    hora = request.form.get('hora', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # Agregar a la lista
    reportes.append({
        'ip': ip,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora
    })

    print(f"[📥 NUEVO REPORTE] {ip} - {usuario} - {sistema} - {hora}")
    return 'Reporte recibido', 200

# Configuración para que Render detecte el puerto
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
