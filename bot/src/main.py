import asyncio
import os

from aiohttp import ClientSession
from airtable_service.airtable import AirtableInfo, get_config_table
from dotenv import load_dotenv
from fetching_service.fetching_utils import fetch_binance
from mongo_service.mongo import MongoDB

load_dotenv()
airtable_info = AirtableInfo(
    api_key=os.getenv("AIRTABLE_API_KEY"),
    base_id=os.getenv("CONFIG_BASE_ID"),
)

config_table = get_config_table(airtable_info)


async def main():
    mongo = MongoDB(os.getenv("MONGO_URI"), "MarketData", "Data")
    async with ClientSession() as session:
        async for row in config_table.iterate(100, 100, session):
            data = await fetch_binance(
                row["fields"]["API"], row["fields"]["Endpoint"], session
            )
            mongo.add_data(row["fields"]["Key"], data)

        mongo.commit_data()


if __name__ == "__main__":
    asyncio.run(main())
