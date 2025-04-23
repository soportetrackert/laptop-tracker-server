import requests
import platform
import socket
import getpass
from datetime import datetime
import cv2
import os

# ========================
# CONFIGURACIÓN
# ========================
SERVER_URL = "https://laptop-tracker-server.onrender.com/report"  # Cambia si estás en local

# ========================
# FUNCIONES
# ========================

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
    hostname = socket.gethostname()
    usuario = getpass.getuser()
    sistema = f"{platform.system()} {platform.release()}"
    try:
        ip = socket.gethostbyname(hostname)
    except:
        ip = "No obtenido"
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        'ip': ip,
        'usuario': usuario,
        'sistema': sistema,
        'hora': hora
    }

def enviar_reporte():
    # Capturar imagen de webcam
    capturar_webcam("webcam.jpg")

    datos = recolectar_info()
    print("📤 Enviando datos:", datos)

    files = {
        "imagen": open("webcam.jpg", "rb")
    }

    try:
        response = requests.post(SERVER_URL, data=datos, files=files)
        print("✅ Respuesta del servidor:", response.status_code)
    except Exception as e:
        print("❌ Error al enviar reporte:", e)

# ========================
# EJECUCIÓN
# ========================
if __name__ == "__main__":
    enviar_reporte()
