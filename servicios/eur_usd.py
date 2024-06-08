#%%
import requests
import re
from datetime import datetime
from decimal import Decimal
from datetime import datetime, timedelta

# %%
def fetch_usd_eur_quote(year):
    res = requests.get('https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/usd.xml')

    raw_xml = res.text
    dic = {}
    # %%
    for x in res.text.split('\n'):
        if "<Obs"  in x: 
            # Regular expression pattern to extract date and observation value
            pattern = r'TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]+)"'

            # Match the pattern in the text
            match = re.search(pattern, x)
            
            if match:
                date_str = match.group(1)
                date = datetime.strptime(date_str, "%Y-%m-%d")
                obs_value = match.group(2)
                dic[date.strftime("%Y-%m-%d")] =  Decimal(obs_value)
            else:
                raise Exception(f"no match for {x}")

    
    current_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

     
    dic['2023-01-01']=Decimal('1.0667')
    dic['2023-12-31']=Decimal('1.1056')

    while current_date <= end_date:
        if current_date.strftime("%Y-%m-%d") not in dic.keys():
            yesterday = current_date - timedelta(days=1)
            dic[current_date.strftime("%Y-%m-%d")] = dic[yesterday.strftime("%Y-%m-%d")]
        current_date += timedelta(days=1)
    
    
    return dic
    # %%