from openpyxl import load_workbook
import xlrd
from modelos.movimiento_corriente import MovimientoCorriente  
from modelos.broker import BrokerEnum
from decimal import Decimal
from modelos.tipo_operacion import TipoOperacion
from datetime import date, datetime
from servicios.id_generator import gen_id
import pandas as pd

def leer_excel_corriente_evo(ruta_archivo,banco):
    records = pd.read_excel(ruta_archivo).to_dict('records')
    operaciones = []

    # Read the data
    for record in records:
        fila = record.values()
        print(fila)
        fecha_contable,fecha_valor,concepto,importe,moneda1,saldo,moneda2 = fila
        operacion = MovimientoCorriente(
            id=gen_id(),
            concepto=concepto,
            importe=Decimal(importe),
            fecha_contable=fecha_contable.date(),
            fecha_valor=fecha_valor.date(),
            banco=banco
        )
        operaciones.append(operacion)
    
    return operaciones

def parse_evo_corriente_date(str_date):
    return datetime.strptime( str_date,"%d-%m-%Y").date()
