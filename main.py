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
import pandas as pd
from servicios.compraventas_por_isin import operaciones_por_isin,agrupar_por_isin
from servicios.compraventa_to_report import compraventa_to_report
from servicios.eur_usd import fetch_all_conv, fetch_eur_conv
from servicios.operations_from_db import fetch_operaciones_from_db


load_dotenv()

# %%
ops = fetch_operaciones_from_db()
ops = ops + split_loader.read_all_splits(os.getenv(constants.EnvironmentVariableNames.SPLIT_PATH))
ops[0]

# %%
compra_ventas = operaciones_por_isin(ops)
# %%
dic_all_curr= fetch_all_conv()
report = []
for x in compra_ventas:
    x_to_report = compraventa_to_report(x,dic_all_curr)
    x_to_report_json = json.loads(x_to_report.to_json())
    report.append(x_to_report_json)

# %%
pd.DataFrame(report).to_excel('report.xlsx')
