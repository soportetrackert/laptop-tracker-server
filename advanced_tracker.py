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
SERVER_URL = "https://laptop-tracker-server.onrender.com/report"

# ========================
# FUNCIONES
# ========================

def capturar_webcam(path='webcam.jpg'):
    try:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(path, frame)
        cam.release()
    except Exception as e:
        print("⚠️ Error al capturar webcam:", e)
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
    # 1) Captura imagen
    capturar_webcam("webcam.jpg")

    # 2) Recolecta datos
    datos = recolectar_info()
    print("📤 DATOS que envío:", datos)

    # 3) Prepara archivos
    try:
        f = open("webcam.jpg", "rb")
    except Exception as e:
        print("❌ No puedo abrir webcam.jpg:", e)
        return

    files = {"imagen": f}
    print("📎 FILES que envío:", files)

    # 4) Envía petición
    try:
        resp = requests.post(SERVER_URL, data=datos, files=files)
        print("✅ Código respuesta:", resp.status_code)
        print("🔁 Cuerpo respuesta:", resp.text)
    except Exception as e:
        print("❌ Error al enviar:", e)
    finally:
        f.close()

if __name__ == "__main__":
    enviar_reporte()
