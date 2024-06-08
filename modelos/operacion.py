from decimal import Decimal
from modelos.tipo_operacion import TipoOperacion
from modelos.broker import BrokerEnum
from datetime import date


from modelos.base_model import BaseModel
class Operacion():
    def __init__(self,
                 id: str,
                 fecha: date,
                 isin: str,
                 tipo: TipoOperacion = None,
                 cantidad: int = None,
                 precio_unitario: Decimal = None,
                 divisa: str = None,
                 nombre: str = None,
                 importe_neto: Decimal = None,
                 broker: BrokerEnum = None,                
                 ):
        self.id: str = id
        self.fecha: date = fecha
        self.isin: str = isin
        self.tipo: TipoOperacion = tipo  # Compra o venta
        self.cantidad: int = cantidad
        self.precio_unitario: Decimal = precio_unitario
        self.divisa: str = divisa
        self.nombre: str = nombre
        self.importe_neto: Decimal = importe_neto
        self.broker: BrokerEnum = broker
        self.restantes: int = cantidad
