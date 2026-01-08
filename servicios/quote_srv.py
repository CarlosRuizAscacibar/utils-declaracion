import requests
import json
from decimal import Decimal

def quote_for_isin_eur(isin) -> Decimal | None:
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "application/json;"
                "q=0.9,image/avif,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }


        response_text = requests.get(f'https://www.justetf.com/api/etfs/{isin}/quote?locale=en&currency=EUR&isin={isin}' , headers=headers).text
        return json.loads(response_text)['latestQuote']['raw']

    except:
        return None
