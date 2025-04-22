import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Ruta para servir las imágenes almacenadas en 'static/uploads'
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/uploads'), filename)

# Ruta principal que muestra los reportes
@app.route('/')
def index():
    # Supón que 'reportes' es una lista de reportes que contiene los datos y nombres de las imágenes
    reportes = [
        {"imagen": "imagen1.jpg", "ip": "192.168.0.1", "usuario": "usuario1", "sistema": "Windows 10"},
        {"imagen": "imagen2.jpg", "ip": "192.168.0.2", "usuario": "usuario2", "sistema": "Linux"}
    ]
    return render_template('index.html', reports=reportes)

if __name__ == '__main__':
    # Usamos la variable de entorno PORT para que Flask escuche en el puerto correcto
    port = int(os.environ.get("PORT", 5000))  # 5000 es el valor por defecto
    app.run(debug=True, host="0.0.0.0", port=port)
