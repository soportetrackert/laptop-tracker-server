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
SERVER_URL = "https://laptop-tracker-server.onrender.com/report"  # tu URL

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
                f.write(b'')  # imagen vacía
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
            'hostname': hostname,
            'usuario': usuario,
            'sistema': sistema,
            'ip': ip,
        }
    except:
        return {
            'hostname': 'No recibido',
            'usuario': 'No recibido',
            'sistema': 'No recibido',
            'ip': 'No recibido',
        }

def enviar_reporte():
    capturar_webcam("webcam.jpg")
    datos = recolectar_info()

    files = {
        "imagen": open("webcam.jpg", "rb")  # CAMPO CORRECTO
    }

    try:
        response = requests.post(SERVER_URL, data=datos, files=files)
        print("✅ Reporte enviado:", response.status_code)
    except Exception as e:
        print("❌ Error al enviar reporte:", e)

# ========================
# EJECUCIÓN
# ========================
if __name__ == "__main__":
    enviar_reporte()
