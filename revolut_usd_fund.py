#%%
print('0')

import pandas as pd
import os
from dotenv import load_dotenv
from servicios.eur_usd import fetch_usd_eur_quote
import datetime
load_dotenv()
from decimal import Decimal
import re





records_csv_usd = pd.read_csv(os.getenv('REVOLUT_CSV_MONETARY'),sep=';').to_dict('records')
print('1')
dic_usd_euro = fetch_usd_eur_quote(2023)

sum_eur_values = Decimal('0.00')

for x in records_csv_usd:
    # pattern = r"(\b[a-z])(?=\w*\b)"
    # date_to_parse = re.sub(pattern, lambda match: match.group().upper(), x['date'])
    date_to_parse = x['date'].replace('dic','dec')
    x['common_format_date'] = datetime.datetime.strptime(date_to_parse,'%d %b %Y %H:%M:%S').date().strftime("%Y-%m-%d")
    eur_conv_value = dic_usd_euro[x['common_format_date']]
    x['eur_conv_value'] = eur_conv_value.to_eng_string()
    eur_value = (Decimal(x['value'].replace('$','').replace(',','')) / eur_conv_value).quantize(Decimal('0.00'))
    x['eur_value'] = eur_value.to_eng_string()
    if 'Interest' in x['description']:
        sum_eur_values += eur_value




# %%
pd.DataFrame(records_csv_usd).to_excel(os.getenv('REVOLUT_MONETARY_RESULT'))
# %%
pd.DataFrame([x for x in records_csv_usd if 'Service' in x['description']]).to_excel(os.getenv('REVOLUT_MONETARY_RESULT'))
# %%
