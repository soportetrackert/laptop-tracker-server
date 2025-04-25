from flask import Flask, request, render_template

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
    ubicacion = request.form.get('ubicacion', 'No recibido')

    reportes.append({
        'ip': ip,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora,
        'ubicacion': ubicacion
    })

    return 'Reporte recibido', 200
