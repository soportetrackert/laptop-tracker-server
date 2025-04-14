@app.route('/report', methods=['POST'])
def report():
    try:
        image = request.files.get('image')
        ip = request.form.get('ip') or request.files.get('ip').read().decode()
        username = request.form.get('username') or request.files.get('username').read().decode()
        system_info_raw = request.form.get('system_info') or request.files.get('system_info').read().decode()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        image_path = ''

        if image and '.' in image.filename:
            filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}")
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = filename

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reports (ip, username, system_info, timestamp, image_path) VALUES (?, ?, ?, ?, ?)",
                           (ip, username, system_info_raw, timestamp, image_path))
            conn.commit()

        return "Reporte recibido", 200
        "Arreglando endpoint /report para leer bien los datos"

    except Exception as e:
        return f"[!] Error al procesar el reporte: {e}", 500
