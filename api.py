from flask import Flask, jsonify

INI_FILE = "/data/statistics.ini"
app = Flask(__name__)

def load_stats(path: str) -> dict:
    stats = {}
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8-sig", "utf-16", "utf-16le", "utf-16be", "latin-1"):
        try:
            text = raw.decode(enc); break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="ignore")

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("[") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        key = k.strip().lower()
        val = v.strip()
        try:
            stats[key] = int(val)
        except ValueError:
            try:
                stats[key] = float(val)
            except ValueError:
                stats[key] = val
    return stats

@app.route("/api/emule")
def emule_stats():
    s = load_stats(INI_FILE)

    # Totales
    up_total = int(float(s.get("totaluploadedbytes", 0)))
    down_total = int(float(s.get("totaldownloadedbytes", 0)))
    runtime_total = int(float(s.get("connruntime", 0)))
    ratio_total = float(up_total / down_total) if down_total > 0 else 0.0

    # Sesión
    up_session = (
        int(s.get("updata_file", 0)) +
        int(s.get("updata_partfile", 0)) +
        int(s.get("upoverheadtotal", 0))
    )
    down_session = (
        int(s.get("downdata_emule", 0)) +
        int(s.get("downdata_mldonkey", 0)) +
        int(s.get("downdata_lmule", 0)) +
        int(s.get("downdata_amule", 0)) +
        int(s.get("downdata_shareaza", 0)) +
        int(s.get("downoverheadtotal", 0))
    )
    runtime_session = runtime_total  # en eMule, ConnRunTime se resetea junto con estadísticas
    ratio_session = float(up_session / down_session) if down_session > 0 else 0.0

    return jsonify({
        # Totales
        "upload_bytes": up_total,
        "download_bytes": down_total,
        "ratio_total": ratio_total,
        "uptime_seconds": runtime_total,

        # Sesión
        "session_upload_bytes": up_session,
        "session_download_bytes": down_session,
        "session_ratio": ratio_session,
        "session_runtime_seconds": runtime_session,

        "status": "up"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
