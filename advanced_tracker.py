import requests
import platform
import getpass
from datetime import datetime
import time

SERVER_URL = 'https://laptop-tracker-server.onrender.com/report'

def obtener_ubicacion(ip):
    try:
        url = f'https://ipapi.co/{ip}/city/'
        ciudad = requests.get(url, timeout=5).text.strip()
        return ciudad
    except:
        return 'No disponible'

def recolectar_info():
    try:
        ip_publica = requests.get('https://api.ipify.org', timeout=5).text
        ubicacion = obtener_ubicacion(ip_publica)
    except Exception as e:
        print("⚠️ No se pudo obtener IP pública o ubicación:", e)
        ip_publica = 'No obtenido'
        ubicacion = 'No disponible'
    usuario = getpass.getuser()
    sistema = f"{platform.system()} {platform.release()}"
    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        'ip': ip_publica,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora,
        'ubicacion': ubicacion
    }

def enviar_reporte():
    info = recolectar_info()
    print("\n📤 Enviando reporte:")
    for k, v in info.items():
        print(f"  {k}: {v}")
    try:
        response = requests.post(SERVER_URL, data=info, timeout=10)
        print(f"✅ Enviado: {response.status_code} - {response.text}")
    except Exception as e:
        print("❌ Error al enviar reporte:", e)

if __name__ == '__main__':
    while True:
        enviar_reporte()
        print("⏳ Esperando 15 minutos para el siguiente envío...\n")
        time.sleep(900)


