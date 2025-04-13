
from typing import List

import pandas as pd

from modelos.constants import TableNames
from modelos.operacion import Operacion
from servicios.persist_dataframe import persist_dataframe
from servicios.validate_dataframe_to_load import remove_present_ids_in_database, validate_data_frame_to_load


def persisitir_operaciones(ops: List[Operacion]):
    df = pd.DataFrame(ops).set_index('id')
    df['tipo'] = df['tipo'].astype('str')
    df['precio_unitario'] = df['precio_unitario'].astype('str')
    df['importe_neto'] = df['importe_neto'].astype('str')
    print(f"Number of rows: {len(df)}")
    validate_data_frame_to_load(df)
    df = remove_present_ids_in_database(df, TableNames.OPERATION)
    persist_dataframe(df, TableNames.OPERATION)