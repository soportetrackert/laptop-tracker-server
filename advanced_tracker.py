import requests
import socket
import platform
import getpass
from datetime import datetime
import pyautogui
import cv2
import os

def recolectar_info():
    try:
        ip = requests.get('https://api.ipify.org').text
    except:
        ip = 'No disponible'

    return {
        'hostname': socket.gethostname(),
        'usuario': getpass.getuser(),
        'sistema': platform.platform(),
        'ip': ip,
        'hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def capturar_webcam(nombre_archivo='webcam.jpg'):
    try:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(nombre_archivo, frame)
        else:
            with open(nombre_archivo, 'wb') as f:
                f.write(b'')  # imagen vacía
        cam.release()
    except Exception as e:
        print("Error al capturar webcam:", e)

def capturar_pantalla(nombre_archivo='screenshot.jpg'):
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(nombre_archivo)
    except Exception as e:
        print("Error al capturar pantalla:", e)

def enviar_reporte():
    url = "https://laptop-tracker-server.onrender.com/report"

    datos = recolectar_info()
    print("Datos recopilados:", datos)

    capturar_webcam()
    capturar_pantalla()

    files = {
        'imagen_webcam': open('webcam.jpg', 'rb'),
        'captura_pantalla': open('screenshot.jpg', 'rb')
    }

    try:
        response = requests.post(url, data=datos, files=files)
        print("Reporte enviado. Código de respuesta:", response.status_code)
    except Exception as e:
        print("Error al enviar reporte:", e)

    # Limpieza
    for f in ['webcam.jpg', 'screenshot.jpg']:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    enviar_reporte()
