from openpyxl import load_workbook
import xlrd
from modelos.movimiento_corriente import MovimientoCorriente  
from modelos.broker import BrokerEnum
from decimal import Decimal
from modelos.tipo_operacion import TipoOperacion
from datetime import date, datetime
from servicios.id_generator import gen_id, gen_id_movimiento_corriente
import pandas as pd

def leer_excel_corriente_evo(ruta_archivo,banco):
    records = pd.read_excel(ruta_archivo).to_dict('records')
    operaciones = []

    # Read the data
    for record in records:
        fila = record.values()
        fecha_contable,fecha_valor,concepto,importe,moneda1,str_saldo,moneda2 = fila
        saldo = Decimal(0).quantize(Decimal('0.01'))
        try:
            saldo=Decimal(str_saldo).quantize(Decimal('0.01'))
        except:
            pass
        operacion = MovimientoCorriente(
            id='',
            concepto=concepto,
            importe=Decimal(importe).quantize(Decimal('0.01')),
            fecha_contable=fecha_contable.date(),
            fecha_valor=fecha_valor.date(),
            banco=banco,
            saldo=saldo
        )
        operacion.id = gen_id_movimiento_corriente(operacion)
        operaciones.append(operacion)
    
    return operaciones

def parse_evo_corriente_date(str_date):
    return datetime.strptime( str_date,"%d-%m-%Y").date()
