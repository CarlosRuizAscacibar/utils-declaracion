from dotenv import load_dotenv
import os
from servicios.lector_fichero_corriente_evo import leer_excel_corriente_evo
import pandas as pd

load_dotenv()
import sqlite3
import json

def validate_data_frame(df):
    memory_conn = sqlite3.connect(":memory:")
    df.to_sql("df", memory_conn)
    ids_rep = not pd.read_sql_query("""
        select id, count(*) from df group by id having count(*) > 1
    """,memory_conn).empty

    if ids_rep: raise RuntimeError("Dataframe has repeated rows")
    memory_conn.close()

def main():
    movs = leer_excel_corriente_evo(os.getenv('MOVIMIENTOS_CUENTA_CORRIENTE_EVO'),'evo')
    df = pd.DataFrame.from_dict([json.loads(x.to_json()) for x in movs]).set_index('id')
    validate_data_frame(df)
    conn = sqlite3.connect(os.getenv('PERSONAL_DATABASE'))
    df.to_sql("bank_movements", conn, if_exists='append')
    conn.close()

if __name__ == '__main__':
    main()