from modelos.base_model import BaseModel
from datetime import date
from decimal import Decimal

class MovimientoCorriente(BaseModel):
    def __init__(self,id: str,
                    concepto: str,
                    importe: Decimal,
                    fecha_contable: date,
                    fecha_valor: date,
                    banco:str
                ):
        self.id: str=id
        self.concepto: str = concepto
        self.importe: Decimal = importe
        self.fecha_contable: date = fecha_contable
        self.fecha_valor: date = fecha_valor
        self.banco: str = banco

