import os
import time
import platform
import socket
import getpass
import threading
import requests
from datetime import datetime
from PIL import ImageGrab
import cv2

SERVER_URL = "https://laptop-tracker-server.onrender.com/report"
INTERVALO_MINUTOS = 15


def recolectar_info():
    try:
        ip = requests.get('https://api.ipify.org').text
    except:
        ip = "No disponible"

    username = getpass.getuser()
    system_info = f"{platform.system()} {platform.release()} | {platform.version()}"
    return {
        "ip": ip,
        "username": username,
        "system_info": system_info
    }


def capturar_webcam():
    try:
        cam = cv2.VideoCapture(0)
        result, image = cam.read()
        if result:
            filename = "webcam.jpg"
            cv2.imwrite(filename, image)
            cam.release()
            return filename
        cam.release()
    except:
        pass
    return None


def capturar_pantalla():
    try:
        imagen = ImageGrab.grab()
        filename = "screenshot.jpg"
        imagen.save(filename)
        return filename
    except:
        return None


def enviar_al_servidor(info, archivos):
    try:
        with open(archivos["webcam"], "rb") as img_file:
            files = {"image": img_file}
            data = {
                "ip": info["ip"],
                "username": info["username"],
                "system_info": info["system_info"]
            }
            print("=== DATOS ENVIADOS AL SERVIDOR ===")
            print("IP:", data["ip"])
            print("Usuario:", data["username"])
            print("Sistema:", data["system_info"])
            print("Archivo imagen:", archivos["webcam"])
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
