#%%
from servicios.lector_fichero_evo import leer_excel_evo_y_mapear_objetos
from modelos.broker import BrokerEnum
import json
from decimal import Decimal
from dotenv import load_dotenv
import os

load_dotenv()

def collect_ops_from_files(files_list: str, broker: BrokerEnum):
    ops = []
    for x in files_list.split(';'):
        ops = ops + leer_excel_evo_y_mapear_objetos(x, broker)
    return ops

ops = []

evo_files_path = os.getenv('SOURCE_EVO_FILES')
ops = ops + collect_ops_from_files(evo_files_path, BrokerEnum.EVO)
my_investor_files_path = os.getenv('SOURCE_MY_INVESTOR_FILES')
ops = ops + collect_ops_from_files(my_investor_files_path, BrokerEnum.MYINVESTOR)


# %%
import pandas as pd
# %%
from servicios.compraventas_por_isin import operaciones_por_isin
compra_ventas = operaciones_por_isin(ops)
compra_ventas = sorted(compra_ventas, key=lambda x: x.venta.fecha.isoformat())
# %%
from servicios.compraventa_to_report import compraventa_to_report
from servicios.eur_usd import fetch_usd_eur_quote
dic_eur_price = fetch_usd_eur_quote()
report = []
for x in compra_ventas:
    x_to_report = compraventa_to_report(x)
    x_to_report_json = json.loads(x_to_report.to_json())
    dec_precio_total_compra = (x_to_report.precio_total_compra / dic_eur_price[x.compra.fecha.strftime('%Y-%m-%d')]).quantize(Decimal('0.00'))
    x_to_report_json['precio_total_compra_eur']= dec_precio_total_compra.to_eng_string()
    dec_precio_total_venta = (x_to_report.precio_total_venta / dic_eur_price[x.venta.fecha.strftime('%Y-%m-%d')]).quantize(Decimal('0.00'))
    x_to_report_json['precio_total_venta_eur']= dec_precio_total_venta.to_eng_string()
    x_to_report_json['ganancia_perdida_eur']= (dec_precio_total_venta - dec_precio_total_compra).to_eng_string()
    report.append(x_to_report_json)

# %%
pd.DataFrame(report).to_excel(os.getenv('MOVEMENTS_RESULT'))
# %%
