from flask import Flask, render_template, request
import requests
import platform
import getpass
from datetime import datetime
import os

app = Flask(__name__)

# Inicialización de una lista para almacenar los reportes (puede ser reemplazada por una base de datos)
reportes = []

# Ruta principal para mostrar los reportes
@app.route('/')
def index():
    return render_template('index.html', reportes=reportes)

# Ruta para recibir los reportes
@app.route('/report', methods=['POST'])
def recibir_reporte():
    # Recibir los datos del reporte desde el cliente
    ip = request.form.get('ip')
    usuario = request.form.get('usuario')
    sistema = request.form.get('sistema')
    hora = request.form.get('hora')
    ubicacion = request.form.get('ubicacion')  # Asegúrate de enviar este campo desde el cliente

    # Almacenar el reporte en la lista
    if ip and usuario and sistema and hora and ubicacion:
        reportes.append({
            'ip': ip,
            'usuario': usuario,
            'sistema': sistema,
            'hora': hora,
            'ubicacion': ubicacion
        })
        return 'Reporte recibido', 200
    return 'Error en los datos', 400

# Configurar el puerto y host según las necesidades de Render
if __name__ == "__main__":
    # Obtener el puerto desde la variable de entorno, si está disponible
    port = int(os.environ.get("PORT", 5000))
    # Ejecutar la app en todas las interfaces de red con el puerto adecuado
    app.run(host="0.0.0.0", port=port, debug=True)
