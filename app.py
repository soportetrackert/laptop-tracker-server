from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)

# Carpeta para guardar imágenes
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Lista en memoria para almacenar reportes
reportes = []

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", reports=reportes)

@app.route("/report", methods=["POST"])
def recibir_reporte():
    try:
        data = request.form
        archivo = request.files.get("imagen")

        hostname = data.get("hostname", "No recibido")
        usuario = data.get("usuario", "No recibido")
        sistema = data.get("sistema", "No recibido")
        ip = data.get("ip", "No recibido")
        hora = data.get("hora", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        nombre_archivo = "no_imagen.png"
        if archivo and archivo.filename:
            nombre_archivo = datetime.now().strftime("%Y%m%d%H%M%S_") + secure_filename(archivo.filename)
            ruta = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
            archivo.save(ruta)

        reporte = {
            "hostname": hostname,
            "usuario": usuario,
            "sistema": sistema,
            "ip": ip,
            "hora": hora,
            "imagen": nombre_archivo
        }
        reportes.append(reporte)
        print(f"[✅] Reporte recibido: {reporte}")
        return "Reporte recibido correctamente", 200

    except Exception as e:
        print(f"[❌] Error al recibir reporte: {e}")
        return "Error procesando el reporte", 500

@app.route("/static/uploads/<filename>")
def ver_imagen(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
