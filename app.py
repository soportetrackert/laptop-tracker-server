import os
import json
from flask import Flask, request, render_template, send_from_directory, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
REPORT_FILE = os.path.join(app.root_path, 'reportes.json')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/debug_reportes', methods=['GET'])
def debug_reportes():
    if os.path.exists(REPORT_FILE):
        return app.response_class(open(REPORT_FILE).read(), mimetype='application/json')
    return jsonify([])

@app.route('/')
def index():
    reportes = []
    if os.path.exists(REPORT_FILE):
        reportes = json.load(open(REPORT_FILE, encoding='utf-8'))
    return render_template('index.html', reports=reportes)

@app.route('/report', methods=['POST'])
def report():
    # Log de headers y raw body
    print("----- REQUEST HEADERS -----")
    print(request.headers)
    print("----- REQUEST BODY -----")
    print(request.get_data(as_text=True))

    # Intenta primero values (form + query)
    ip = request.values.get('ip')
    usuario = request.values.get('usuario')
    sistema = request.values.get('sistema')
    hora = request.values.get('hora')

    # Si no hay nada, cae a JSON
    if not any([ip, usuario, sistema, hora]):
        js = request.get_json(silent=True) or {}
        ip = js.get('ip', 'No recibido')
        usuario = js.get('usuario', 'No recibido')
        sistema = js.get('sistema', 'No recibido')
        hora = js.get('hora', 'No recibido')

    # Si aún así quedan None, pon "No recibido"
    ip = ip or 'No recibido'
    usuario = usuario or 'No recibido'
    sistema = sistema or 'No recibido'
    hora = hora or 'No recibido'

    imagen = request.files.get('imagen')
    print("📥 Valores parseados:", dict(ip=ip, usuario=usuario, sistema=sistema, hora=hora))
    print("📥 FILES keys:", request.files.keys())

    filename = None
    if imagen and imagen.filename:
        safe = f"{hora.replace(':','-')}_{imagen.filename.replace(' ','_')}"
        imagen.save(os.path.join(UPLOAD_FOLDER, safe))
        filename = safe
        print("✅ Imagen guardada:", safe)
    else:
        print("⚠️ No llegó imagen")

    nuevo = {"ip":ip,"usuario":usuario,"sistema":sistema,"hora":hora,"imagen":filename}
    print("💾 A escribir en JSON:", nuevo)

    rep = []
    if os.path.exists(REPORT_FILE):
        rep = json.load(open(REPORT_FILE, encoding='utf-8'))
    rep.insert(0, nuevo)
    json.dump(rep, open(REPORT_FILE,'w',encoding='utf-8'), ensure_ascii=False, indent=4)

    return jsonify(status='ok')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    p = int(os.environ.get('PORT',5000))
    app.run(debug=True, host='0.0.0.0', port=p)
