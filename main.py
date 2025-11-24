#%%
from servicios.lector_fichero_evo import leer_excel_evo_y_mapear_objetos
from modelos.broker import BrokerEnum
import json
from decimal import Decimal
from dotenv import load_dotenv
import os
import modelos.constants as constants
import pandas as pd
import loader.split_loader as split_loader

load_dotenv()

def collect_ops_from_files(files_list: str, broker: BrokerEnum):
    ops = []
    for x in files_list.split(';'):
        ops = ops + leer_excel_evo_y_mapear_objetos(x, broker)
    return ops


def collect_all_ops_from_files():
    ops = []
    evo_files_path = os.getenv('SOURCE_EVO_FILES')
    ops = ops + collect_ops_from_files(evo_files_path, BrokerEnum.EVO)
    my_investor_files_path = os.getenv('SOURCE_MY_INVESTOR_FILES')
    ops = ops + collect_ops_from_files(my_investor_files_path, BrokerEnum.MYINVESTOR)

from servicios.operations_from_db import fetch_operaciones_from_db
# %%
import pandas as pd
ops = fetch_operaciones_from_db()
ops = ops + split_loader.read_all_splits(os.getenv(constants.EnvironmentVariableNames.SPLIT_PATH))
ops[0]

# %%
from servicios.compraventas_por_isin import operaciones_por_isin,agrupar_por_isin
compra_ventas = operaciones_por_isin(ops)
compra_ventas = sorted(compra_ventas, key=lambda x: x.venta.fecha.isoformat())
# %%
from servicios.compraventa_to_report import compraventa_to_report
from servicios.eur_usd import fetch_usd_eur_quote
dic_eur_price = fetch_usd_eur_quote(2023)
dic_eur_price = dic_eur_price | fetch_usd_eur_quote(2024)
dic_eur_price = dic_eur_price | fetch_usd_eur_quote(2025)
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
pd.DataFrame(report).to_excel('report.xlsx')
# %%
pd.DataFrame(compra_ventas).to_excel('compra_ventas.xlsx')
# %%
pd.DataFrame(agrupar_por_isin(ops)['IE00B652H904']).to_excel('IE00B652H904.xlsx')