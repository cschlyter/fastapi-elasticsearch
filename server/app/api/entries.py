from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends

from app.models.schemas import EntryPayloadSchema, EntryResponseSchema
from app.config import get_elasticsearch, AsyncElasticsearch

router = APIRouter()


@router.post("/", response_model=EntryResponseSchema, status_code=201)
async def create_entry(
    payload: EntryPayloadSchema, es: AsyncElasticsearch = Depends(get_elasticsearch)
) -> EntryResponseSchema:
    doc = {
        "text": payload.text,
        "timestamp": payload.timestamp,
    }
    result = await es.index(index="test-index", document=doc)

    entry = EntryResponseSchema(
        id=result["_id"],
        text=payload.text,
        timestamp=payload.timestamp,
    )
    return entry


@router.get("/", response_model=List[EntryResponseSchema])
async def search_entries(
    query_text: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    es: AsyncElasticsearch = Depends(get_elasticsearch),
) -> List[EntryResponseSchema]:
    search_query = {
        "bool": {
            "must": [],
            "filter": [],
        }
    }

    if query_text:
        search_query["bool"]["must"].append(
            {"match": {"text": {"query": query_text, "fuzziness": "AUTO"}}}
        )

    results = await es.search(index="test-index", body={"query": search_query})

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
