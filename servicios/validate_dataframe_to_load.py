import sqlite3
import pandas as pd
import os

def validate_data_frame_to_load(df):
    memory_conn = sqlite3.connect(":memory:")
    df.to_sql("df", memory_conn)
    ids_rep = not pd.read_sql_query("""
        select id, count(*) from df group by id having count(*) > 1
    """,memory_conn).empty

    if ids_rep: raise RuntimeError("Dataframe has repeated rows")
    memory_conn.close()

def remove_present_ids_in_database(df_new_rows: pd.DataFrame, table):
    db_path = os.getenv('PERSONAL_DATABASE')
    remove_present_ids_in_database_with_path(df_new_rows, table, db_path)


def remove_present_ids_in_database_with_path(df_new_rows: pd.DataFrame, table, db_path):
    with sqlite3.connect(":memory:") as memory_conn, sqlite3.connect(db_path) as conn:
        existing_rows = pd.read_sql_query(
            f"select id from {table}",
            conn
        )

        df_new_rows.to_sql(
            "df_new_rows",
            memory_conn,
            if_exists="replace",
            index=False
        )
        existing_rows.to_sql(
            "existing_rows",
            memory_conn,
            if_exists="replace",
            index=False
        )

        rows_not_in_db = pd.read_sql_query("""
            select *
            from df_new_rows
            where id not in (select id from existing_rows)
        """, memory_conn)

        rows_in_db = pd.read_sql_query("""
            select *
            from df_new_rows
            where id in (select id from existing_rows)
        """, memory_conn)

        print(
            f"Removed {rows_in_db.shape[0]} rows "
            f"as the id was present in table {table}"
        )

    # outside the with: connections are closed
    return rows_not_in_db.set_index("id")



