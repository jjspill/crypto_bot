import asyncio
import os

from aiohttp import ClientSession
from airtable_service.airtable import AirtableInfo, get_config_table
from dotenv import load_dotenv
from fetching_service.fetching_utils import extract_data, fetch_binance, fetch_fng
from mongo_service.mongo import MongoDB
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
airtable_info = AirtableInfo(
    api_key=os.getenv("AIRTABLE_API_KEY"),
    base_id=os.getenv("CONFIG_BASE_ID"),
)
config_table = get_config_table(airtable_info)
CLIENT = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi("1"))


async def main():
    print("Starting main")
    mongo = MongoDB(CLIENT, "MarketData", "Data")  # Initialize MongoDB
    async with ClientSession() as session:
        # Iterate over the config table and fetch data
        async for row in config_table.iterate(100, 100, session):
            try:
                query_str = row["fields"]["Query"] if "Query" in row["fields"] else ""
                data = await fetch_binance(
                    row["fields"]["API"], row["fields"]["Endpoint"], query_str, session
                )
                # Extract data from response given the config
                extracted_data = extract_data(data, row["fields"])
                mongo.add_data(extracted_data)

            except Exception as e:
                print(f"Error fetching data for {row['fields']['Key']}")
                print(f"Error: {e}")
                continue

        fng = await fetch_fng(session)
        mongo.add_data({"fng": fng})  # Add FNG data to MongoDB
        mongo.commit_data()
        print("Finished main")


def handler(event, context):
    return asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
