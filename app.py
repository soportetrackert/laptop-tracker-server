@app.route("/")
def index():
    if not os.path.exists("reportes.json"):
        return render_template("index.html", reports=[])

    with open("reportes.json", "r") as f:
        datos = json.load(f)

    reports = []
    for i, r in enumerate(datos):
        reports.append({
            "id": i + 1,
            "hostname": r.get("hostname", "N/A"),
            "username": r.get("username", "N/A"),
            "system": r.get("system_info", "N/A"),
            "ip": r.get("ip", "N/A"),
            "fecha": r.get("hora", "N/A"),
            "imagen": r.get("imagen")
        })

    return render_template("index.html", reports=reports)
