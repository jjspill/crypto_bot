import re
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


def encode_query_string(query_string: str, api: str) -> str:
    query_params = parse_qsl(query_string)
    encoded_query_string = urlencode(query_params)
    # Using proxy for BinanceCOM and BinanceDER, encode '&' as '%26'
    if api != "BinanceUS":
        encoded_query_string = query_string.replace("&", "%26")
    return encoded_query_string


async def fetch_binance(
    api: str, endpoint: str, query: str, session: aiohttp.ClientSession
) -> dict:
    url = map_api_to_url(api, endpoint) + "?" + encode_query_string(query, api)
    print(url)
    async with session.get(url) as response:
        data = await response.json()
        return data


# Extracts the path and fields from the config
def get_endpoint_config(row: dict) -> dict:
    path = [key.strip() for key in row.get("Path", "").split(",") if key.strip()]
    fields = [
        field.strip() for field in row.get("Fields", "").split(",") if field.strip()
    ]
    return {"path": path, "fields": fields}


# Navigates the data dict using the path and extracts the fields
def extract_data(data: dict, row: dict) -> dict:
    config = get_endpoint_config(row)
    db_key = row.get("Key", "") + "_" if "Key" in row else ""
    try:
        for key in config["path"]:
            if key.isdigit():
                key = int(key)
            data = data[key]
        return {
            db_key + camel_to_snake(field): data[field] for field in config["fields"]
        }
    except Exception as e:
        raise ValueError(
            f"Error extracting data for {db_key} with config {config}: {e}"
        )


# def extract_response_field(response: dict, path: str) -> str:
#     keys = path.split(",")
#     keys = [key.strip() for key in keys]
#     data = response
#     try:
#         for key in keys:
#             if key.isdigit():
#                 key = int(key)
#             data = data[key]
#         return data
#     except Exception as e:
#         raise ValueError(f"Field {path} not found in response: {response}")


async def fetch_fng(session: aiohttp.ClientSession) -> dict:
    url = "https://api.alternative.me/fng/"
    async with session.get(url) as response:
        data = await response.json()
        data = data["data"][0]["value"]
        return data


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
