import os
import json
from flask import Flask, request, render_template, send_from_directory, jsonify

# Inicialización de la app
app = Flask(__name__)

# Directorios y archivo de reportes
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
REPORT_FILE = os.path.join(app.root_path, 'reportes.json')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ruta de depuración para ver el contenido de reportes.json
@app.route('/debug_reportes', methods=['GET'])
def debug_reportes():
    """
    Muestra el contenido de reportes.json en formato JSON para depuración.
    """
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            data = f.read()
    else:
        data = '[]'
    return app.response_class(data, mimetype='application/json')

# Ruta principal: muestra el dashboard
@app.route('/')
def index():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)
    else:
        reportes = []
    return render_template('index.html', reports=reportes)

# Endpoint de recepción de reportes
@app.route('/report', methods=['POST'])
def report():
    # Datos de formulario
    ip = request.form.get('ip', 'No recibido')
    usuario = request.form.get('usuario', 'No recibido')
    sistema = request.form.get('sistema', 'No recibido')
    hora = request.form.get('hora', 'No recibido')
    imagen = request.files.get('imagen')

    # Debug prints en consola
    print('🔔 Se recibió un reporte')
    print('📥 FORM DATA:', request.form)
    print('📥 FILES:', request.files)

    # Guardar imagen
    filename = None
    if imagen and imagen.filename:
        safe_name = hora.replace(':', '-') + '_' + imagen.filename.replace(' ', '_')
        path = os.path.join(UPLOAD_FOLDER, safe_name)
        imagen.save(path)
        filename = safe_name
        print('✅ Imagen guardada en', path)
    else:
        print('⚠️ No se recibió archivo de imagen')

    # Construir reporte
    nuevo_reporte = {
        'ip': ip,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora,
        'imagen': filename
    }
    print('💾 Reporte a guardar:', nuevo_reporte)

    # Cargar y actualizar reportes.json
    try:
        if os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, 'r', encoding='utf-8') as f:
                reportes = json.load(f)
        else:
            reportes = []
        reportes.insert(0, nuevo_reporte)
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(reportes, f, ensure_ascii=False, indent=4)
        print('✅ reportes.json actualizado')
    except Exception as e:
        print('❌ Error al escribir reportes.json:', e)

    return jsonify(status='ok'), 200

# Servir imágenes
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Arranque de la app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f'🚀 Servidor arrancando en 0.0.0.0:{port}')
    app.run(debug=True, host='0.0.0.0', port=port)
