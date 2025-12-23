from decimal import Decimal
from modelos.compra_venta import CompraVenta
from modelos.operacion import Operacion
from modelos.tipo_operacion import TipoOperacion
from modelos.broker import BrokerEnum
from datetime import date


from modelos.base_model import BaseModel
from dataclasses import dataclass

@dataclass
class CarteraIsin():
    isin: str
    operaciones: list[Operacion]
    compra_ventas: list[CompraVenta]
    acciones_actual: int
    