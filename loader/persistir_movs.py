
from typing import List

import pandas as pd

from modelos import constants
from modelos.constants import TableNames
from modelos.movimiento_corriente import MovimientoCorriente
from servicios.persist_dataframe import persist_dataframe
from servicios.validate_dataframe_to_load import remove_present_ids_in_database, validate_data_frame_to_load

def movs_to_dataframe(movs: List[MovimientoCorriente]) -> pd.DataFrame:
    print(f'extracted {len(movs)} movements')
    mov_df = pd.DataFrame(movs).set_index('id')
    mov_df['importe'] = mov_df['importe'].apply(str)
    mov_df['saldo'] = mov_df['saldo'].apply(str)
    return mov_df

def persistir_movimientos(movs: List[MovimientoCorriente]):
    mov_df = movs_to_dataframe(movs)
    validate_data_frame_to_load(mov_df)
    mov_df = remove_present_ids_in_database(mov_df, constants.TableNames.BANK_MOVEMENT)
    persist_dataframe(mov_df, constants.TableNames.BANK_MOVEMENT)
    print('File loaded to the database')




    
