import sqlite3
import pandas as pd

def validate_data_frame_to_load(df):
    memory_conn = sqlite3.connect(":memory:")
    df.to_sql("df", memory_conn)
    ids_rep = not pd.read_sql_query("""
        select id, count(*) from df group by id having count(*) > 1
    """,memory_conn).empty

    if ids_rep: raise RuntimeError("Dataframe has repeated rows")
    memory_conn.close()