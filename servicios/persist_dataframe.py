import sqlite3
import os
import pandas as pd

from modelos.constants import EnvironmentVariableNames

def persist_dataframe(df: pd.DataFrame, table_name):
    with sqlite3.connect(os.getenv(EnvironmentVariableNames.PERSONAL_DATABASE)) as conn:
        df.to_sql(table_name, conn, if_exists='append')