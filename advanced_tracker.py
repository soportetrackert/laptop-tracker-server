# advanced_tracker.py
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
    try:
        ip_publica = requests.get('https://api.ipify.org').text
    except:
        ip_publica = 'No obtenido'
    return {
        'ip': ip_publica,
        'usuario': getpass.getuser(),
        'sistema': f"{platform.system()} {platform.release()}",
        'hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def enviar_reporte():
    capturar_webcam('webcam.jpg')
    info = recolectar_info()
    print('📤 INFO:', info)

    files = {'imagen': open('webcam.jpg', 'rb')}
    response = requests.post(SERVER_URL, data=info, files=files)
    print('✅ STATUS:', response.status_code, response.text)

if __name__ == '__main__':
    enviar_reporte()
