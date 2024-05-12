#%%
import requests
import re
from datetime import datetime
from decimal import Decimal
# %%
def fetch_usd_eur_quote():
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
    dic['2023-12-26']=Decimal('1.1044')
    return dic
    # %%