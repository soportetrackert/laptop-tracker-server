import requests
import getpass
import platform
from datetime import datetime

# Función para obtener la IP pública
def obtener_ip_publica():
    try:
        ip_publica = requests.get('https://api.ipify.org', timeout=5).text
        return ip_publica
    except requests.RequestException:
        return None

# Función para obtener la geolocalización
def obtener_geolocalizacion(ip_publica):
    try:
        url = f"https://ipinfo.io/{ip_publica}/json"
        response = requests.get(url, timeout=5)
        data = response.json()

        # Extracción de información relevante
        ciudad = data.get("city", "Desconocida")
        region = data.get("region", "Desconocida")
        pais = data.get("country", "Desconocido")
        ubicacion = f"{ciudad}, {region}, {pais}"

        return ubicacion  # Retorna la ubicación completa
    except Exception as e:
        print("⚠️ Error al obtener geolocalización:", e)
        return "Desconocida"

# Función para recolectar la información del sistema
def recolectar_info():
    try:
        ip_publica = obtener_ip_publica()
        if ip_publica:
            ubicacion = obtener_geolocalizacion(ip_publica)
        else:
            ubicacion = "Desconocida"
            ip_publica = 'No obtenido'
    except Exception as e:
        print("⚠️ No se pudo obtener IP pública:", e)
        ip_publica = 'No obtenido'
        ubicacion = 'Desconocida'

    usuario = getpass.getuser()
    sistema = f"{platform.system()} {platform.release()}"
    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Retornar los datos recolectados
    return {
        'ip': ip_publica,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora,
        'ubicacion': ubicacion  # Incluir la ubicación en el diccionario
    }

# Enviar la información al servidor
def enviar_datos():
    url = "https://laptop-tracker-server.onrender.com/report"  # Reemplazar con tu URL del servidor

    # Recolectamos la información
    datos = recolectar_info()

    # Enviar la información al servidor
    try:
        response = requests.post(url, data=datos)
        if response.status_code == 200:
            print("✅ Reporte enviado con éxito")
        else:
            print(f"❌ Error al enviar reporte: {response.status_code}")
    except requests.RequestException as e:
        print(f"⚠️ Error al contactar con el servidor: {e}")

# Llamamos a la función para enviar los datos
if __name__ == "__main__":
    enviar_datos()
