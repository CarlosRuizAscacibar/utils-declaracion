from dotenv import load_dotenv
import os
from servicios.lector_fichero_corriente_evo import leer_excel_corriente_evo
import pandas as pd
from servicios.validate_dataframe_to_load import validate_data_frame_to_load
load_dotenv()
import sqlite3
import json
from servicios.persist_dataframe import persist_dataframe


def main():
    movs = leer_excel_corriente_evo(os.getenv('MOVIMIENTOS_CUENTA_CORRIENTE_EVO'),'evo')
    df = pd.DataFrame.from_dict([json.loads(x.to_json()) for x in movs]).set_index('id')
    validate_data_frame_to_load(df)
    persist_dataframe(df,"bank_movements")

if __name__ == '__main__':
    main()