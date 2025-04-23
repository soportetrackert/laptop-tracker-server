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
    cam.release()

def recolectar_info():
    # Para IP pública, llama a un servicio externo
    try:
        ip_publica = requests.get('https://api.ipify.org').text
    except:
        ip_publica = 'No obtenido'
    return {
        'ip': ip_publica,
        'usuario': getpass.getuser(),
        'sistema': f"{platform.system()} {platform.release()}",
        'hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def enviar_reporte():
    capturar_webcam('webcam.jpg')
    info = recolectar_info()
    print('📤 INFO:', info)

    # Construye multipart con campos de texto y archivo
    files = {
        'ip':      (None, info['ip']),
        'usuario': (None, info['usuario']),
        'sistema': (None, info['sistema']),
        'hora':    (None, info['hora']),
        'imagen':  ('webcam.jpg', open('webcam.jpg','rb'), 'image/jpeg')
    }
    print('📎 PARTES:', files.keys())

    r = requests.post(SERVER_URL, files=files)
    print('✅ STATUS:', r.status_code, r.text)

if __name__ == '__main__':
    enviar_reporte()
