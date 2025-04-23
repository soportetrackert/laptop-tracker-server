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
    # Captura webcam
    capturar_webcam("webcam.jpg")
    datos = recolectar_info()
    files = {"imagen": open("webcam.jpg", "rb")}

    # Trazas de debug
    print("📤 DATOS que envío:", datos)
    print("📎 FILES que envío:", files)

    try:
        resp = requests.post(SERVER_URL, data=datos, files=files)
        print("✅ Código respuesta:", resp.status_code)
        print("🔁 Texto respuesta:", resp.text)
    except Exception as e:
        print("❌ Error al enviar:", e)

if __name__ == "__main__":
    enviar_reporte()
