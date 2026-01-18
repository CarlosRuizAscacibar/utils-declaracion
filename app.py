from datetime import date, datetime
import math
import subprocess
from flask import Flask, jsonify, send_from_directory
import os
from flask.json.provider import DefaultJSONProvider
from enum import Enum

from pydantic import BaseModel
from loader import split_loader
from modelos import constants
from servicios import compraventas_por_isin, operations_from_db, year_report_srv, backup_service
from servicios.eur_usd import fetch_all_conv
app = Flask(__name__, static_folder='static')
import dotenv
dotenv.load_dotenv()

def is_nan(x):
    try:
        return math.isnan(x)
    except (TypeError, ValueError):
        return False
    
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.model_dump(mode="json")
        if isinstance(obj, Enum):
            return obj.value
        if is_nan(obj):
            return None
        if isinstance(obj, (datetime, date)):
            return obj.strftime("%d-%m-%Y")
        return super().default(obj)

    
app.json = CustomJSONProvider(app)

@app.route("/cartera/<isin>", methods=["GET"])
def ping(isin):
    all_ops = operations_from_db.fetch_compras_ventas_from_db()
    all_ops = all_ops + split_loader.read_all_splits(os.getenv(constants.EnvironmentVariableNames.SPLIT_PATH))
    dic_curr = fetch_all_conv()

    return jsonify(compraventas_por_isin.cartere_isin(all_ops, isin, dic_curr))

@app.route("/report/year/<year>", methods=["GET"])
def year_report(year):
    all_ops = operations_from_db.fetch_compras_ventas_from_db()
    all_ops = all_ops + split_loader.read_all_splits(os.getenv(constants.EnvironmentVariableNames.SPLIT_PATH))
    dic_curr = fetch_all_conv()
    
    return jsonify(year_report_srv.year_report(all_ops, year, dic_curr))

@app.route("/diferentes_acciones", methods=["GET"])
def diferentes_acciones():
    return jsonify(operations_from_db.stocks_in_account())

@app.route("/backup", methods=["POST"])
def backup_database():
    success, message, path = backup_service.create_database_backup()

    if success:
        return jsonify({"message": message, "path": path})
    else:
        return jsonify({"error": message}), 500

@app.route("/backup/last", methods=["GET"])
def get_last_backup():
    last_backup = backup_service.get_last_backup_time()
    if last_backup:
        return jsonify({"last_backup": last_backup})
    else:
        return jsonify({"last_backup": None}), 404

@app.route("/load_files", methods=["POST"])
def load_files():
    try:
        result = subprocess.run(["python", "load_all_files.py"], capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            return jsonify({"message": "Files loaded successfully", "output": result.stdout})
        else:
            return jsonify({"error": result.stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
