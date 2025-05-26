import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_swell_price():
    api_key = os.getenv('CMC_API_KEY')
    if not api_key:
        raise ValueError("Please set the 'CMC_API_KEY' environment variable.")

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': 'SWELL',
        'convert': 'USD'
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    try:
        price = data['data']['SWELL']['quote']['USD']['price']
        return price
    except KeyError:
        print("SWELL data not found in the API response.")
