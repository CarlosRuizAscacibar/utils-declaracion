import string
import random
from modelos.movimiento_corriente import MovimientoCorriente
from modelos.operacion import Operacion
import hashlib
alphabet = string.ascii_lowercase + string.digits
_ID_DATEFORMAT="%Y%m%d"

def gen_id():
    return ''.join(random.choices(alphabet, k=12))

def gen_id_for_obj(obj):
    if isinstance(obj, MovimientoCorriente):
        return gen_id_movimiento_corriente(obj)
    return gen_id()

def gen_id_movimiento_corriente(mov: MovimientoCorriente):
    return mov.fecha_contable.strftime(_ID_DATEFORMAT) + "_" + hash_for_id(mov.concepto) + "_" +  str(mov.importe) + "_" + mov.banco + "_" + str(mov.saldo)

def gen_id_operacion(op: Operacion):
    return f'{op.fecha.strftime(_ID_DATEFORMAT)}_{op.isin}_{op.cantidad}_{op.tipo.name}_{str(op.importe_neto)}_{op.broker}'

def hash_for_id(str_to_hash):
    return hashlib.sha256(str_to_hash.encode('utf-8')).hexdigest()[:10]