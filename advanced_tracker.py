import os
import cv2
import time
import json
import socket
import psutil
import pyautogui
import getpass
import platform
import requests
import threading
from datetime import datetime

SERVER_URL = "https://laptop-tracker-server.onrender.com/report"
INTERVALO_MINUTOS = 15

def capturar_webcam():
    try:
        cam = cv2.VideoCapture(0)
        result, image = cam.read()
        cam.release()
        if result:
            filename = "webcam.jpg"
            cv2.imwrite(filename, image)
            return filename
    except Exception as e:
        print(f"[!] Error al capturar webcam: {e}")
    return None

def capturar_pantalla():
    try:
        screenshot = pyautogui.screenshot()
        filename = "screenshot.jpg"
        screenshot.save(filename)
        return filename
    except Exception as e:
        print(f"[!] Error al capturar pantalla: {e}")
    return None

def obtener_ip_publica():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Desconocida"

def obtener_geolocalizacion(ip):
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json")
        data = res.json()
        return {
            "ciudad": data.get("city"),
            "region": data.get("region"),
            "pais": data.get("country"),
            "loc": data.get("loc")
        }
    except:
        return {}

def recolectar_info():
    ip_publica = obtener_ip_publica()
    info = {
        "ip_publica": ip_publica,
        "usuario": getpass.getuser(),
        "sistema": f"{platform.system()} {platform.release()}",
        "version": platform.version(),
        "nombre_equipo": socket.gethostname(),
        "hora": str(datetime.now())
    }
    info.update(obtener_geolocalizacion(ip_publica))
    return info

def enviar_al_servidor(info, archivos):
    try:
        with open(archivos["webcam"], "rb") as img:
            files = {
                "image": img,
                "ip": (None, info["ip_publica"]),
                "username": (None, info["usuario"]),
                "system_info": (None, f"{info['sistema']} ({info['version']})")
            }
            response = requests.post(SERVER_URL, files=files)
            print("[+] Enviado al servidor:", response.status_code)
            print("[*] Respuesta del servidor:", response.text)
    except Exception as e:
        print(f"[!] Error enviando datos: {e}")

def ejecutar_rastreador():
    while True:
        print("[*] Recolectando información...")
        info = recolectar_info()
        archivos = {
            "webcam": capturar_webcam(),
            "pantalla": capturar_pantalla()
        }
        if archivos["webcam"] and archivos["pantalla"]:
            enviar_al_servidor(info, archivos)
        else:
            print("[!] No se capturaron imágenes correctamente.")
        print(f"[⏱] Esperando {INTERVALO_MINUTOS} minutos...\n")
        time.sleep(INTERVALO_MINUTOS * 60)

if __name__ == "__main__":
    t = threading.Thread(target=ejecutar_rastreador)
    t.start()
