from modelos.base_model import BaseModel
from datetime import date
from decimal import Decimal
from dataclasses import dataclass

@dataclass
class MovimientoCorriente(BaseModel):
    id: str
    concepto: str 
    importe: Decimal 
    fecha_contable: date 
    fecha_valor: date 
    banco: str 
    saldo: Decimal
    tipo: str = ""


