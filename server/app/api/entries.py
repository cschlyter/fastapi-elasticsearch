from datetime import datetime
from typing import List, Optional

from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends

from app.api import crud
from app.config import get_async_elasticsearch
from app.models.schemas import EntryPayloadSchema, EntryResponseSchema

router = APIRouter()


@router.post("/", response_model=EntryResponseSchema, status_code=201)
async def create_entry(
    payload: EntryPayloadSchema,
    es: AsyncElasticsearch = Depends(get_async_elasticsearch),
) -> EntryResponseSchema:
    entry = await crud.post(payload, es)
    return entry


@router.get("/", response_model=List[EntryResponseSchema])
async def search_entries(
    query: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    es: AsyncElasticsearch = Depends(get_async_elasticsearch),
) -> List[EntryResponseSchema]:
    entries = await crud.search(es, query, start_date, end_date)

    return entries
