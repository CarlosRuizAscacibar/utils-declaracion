import requests

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from modelos.operacion import Operacion
from modelos.tipo_operacion import TipoOperacion
from servicios.id_generator import gen_id_operacion
import json
from getpass import getpass
import datetime
from dotenv import load_dotenv
import os
from servicios.my_investor import get_access_token, get_bank_movements, get_completed_stock_orders
from dateutil.relativedelta import relativedelta
from modelos.constants import EnvironmentVariableNames

load_dotenv()

now = datetime.datetime.now()
two_years = relativedelta(years=2)
two_years_ago = now - two_years
dateformat = "%Y%m%d"
now_str = now.strftime(dateformat)
two_years_ago_str = two_years_ago.strftime(dateformat)

access_token = get_access_token(getpass("my investor user"), getpass("my investor password"))
movements_json = get_bank_movements(two_years_ago, now, access_token)
filename = f"movements_from_{now_str}_to_{two_years_ago_str}.json"
file_full_path= os.getenv(EnvironmentVariableNames.JSON_BANK_MY_INVESTOR) + '/' + filename

print(f'saving in file {file_full_path}')

with open( file_full_path,"w",encoding="utf8") as f:
    f.write(json.dumps(movements_json, indent="  "))

