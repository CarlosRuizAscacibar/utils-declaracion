import requests
import pandas as pd
import json
import datetime
import sqlite3
import os
import dotenv

dotenv.load_dotenv()
response = requests.get('https://wise.com/rates/history+live?source=EUR&target=GBP&length=5&resolution=daily&unit=year')
dic_res = json.loads(response.text)
for x in dic_res:
    x['str_time']=datetime.datetime.fromtimestamp(x['time']/1000).date().strftime('%Y-%m-%d')
df = pd.DataFrame(dic_res)
conn = sqlite3.connect(os.getenv('PERSONAL_DATABASE'))
df.to_sql('eur_gbp', conn, if_exists='append', index=False)
conn.close()