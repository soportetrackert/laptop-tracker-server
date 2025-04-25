from flask import Flask, request, render_template

app = Flask(__name__)

# Simulamos una base de datos o lista para almacenar los reportes
reportes = []

@app.route('/')
def index():
    return render_template('index.html', reportes=reportes)

@app.route('/report', methods=['POST'])
def report():
    ip = request.form.get('ip')
    usuario = request.form.get('usuario')
    sistema = request.form.get('sistema')
    hora = request.form.get('hora')
    ubicacion = request.form.get('ubicacion')  # Recibe el campo de geolocalización

    # Agregar los datos del reporte a la lista
    reportes.append({
        'ip': ip,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora,
        'ubicacion': ubicacion
    })

    # Aquí se pueden almacenar los datos en una base de datos o hacer cualquier otra acción
    print(f"IP: {ip}, Usuario: {usuario}, Sistema: {sistema}, Hora: {hora}, Ubicación: {ubicacion}")

    return "Reporte recibido"

if __name__ == '__main__':
    app.run(debug=True)
