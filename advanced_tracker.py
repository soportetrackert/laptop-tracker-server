# advanced_tracker.py corregido y verificado
import requests
import platform
import socket
import getpass
from datetime import datetime
import cv2

SERVER_URL = 'https://laptop-tracker-server.onrender.com/report'

def capturar_webcam(path='webcam.jpg'):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(path, frame)
    else:
        print("⚠️ No se pudo capturar imagen de la webcam")
    cam.release()

def recolectar_info():
    try:
        ip_publica = requests.get('https://api.ipify.org').text
    except:
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
    print("📤 Datos recolectados:")
    for k, v in info.items():
        print(f"  {k}: {v}")
    
    try:
        with open('webcam.jpg', 'rb') as img:
            files = {'imagen': img}
            response = requests.post(SERVER_URL, data=info, files=files)
            print(f"✅ Enviado: {response.status_code} - {response.text}")
    except Exception as e:
        print("❌ Error al enviar reporte:", e)

if __name__ == '__main__':
    enviar_reporte()
