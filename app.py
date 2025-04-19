import requests
import socket
import platform
import getpass
import json
import os
from datetime import datetime
from PIL import ImageGrab
import cv2

def obtener_ip_publica():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "No disponible"

def obtener_geo(ip):
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json").json()
        return res
    except:
        return {}

def recolectar_info():
    ip = obtener_ip_publica()
    geo = obtener_geo(ip)
    return {
        "ip": ip,
        "username": getpass.getuser(),
        "system_info": f"{platform.system()} {platform.release()}",
        "hostname": socket.gethostname(),
        "ciudad": geo.get("city", "N/A"),
        "region": geo.get("region", "N/A"),
        "pais": geo.get("country", "N/A"),
        "loc": geo.get("loc", "N/A"),
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def capturar_webcam(nombre_archivo="webcam.jpg"):
    try:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(nombre_archivo, frame)
        cam.release()
    except:
        pass

def enviar_reporte():
    datos = recolectar_info()
    capturar_webcam("webcam.jpg")

    with open("webcam.jpg", "rb") as img:
        files = {"image": img}
        response = requests.post(
            "https://laptop-tracker-server.onrender.com/report",  # Cambia por tu URL si es diferente
            data=datos,
            files=files
        )
    print("Respuesta del servidor:", response.status_code, response.text)

if __name__ == "__main__":
    enviar_reporte()
