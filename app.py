@app.route('/report', methods=['POST'])
def report():
    print("🔔 Se recibió un reporte")

    ip = request.form.get("ip", "No recibido")
    usuario = request.form.get("usuario", "No recibido")
    sistema = request.form.get("sistema", "No recibido")
    hora = request.form.get("hora", "No recibido")
    imagen = request.files.get("imagen")

    print("📥 FORM DATA:")
    print("IP:", ip)
    print("Usuario:", usuario)
    print("Sistema:", sistema)
    print("Hora:", hora)
    print("Imagen:", imagen.filename if imagen else "No recibida")

    filename = None
    if imagen and imagen.filename:
        filename = f"{hora.replace(':', '-')}_{imagen.filename}"
        ruta_guardado = os.path.join(UPLOAD_FOLDER, filename)
        print("📂 Guardando imagen en:", ruta_guardado)
        imagen.save(ruta_guardado)

    reporte = {
        "ip": ip,
        "usuario": usuario,
        "sistema": sistema,
        "hora": hora,
        "imagen": filename if filename else None
    }

    print("💾 Registro que se va a guardar:", reporte)

    # Guardar reporte en reportes.json
    try:
        if os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, 'r', encoding='utf-8') as f:
                reportes = json.load(f)
        else:
            reportes = []

        reportes.insert(0, reporte)

        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(reportes, f, ensure_ascii=False, indent=4)

        print("✅ Reporte guardado con éxito.")
    except Exception as e:
        print("❌ Error guardando el reporte:", e)

    return "Reporte recibido", 200
