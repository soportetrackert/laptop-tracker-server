from flask import Flask, request, render_template, send_from_directory
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

reportes = []

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", reports=reportes)

@app.route("/report", methods=["POST"])
def report():
    print("[INFO] Reporte recibido.")

    try:
        ip = request.form.get("ip") or "No recibido"
        username = request.form.get("usuario") or "No recibido"
        system = request.form.get("sistema") or "No recibido"
        hostname = request.form.get("hostname") or "No recibido"
        fecha = request.form.get("hora") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        imagen = request.files.get("imagen")
        filename = None

        if imagen:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = secure_filename(f"{hostname}_{timestamp}.jpg")
            path = os.path.join(UPLOAD_FOLDER, filename)
            imagen.save(path)
            print(f"[INFO] Imagen guardada: {filename}")
        else:
            print("[WARN] Imagen no recibida.")

        reporte = {
            "ip": ip,
            "username": username,
            "system": system,
            "hostname": hostname,
            "fecha": fecha,
            "imagen": filename
        }

        reportes.append(reporte)
        print(f"[INFO] Reporte almacenado: {reporte}")

        return "Reporte recibido", 200
    except Exception as e:
        print("[ERROR]", e)
        return "Error procesando reporte", 500

@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
