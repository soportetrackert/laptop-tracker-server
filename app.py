from flask import Flask, request, render_template
import os

app = Flask(__name__)

reportes = []

@app.route('/')
def index():
    return render_template('index.html', reportes=reportes)

@app.route('/report', methods=['POST'])
def report():
    ip = request.form.get('ip', 'No recibido')
    usuario = request.form.get('usuario', 'No recibido')
    sistema = request.form.get('sistema', 'No recibido')
    hora = request.form.get('hora', 'No recibido')

    datos = {
        'ip': ip,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora
    }

    print("📥 Reporte recibido:", datos)
    reportes.insert(0, datos)
    return 'Reporte recibido', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
