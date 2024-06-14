import sqlite3
import os

def persist_dataframe(df, table_name):
    conn = sqlite3.connect(os.getenv('PERSONAL_DATABASE'))
    df.to_sql(table_name, conn, if_exists='append')
    conn.close()