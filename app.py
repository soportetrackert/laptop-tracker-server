import os
import json
from flask import Flask, request, render_template, send_from_directory

# ——————————————
# Inicialización de Flask
# ——————————————
app = Flask(__name__)

# ——————————————
# Configuración de rutas y archivos
# ——————————————
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
REPORT_FILE = os.path.join(app.root_path, 'reportes.json')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ——————————————
# Ruta principal: muestra el dashboard
# ——————————————
@app.route('/')
def index():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reportes = json.load(f)
    else:
        reportes = []
    return render_template('index.html', reports=reportes)

# ——————————————
# Endpoint de recepción de reportes
# ——————————————
@app.route('/report', methods=['POST'])
def report():
    print("🔔 Se recibió un reporte")

    # Lee datos del formulario
    ip = request.form.get("ip", "No recibido")
    usuario = request.form.get("usuario", "No recibido")
    sistema = request.form.get("sistema", "No recibido")
    hora = request.form.get("hora", "No recibido")
    imagen = request.files.get("imagen")

    # Imprime en consola para depuración
    print("📥 FORM DATA:")
    print("  IP:     ", ip)
    print("  Usuario:", usuario)
    print("  Sistema:", sistema)
    print("  Hora:   ", hora)
    print("  Imagen: ", imagen.filename if imagen else "No recibida")

    # Guarda la imagen si llegó
    filename = None
    if imagen and imagen.filename:
        safe_name = imagen.filename.replace(" ", "_")
        filename = f"{hora.replace(':','-')}_{safe_name}"
        path = os.path.join(UPLOAD_FOLDER, filename)
        print("📂 Guardando imagen en:", path)
        imagen.save(path)

    # Prepara el reporte a guardar
    nuevo_reporte = {
        "ip": ip,
        "usuario": usuario,
        "sistema": sistema,
        "hora": hora,
        "imagen": filename
    }
    print("💾 Registro que se va a guardar:", nuevo_reporte)

    # Carga existentes y agrega al inicio
    try:
        if os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, 'r', encoding='utf-8') as f:
                reportes = json.load(f)
        else:
            reportes = []
        reportes.insert(0, nuevo_reporte)
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(reportes, f, ensure_ascii=False, indent=4)
        print("✅ Reporte guardado con éxito.")
    except Exception as e:
        print("❌ Error guardando el reporte:", e)

    return "Reporte recibido", 200

# ——————————————
# Servir imágenes
# ——————————————
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ——————————————
# Arranque del servidor
# ——————————————
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Iniciando en 0.0.0.0:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
