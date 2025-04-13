import requests
import json 
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from decimal import Decimal

from modelos import constants
from modelos.movimiento_corriente import MovimientoCorriente
from servicios.id_generator import gen_id_movimiento_corriente

def get_access_token(usr,password):
    token_url = "https://api.myinvestor.es/login/api/v1/auth/token"
    token_params = {
        "customerId": usr ,
        "password":  password ,
        "deviceId": "17f35a53-0092-4026-9de1-8989c9f69aac",
        "platform": "BROWSER",
        "accessType": "USERNAME",
    }

    resp_token = requests.post(token_url, json=token_params)
    access_token = json.loads(resp_token.text)["payload"]["data"]["accessToken"]
    return access_token

def get_completed_stock_orders(date_from: datetime, date_to: datetime, access_token: str):

    headers = {"authorization": "Bearer " + access_token}
    dateformat = "%Y-%m-%d"
    from_str = date_from.strftime(dateformat)
    to_str = date_to.strftime(dateformat)
    stock_account_id = os.getenv('MY_INVESTOR_SECURITIES_ACCOUNT')

    params = {
        'status':f'COMPLETE',
        'dateFrom':f'{from_str}',
        'dateTo':f'{to_str}',
        'stockAccountId':stock_account_id,
        'type':f'ALL'
        
    }
    response = requests.get(
        f"https://app.myinvestor.es/ms-broker/v2/stock-orders",
        params=params,
        headers=headers,
    )


    order_ids = [x["id"] for x in json.loads(response.text)["payload"]["data"]]

    orders_json = []
    for x in order_ids:
        response = requests.get(
            "https://app.myinvestor.es/ms-broker/v2/stock-orders/" + x,
            params=params,
            headers=headers,
        )
        print(f"mynvestor oder request {x} status {response.status_code}")
        json_data = json.loads(response.text)["payload"]["data"]
        orders_json.append(json_data)
    return orders_json




def get_bank_movements(date_from: datetime, date_to: datetime, access_token: str):
    load_dotenv()

    dateformat = "%Y%m%d"
    date_to_str = date_to.strftime(dateformat)
    date_from_str = date_from.strftime(dateformat)

    headers = {"authorization": "Bearer " + access_token}


    url= f'https://app.myinvestor.es/myinvestor-server/api/v2/cash-accounts/'
    url = url + f'{os.getenv("MY_INVESTOR_CASH_ACCOUNT")}/flows?dateFrom={date_from_str}&dateTo={date_to_str}'
    
    movements_response = requests.get(url,headers=headers)
    assert movements_response.status_code == 200


    dic_movements_resp = json.loads(movements_response.text)
    mov_list = dic_movements_resp['payload']['data']['flowList']

    print(len(mov_list))
    
    return mov_list