import requests
import platform
import socket
import getpass
from datetime import datetime
import cv2
import os

SERVER_URL = "https://laptop-tracker-server.onrender.com/report"

def capturar_webcam(path='webcam.jpg'):
    try:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(path, frame)
        cam.release()
    except:
        with open(path, 'wb') as f:
            f.write(b'')

def recolectar_info():
    hostname = socket.gethostname()
    usuario = getpass.getuser()
    sistema = f"{platform.system()} {platform.release()}"
    try:
        ip = socket.gethostbyname(hostname)
    except:
        ip = "No obtenido"
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {'ip': ip, 'usuario': usuario, 'sistema': sistema, 'hora': hora}

def enviar_reporte():
    capturar_webcam("webcam.jpg")
    info = recolectar_info()
    print("📤 INFO:", info)

    # Preparo multipart con campos de texto y archivo
    files = {
        'ip':        (None, info['ip']),
        'usuario':   (None, info['usuario']),
        'sistema':   (None, info['sistema']),
        'hora':      (None, info['hora']),
        'imagen':    ('webcam.jpg', open('webcam.jpg','rb'), 'image/jpeg')
    }
    print("📎 PARTES multipart:", list(files.keys()))

    try:
        r = requests.post(SERVER_URL, files=files)
        print("✅ Código:", r.status_code, "| Cuerpo:", r.text)
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    enviar_reporte()
