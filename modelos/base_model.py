import json
from datetime import datetime
from datetime import date
from enum import Enum
from decimal import Decimal

def default_serial(o):
    if isinstance(o,datetime) or isinstance(o,date):
        return o.isoformat()
    if isinstance(o,Enum):
        return o.name
    if isinstance(o, Decimal):
        return o.to_eng_string()
    else:
        return o.__dict__

class BaseModel:
    def to_json(self):
       return json.dumps(self, default=default_serial)