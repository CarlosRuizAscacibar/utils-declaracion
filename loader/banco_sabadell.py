#%%
import pandas as pd
import dotenv
import datetime
dotenv.load_dotenv()
import os
from decimal import Decimal
from modelos.movimiento_corriente import MovimientoCorriente
file_path = os.getenv('MOVIMIENTOS_SABADELL')
from servicios.id_generator import gen_id_movimiento_corriente
from servicios.validate_dataframe_to_load import validate_data_frame_to_load, remove_present_ids_in_database
from servicios.persist_dataframe import persist_dataframe
from servicios.date_parser import parse_dd_mm_yyyy
import modelos.constants as constants
from os import listdir
from os.path import isfile, join


def read_sabadell_excel(current_file):
    df = pd.read_excel(current_file)[7:]
    df.columns = df.iloc[0]  # Set the column headers to the values of the first row
    df = df[1:].reset_index(drop=True)
    df.columns.name = 'index'
    return df

def convert_row_to_movement(x):
    fecha_operacion_str, concepto,fecha_valor_str, importe_str, saldo_str = x[:5]
    fecha_operacion = parse_dd_mm_yyyy(fecha_operacion_str)
    fecha_valor = parse_dd_mm_yyyy(fecha_valor_str)
    importe = Decimal(importe_str).quantize(Decimal('0.01'))
    saldo = Decimal(saldo_str).quantize(Decimal('0.01'))

    mov = MovimientoCorriente(id='',banco=constants.BankNames.SABADELL, concepto=concepto, importe=importe, fecha_contable=fecha_operacion, fecha_valor=fecha_valor, saldo=saldo)
    mov.id = gen_id_movimiento_corriente(mov)
    return mov

def read_single_file(file_path):
    print(f'Reading sabadell file {file_path}')
    df = read_sabadell_excel(file_path)
    movs = [convert_row_to_movement(x) for x in df.values]
    print(f'extracted {len(movs)} movements')
    mov_df = pd.DataFrame(movs).set_index('id')
    mov_df['importe'] = mov_df['importe'].apply(str)
    mov_df['saldo'] = mov_df['saldo'].apply(str)
    validate_data_frame_to_load(mov_df)
    mov_df = remove_present_ids_in_database(mov_df, constants.TableNames.BANK_MOVEMENT)
    persist_dataframe(mov_df, constants.TableNames.BANK_MOVEMENT)
    print('File loaded to the database')

def process_all_files_from_folder(file_path):
    files_in_folder = [f'{file_path}/{f}' for f in listdir(file_path) if isfile(join(file_path, f))]
    for current_file in files_in_folder:
        read_single_file(current_file)

if __name__ == '__main__':
    process_all_files_from_folder(file_path)
