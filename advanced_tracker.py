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
        res = requests.get(f"https://ipinfo.io/{ip}/json")
        data = res.json()
        print(f"[*] Geolocalización obtenida: {data}")
        return {
            "ciudad": data.get("city"),
            "region": data.get("region"),
            "pais": data.get("country"),
            "loc": data.get("loc")
        }
    except Exception as e:
        print(f"[!] Error al obtener geolocalización: {e}")
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
    print("[*] Información recolectada:")
    print(json.dumps(info, indent=2))
    return info

def enviar_al_servidor(info, archivos):
    try:
        if not archivos["webcam"]:
            print("[!] No se encontró archivo de webcam para enviar.")
            return
        # Abre el archivo de imagen en modo binario.
        with open(archivos["webcam"], "rb") as img:
            files = {"image": img}
            # Envía los datos de texto en el campo 'data'.
            data = {
                "ip": info["ip_publica"],
                "username": info["usuario"],
                "system_info": f"{info['sistema']} ({info['version']})"
            }
            print("[*] Enviando datos al servidor:")
            print("   Datos:", data)
            response = requests.post(SERVER_URL, files=files, data=data)
            print("[+] Enviado al servidor:", response.status_code)
            print("[*] Respuesta del servidor:", response.text)
    except Exception as e:
        print(f"[!] Error enviando datos: {e}")

def ejecutar_rastreador():
    while True:
        print("\n[*] Recolectando información para nuevo reporte...")
        info = recolectar_info()
        archivos = {
            "webcam": capturar_webcam(),
            "pantalla": capturar_pantalla()  # Se capta, pero no se utiliza en el envío actual
        }
        if archivos["webcam"]:
            enviar_al_servidor(info, archivos)
        else:
            print("[!] No se capturó imagen correctamente, reporte cancelado.")
        print(f"[⏱] Esperando {INTERVALO_MINUTOS} minutos...\n")
        time.sleep(INTERVALO_MINUTOS * 60)

if __name__ == "__main__":
    t = threading.Thread(target=ejecutar_rastreador)
    t.start()
