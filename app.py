from datetime import date, datetime
import math
from flask import Flask, jsonify
import os
from flask.json.provider import DefaultJSONProvider
from enum import Enum

from pydantic import BaseModel
from loader import split_loader
from modelos import constants
from servicios import compraventas_por_isin, operations_from_db, year_report_srv
from servicios.eur_usd import fetch_all_conv
app = Flask(__name__)
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
    all_ops = operations_from_db.fetch_operaciones_from_db()
    all_ops = all_ops + split_loader.read_all_splits(os.getenv(constants.EnvironmentVariableNames.SPLIT_PATH))
    dic_curr = fetch_all_conv()

    return jsonify(compraventas_por_isin.cartere_isin(all_ops, isin, dic_curr))

@app.route("/report/year/<year>", methods=["GET"])
def year_report(year):
    all_ops = operations_from_db.fetch_operaciones_from_db()
    all_ops = all_ops + split_loader.read_all_splits(os.getenv(constants.EnvironmentVariableNames.SPLIT_PATH))
    dic_curr = fetch_all_conv()
    
    return jsonify(year_report_srv.year_report(all_ops, year, dic_curr))

@app.route("/diferentes_acciones", methods=["GET"])
def diferentes_acciones():
    return jsonify(operations_from_db.stocks_in_account())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
