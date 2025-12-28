from decimal import Decimal
from modelos.compra_venta import CompraVenta, CompraVentaReport
from modelos.movimiento_corriente import MovimientoCorriente
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
    compra_ventas_report: list[CompraVentaReport]
    dividendos: list[MovimientoCorriente]
    beneficio_dividendos: Decimal
    