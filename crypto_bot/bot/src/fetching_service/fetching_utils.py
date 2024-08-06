from urllib.parse import parse_qsl, urlencode

import aiohttp
from fetching_service.constants import URLs

url_constants = URLs()


def map_api_to_url(api: str, endpoint: str) -> str:
    if api == "BinanceUS":
        return url_constants.binance_us_url + endpoint
    elif api == "BinanceCOM":
        return url_constants.proxy_url + url_constants.binance_com_url + endpoint
    elif api == "BinanceDER":
        if "fapi" in endpoint:
            return url_constants.proxy_url + url_constants.binance_usdt_url + endpoint
        elif "dapi" in endpoint:
            return url_constants.proxy_url + url_constants.binance_coin_url + endpoint

    raise ValueError(f"Invalid API: {api}")


def encode_query_string(query_string):
    query_params = parse_qsl(query_string)
    encoded_query_string = urlencode(query_params)
    encoded_query_string = query_string.replace("&", "%26")
    return encoded_query_string


async def fetch_binance(
    api: str, endpoint: str, query: str, session: aiohttp.ClientSession
) -> dict:
    url = map_api_to_url(api, endpoint) + "?" + encode_query_string(query)
    print(url)
    async with session.get(url) as response:
        data = await response.json()
        return data


def extract_response_field(response: dict, path: str) -> str:
    keys = path.split(",")
    keys = [key.strip() for key in keys]
    data = response
    try:
        for key in keys:
            if key.isdigit():
                key = int(key)
            data = data[key]
        return data
    except Exception as e:
        raise ValueError(f"Field {path} not found in response: {response}")


async def fetch_fng(session: aiohttp.ClientSession) -> dict:
    url = "https://api.alternative.me/fng/"
    async with session.get(url) as response:
        data = await response.json()
        data = data["data"][0]["value"]
        return data
