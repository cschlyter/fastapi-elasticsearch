from datetime import datetime
from typing import List, Optional

from elasticsearch import AsyncElasticsearch

from app import constants
from app.models.schemas import EntryPayloadSchema, EntryResponseSchema


async def post(
    payload: EntryPayloadSchema, es: AsyncElasticsearch
) -> EntryResponseSchema:
    doc = {
        "text": payload.text,
        "timestamp": payload.timestamp,
    }
    result = await es.index(index=constants.ES_INDEX, document=doc)

    entry = EntryResponseSchema(
        id=result["_id"],
        text=payload.text,
        timestamp=payload.timestamp,
    )
    return entry


async def search(
    es: AsyncElasticsearch,
    query: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[EntryResponseSchema]:
    search_query = {
        "bool": {
            "must": [],
            "filter": [],
        }
    }

    if query:
        search_query["bool"]["must"].append(
            {"match": {"text": {"query": query, "fuzziness": "AUTO"}}}
        )

    if start_date or end_date:
        date_filter = {}
        if start_date:
            date_filter["gte"] = start_date.isoformat()
        if end_date:
            date_filter["lte"] = end_date.isoformat()
        search_query["bool"]["filter"].append({"range": {"timestamp": date_filter}})

    results = await es.search(
        index=constants.ES_INDEX, size=100, body={"query": search_query}
    )

    hits = results.get("hits", {}).get("hits", [])

    entries = []
    for hit in hits:
        entry_data = hit["_source"]
        entries.append(
            EntryResponseSchema(
                id=hit["_id"],
                text=entry_data["text"],
                timestamp=entry_data["timestamp"],
            )
        )

    return entries
