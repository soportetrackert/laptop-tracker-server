# 📡 Laptop Tracker Server

Este es un servidor Flask que recibe reportes de laptops monitoreadas. Guarda información como IP, usuario, sistema operativo y una imagen (webcam o de prueba).

## 🚀 Características
- Interfaz web protegida con login
- Recepción de reportes desde clientes
- Base de datos SQLite local
- Panel de control con imágenes

## 🛠 Requisitos
- Python 3.7+
- Flask

## ▶️ Uso local

```bash
pip install -r requirements.txt
python app.py
```

- Accede a: http://127.0.0.1:5000
- Usuario: `admin` | Contraseña: `admin123`

## 🌍 Despliegue en Render

1. Sube este proyecto a GitHub
2. Ve a [Render.com](https://render.com) y crea un nuevo Web Service
3. Configura:
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `python app.py`
   - **Environment**: Python 3.x
4. ¡Listo! Render te dará una URL pública

## 📥 Endpoint del cliente

El cliente debe enviar un POST a:

```
/report
```

Con los campos: `ip`, `username`, `system_info`, y archivo `image`.