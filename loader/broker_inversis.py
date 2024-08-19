from dotenv import load_dotenv
import sys
sys.path.append("..")
import os
from servicios.lector_fichero_evo import leer_excel_evo_y_mapear_objetos
import pandas as pd

load_dotenv()
import sqlite3
import json
from modelos.constants import EnvironmentVariableNames, TableNames
from servicios.validate_dataframe_to_load import remove_present_ids_in_database,validate_data_frame_to_load
from servicios.persist_dataframe import persist_dataframe

def load_inversis_broker_operations(file_path, bank):
    movs = leer_excel_evo_y_mapear_objetos(file_path,bank)
    df = pd.DataFrame(movs).set_index('id')
    df['tipo'] = df['tipo'].astype('str')
    df['precio_unitario'] = df['precio_unitario'].astype('str')
    df['importe_neto'] = df['importe_neto'].astype('str')
    print(f"Number of rows: {len(df)}")
    validate_data_frame_to_load(df)
    df = remove_present_ids_in_database(df, TableNames.OPERATION)
    persist_dataframe(df, TableNames.OPERATION)
