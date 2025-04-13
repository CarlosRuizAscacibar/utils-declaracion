import requests
import pandas as pd
import json
import datetime
import sqlite3
import os
import dotenv

dotenv.load_dotenv()
response = requests.get('https://wise.com/rates/history+live?source=EUR&target=USD&length=5&resolution=daily&unit=year')
dic_res = json.loads(response.text)
conn = sqlite3.connect(os.getenv('PERSONAL_DATABASE'))
fetched_days = set()
dic_res_not_dups = []
for x in dic_res:
    x['str_time']=datetime.datetime.fromtimestamp(x['time']/1000).date().strftime('%Y-%m-%d')
    if x['str_time'] not in fetched_days:
        fetched_days.add(x['str_time'])
        dic_res_not_dups.append(x)
exisiting = pd.read_sql("select str_time from eur_usd", conn).to_dict("list")['str_time']
dic_res_not_dups = [x for x in dic_res_not_dups if x['str_time'] not in exisiting]
df = pd.DataFrame(dic_res_not_dups)
df.to_sql('eur_usd', conn, if_exists='append', index=False)
conn.close()