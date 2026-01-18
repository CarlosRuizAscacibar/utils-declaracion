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
from servicios.my_investor import get_access_token, get_completed_stock_orders
from dateutil.relativedelta import relativedelta
import argparse

load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Get MyInvestor orders data')
parser.add_argument('--username', '-u', help='MyInvestor username')
parser.add_argument('--password', '-p', help='MyInvestor password')
args = parser.parse_args()

# Get credentials from arguments or prompt
user = args.username
password = args.password

if not user:
    user = input("My Investor user: ")
if not password:
    password = getpass("My Investor password: ")

if not user or not password:
    print("Error: Username and password are required")
    exit(1)

now = datetime.datetime.now()
two_years = relativedelta(years=2)
two_years_ago = now - two_years
dateformat = "%Y%m%d"
now_str = now.strftime(dateformat)
two_years_ago_str = two_years_ago.strftime(dateformat)

access_token = get_access_token(user, password)
orders_json = get_completed_stock_orders(two_years_ago, now, access_token)
filename = f"orders_from_{now_str}_to_{two_years_ago_str}.json"

with open(
    os.getenv('JSON_BROKER_MY_INVESTOR') + '/' + filename,
    "w",
    encoding="utf8",
) as f:
    f.write(json.dumps(orders_json, indent="  "))
