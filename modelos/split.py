from datetime import datetime
from pydantic import BaseModel, Field


class Split(BaseModel):
    id: str = Field(..., description="Identificador unico del split")
    isin: str = Field(..., description="Identificador ISIN del valor")
    fecha: datetime = Field(..., description="Fecha del evento")
    numOriginal: int = Field(..., description="Número original de acciones antes del split")
    numDestino: int = Field(..., description="Número resultante de acciones después del split")
