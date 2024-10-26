from flask import Flask, jsonify, request, abort
import psutil
from config import LOCAL
import socket
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='/app/.env')

app = Flask(__name__)

try:
    ip_master_resolved = socket.gethostbyname(os.getenv('IP_MASTER'))
    AUTHORIZED_IPS = [ip_master_resolved, LOCAL]
except socket.gaierror:
    print(f"Impossible de résoudre le nom de domaine {os.getenv('IP_MASTER')}")
    AUTHORIZED_IPS = [LOCAL]

@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    if client_ip not in AUTHORIZED_IPS:
        abort(403)  # Refuser l'accès avec un code 403 (Forbidden)

@app.route('/resources')
def resources():
    # Obtenir des informations sur l'utilisation du CPU, de la mémoire et du disque
    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')

    return jsonify({
        "cpu_usage": cpu_usage,
        "memory_total": memory_info.total,
        "memory_used": memory_info.used,
        "memory_percentage": memory_info.percent,
        "disk_total": disk_usage.total,
        "disk_used": disk_usage.used,
        "disk_percentage": disk_usage.percent
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
