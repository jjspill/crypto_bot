import asyncio
import os

from aiohttp import ClientSession
from airtable_service.airtable import AirtableInfo, get_config_table
from dotenv import load_dotenv
from fetching_service.fetching_utils import (
    extract_response_field,
    fetch_binance,
    fetch_fng,
)
from mongo_service.mongo import MongoDB

load_dotenv()
airtable_info = AirtableInfo(
    api_key=os.getenv("AIRTABLE_API_KEY"),
    base_id=os.getenv("CONFIG_BASE_ID"),
)

config_table = get_config_table(airtable_info)


async def main():
    print("Starting main")
    mongo = MongoDB("MarketData", "Data")
    async with ClientSession() as session:
        async for row in config_table.iterate(100, 100, session):
            try:
                query = row["fields"]["Query"] if "Query" in row["fields"] else ""
                data = await fetch_binance(
                    row["fields"]["API"], row["fields"]["Endpoint"], query, session
                )
                # print("Data", data)
                extracted_data = (
                    extract_response_field(data, row["fields"]["Path"])
                    if "Path" in row["fields"]
                    else data
                )
                print("Extracted data", extracted_data)
                mongo.add_data(row["fields"]["Key"], extracted_data)

            except Exception as e:
                print(f"Error fetching data for {row['fields']['Key']}")
                print(f"Error: {e}")
                continue

        fng = await fetch_fng(session)
        mongo.add_data("fng", fng)
        mongo.commit_data()
        print("Finished main")


def handler(event, context):
    return asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
