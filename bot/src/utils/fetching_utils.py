from typing import List
import requests

BINANCE_BASE_URL = 'https://api.binance.us/api/v3'

def fetch_binance(endpoint: str): 
    url = f"{BINANCE_BASE_URL}/{endpoint}"
    try:     
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
    



def extract_binance(fields: List[str]):
    responses = {}
    for field in fields:
        responses[field] = fetch_binance(field)

    return responses

FIELDS = ["ticker/price?symbol=BTCUSD"]

print(extract_binance(FIELDS))
