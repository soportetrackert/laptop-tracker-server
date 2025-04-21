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
            "ciudad": data.get("city", "N/A"),
            "region": data.get("region", "N/A"),
            "pais": data.get("country", "N/A"),
            "loc": data.get("loc", "N/A")
        }
    except:
        return {
            "ciudad": "N/A",
            "region": "N/A",
            "pais": "N/A",
            "loc": "N/A"
        }

def recolectar_info():
    ip = obtener_ip_publica()
    geodata = obtener_geolocalizacion(ip)
    info = {
        "ip": ip,
        "username": getpass.getuser(),
        "system_info": f"{platform.system()} {platform.release()} ({platform.version()})",
        "hostname": socket.gethostname(),
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ciudad": geodata["ciudad"],
        "region": geodata["region"],
        "pais": geodata["pais"],
        "loc": geodata["loc"]
    }
    print("[*] Datos recopilados para envío:")
    print(json.dumps(info, indent=2))
    return info

def enviar_al_servidor(info, archivos):
    try:
        with open(archivos["webcam"], "rb") as img_file:
            files = {"image": img_file}
            data = info  # ✅ ahora se envía TODO el diccionario de info
            print("[*] Enviando al servidor...")
            print("  Payload:", data)
            response = requests.post(SERVER_URL, data=data, files=files)
            print(f"[+] Respuesta del servidor: {response.status_code} {response.text}")
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
