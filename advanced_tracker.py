import requests
import socket
import platform
import getpass
import json
import os
from datetime import datetime
from PIL import ImageGrab
import cv2

# ===============================
# 📡 RECOLECTAR INFORMACIÓN
# ===============================
def recolectar_info():
    try:
        ip = requests.get("https://ipinfo.io/ip").text.strip()
        ubicacion = requests.get("https://ipinfo.io/json").json()
    except:
        ip = "No IP"
        ubicacion = {}

    return {
        "ip": ip,
        "username": getpass.getuser(),
        "system_info": f"{platform.system()} {platform.release()} ({platform.version()})",
        "hostname": socket.gethostname(),
        "ciudad": ubicacion.get("city", ""),
        "region": ubicacion.get("region", ""),
        "pais": ubicacion.get("country", ""),
        "loc": ubicacion.get("loc", ""),
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# ===============================
# 📸 CAPTURAR IMAGEN DE WEBCAM O IMAGEN POR DEFECTO
# ===============================
def capturar_imagen(nombre_archivo="captura.jpg"):
    try:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(nombre_archivo, frame)
        else:
            raise Exception("No se pudo capturar imagen.")
        cam.release()
    except:
        # Imagen de prueba si la webcam falla
        imagen_prueba = ImageGrab.grab()
        imagen_prueba.save(nombre_archivo)

    return nombre_archivo

# ===============================
# 📤 ENVIAR DATOS AL SERVIDOR
# ===============================
def enviar_al_servidor(info, imagen_path):
    url = "https://laptop-tracker-server.onrender.com/report"  # Tu URL de Render

    try:
        with open(imagen_path, "rb") as img:
            files = {"image": img}
            data = {
                "ip": info.get("ip", "No IP"),
                "username": info.get("username", "No user"),
                "system_info": info.get("system_info", "No system"),
                "hostname": info.get("hostname", "No hostname"),
                "ciudad": info.get("ciudad", ""),
                "region": info.get("region", ""),
                "pais": info.get("pais", ""),
                "loc": info.get("loc", ""),
                "hora": info.get("hora", "")
            }

            response = requests.post(url, data=data, files=files)
            print("✅ Enviado:", response.status_code)
    except Exception as e:
        print("❌ Error al enviar:", e)

# ===============================
# 🚀 EJECUCIÓN PRINCIPAL
# ===============================
if __name__ == "__main__":
    print("📡 Recolectando información...")
    info = recolectar_info()
    print(json.dumps(info, indent=2))

    print("📸 Capturando imagen...")
    imagen = capturar_imagen()

    print("📤 Enviando reporte al servidor...")
    enviar_al_servidor(info, imagen)

    # Eliminar la imagen local después de enviarla
    os.remove(imagen)
