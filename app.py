from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Datos de ejemplo, los puedes reemplazar con los datos reales
datos = [
    {'hostname': 'Laptop1', 'usuario': 'franklin', 'sistema': 'Windows', 'ip': '192.168.1.1'},
    {'hostname': 'Laptop2', 'usuario': 'user2', 'sistema': 'MacOS', 'ip': '192.168.1.2'}
]

@app.route('/')
def index():
    # Imprime los datos para depuración
    print("Datos recibidos:", datos)

    # Si 'datos' es una lista de diccionarios, verifica si cada diccionario tiene 'hostname'
    for r in datos:
        if 'hostname' not in r:
            print("Falta 'hostname' en uno de los reportes:", r)

    # Pasa los datos a la plantilla
    return render_template("index.html", reports=datos)

# Ruta para manejar los reportes recibidos desde el cliente
@app.route('/report', methods=['POST'])
def report():
    # Recibe los datos enviados desde el cliente
    reporte = request.json
    print("Reporte recibido:", reporte)

    # Aquí puedes agregar el reporte a la lista 'datos' si quieres almacenarlo
    datos.append(reporte)

    return jsonify({"message": "Reporte recibido con éxito"}), 200

if __name__ == '__main__':
    app.run(debug=True)
