import asyncio
import os

from aiohttp import ClientSession
from airtable.airtable import AirtableInfo, get_config_table
from dotenv import load_dotenv

load_dotenv()

airtable_info = AirtableInfo(
    api_key=os.getenv("AIRTABLE_API_KEY"),
    base_id=os.getenv("CONFIG_BASE_ID"),
)
print(airtable_info)
config_table = get_config_table(airtable_info)


async def fetch_rows():
    session = ClientSession()
    async for row in config_table.iterate(100, 100, session):
        print(row)


asyncio.run(fetch_rows())
