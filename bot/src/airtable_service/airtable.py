from dataclasses import dataclass
from typing import Any, TypedDict, cast

from aiohttp import ClientSession
from asyncstdlib import any_iter


class AirtableRecord(TypedDict):
    fields: dict[str, Any]
    id: str
    createdTime: str


class AirtablePage(TypedDict):
    records: list[AirtableRecord]
    offset: str | None


class AirtableTable:
    table_name: str
    api_key: str
    base_id: str
    airtable_url: str
    view_name: str | None
    fields: list[str] | None

    def __init__(
        self,
        api_key: str,
        base_id: str,
        table_name: str,
        *,
        airtable_url: str = "https://api.airtable.com/v0",
        view_name: str | None = None,
        fields: list[str] | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_id = base_id
        self.table_name = table_name
        self.airtable_url = airtable_url
        self.view_name = view_name
        self.fields = fields

    # todo: put iteration logic into a generic class
    async def get_page(
        self,
        page_size: int,
        max_records: int,
        session: ClientSession,
        offset: str | None = None,
    ) -> tuple[AirtablePage, str | None]:
        params: dict[str, int | str] = {
            "maxRecords": max_records,
            "pageSize": page_size,
        }
        if offset is not None:
            params["offset"] = offset
        if self.view_name is not None:
            params["view"] = self.view_name
        if self.fields is not None:
            params["fields[]"] = [f for f in self.fields]
        async with session.get(
            f"{self.airtable_url}/{self.base_id}/{self.table_name}",
            params=params,
            headers={"Authorization": f"Bearer {self.api_key}"},
        ) as response:
            response.raise_for_status()
            page = cast(AirtablePage, await response.json())
            return page, page.get("offset", None)

    async def iterate(self, page_size: int, max_records: int, session: ClientSession):
        offset = "Not None"
        while offset is not None:
            page, offset = await self.get_page(
                page_size,
                max_records,
                offset=None if offset == "Not None" else offset,
                session=session,
            )
            async for record in any_iter(page["records"]):
                yield record


@dataclass
class AirtableInfo:
    api_key: str
    base_id: str


def get_config_table(context: AirtableInfo):
    return AirtableTable(context.api_key, context.base_id, "Config")


def get_field(field: str, record: AirtableRecord) -> Any:
    if record["fields"] and field in record["fields"]:
        return record["fields"][field]

    return None
