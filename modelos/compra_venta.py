from modelos.operacion import Operacion
from modelos.base_model import BaseModel
from datetime import date
from decimal import Decimal

class CompraVenta(BaseModel):
    def __init__(self, compra: Operacion, venta: Operacion, cantidad: int):
        self.compra: Operacion = compra
        self.venta: Operacion = venta
        self.cantidad: int = cantidad
    
class CompraVentaReport(BaseModel):
    def __init__(self,
        nombre: str, 
        isin: str,
        fecha_compra: date,
        broker_compra: str,
        precio_unitario_compra: Decimal,
        fecha_venta: date,
        broker_venta: str,
        precio_unitario_venta: Decimal,
        cantidad: int,
        precio_total_compra: Decimal,
        precio_total_venta: Decimal,
        ganancia_perdida: Decimal
    ):
        self.nombre = nombre
        self.isin = isin
        self.fecha_compra = fecha_compra
        self.broker_compra = broker_compra
        self.precio_unitario_compra = precio_unitario_compra
        self.fecha_venta = fecha_venta
        self.broker_venta = broker_venta
        self.precio_unitario_venta = precio_unitario_venta
        self.cantidad = cantidad
        self.precio_total_compra = precio_total_compra
        self.precio_total_venta = precio_total_venta
        self.ganancia_perdida = ganancia_perdida