from fundingrate import funding_dydx
from gnews import GNews

# google_news = GNews()
# pakistan_news = google_news.get_news("Pakistan")
# print(pakistan_news[0])


dydx = funding_dydx(["BTC-USD", "ETH-USD", "SOL-USD"], version="v3")
dydx_rates = dydx.get_formatted_funding_rates()
print("HERE", dydx_rates.info())
dydx_rates.head()
