import datetime
from typing import List
from loader.persistir_movs import persistir_movimientos
from loader.persistir_ops import persisitir_operaciones
from modelos import constants
from modelos.movimiento_corriente import MovimientoCorriente
from servicios.utils import list_files_in_folder
from modelos.constants import EnvironmentVariableNames,MovementTypes
from modelos.tipo_operacion import TipoOperacion
from modelos.operation_details import OrderDetails
import os
from decimal import Decimal
import json
from servicios.id_generator import gen_id_movimiento_corriente, gen_id_operacion
from modelos.operacion import Operacion

def load_all_operations_and_persist():
    persisitir_operaciones(load_all_operations_from_json())

def load_all_operations_from_json() -> List[Operacion]:
    file_path = os.getenv(EnvironmentVariableNames.JSON_BROKER_MY_INVESTOR)
    files_in_folder = list_files_in_folder(file_path)
    operations = []
    operations_ids = set()
    for json_file in files_in_folder:
        ops_in_read_file = read_operations_from_json(json_file)
        for x in ops_in_read_file:
            if x.id not in operations_ids:
                operations_ids.add(x.id)
                operations.append(x)
    return operations



def read_operations_from_json(json_path) -> List[Operacion]:
    contents = ''
    with open(json_path, 'r', encoding='utf8') as f:
        contents = f.read()

    operations = []
    json_orders = json.loads(contents)
    for x in json_orders:
        order = OrderDetails(**x)
        operations.append(order_to_operation(order))
    return operations
    
    

def myinvestor_order_get_operacion_type(order: OrderDetails) -> TipoOperacion:
    if order.orderOperationTypeEnum == 'BUY':
        return TipoOperacion.COMPRA
    if order.orderOperationTypeEnum == 'SELL':
        return TipoOperacion.VENTA
    raise ValueError("unknown myinvestor orderOperationTypeEnum "+ order.orderOperationTypeEnum)

def order_to_operation(order:OrderDetails) -> Operacion:
    operacion = Operacion(
                fecha=order.finishDate.date(), 
                isin=order.instrumentIsin, 
                tipo=myinvestor_order_get_operacion_type(order), 
                cantidad=order.shares, 
                precio_unitario=Decimal(order.priceCurrency).quantize(Decimal('0.01')), 
                divisa=order.instrumentCurrency, 
                nombre=order.instrumentName, 
                importe_neto=Decimal(order.netAmountCurrency).quantize(Decimal('0.01')), 
                broker='myinvestor',
                restantes=order.shares
            )
    operacion.id = gen_id_operacion(operacion)
    return operacion


def remove_characters(s: str, n: int, y: int) -> str:
    return s[n:len(s) - y]
def to_dec_quant(num):
    return Decimal(num).quantize(Decimal('0.01'))


def to_movimiento(mov_dic):
    concepto = remove_characters(mov_dic['operationRef'], 28, 25).strip()
    importe = to_dec_quant(mov_dic['amount'])
    saldo = to_dec_quant(mov_dic['totalBalance'])
    fecha_operacion = datetime.datetime.fromtimestamp(mov_dic['operationDate']/1000.0,tz=datetime.timezone.utc).date()
    tipo = translate_tipo(mov_dic['operationType'])
    mov = MovimientoCorriente(id='',banco=constants.BankNames.MYINVESTOR, concepto=concepto, importe=importe, fecha_contable=fecha_operacion, fecha_valor=fecha_operacion, saldo=saldo, tipo=tipo)
    mov.id = gen_id_movimiento_corriente(mov)
    return mov

def read_movements_from_json(json_path) -> list[MovimientoCorriente]:
    contents = ''
    with open(json_path, 'r', encoding='utf8') as f:
        contents = f.read()

    movements = []
    json_orders = json.loads(contents)
    for x in json_orders:
        movement = to_movimiento(x)
        movements.append(movement)
    return movements

def read_all_movements() -> List[MovimientoCorriente]:
    file_path = os.getenv(EnvironmentVariableNames.JSON_BANK_MY_INVESTOR)
    files_in_folder = list_files_in_folder(file_path)
    operations = []
    operations_ids = set()
    for json_file in files_in_folder:
        ops_in_read_file = read_movements_from_json(json_file)
        print(f'file {json_file} has {len(ops_in_read_file)} movements')
        for x in ops_in_read_file:
            if x.id not in operations_ids:
                operations_ids.add(x.id)
                operations.append(x)
        print(f'detected {len(operations)} unique movements')
    return operations

def load_all_movements_and_persist():
    movements = read_all_movements()
    persistir_movimientos(movements)
    
    #movimientos = [to_movimiento(x) for x in mov_list]
    #movimientos

def translate_tipo(raw_tipo):
    raw_tipo_tipo = {
        "COMPRA RV CONTADO": MovementTypes.COMPRA_VALOR,
        "VENTA DE VALORES": MovementTypes.VENTA_VALOR,
        "ABONO DE DIVIDENDO": MovementTypes.DIVIDENDO,
        "TRANSFERENCIA SEPA": MovementTypes.TRANSFERENCIA,
        "LIQUIDAC. INTERESES": MovementTypes.INTERESES,
        "TRANSFERENCIA INMEDIATA": MovementTypes.TRANSFERENCIA
    }
    if raw_tipo in raw_tipo_tipo:
        return raw_tipo_tipo[raw_tipo]
