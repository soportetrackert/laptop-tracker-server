import requests
import platform
import getpass
from datetime import datetime
import cv2
import os

SERVER_URL = 'https://laptop-tracker-server.onrender.com/report'

def capturar_webcam(path='webcam.jpg'):
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            raise Exception("No se pudo acceder a la webcam")
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(path, frame)
            print("📸 Imagen capturada exitosamente.")
        else:
            print("⚠️ No se pudo capturar imagen de la webcam.")
    except Exception as e:
        print("❌ Error al capturar imagen:", e)
    finally:
        cam.release()

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
    capturar_webcam('webcam.jpg')
    info = recolectar_info()

    print("\n📤 DATOS RECOLECTADOS:")
    for k, v in info.items():
        print(f"  {k}: {v}")

    print("\n🧪 VERIFICACIÓN FINAL antes del envío:")
    print("➡️ Form data que se enviará:")
    for k, v in info.items():
        print(f"  {k}: {v}")
    print("📁 ¿El archivo webcam.jpg existe?:", os.path.exists('webcam.jpg'))

    try:
        with open('webcam.jpg', 'rb') as img:
            files = {'imagen': img}
            response = requests.post(SERVER_URL, data=info, files=files, timeout=10)
            print(f"✅ Enviado: {response.status_code} - {response.text}")
    except Exception as e:
        print("❌ Error al enviar reporte:", e)

if __name__ == '__main__':
    enviar_reporte()
