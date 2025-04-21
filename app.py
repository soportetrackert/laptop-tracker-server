from flask import Flask, request, render_template
import os
from datetime import datetime

app = Flask(__name__)

# Lista global para almacenar los reportes recibidos
reportes = []

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", reports=reportes)

@app.route('/report', methods=['POST'])
def report():
    data = request.form.to_dict()

    # Extraer campos esperados del formulario
    reporte = {
        'hostname': data.get('hostname', 'No recibido'),
        'usuario': data.get('usuario', 'No recibido'),
        'sistema': data.get('sistema', 'No recibido'),
        'ip': data.get('ip', 'No recibido'),
        'hora': data.get('hora', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    }

    # Agrega el nuevo reporte a la lista
    reportes.insert(0, reporte)
    print("Reporte recibido:", reporte)

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
