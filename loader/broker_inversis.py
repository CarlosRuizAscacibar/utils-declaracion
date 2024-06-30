from dotenv import load_dotenv
import sys
sys.path.append("..")
import os
from servicios.lector_fichero_evo import leer_excel_evo_y_mapear_objetos
import pandas as pd

load_dotenv()
import sqlite3
import json
from modelos.constants import EnvironmentVariableNames


def validate_data_frame(df):
    memory_conn = sqlite3.connect(":memory:")
    df['tipo'] = df['tipo'].astype('str')
    df['precio_unitario'] = df['precio_unitario'].astype('str')
    df['importe_neto'] = df['importe_neto'].astype('str')
    df.to_sql("df", memory_conn)
    ids_rep = not pd.read_sql_query("""
        select id, count(*) from df group by id having count(*) > 1
    """,memory_conn).empty

    if ids_rep: raise RuntimeError("Dataframe has repeated rows")
    memory_conn.close()

def load_inversis_broker_operations(file_path, bank):
    movs = leer_excel_evo_y_mapear_objetos(file_path,bank)
    df = pd.DataFrame(movs).set_index('id')
    validate_data_frame(df)
    conn = sqlite3.connect(os.getenv(EnvironmentVariableNames.PERSONAL_DATABASE))
    df.to_sql("operacion", conn, if_exists='append')
    conn.close()
