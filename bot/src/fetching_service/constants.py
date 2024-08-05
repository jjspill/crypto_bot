from dataclasses import dataclass


@dataclass
class URLs:
    binance_us_url: str = "https://api.binance.us/api/v3"
    binance_usdt_url: str = "https://fapi.binance.com"
    binance_coin_url: str = "https://dapi.binance.com"
    binance_com_url: str = "https://api4.binance.com/"
    proxy_url: str = (
        "https://5anv066yv9.execute-api.eu-central-1.amazonaws.com/prod?url="
    )
