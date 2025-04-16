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
            print("[*] Imagen de webcam capturada.")
            return filename
        else:
            print("[!] No se pudo capturar imagen de la webcam.")
    except Exception as e:
        print(f"[!] Error al capturar webcam: {e}")
    return None

def capturar_pantalla():
    try:
        screenshot = pyautogui.screenshot()
        filename = "screenshot.jpg"
        screenshot.save(filename)
        print("[*] Captura de pantalla realizada.")
        return filename
    except Exception as e:
        print(f"[!] Error al capturar pantalla: {e}")
    return None

def obtener_ip_publica():
    try:
        ip = requests.get("https://api.ipify.org").text
        print(f"[*] IP pública obtenida: {ip}")
        return ip
    except Exception as e:
        print(f"[!] Error al obtener IP pública: {e}")
        return "Desconocida"

def obtener_geolocalizacion(ip):
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        if res.status_code == 200:
            data = res.json()
            print(f"[*] Geolocalización obtenida: {data}")
            return {
                "ciudad": data.get("city"),
                "region": data.get("region"),
                "pais": data.get("country"),
                "loc": data.get("loc")
            }
        else:
            print(f"[!] Error {res.status_code} al obtener geolocalización.")
            return {}
    except Exception as e:
        print(f"[!] Error al obtener geolocalización: {e}")
        return {}

def recolectar_info():
    ip = obtener_ip_publica()
    info = {
        "ip": ip,
        "username": getpass.getuser(),
        "system_info": f"{platform.system()} {platform.release()} ({platform.version()})",
        "nombre_equipo": socket.gethostname(),
        "hora": str(datetime.now())
    }
    info.update(obtener_geolocalizacion(ip))
    print("[*] Información recolectada:", json.dumps(info, indent=2))
    return info

def enviar_al_servidor(info, archivos):
    try:
        with open(archivos["webcam"], "rb") as img_file:
            files = {"image": img_file}
            data = {
                "ip": info["ip"],
                "username": info["username"],
                "system_info": info["system_info"]
            }
            print("[*] Enviando al servidor:")
            print("  data:", data)
            response = requests.post(SERVER_URL, data=data, files=files)
            print("[+] Respuesta:", response.status_code, response.text)
    except Exception as e:
        print(f"[!] Error al enviar al servidor: {e}")

def ejecutar_rastreador():
    while True:
        print("\n[*] Ejecutando rastreador...")
        info = recolectar_info()
        webcam = capturar_webcam()
        pantalla = capturar_pantalla()
        archivos = {"webcam": webcam, "pantalla": pantalla}
        if webcam:
            enviar_al_servidor(info, archivos)
        else:
            print("[!] No se capturó webcam.")
        time.sleep(INTERVALO_MINUTOS * 60)

if __name__ == "__main__":
    t = threading.Thread(target=ejecutar_rastreador)
    t.start()
