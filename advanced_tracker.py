import requests
import platform
import getpass
from datetime import datetime

SERVER_URL = 'https://laptop-tracker-server.onrender.com/report'

def recolectar_info():
    try:
        ip_publica = requests.get('https://api.ipify.org', timeout=5).text
    except Exception as e:
        print("⚠️ No se pudo obtener IP pública:", e)
        ip_publica = 'No obtenido'
    usuario = getpass.getuser()
    sistema = f"{platform.system()} {platform.release()}"
    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        'ip': ip_publica,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora
    }

def enviar_reporte():
    info = recolectar_info()

    print("\n📤 DATOS RECOLECTADOS:")
    for k, v in info.items():
        print(f"  {k}: {v}")

    try:
        response = requests.post(SERVER_URL, data=info, timeout=10)
        print(f"✅ Enviado: {response.status_code} - {response.text}")
    except Exception as e:
        print("❌ Error al enviar reporte:", e)

if __name__ == '__main__':
    enviar_reporte()
