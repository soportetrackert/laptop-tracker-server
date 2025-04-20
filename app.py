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
