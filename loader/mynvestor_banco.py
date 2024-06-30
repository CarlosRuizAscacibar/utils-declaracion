import pandas as pd
import dotenv
import datetime
dotenv.load_dotenv()
import os
from decimal import Decimal
from modelos.movimiento_corriente import MovimientoCorriente
from servicios.id_generator import gen_id_movimiento_corriente
from servicios.validate_dataframe_to_load import validate_data_frame_to_load
from servicios.persist_dataframe import persist_dataframe
import modelos.constants as constants

def parse_my_investor_date(str_date):
    return datetime.datetime.strptime( str_date,"%d/%m/%Y").date()

def process_raw_excel_dataframe(df):
    df = df[8:]
    df =  df.drop(df.columns[0], axis=1)
    df.columns = df.iloc[0]  # Set the column headers to the values of the first row
    df = df[1:].reset_index(drop=True)
    df.columns.name = 'index'
    df = df.drop(df.columns[3], axis=1)
    df['Movimiento'] = df['Movimiento'].fillna('')
    return df

def convert_row_to_movement(x):
    fecha_operacion_str, fecha_valor_str, concepto, importe_str, saldo_str = x
    fecha_operacion = parse_my_investor_date(fecha_operacion_str)
    fecha_valor = parse_my_investor_date(fecha_valor_str)
    importe = Decimal(importe_str).quantize(Decimal('0.01'))
    saldo = Decimal(saldo_str).quantize(Decimal('0.01'))

    mov = MovimientoCorriente(id='',banco="myinvestor", concepto=concepto, importe=importe, fecha_contable=fecha_operacion, fecha_valor=fecha_valor, saldo=saldo)
    mov.id = gen_id_movimiento_corriente(mov)
    return mov

def process_file(file_path):
    df = pd.read_excel(file_path)
    df = process_raw_excel_dataframe(df)
    movs = []
    for x in df.values:
        mov = convert_row_to_movement(x)
        movs.append(mov)
    
    mov_df = pd.DataFrame(movs).set_index('id')
    mov_df['importe'] = mov_df['importe'].apply(str)
    mov_df['saldo'] = mov_df['saldo'].apply(str)
    validate_data_frame_to_load(mov_df)
    persist_dataframe(mov_df, constants.TableNames.BANK_MOVEMENT)

if __name__ == '__main__':
    file_path = os.getenv('MOVIMIENTOS_MY_INVESTOR')
    process_file(file_path)