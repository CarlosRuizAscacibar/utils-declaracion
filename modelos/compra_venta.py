from modelos.operacion import Operacion
from modelos.base_model import BaseModel
from datetime import date
from decimal import Decimal
from dataclasses import dataclass
@dataclass
class CompraVenta(BaseModel):
    compra: Operacion
    venta: Operacion
    cantidad: int
        
@dataclass
class CompraVentaReport(BaseModel):
    nombre: str 
    isin: str
    fecha_compra: date
    broker_compra: str
    precio_unitario_compra: Decimal
    fecha_venta: date
    broker_venta: str
    precio_unitario_venta: Decimal
    cantidad: int
    precio_total_compra: Decimal
    precio_total_venta: Decimal
    ganancia_perdida: Decimal
