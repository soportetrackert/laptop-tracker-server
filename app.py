from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from datetime import datetime
import os, json

app = Flask(__name__)
app.secret_key = "clave-super-secreta"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/report", methods=["POST"])
def report():
    # ⚠️ Asegurarse de que se reciben todos los campos correctamente
    campos = ["ip", "username", "system_info", "hostname", "ciudad", "region", "pais", "loc", "hora"]
    data = {campo: request.form.get(campo, "No recibido") for campo in campos}

    # Imagen
    image = request.files.get("image")
    filename = None
    if image:
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        image.save(os.path.join(UPLOAD_FOLDER, filename))

    # Construir reporte
    reporte = data
    reporte["imagen"] = filename

    print("✅ Nuevo reporte recibido:")
    print(json.dumps(reporte, indent=2))

    if not os.path.exists("reportes.json"):
        with open("reportes.json", "w") as f:
            json.dump([], f)

    with open("reportes.json", "r") as f:
        datos = json.load(f)
    datos.insert(0, reporte)
    with open("reportes.json", "w") as f:
        json.dump(datos, f, indent=2)

    return "Reporte recibido"

@app.route("/")
def index():
    if not os.path.exists("reportes.json"):
        return "No hay reportes aún."

    with open("reportes.json", "r") as f:
        datos = json.load(f)

    return render_template("index.html", reports=datos)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
