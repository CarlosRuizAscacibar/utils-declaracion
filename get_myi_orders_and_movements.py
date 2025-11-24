
from datetime import datetime
from getpass import getpass
import datetime
from pathlib import Path
from dotenv import load_dotenv
import os
from servicios.my_investor import get_access_token, get_bank_movements, get_completed_stock_orders
from dateutil.relativedelta import relativedelta
from modelos.constants import EnvironmentVariableNames
import json

def can_create_file(path: str) -> bool:
    test_file = Path(path)

    try:
        with open(test_file, "w") as f:
            f.write("test")
        test_file.unlink()  # remove test file
        return True
    except Exception as e:
        print(f"❌ Cannot create file: {e}")
        return False



load_dotenv()

now = datetime.datetime.now()
two_years = relativedelta(years=2)
two_years_ago = now - two_years
dateformat = "%Y%m%d"
now_str = now.strftime(dateformat)
two_years_ago_str = two_years_ago.strftime(dateformat)
filename_movements = f"movements_from_{now_str}_to_{two_years_ago_str}.json"
file_movements_full_path= os.getenv(EnvironmentVariableNames.JSON_BANK_MY_INVESTOR) + '/' + filename_movements
filename_orders = f"orders_from_{now_str}_to_{two_years_ago_str}.json"
file_orders_full_path = os.getenv(EnvironmentVariableNames.JSON_BROKER_MY_INVESTOR) + '/' + filename_orders
can_create_file(file_movements_full_path)
can_create_file(file_orders_full_path)

access_token = get_access_token(getpass("my investor user"), getpass("my investor password"))

movements_json = get_bank_movements(two_years_ago, now, access_token)
print(f'saving movements in file {file_movements_full_path}')

with open( file_movements_full_path,"w",encoding="utf8") as f:
    f.write(json.dumps(movements_json, indent="  "))

orders_json = get_completed_stock_orders(two_years_ago, now, access_token)
print(f'saving orders in file {file_orders_full_path}')

with open(file_orders_full_path,"w",encoding="utf8") as f:
    f.write(json.dumps(orders_json, indent="  "))
