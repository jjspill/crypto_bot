import aiohttp
from fetching_service.constants import URLs

url_constants = URLs()


def map_api_to_url(api: str, endpoint: str):
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


async def fetch_binance(
    api: str, endpoint: str, session: aiohttp.ClientSession
) -> dict:
    url = map_api_to_url(api, endpoint)
    try:
        async with session.get(url) as response:
            data = await response.json()
            return data

    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return dict(e)
