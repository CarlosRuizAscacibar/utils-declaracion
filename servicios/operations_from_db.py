from decimal import Decimal
import os
import dotenv
from modelos.constants import EnvironmentVariableNames
import sqlite3
import pandas as pd
from modelos.operacion import Operacion
from servicios.lector_fichero_evo import _parse_operacion, parse_evo_date
dotenv.load_dotenv()
db_path = os.getenv(EnvironmentVariableNames.PERSONAL_DATABASE)
from modelos.broker import BrokerEnum


def _parse_broker(broker_str: str) -> BrokerEnum:
        if not broker_str:
            return None
        stripped_broker = broker_str.strip().lower()
        if 'evo' in stripped_broker:
            return BrokerEnum.EVO
        if 'myinvestor' in stripped_broker:
            return BrokerEnum.MYINVESTOR
        
def parse_operacion_record(operacion) -> Operacion:
    operacion['tipo'] = _parse_operacion(operacion['tipo'])
    operacion['broker'] = _parse_broker(operacion['broker'])
    operacion['fecha'] = parse_evo_date(operacion['fecha'])
    operacion['precio_unitario'] = Decimal(operacion['precio_unitario'])
    operacion['importe_neto'] = Decimal(operacion['importe_neto'])
    
    return Operacion(**operacion)

def fetch_operaciones_from_db():
    conn = sqlite3.connect(db_path)
    operacion_records = pd.read_sql("select * from operacion", conn).to_dict('records')
    operaciones = [parse_operacion_record(x) for x in operacion_records]
    return operaciones


