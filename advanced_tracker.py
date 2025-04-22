import requests
import platform
import socket
import getpass
from datetime import datetime
import cv2
import pyautogui
import os

SERVER_URL = "https://laptop-tracker-server.onrender.com/report"  # Usa tu URL real

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

def capturar_pantalla(path='pantalla.jpg'):
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
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
        ip = "0.0.0.0"
    return {
        'ip': ip,
        'usuario': usuario,
        'sistema': sistema
    }

def enviar_reporte():
    capturar_webcam("webcam.jpg")
    datos = recolectar_info()
    files = {
        "imagen": open("webcam.jpg", "rb")
    }

    try:
        response = requests.post(SERVER_URL, data=datos, files=files)
        print("Respuesta del servidor:", response.status_code)
    except Exception as e:
        print("Error al enviar reporte:", e)

if __name__ == "__main__":
    enviar_reporte()
