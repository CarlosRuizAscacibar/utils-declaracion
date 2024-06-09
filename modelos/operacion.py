from decimal import Decimal
from modelos.tipo_operacion import TipoOperacion
from modelos.broker import BrokerEnum
from datetime import date


from modelos.base_model import BaseModel
from dataclasses import dataclass

@dataclass
class Operacion():
    fecha: date = None
    isin: str = None
    tipo: TipoOperacion = None
    cantidad: int = 0
    precio_unitario: Decimal = None
    divisa: str = None
    nombre: str = None
    importe_neto: Decimal = None
    broker: BrokerEnum = None
    restantes: int    = 0