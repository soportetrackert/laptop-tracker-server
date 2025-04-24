@app.route('/report', methods=['POST'])
def report():
    print('🔔 Se recibió un reporte')
    print('📥 FORM DATA:', request.form)

    ip = request.form.get('ip', 'No recibido')
    usuario = request.form.get('usuario', 'No recibido')
    sistema = request.form.get('sistema', 'No recibido')
    hora = request.form.get('hora', 'No recibido')

    nuevo = {
        'ip': ip,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora,
        'imagen': None  # Siempre None mientras no se use imagen
    }

    reportes = []
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)
    reportes.insert(0, nuevo)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(reportes, f, ensure_ascii=False, indent=4)
    print('✅ Reporte guardado:', nuevo)

    return jsonify(status='ok')
