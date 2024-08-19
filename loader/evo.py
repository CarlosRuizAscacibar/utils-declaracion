from dotenv import load_dotenv
import os
from servicios.lector_fichero_corriente_evo import leer_excel_corriente_evo
import pandas as pd
from servicios.validate_dataframe_to_load import validate_data_frame_to_load, remove_present_ids_in_database
load_dotenv()
import sqlite3
import json
from servicios.persist_dataframe import persist_dataframe
import modelos.constants as constants


def process_file(file_path):
    movs = leer_excel_corriente_evo(file_path,constants.BankNames.EVO)
    df = pd.DataFrame.from_dict([json.loads(x.to_json()) for x in movs]).set_index('id')
    print(f"Number of rows: {len(df)}")
    validate_data_frame_to_load(df)
    df = remove_present_ids_in_database(df,constants.TableNames.BANK_MOVEMENT)
    persist_dataframe(df,constants.TableNames.BANK_MOVEMENT)

if __name__ == '__main__':
    process_file(os.getenv(constants.EnvironmentVariableNames.MOVIMIENTOS_CUENTA_CORRIENTE_EVO))