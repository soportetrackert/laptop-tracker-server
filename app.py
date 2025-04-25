from flask import Flask, request, render_template, redirect, url_for, Response
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)

reportes = []

# Autenticación básica
USERNAME = 'admin'
PASSWORD = 'Ecodelta2030@'

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        'Acceso no autorizado. Proporcione credenciales válidas.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    return render_template('index.html', reportes=reportes)

@app.route('/report', methods=['POST'])
def report():
    ip = request.form.get('ip') or 'No recibido'
    usuario = request.form.get('usuario') or 'No recibido'
    sistema = request.form.get('sistema') or 'No recibido'
    hora = request.form.get('hora') or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ubicacion = request.form.get('ubicacion') or 'No disponible'

    reporte = {
        'ip': ip,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora,
        'ubicacion': ubicacion
    }
    reportes.append(reporte)
    print(f"[REPORTE RECIBIDO] {reporte}")
    return 'Reporte recibido', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
