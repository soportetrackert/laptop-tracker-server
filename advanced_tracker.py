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
        else:
            with open(path, 'wb') as f:
                f.write(b'')
        cam.release()
    except:
        with open(path, 'wb') as f:
            f.write(b'')

def recolectar_info():
    try:
        hostname = socket.gethostname()
        usuario = getpass.getuser()
        sistema = f"{platform.system()} {platform.release()}"
        ip = socket.gethostbyname(hostname)
        return {
            'ip': ip,
            'usuario': usuario,
            'sistema': sistema
        }
    except:
        return {
            'ip': 'No recibido',
            'usuario': 'No recibido',
            'sistema': 'No recibido'
        }

def enviar_reporte():
    capturar_webcam("webcam.jpg")
    datos = recolectar_info()

    files = {
        "imagen": open("webcam.jpg", "rb")  # Debe ser exactamente "imagen"
    }

    try:
        response = requests.post(SERVER_URL, data=datos, files=files)
        print("✅ Enviado:", response.status_code)
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    enviar_reporte()
