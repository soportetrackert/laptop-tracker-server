from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Ruta para mostrar la imagen
@app.route('/ver_imagen/<filename>')
def ver_imagen(filename):
    # Asegúrate de que 'uploads' es la carpeta correcta donde están almacenadas tus imágenes
    return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)

# Página principal
@app.route('/')
def index():
    # Simulando algunos reportes con imágenes para demostración
    reportes = [
        {'imagen': 'image1.jpg'},
        {'imagen': 'image2.jpg'},
    ]
    return render_template("index.html", reports=reportes)

if __name__ == "__main__":
    app.run(debug=True)
